import ROOT
import numpy as np
import argparse
import os

if "/home/submit/pdmonte/CMSSW_10_6_27/src/Hrare2023/analysis/functions.so" not in ROOT.gSystem.GetLibraries():
    ROOT.gSystem.CompileMacro("/home/submit/pdmonte/CMSSW_10_6_27/src/Hrare2023/analysis/functions.cc","k")


s = '''
    Double_t fitf(Double_t *x, Double_t *par) {
        
        Double_t aL = pow((par[5]/abs(par[3])), par[5]) * exp(-par[3]*par[3]/2);
        Double_t aR = pow((par[6]/abs(par[4])), par[6]) * exp(-par[4]*par[4]/2);
        Double_t bL = par[5]/abs(par[3]) - abs(par[3]);
        Double_t bR = par[6]/abs(par[4]) - abs(par[4]);

        Double_t arg = (x[0]-par[1])/par[2];
        Double_t val = 0.0;

        if (arg < -par[3]){
                val = aL * pow((bL - arg), -par[5]);
        } else if (arg <= par[4]){
                val = exp(-0.5*arg*arg);
        } else {
                val = aR * pow((bR + arg), -par[6]);
        }

        return par[0] * val;
    }

    TF1 *func = new TF1("crystalball", fitf, 100, 150, 7);  //name, C func, xrange, numParams
    func->SetParameters(500, 125, 20, 10, 10, 10, 10);                      //Value each param
    func->SetParNames("N", "mu", "sigma", "alphaL", "alphaR", "nL", "nR");   //Name each param
    func->SetParLimits(1, 100, 150); // set limit mu
    func->SetParLimits(2, 0.001, 100); // set limit sigma
    func->SetParLimits(3, 0.001, 100); // set limit alphaL
    func->SetParLimits(4, 0.001, 100); // set limit alphaR
    func->SetParLimits(5, 0.001, 20); // set limit nL
    func->SetParLimits(6, 0.001, 20); // set limit nR
    '''

ROOT.gInterpreter.ProcessLine(s)

def getNumVarsFromCode(code):
    nVars = 0
    while(code > 0):
        nVars += int(code%2)
        code = int(code/2)
    return nVars


def getTotalNumVars(modelName):
    splitted = modelName.split("_")
    numVars = getNumVarsFromCode(int(splitted[1].replace("df", "")))
    numVars += getNumVarsFromCode(int(splitted[2].replace("dl", "")))
    numVars += len(splitted) - 3
    if "opt" in modelName:
        numVars -= 1
    return numVars


def sigmoid(x, a=0.4, b=113):
    return 1/(1+np.exp(-a*(x-b)))


def getLoss(mu, N=4000, integral=180000):
    fact = 1 if mu < 115 else 10
    return (-np.log(abs(mu-125)**2/(1+np.exp(0.3*(mu-100)))) + N/1000 + np.sqrt(integral)/28.5)*fact


parser = argparse.ArgumentParser(description="Famous Submitter")
parser.add_argument("-m", "--modelName", type=str, required=True, help="Input the model name (e.g. BDTG_df55_dl12_v1_v13).")
parser.add_argument("-c", "--channel", type=str, required=True, help="Channel (e.g. phi, omega, d0starrho, d0star).")
options = parser.parse_args()

date = "OCT27"
mesonCat = ""
mesonNum = 0
if (options.channel == "omega"):
    mesonCat = "OmegaCat"
    mesonNum = 1038
elif (options.channel == "phi"):
    mesonCat = "Phi3Cat"
    mesonNum = 1039
elif (options.channel == "d0starrho"):
    mesonCat = "D0StarRhoCat"
    mesonNum = 1040
elif (options.channel == "d0star"):
    mesonCat = "D0StarCat"
    mesonNum = 1041
else:
    raise Exception("Wrong channel.")

chainSGN = ROOT.TChain("events")
chainSGN.Add("/data/submit/pdmonte/outputs/{0}/2018/outname_mc{1}_GFcat_{2}_2018.root".format(date, mesonNum, mesonCat))

chainSGN0 = ROOT.TChain("events")
chainSGN1 = ROOT.TChain("events")
chainSGN2 = ROOT.TChain("events")
chainSGN0.Add("/data/submit/pdmonte/outputs/{0}/2018/outname_mc{1}_GFcat_{2}_2018_sample0.root".format(date, mesonNum, mesonCat))
chainSGN1.Add("/data/submit/pdmonte/outputs/{0}/2018/outname_mc{1}_GFcat_{2}_2018_sample1.root".format(date, mesonNum, mesonCat))
chainSGN2.Add("/data/submit/pdmonte/outputs/{0}/2018/outname_mc{1}_GFcat_{2}_2018_sample2.root".format(date, mesonNum, mesonCat))

chainBKG = ROOT.TChain("events")
chainBKG.Add("/data/submit/pdmonte/outputs/{0}/2018/outname_mc10_GFcat_{1}_2018.root".format(date, mesonCat))
chainBKG.Add("/data/submit/pdmonte/outputs/{0}/2018/outname_mc11_GFcat_{1}_2018.root".format(date, mesonCat))
chainBKG.Add("/data/submit/pdmonte/outputs/{0}/2018/outname_mc12_GFcat_{1}_2018.root".format(date, mesonCat))
chainBKG.Add("/data/submit/pdmonte/outputs/{0}/2018/outname_mc13_GFcat_{1}_2018.root".format(date, mesonCat))
chainBKG.Add("/data/submit/pdmonte/outputs/{0}/2018/outname_mc14_GFcat_{1}_2018.root".format(date, mesonCat))

#dfSGN = ROOT.RDataFrame(chainSGN)
dfSGN0 = ROOT.RDataFrame(chainSGN0)
dfSGN1 = ROOT.RDataFrame(chainSGN1)
dfSGN2 = ROOT.RDataFrame(chainSGN2)
dfBKG = ROOT.RDataFrame(chainBKG)

if options.modelName == "RECO":

    #dfSGN = (dfSGN.Define("scale", "w*lumiIntegrated"))
    dfSGN0 = (dfSGN0.Define("scale", "w*lumiIntegrated/3."))
    dfSGN1 = (dfSGN1.Define("scale", "w*lumiIntegrated/3."))
    dfSGN2 = (dfSGN2.Define("scale", "w*lumiIntegrated/3."))
    dfBKG = (dfBKG.Define("scale", "w*lumiIntegrated"))

    nbins, xlow, xhigh = 200, 105, 145
    #h3 = dfSGN.Histo1D(("hist", "HCandMass RECO", nbins, xlow, xhigh), "HCandMass", "scale")
    h3 = dfSGN0.Histo1D(("hist", "HCandMass RECO", nbins, xlow, xhigh), "HCandMass", "scale").GetValue()
    h31 = dfSGN1.Histo1D(("hist", "HCandMass RECO", nbins, xlow, xhigh), "HCandMass", "scale").GetValue()
    h32 = dfSGN2.Histo1D(("hist", "HCandMass RECO", nbins, xlow, xhigh), "HCandMass", "scale").GetValue()
    h3.Add(h31)
    h3.Add(h32)
    h6 = dfBKG.Histo1D(("hist", "HCandMass RECO", nbins, xlow, xhigh), "HCandMass", "scale")

    #NSig_predTOT = h3.Integral(h3.FindBin(117), h3.FindBin(133))
    NSig_pred = h3.Integral(h3.FindBin(117), h3.FindBin(133))
    NBkg_pred = h6.Integral(h6.FindBin(117), h6.FindBin(133))

    #hError = dfSGN.Define("good", "goodMeson_pt - goodMeson_pt_GEN").Histo1D(("hist", "RECO - GEN", nbins, -30, 30), "good", "scale")
    hError = dfSGN0.Define("good", "goodMeson_pt - goodMeson_pt_GEN").Histo1D(("hist", "RECO - GEN", nbins, -30, 30), "good", "scale").GetValue()
    hError1 = dfSGN1.Define("good", "goodMeson_pt - goodMeson_pt_GEN").Histo1D(("hist", "RECO - GEN", nbins, -30, 30), "good", "scale").GetValue()
    hError2 = dfSGN2.Define("good", "goodMeson_pt - goodMeson_pt_GEN").Histo1D(("hist", "RECO - GEN", nbins, -30, 30), "good", "scale").GetValue()
    hError.Add(hError1)
    hError.Add(hError2)

    errorMeson = hError.GetStdDev()

else:
    s = '''
    TMVA::Experimental::RReader modelScale0("/data/submit/pdmonte/TMVA_models/weightsOpts/TMVARegression_{modelName}_{channel}_0.weights.xml");
    computeModelScale0 = TMVA::Experimental::Compute<{numVarsTotal}, float>(modelScale0);
    '''.format(modelName=options.modelName, channel=options.channel, numVarsTotal=getTotalNumVars(options.modelName))
    s += '''
    TMVA::Experimental::RReader modelScale1("/data/submit/pdmonte/TMVA_models/weightsOpts/TMVARegression_{modelName}_{channel}_1.weights.xml");
    computeModelScale1 = TMVA::Experimental::Compute<{numVarsTotal}, float>(modelScale1);
    '''.format(modelName=options.modelName, channel=options.channel, numVarsTotal=getTotalNumVars(options.modelName))
    s += '''
    TMVA::Experimental::RReader modelScale2("/data/submit/pdmonte/TMVA_models/weightsOpts/TMVARegression_{modelName}_{channel}_2.weights.xml");
    computeModelScale2 = TMVA::Experimental::Compute<{numVarsTotal}, float>(modelScale2);
    '''.format(modelName=options.modelName, channel=options.channel, numVarsTotal=getTotalNumVars(options.modelName))

    ROOT.gInterpreter.ProcessLine(s)
    variables = list(ROOT.modelScale0.GetVariableNames())

    dfSGN0 = (dfSGN0.Define("scale", "w*lumiIntegrated/3.")
            .Define("scaleFactor", ROOT.computeModelScale0, variables)
            .Define("goodMeson_pt_PRED", "scaleFactor[0]*goodMeson_pt[0]")
            .Define("HCandMass_varPRED", "compute_HiggsVars_var(goodMeson_pt_PRED, goodMeson_eta[0], goodMeson_phi[0], goodMeson_mass[0], goodPhotons_pt[0], goodPhotons_eta[0], goodPhotons_phi[0], 0)"))
    dfSGN1 = (dfSGN1.Define("scale", "w*lumiIntegrated/3.")
            .Define("scaleFactor", ROOT.computeModelScale1, variables)
            .Define("goodMeson_pt_PRED", "scaleFactor[0]*goodMeson_pt[0]")
            .Define("HCandMass_varPRED", "compute_HiggsVars_var(goodMeson_pt_PRED, goodMeson_eta[0], goodMeson_phi[0], goodMeson_mass[0], goodPhotons_pt[0], goodPhotons_eta[0], goodPhotons_phi[0], 0)"))
    dfSGN2 = (dfSGN2.Define("scale", "w*lumiIntegrated/3.")
            .Define("scaleFactor", ROOT.computeModelScale2, variables)
            .Define("goodMeson_pt_PRED", "scaleFactor[0]*goodMeson_pt[0]")
            .Define("HCandMass_varPRED", "compute_HiggsVars_var(goodMeson_pt_PRED, goodMeson_eta[0], goodMeson_phi[0], goodMeson_mass[0], goodPhotons_pt[0], goodPhotons_eta[0], goodPhotons_phi[0], 0)"))

    dfBKG = (dfBKG.Define("scale", "w*lumiIntegrated")
            .Define("scaleFactor0", ROOT.computeModelScale0, variables)
            .Define("scaleFactor1", ROOT.computeModelScale1, variables)
            .Define("scaleFactor2", ROOT.computeModelScale2, variables)
            .Define("goodMeson_pt_PRED", "(scaleFactor0[0]*goodMeson_pt[0] + scaleFactor1[0]*goodMeson_pt[0] + scaleFactor2[0]*goodMeson_pt[0])/3")
            .Define("HCandMass_varPRED", "compute_HiggsVars_var(goodMeson_pt_PRED, goodMeson_eta[0], goodMeson_phi[0], goodMeson_mass[0], goodPhotons_pt[0], goodPhotons_eta[0], goodPhotons_phi[0], 0)"))

    nbins, xlow, xhigh = 200, 105, 145
    h3 = dfSGN0.Histo1D(("hist", "HCandMass RECO + PT PREDICTED", nbins, xlow, xhigh), "HCandMass_varPRED", "scale").GetValue()
    h31 = dfSGN1.Histo1D(("hist", "HCandMass RECO + PT PREDICTED", nbins, xlow, xhigh), "HCandMass_varPRED", "scale").GetValue()
    h32 = dfSGN2.Histo1D(("hist", "HCandMass RECO + PT PREDICTED", nbins, xlow, xhigh), "HCandMass_varPRED", "scale").GetValue()
    h3.Add(h31)
    h3.Add(h32)
    h6 = dfBKG.Histo1D(("hist", "HCandMass RECO + PT PREDICTED", nbins, xlow, xhigh), "HCandMass_varPRED", "scale")

    NSig_pred = h3.Integral(h3.FindBin(117), h3.FindBin(133))
    NBkg_pred = h6.Integral(h6.FindBin(117), h6.FindBin(133))

    hError = dfSGN0.Define("good", "goodMeson_pt_PRED - goodMeson_pt_GEN").Histo1D(("hist", "PRED - GEN", nbins, -30, 30), "good", "scale").GetValue()
    hError1 = dfSGN1.Define("good", "goodMeson_pt_PRED - goodMeson_pt_GEN").Histo1D(("hist", "PRED - GEN", nbins, -30, 30), "good", "scale").GetValue()
    hError2 = dfSGN2.Define("good", "goodMeson_pt_PRED - goodMeson_pt_GEN").Histo1D(("hist", "PRED - GEN", nbins, -30, 30), "good", "scale").GetValue()
    hError.Add(hError1)
    hError.Add(hError2)
    errorMeson = hError.GetStdDev()

canvas = ROOT.TCanvas("canvas", "canvas", 1600, 700)
mu_best, norm_best, chi_best = 0, 0, float('inf')

for i in range(3):
    h6.Fit("crystalball", "QM", "", 100., 150.)
    mu, normalisation, chi = h6.GetFunction("crystalball").GetParameter(1), h6.GetFunction("crystalball").GetParameter(0), h6.GetFunction("crystalball").GetChisquare()
    if chi < chi_best:
        mu_best, norm_best, chi_best = mu, normalisation, chi

ROOT.gInterpreter.ProcessLine('func->SetParameters(1000, 125, 2, 1, 1, 10, 10);')

for i in range(3):
    h6.Fit("crystalball", "QM", "", 100., 150.)
    mu, normalisation, chi = h6.GetFunction("crystalball").GetParameter(1), h6.GetFunction("crystalball").GetParameter(0), h6.GetFunction("crystalball").GetChisquare()
    if chi < chi_best:
        mu_best, norm_best, chi_best = mu, normalisation, chi

maxBin = h6.GetMaximumBin()
xMax, yMax = h6.GetBinCenter(maxBin), h6.GetBinContent(maxBin)

ROOT.gInterpreter.ProcessLine('func->SetParameters({}, {}, 20, 10, 10, 10, 10);'.format(round(yMax, 2), round(xMax, 2)))

for i in range(3):
    h6.Fit("crystalball", "QM", "", 100., 150.)
    mu, normalisation, chi = h6.GetFunction("crystalball").GetParameter(1), h6.GetFunction("crystalball").GetParameter(0), h6.GetFunction("crystalball").GetChisquare()
    if chi < chi_best:
        mu_best, norm_best, chi_best = mu, normalisation, chi

ROOT.gInterpreter.ProcessLine('func->SetParameters({}, {}, 2, 1, 1, 10, 10);'.format(round(yMax, 2), round(xMax, 2)))

for i in range(3):
    h6.Fit("crystalball", "QM", "", 100., 150.)
    mu, normalisation, chi = h6.GetFunction("crystalball").GetParameter(1), h6.GetFunction("crystalball").GetParameter(0), h6.GetFunction("crystalball").GetChisquare()
    if chi < chi_best:
        mu_best, norm_best, chi_best = mu, normalisation, chi

print(errorMeson)
print(NSig_pred)
print(NBkg_pred)
eff = NSig_pred/np.sqrt(NBkg_pred)
print("Maximize PRED: ", eff)
print("Chi**2: ", chi_best)
print("mu: ", mu_best)
print("normalisation: ", norm_best)
loss = getLoss(mu, normalisation, NBkg_pred)
print("Loss: ", loss)

save_dir = '/data/submit/pdmonte/TMVA_models/evalFiles/'
if not os.path.isdir(save_dir):
    os.mkdir(save_dir)

# Write the evaluation to a file
evalFile = f'{save_dir}eval_{options.modelName}_{options.channel}.out'
with open(evalFile, 'w') as f:
    f.write("{}\t{}\t{}\t{}".format(options.modelName, errorMeson, eff, loss))

