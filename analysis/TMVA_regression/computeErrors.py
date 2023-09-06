import ROOT
import numpy as np
import argparse
import os

if "/home/submit/pdmonte/CMSSW_10_6_27/src/Hrare2023/analysis/functions.so" not in ROOT.gSystem.GetLibraries():
    ROOT.gSystem.CompileMacro("/home/submit/pdmonte/CMSSW_10_6_27/src/Hrare2023/analysis/functions.cc","k")


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
    return numVars

parser = argparse.ArgumentParser(description="Famous Submitter")
parser.add_argument("-m", "--modelName", type=str, required=True, help="Input the model name (e.g. BDTG_df55_dl12_v1_v13).")
parser.add_argument("-c", "--channel", type=str, required=True, help="Channel (e.g. phi, omega, d0starrho, d0star).")
options = parser.parse_args()

date = "AUG24"
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
    dfSGN0 = (dfSGN0.Define("scale", "w*lumiIntegrated"))
    dfSGN1 = (dfSGN1.Define("scale", "w*lumiIntegrated"))
    dfSGN2 = (dfSGN2.Define("scale", "w*lumiIntegrated"))
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
    NSig_pred = h3.Integral(h3.FindBin(117), h3.FindBin(133))/3. #account for weigts x3
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
    TMVA::Experimental::RReader modelScale0("/data/submit/pdmonte/TMVA_models/weightsVars/TMVARegression_{modelName}_{channel}_0.weights.xml");
    computeModelScale0 = TMVA::Experimental::Compute<{numVarsTotal}, float>(modelScale0);
    '''.format(modelName=options.modelName, channel=options.channel, numVarsTotal=getTotalNumVars(options.modelName))
    s += '''
    TMVA::Experimental::RReader modelScale1("/data/submit/pdmonte/TMVA_models/weightsVars/TMVARegression_{modelName}_{channel}_1.weights.xml");
    computeModelScale1 = TMVA::Experimental::Compute<{numVarsTotal}, float>(modelScale1);
    '''.format(modelName=options.modelName, channel=options.channel, numVarsTotal=getTotalNumVars(options.modelName))
    s += '''
    TMVA::Experimental::RReader modelScale2("/data/submit/pdmonte/TMVA_models/weightsVars/TMVARegression_{modelName}_{channel}_2.weights.xml");
    computeModelScale2 = TMVA::Experimental::Compute<{numVarsTotal}, float>(modelScale2);
    '''.format(modelName=options.modelName, channel=options.channel, numVarsTotal=getTotalNumVars(options.modelName))

    ROOT.gInterpreter.ProcessLine(s)
    variables = list(ROOT.modelScale0.GetVariableNames())

    dfSGN0 = (dfSGN0.Define("scale", "w*lumiIntegrated")
            .Define("scaleFactor", ROOT.computeModelScale0, variables)
            .Define("goodMeson_pt_PRED", "scaleFactor[0]*goodMeson_pt[0]")
            .Define("HCandMass_varPRED", "compute_HiggsVars_var(goodMeson_pt_PRED, goodMeson_eta[0], goodMeson_phi[0], goodMeson_mass[0], goodPhotons_pt[0], goodPhotons_eta[0], goodPhotons_phi[0], 0)"))
    dfSGN1 = (dfSGN1.Define("scale", "w*lumiIntegrated")
            .Define("scaleFactor", ROOT.computeModelScale1, variables)
            .Define("goodMeson_pt_PRED", "scaleFactor[0]*goodMeson_pt[0]")
            .Define("HCandMass_varPRED", "compute_HiggsVars_var(goodMeson_pt_PRED, goodMeson_eta[0], goodMeson_phi[0], goodMeson_mass[0], goodPhotons_pt[0], goodPhotons_eta[0], goodPhotons_phi[0], 0)"))
    dfSGN2 = (dfSGN2.Define("scale", "w*lumiIntegrated")
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

    NSig_pred = h3.Integral(h3.FindBin(117), h3.FindBin(133))/3. #account for weigts x3
    NBkg_pred = h6.Integral(h6.FindBin(117), h6.FindBin(133))

    hError = dfSGN0.Define("good", "goodMeson_pt_PRED - goodMeson_pt_GEN").Histo1D(("hist", "PRED - GEN", nbins, -30, 30), "good", "scale").GetValue()
    hError1 = dfSGN1.Define("good", "goodMeson_pt_PRED - goodMeson_pt_GEN").Histo1D(("hist", "PRED - GEN", nbins, -30, 30), "good", "scale").GetValue()
    hError2 = dfSGN2.Define("good", "goodMeson_pt_PRED - goodMeson_pt_GEN").Histo1D(("hist", "PRED - GEN", nbins, -30, 30), "good", "scale").GetValue()
    hError.Add(hError1)
    hError.Add(hError2)
    errorMeson = hError.GetStdDev()

print(errorMeson)
print(NSig_pred)
print(NBkg_pred)
print("Maximize PRED: ", NSig_pred/np.sqrt(NBkg_pred))

save_dir = '/data/submit/pdmonte/TMVA_models/evalFiles/'
if not os.path.isdir(save_dir):
    os.mkdir(save_dir)

# Write the evaluation to a file
evalFile = f'{save_dir}eval_{options.modelName}_{options.channel}.out'
with open(evalFile, 'w') as f:
    f.write("{}\t{}\t{}".format(options.modelName, errorMeson, NSig_pred/np.sqrt(NBkg_pred)))

