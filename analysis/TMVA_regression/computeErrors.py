import ROOT
import numpy as np
import pandas as pd
import argparse
import os

if "/home/submit/pdmonte/CMSSW_10_6_27/src/Hrare2023/analysis/functions.so" not in ROOT.gSystem.GetLibraries():
    ROOT.gSystem.CompileMacro("/home/submit/pdmonte/CMSSW_10_6_27/src/Hrare2023/analysis/functions.cc","k")


def getNumVarsExtra(modelName):
    if modelName.count("NONE") == 1:
        return 0
    elif modelName.count("var") > 0:
        return modelName.count("var")
    else:
        return -1


parser = argparse.ArgumentParser(description="Famous Submitter")
parser.add_argument("-m", "--modelName", type=str, required=True, help="Input the model name (e.g. BDTG_var1_var2).")
options = parser.parse_args()

date = "JUL22"

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

if options.modelName == "RECO":

    dfSGN = ROOT.RDataFrame(chainSGN)
    dfSGN = (dfSGN.Define("scale", "w*lumiIntegrated"))

    dfBKG = ROOT.RDataFrame(chainBKG)
    dfBKG = (dfBKG.Define("scale", "w*lumiIntegrated"))

    cols = ["goodMeson_pt_GEN", "goodMeson_pt"]
    x = dfSGN.AsNumpy(columns=cols)
    pddf_SGN = pd.DataFrame(x)

    goodMesonDiffReco = [x[0] for x in pddf_SGN["goodMeson_pt"].values] - pddf_SGN["goodMeson_pt_GEN"].values
    errorMeson = np.sqrt(np.mean(goodMesonDiffReco**2))
    
    nbins, xlow, xhigh = 200, 105, 145
    h3 = dfSGN.Histo1D(("hist", "HCandMass RECO", nbins, xlow, xhigh), "HCandMass", "scale")
    h6 = dfBKG.Histo1D(("hist", "HCandMass RECO", nbins, xlow, xhigh), "HCandMass", "scale")
    NSig_pred = h3.Integral(h3.FindBin(115), h3.FindBin(135))
    NBkg_pred = h6.Integral(h6.FindBin(115), h6.FindBin(135))

else:
    s = '''
    TMVA::Experimental::RReader modelScale("/data/submit/pdmonte/TMVA_models/weightsVars/TMVARegression_{modelName}.weights.xml");
    computeModelScale = TMVA::Experimental::Compute<{numVarsTotal}, float>(modelScale);
    '''.format(modelName=options.modelName, numVarsTotal=getNumVarsExtra(options.modelName) + 8 + 4)

    ROOT.gInterpreter.ProcessLine(s)
    variables = list(ROOT.modelScale.GetVariableNames())

    dfSGN = ROOT.RDataFrame(chainSGN)
    dfSGN = (dfSGN.Define("scale", "w*lumiIntegrated")
            .Define("scaleFactor", ROOT.computeModelScale, variables)
            .Define("goodMeson_pt_PRED", "scaleFactor[0]*goodMeson_pt[0]")
            .Define("HCandMass_varPRED", "compute_HiggsVars_var(goodMeson_pt_PRED, goodMeson_eta[0], goodMeson_phi[0], goodMeson_mass[0], goodPhotons_pt[0], goodPhotons_eta[0], goodPhotons_phi[0], 0)"))

    dfBKG = ROOT.RDataFrame(chainBKG)
    dfBKG = (dfBKG.Define("scale", "w*lumiIntegrated")
            .Define("scaleFactor", ROOT.computeModelScale, variables)
            .Define("goodMeson_pt_PRED", "scaleFactor[0]*goodMeson_pt[0]")
            .Define("HCandMass_varPRED", "compute_HiggsVars_var(goodMeson_pt_PRED, goodMeson_eta[0], goodMeson_phi[0], goodMeson_mass[0], goodPhotons_pt[0], goodPhotons_eta[0], goodPhotons_phi[0], 0)"))

    cols = ["goodMeson_pt_GEN", "goodMeson_pt_PRED"]
    x = dfSGN.AsNumpy(columns=cols)
    pddf_SGN = pd.DataFrame(x)

    goodMesonDiffPred = pddf_SGN["goodMeson_pt_PRED"].values - pddf_SGN["goodMeson_pt_GEN"].values
    errorMeson = np.sqrt(np.mean(goodMesonDiffPred**2))
    
    nbins, xlow, xhigh = 200, 105, 145
    h3 = dfSGN.Histo1D(("hist", "HCandMass RECO + PT PREDICTED", nbins, xlow, xhigh), "HCandMass_varPRED", "scale")
    h6 = dfBKG.Histo1D(("hist", "HCandMass RECO + PT PREDICTED", nbins, xlow, xhigh), "HCandMass_varPRED", "scale")
    NSig_pred = h3.Integral(h3.FindBin(115), h3.FindBin(135))
    NBkg_pred = h6.Integral(h6.FindBin(115), h6.FindBin(135))

print(errorMeson)
print(NSig_pred)
print(NBkg_pred)
print("Maximize PRED: ", NSig_pred/np.sqrt(NBkg_pred))

save_dir = '/data/submit/pdmonte/TMVA_models/evalFiles/'
if not os.path.isdir(save_dir):
    os.mkdir(save_dir)

# Write the evaluation to a file
evalFile = f'{save_dir}evaluation_{options.modelName}.out'
with open(evalFile, 'w') as f:
    f.write("{}\t{}\t{}".format(options.modelName, errorMeson, NSig_pred/np.sqrt(NBkg_pred)))

