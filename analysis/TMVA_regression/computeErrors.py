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
options = parser.parse_args()

date = "JUL31"

chainSGN = ROOT.TChain("events")
#chainSGN.Add("/data/submit/pdmonte/outputs/{0}/2018/outname_mc1038_GFcat_OmegaCat_2018.root".format(date))
chainSGN.Add("/data/submit/pdmonte/outputs/{0}/2018/outname_mc1039_GFcat_Phi3Cat_2018.root".format(date))
#chainSGN.Add("/data/submit/pdmonte/outputs/{0}/2018/outname_mc1040_GFcat_D0StarRhoCat_2018.root".format(date))
#chainSGN.Add("/data/submit/pdmonte/outputs/{0}/2018/outname_mc1041_GFcat_D0StarCat_2018.root".format(date))

chainBKG = ROOT.TChain("events")
chainBKG.Add("/data/submit/pdmonte/outputs/{0}/2018/outname_mc10_GFcat_Phi3Cat_2018.root".format(date))
chainBKG.Add("/data/submit/pdmonte/outputs/{0}/2018/outname_mc11_GFcat_Phi3Cat_2018.root".format(date))
chainBKG.Add("/data/submit/pdmonte/outputs/{0}/2018/outname_mc12_GFcat_Phi3Cat_2018.root".format(date))
chainBKG.Add("/data/submit/pdmonte/outputs/{0}/2018/outname_mc13_GFcat_Phi3Cat_2018.root".format(date))
chainBKG.Add("/data/submit/pdmonte/outputs/{0}/2018/outname_mc14_GFcat_Phi3Cat_2018.root".format(date))

dfSGN = ROOT.RDataFrame(chainSGN)
dfBKG = ROOT.RDataFrame(chainBKG)

if options.modelName == "RECO":

    dfSGN = (dfSGN.Define("scale", "w*lumiIntegrated"))

    dfBKG = (dfBKG.Define("scale", "w*lumiIntegrated"))

    nbins, xlow, xhigh = 200, 105, 145
    h3 = dfSGN.Histo1D(("hist", "HCandMass RECO", nbins, xlow, xhigh), "HCandMass", "scale")
    h6 = dfBKG.Histo1D(("hist", "HCandMass RECO", nbins, xlow, xhigh), "HCandMass", "scale")
    NSig_pred = h3.Integral(h3.FindBin(117), h3.FindBin(133))
    NBkg_pred = h6.Integral(h6.FindBin(117), h6.FindBin(133))

    hError = dfSGN.Define("good", "goodMeson_pt - goodMeson_pt_GEN").Histo1D(("hist", "RECO - GEN", nbins, -30, 30), "good", "scale")
    errorMeson = hError.GetValue().GetStdDev()


else:
    s = '''
    TMVA::Experimental::RReader modelScale("/data/submit/pdmonte/TMVA_models/weightsVars/TMVARegression_{modelName}.weights.xml");
    computeModelScale = TMVA::Experimental::Compute<{numVarsTotal}, float>(modelScale);
    '''.format(modelName=options.modelName, numVarsTotal=getTotalNumVars(options.modelName))

    ROOT.gInterpreter.ProcessLine(s)
    variables = list(ROOT.modelScale.GetVariableNames())

    dfSGN = (dfSGN.Define("scale", "w*lumiIntegrated")
            .Define("scaleFactor", ROOT.computeModelScale, variables)
            .Define("goodMeson_pt_PRED", "scaleFactor[0]*goodMeson_pt[0]")
            .Define("HCandMass_varPRED", "compute_HiggsVars_var(goodMeson_pt_PRED, goodMeson_eta[0], goodMeson_phi[0], goodMeson_mass[0], goodPhotons_pt[0], goodPhotons_eta[0], goodPhotons_phi[0], 0)"))

    dfBKG = (dfBKG.Define("scale", "w*lumiIntegrated")
            .Define("scaleFactor", ROOT.computeModelScale, variables)
            .Define("goodMeson_pt_PRED", "scaleFactor[0]*goodMeson_pt[0]")
            .Define("HCandMass_varPRED", "compute_HiggsVars_var(goodMeson_pt_PRED, goodMeson_eta[0], goodMeson_phi[0], goodMeson_mass[0], goodPhotons_pt[0], goodPhotons_eta[0], goodPhotons_phi[0], 0)"))

    nbins, xlow, xhigh = 200, 105, 145
    h3 = dfSGN.Histo1D(("hist", "HCandMass RECO + PT PREDICTED", nbins, xlow, xhigh), "HCandMass_varPRED", "scale")
    h6 = dfBKG.Histo1D(("hist", "HCandMass RECO + PT PREDICTED", nbins, xlow, xhigh), "HCandMass_varPRED", "scale")
    NSig_pred = h3.Integral(h3.FindBin(117), h3.FindBin(133))
    NBkg_pred = h6.Integral(h6.FindBin(117), h6.FindBin(133))

    hError = dfSGN.Define("good", "goodMeson_pt_PRED - goodMeson_pt_GEN").Histo1D(("hist", "PRED - GEN", nbins, -30, 30), "good", "scale")
    errorMeson = hError.GetValue().GetStdDev()

print(errorMeson)
print(NSig_pred)
print(NBkg_pred)
print("Maximize PRED: ", NSig_pred/np.sqrt(NBkg_pred))

save_dir = '/data/submit/pdmonte/TMVA_models/evalFiles/'
if not os.path.isdir(save_dir):
    os.mkdir(save_dir)

# Write the evaluation to a file
evalFile = f'{save_dir}eval_{options.modelName}.out'
with open(evalFile, 'w') as f:
    f.write("{}\t{}\t{}".format(options.modelName, errorMeson, NSig_pred/np.sqrt(NBkg_pred)))

