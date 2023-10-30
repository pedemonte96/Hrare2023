import ROOT
import math
from drawMacro import *

if "/home/submit/pdmonte/CMSSW_10_6_27/src/Hrare2023/analysis/func_marti.so" not in ROOT.gSystem.GetLibraries():
    ROOT.gSystem.CompileMacro("/home/submit/pdmonte/CMSSW_10_6_27/src/Hrare2023/analysis/func_marti.cc","k")

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
    if "opt" in modelName:
        numVars -= 1
    return numVars


if __name__ == "__main__":

    pi1Mass = 0.13957018
    k1Mass = 0.493677
    mass1, mass2 = 0, 0

    modelNameOmega = "BDTG_df13_dl3620_v0_v1_opt14816"
    modelNamePhi3 = "BDTG_df13_dl3620_v0_v1_opt13545"
    modelNameD0Star2 = "BDTG_df7_dl3684_v0_v1_opt15136"
    modelNameD0Star3 = "xx"

    date = "OCT27"

    chainSGN_Phi3 = ROOT.TChain("events")
    chainSGN_Omega = ROOT.TChain("events")
    chainSGN_D0Star2 = ROOT.TChain("events")
    chainSGN_D0Star3 = ROOT.TChain("events")
    chainSGN_Phi3.Add("/data/submit/pdmonte/outputs/{0}/2018/outname_mc{1}_GFcat_{2}_2018.root".format(date, 1039, "Phi3Cat"))
    chainSGN_Omega.Add("/data/submit/pdmonte/outputs/{0}/2018/outname_mc{1}_GFcat_{2}_2018.root".format(date, 1038, "OmegaCat"))
    chainSGN_D0Star2.Add("/data/submit/pdmonte/outputs/{0}/2018/outname_mc{1}_GFcat_{2}_2018.root".format(date, 1041, "D0StarCat"))
    chainSGN_D0Star3.Add("/data/submit/pdmonte/outputs/{0}/2018/outname_mc{1}_GFcat_{2}_2018.root".format(date, 1040, "D0StarRhoCat"))

    chainSGN_Omega_0 = ROOT.TChain("events")
    chainSGN_Omega_1 = ROOT.TChain("events")
    chainSGN_Omega_2 = ROOT.TChain("events")
    chainSGN_Omega_0.Add("/data/submit/pdmonte/outputs/{0}/2018/outname_mc{1}_GFcat_{2}_2018_sample0.root".format(date, 1038, "OmegaCat"))
    chainSGN_Omega_1.Add("/data/submit/pdmonte/outputs/{0}/2018/outname_mc{1}_GFcat_{2}_2018_sample1.root".format(date, 1038, "OmegaCat"))
    chainSGN_Omega_2.Add("/data/submit/pdmonte/outputs/{0}/2018/outname_mc{1}_GFcat_{2}_2018_sample2.root".format(date, 1038, "OmegaCat"))
    dfSGN_Omega_0 = ROOT.RDataFrame(chainSGN_Omega_0)
    dfSGN_Omega_1 = ROOT.RDataFrame(chainSGN_Omega_1)
    dfSGN_Omega_2 = ROOT.RDataFrame(chainSGN_Omega_2)

    chainSGN_Phi3_0 = ROOT.TChain("events")
    chainSGN_Phi3_1 = ROOT.TChain("events")
    chainSGN_Phi3_2 = ROOT.TChain("events")
    chainSGN_Phi3_0.Add("/data/submit/pdmonte/outputs/{0}/2018/outname_mc{1}_GFcat_{2}_2018_sample0.root".format(date, 1039, "Phi3Cat"))
    chainSGN_Phi3_1.Add("/data/submit/pdmonte/outputs/{0}/2018/outname_mc{1}_GFcat_{2}_2018_sample1.root".format(date, 1039, "Phi3Cat"))
    chainSGN_Phi3_2.Add("/data/submit/pdmonte/outputs/{0}/2018/outname_mc{1}_GFcat_{2}_2018_sample2.root".format(date, 1039, "Phi3Cat"))
    dfSGN_Phi3_0 = ROOT.RDataFrame(chainSGN_Phi3_0)
    dfSGN_Phi3_1 = ROOT.RDataFrame(chainSGN_Phi3_1)
    dfSGN_Phi3_2 = ROOT.RDataFrame(chainSGN_Phi3_2)

    chainSGN_D0Star2_0 = ROOT.TChain("events")
    chainSGN_D0Star2_1 = ROOT.TChain("events")
    chainSGN_D0Star2_2 = ROOT.TChain("events")
    chainSGN_D0Star2_0.Add("/data/submit/pdmonte/outputs/{0}/2018/outname_mc{1}_GFcat_{2}_2018_sample0.root".format(date, 1041, "D0StarCat"))
    chainSGN_D0Star2_1.Add("/data/submit/pdmonte/outputs/{0}/2018/outname_mc{1}_GFcat_{2}_2018_sample1.root".format(date, 1041, "D0StarCat"))
    chainSGN_D0Star2_2.Add("/data/submit/pdmonte/outputs/{0}/2018/outname_mc{1}_GFcat_{2}_2018_sample2.root".format(date, 1041, "D0StarCat"))
    dfSGN_D0Star2_0 = ROOT.RDataFrame(chainSGN_D0Star2_0)
    dfSGN_D0Star2_1 = ROOT.RDataFrame(chainSGN_D0Star2_1)
    dfSGN_D0Star2_2 = ROOT.RDataFrame(chainSGN_D0Star2_2)

    chainSGN_D0Star3_0 = ROOT.TChain("events")
    chainSGN_D0Star3_1 = ROOT.TChain("events")
    chainSGN_D0Star3_2 = ROOT.TChain("events")
    chainSGN_D0Star3_0.Add("/data/submit/pdmonte/outputs/{0}/2018/outname_mc{1}_GFcat_{2}_2018_sample0.root".format(date, 1040, "D0StarRhoCat"))
    chainSGN_D0Star3_1.Add("/data/submit/pdmonte/outputs/{0}/2018/outname_mc{1}_GFcat_{2}_2018_sample1.root".format(date, 1040, "D0StarRhoCat"))
    chainSGN_D0Star3_2.Add("/data/submit/pdmonte/outputs/{0}/2018/outname_mc{1}_GFcat_{2}_2018_sample2.root".format(date, 1040, "D0StarRhoCat"))
    dfSGN_D0Star3_0 = ROOT.RDataFrame(chainSGN_D0Star3_0)
    dfSGN_D0Star3_1 = ROOT.RDataFrame(chainSGN_D0Star3_1)
    dfSGN_D0Star3_2 = ROOT.RDataFrame(chainSGN_D0Star3_2)

    chainBKG_Omega = ROOT.TChain("events")
    chainBKG_Omega.Add("/data/submit/pdmonte/outputs/{0}/2018/outname_mc10_GFcat_{1}_2018.root".format(date, "OmegaCat"))
    chainBKG_Omega.Add("/data/submit/pdmonte/outputs/{0}/2018/outname_mc11_GFcat_{1}_2018.root".format(date, "OmegaCat"))
    chainBKG_Omega.Add("/data/submit/pdmonte/outputs/{0}/2018/outname_mc12_GFcat_{1}_2018.root".format(date, "OmegaCat"))
    chainBKG_Omega.Add("/data/submit/pdmonte/outputs/{0}/2018/outname_mc13_GFcat_{1}_2018.root".format(date, "OmegaCat"))
    chainBKG_Omega.Add("/data/submit/pdmonte/outputs/{0}/2018/outname_mc14_GFcat_{1}_2018.root".format(date, "OmegaCat"))

    chainBKG_Phi3 = ROOT.TChain("events")
    chainBKG_Phi3.Add("/data/submit/pdmonte/outputs/{0}/2018/outname_mc10_GFcat_{1}_2018.root".format(date, "Phi3Cat"))
    chainBKG_Phi3.Add("/data/submit/pdmonte/outputs/{0}/2018/outname_mc11_GFcat_{1}_2018.root".format(date, "Phi3Cat"))
    chainBKG_Phi3.Add("/data/submit/pdmonte/outputs/{0}/2018/outname_mc12_GFcat_{1}_2018.root".format(date, "Phi3Cat"))
    chainBKG_Phi3.Add("/data/submit/pdmonte/outputs/{0}/2018/outname_mc13_GFcat_{1}_2018.root".format(date, "Phi3Cat"))
    chainBKG_Phi3.Add("/data/submit/pdmonte/outputs/{0}/2018/outname_mc14_GFcat_{1}_2018.root".format(date, "Phi3Cat"))

    chainBKG_D0Star2 = ROOT.TChain("events")
    chainBKG_D0Star2.Add("/data/submit/pdmonte/outputs/{0}/2018/outname_mc10_GFcat_{1}_2018.root".format(date, "D0StarCat"))
    chainBKG_D0Star2.Add("/data/submit/pdmonte/outputs/{0}/2018/outname_mc11_GFcat_{1}_2018.root".format(date, "D0StarCat"))
    chainBKG_D0Star2.Add("/data/submit/pdmonte/outputs/{0}/2018/outname_mc12_GFcat_{1}_2018.root".format(date, "D0StarCat"))
    chainBKG_D0Star2.Add("/data/submit/pdmonte/outputs/{0}/2018/outname_mc13_GFcat_{1}_2018.root".format(date, "D0StarCat"))
    chainBKG_D0Star2.Add("/data/submit/pdmonte/outputs/{0}/2018/outname_mc14_GFcat_{1}_2018.root".format(date, "D0StarCat"))

    chainBKG_D0Star3 = ROOT.TChain("events")
    chainBKG_D0Star3.Add("/data/submit/pdmonte/outputs/{0}/2018/outname_mc10_GFcat_{1}_2018.root".format(date, "D0StarRhoCat"))
    chainBKG_D0Star3.Add("/data/submit/pdmonte/outputs/{0}/2018/outname_mc11_GFcat_{1}_2018.root".format(date, "D0StarRhoCat"))
    chainBKG_D0Star3.Add("/data/submit/pdmonte/outputs/{0}/2018/outname_mc12_GFcat_{1}_2018.root".format(date, "D0StarRhoCat"))
    chainBKG_D0Star3.Add("/data/submit/pdmonte/outputs/{0}/2018/outname_mc13_GFcat_{1}_2018.root".format(date, "D0StarRhoCat"))
    chainBKG_D0Star3.Add("/data/submit/pdmonte/outputs/{0}/2018/outname_mc14_GFcat_{1}_2018.root".format(date, "D0StarRhoCat"))

    dfSGN_Phi3 = ROOT.RDataFrame(chainSGN_Phi3)
    dfSGN_Phi3 = (dfSGN_Phi3.Define("scale", "w*lumiIntegrated")
                    .Define("newDitrackMass", "sum2Body(goodMeson_trk1_pt[0], goodMeson_trk1_eta[0], goodMeson_trk1_phi[0], {}, goodMeson_trk2_pt[0], goodMeson_trk2_eta[0], goodMeson_trk2_phi[0], {}).M()".format(pi1Mass, pi1Mass))
                    .Define("DiffFittedMass", "goodMeson_ditrk_mass - goodMeson_ditrk_mass_GEN")
                    .Define("DiffSumMass", "newDitrackMass - goodMeson_ditrk_mass_GEN")
                    .Define("DiffRawMass", "goodMeson_mass_raw - goodMeson_mass_GEN")
                    .Define("DiffModifiedMass", "goodMeson_mass - goodMeson_mass_GEN")
                    .Define("Residual_ditrk_pt", "goodMeson_ditrk_pt - goodMeson_ditrk_pt_GEN")
                    .Define("Residual_old_pt", "goodMeson_pt - goodMeson_pt_GEN")
                    .Define("Residual_ditrk_mass", "goodMeson_ditrk_mass - goodMeson_ditrk_mass_GEN")
                    .Define("Residual_ditrk_eta", "goodMeson_ditrk_eta - goodMeson_ditrk_eta_GEN")
                    .Define("Residual_ditrk_phi", "goodMeson_ditrk_phi - goodMeson_ditrk_phi_GEN"))
    
    dfSGN_Omega = ROOT.RDataFrame(chainSGN_Omega)
    dfSGN_Omega = (dfSGN_Omega.Define("scale", "w*lumiIntegrated")
                    .Define("newDitrackMass", "sum2Body(goodMeson_trk1_pt[0], goodMeson_trk1_eta[0], goodMeson_trk1_phi[0], {}, goodMeson_trk2_pt[0], goodMeson_trk2_eta[0], goodMeson_trk2_phi[0], {}).M()".format(pi1Mass, pi1Mass))
                    .Define("DiffFittedMass", "goodMeson_ditrk_mass - goodMeson_ditrk_mass_GEN")
                    .Define("DiffSumMass", "newDitrackMass - goodMeson_ditrk_mass_GEN")
                    .Define("DiffRawMass", "goodMeson_mass_raw - goodMeson_mass_GEN")
                    .Define("DiffModifiedMass", "goodMeson_mass - goodMeson_mass_GEN")
                    .Define("Residual_ditrk_pt", "goodMeson_ditrk_pt - goodMeson_ditrk_pt_GEN")
                    .Define("Residual_old_pt", "goodMeson_pt - goodMeson_pt_GEN")
                    .Define("Residual_ditrk_mass", "goodMeson_ditrk_mass - goodMeson_ditrk_mass_GEN")
                    .Define("Residual_ditrk_eta", "goodMeson_ditrk_eta - goodMeson_ditrk_eta_GEN")
                    .Define("Residual_ditrk_phi", "goodMeson_ditrk_phi - goodMeson_ditrk_phi_GEN"))
    
    dfSGN_D0Star2 = ROOT.RDataFrame(chainSGN_D0Star2)
    dfSGN_D0Star2 = (dfSGN_D0Star2.Define("scale", "w*lumiIntegrated")
                    .Define("newDitrackMass", "sum2Body(goodMeson_trk1_pt[0], goodMeson_trk1_eta[0], goodMeson_trk1_phi[0], {}, goodMeson_trk2_pt[0], goodMeson_trk2_eta[0], goodMeson_trk2_phi[0], {}).M()".format(pi1Mass, k1Mass))
                    .Define("DiffFittedMass", "goodMeson_ditrk_mass - goodMeson_ditrk_mass_GEN")
                    .Define("DiffSumMass", "newDitrackMass - goodMeson_ditrk_mass_GEN")
                    .Define("DiffRawMass", "goodMeson_mass_raw - goodMeson_mass_GEN")
                    .Define("DiffModifiedMass", "goodMeson_mass - goodMeson_mass_GEN")
                    .Define("Residual_ditrk_pt", "goodMeson_ditrk_pt - goodMeson_ditrk_pt_GEN")
                    .Define("Residual_old_pt", "goodMeson_pt - goodMeson_pt_GEN")
                    .Define("Residual_ditrk_mass", "goodMeson_ditrk_mass - goodMeson_ditrk_mass_GEN")
                    .Define("Residual_ditrk_eta", "goodMeson_ditrk_eta - goodMeson_ditrk_eta_GEN")
                    .Define("Residual_ditrk_phi", "goodMeson_ditrk_phi - goodMeson_ditrk_phi_GEN"))
    
    dfSGN_D0Star3 = ROOT.RDataFrame(chainSGN_D0Star3)
    dfSGN_D0Star3 = (dfSGN_D0Star3.Define("scale", "w*lumiIntegrated")
                    .Define("newDitrackMass", "sum2Body(goodMeson_trk1_pt[0], goodMeson_trk1_eta[0], goodMeson_trk1_phi[0], {}, goodMeson_trk2_pt[0], goodMeson_trk2_eta[0], goodMeson_trk2_phi[0], {}).M()".format(pi1Mass, k1Mass))
                    .Define("DiffFittedMass", "goodMeson_ditrk_mass - goodMeson_ditrk_mass_GEN")
                    .Define("DiffSumMass", "newDitrackMass - goodMeson_ditrk_mass_GEN")
                    .Define("DiffRawMass", "goodMeson_mass_raw - goodMeson_mass_GEN")
                    .Define("DiffModifiedMass", "goodMeson_mass - goodMeson_mass_GEN")
                    .Define("Residual_ditrk_pt", "goodMeson_ditrk_pt - goodMeson_ditrk_pt_GEN")
                    .Define("Residual_old_pt", "goodMeson_pt - goodMeson_pt_GEN")
                    .Define("Residual_ditrk_mass", "goodMeson_ditrk_mass - goodMeson_ditrk_mass_GEN")
                    .Define("Residual_ditrk_eta", "goodMeson_ditrk_eta - goodMeson_ditrk_eta_GEN")
                    .Define("Residual_ditrk_phi", "goodMeson_ditrk_phi - goodMeson_ditrk_phi_GEN"))
    
    s = '''
    TMVA::Experimental::RReader modelScaleOmega0("/data/submit/pdmonte/TMVA_models/weightsOpts/TMVARegression_{modelName}_{channel}_0.weights.xml");
    computeModelScaleOmega0 = TMVA::Experimental::Compute<{numVarsTotal}, float>(modelScaleOmega0);
    TMVA::Experimental::RReader modelScaleOmega1("/data/submit/pdmonte/TMVA_models/weightsOpts/TMVARegression_{modelName}_{channel}_1.weights.xml");
    computeModelScaleOmega1 = TMVA::Experimental::Compute<{numVarsTotal}, float>(modelScaleOmega1);
    TMVA::Experimental::RReader modelScaleOmega2("/data/submit/pdmonte/TMVA_models/weightsOpts/TMVARegression_{modelName}_{channel}_2.weights.xml");
    computeModelScaleOmega2 = TMVA::Experimental::Compute<{numVarsTotal}, float>(modelScaleOmega2);
    '''.format(modelName=modelNameOmega, channel="omega", numVarsTotal=getTotalNumVars(modelNameOmega))
    s += '''
    TMVA::Experimental::RReader modelScalePhi0("/data/submit/pdmonte/TMVA_models/weightsOpts/TMVARegression_{modelName}_{channel}_0.weights.xml");
    computeModelScalePhi0 = TMVA::Experimental::Compute<{numVarsTotal}, float>(modelScalePhi0);
    TMVA::Experimental::RReader modelScalePhi1("/data/submit/pdmonte/TMVA_models/weightsOpts/TMVARegression_{modelName}_{channel}_1.weights.xml");
    computeModelScalePhi1 = TMVA::Experimental::Compute<{numVarsTotal}, float>(modelScalePhi1);
    TMVA::Experimental::RReader modelScalePhi2("/data/submit/pdmonte/TMVA_models/weightsOpts/TMVARegression_{modelName}_{channel}_2.weights.xml");
    computeModelScalePhi2 = TMVA::Experimental::Compute<{numVarsTotal}, float>(modelScalePhi2);
    '''.format(modelName=modelNamePhi3, channel="phi", numVarsTotal=getTotalNumVars(modelNamePhi3))
    s += '''
    TMVA::Experimental::RReader modelScaleD0Star0("/data/submit/pdmonte/TMVA_models/weightsOpts/TMVARegression_{modelName}_{channel}_0.weights.xml");
    computeModelScaleD0Star0 = TMVA::Experimental::Compute<{numVarsTotal}, float>(modelScaleD0Star0);
    TMVA::Experimental::RReader modelScaleD0Star1("/data/submit/pdmonte/TMVA_models/weightsOpts/TMVARegression_{modelName}_{channel}_1.weights.xml");
    computeModelScaleD0Star1 = TMVA::Experimental::Compute<{numVarsTotal}, float>(modelScaleD0Star1);
    TMVA::Experimental::RReader modelScaleD0Star2("/data/submit/pdmonte/TMVA_models/weightsOpts/TMVARegression_{modelName}_{channel}_2.weights.xml");
    computeModelScaleD0Star2 = TMVA::Experimental::Compute<{numVarsTotal}, float>(modelScaleD0Star2);
    '''.format(modelName=modelNameD0Star2, channel="d0star", numVarsTotal=getTotalNumVars(modelNameD0Star2))
    ROOT.gInterpreter.ProcessLine(s)
    variablesOmega = list(ROOT.modelScaleOmega0.GetVariableNames())
    variablesPhi = list(ROOT.modelScalePhi0.GetVariableNames())
    variablesD0Star = list(ROOT.modelScaleD0Star0.GetVariableNames())
    #variablesOmega = list(ROOT.modelScaleOmega0.GetVariableNames())

    dfSGN_Omega_0 = (dfSGN_Omega_0.Define("scale", "w*lumiIntegrated/3.")
        .Define("scaleFactor", ROOT.computeModelScaleOmega0, variablesOmega)
        .Define("goodMeson_pt_PRED", "scaleFactor[0]*goodMeson_pt[0]")
        .Define("Residual_old_pt", "goodMeson_pt - goodMeson_pt_GEN")
        .Define("Residual_new_pt", "goodMeson_pt_PRED - goodMeson_pt_GEN")
        .Define("HCandMass_varPRED", "compute_HiggsVars_var(goodMeson_pt_PRED, goodMeson_eta[0], goodMeson_phi[0], goodMeson_mass[0], goodPhotons_pt[0], goodPhotons_eta[0], goodPhotons_phi[0], 0)"))
    dfSGN_Omega_1 = (dfSGN_Omega_1.Define("scale", "w*lumiIntegrated/3.")
        .Define("scaleFactor", ROOT.computeModelScaleOmega1, variablesOmega)
        .Define("goodMeson_pt_PRED", "scaleFactor[0]*goodMeson_pt[0]")
        .Define("Residual_old_pt", "goodMeson_pt - goodMeson_pt_GEN")
        .Define("Residual_new_pt", "goodMeson_pt_PRED - goodMeson_pt_GEN")
        .Define("HCandMass_varPRED", "compute_HiggsVars_var(goodMeson_pt_PRED, goodMeson_eta[0], goodMeson_phi[0], goodMeson_mass[0], goodPhotons_pt[0], goodPhotons_eta[0], goodPhotons_phi[0], 0)"))
    dfSGN_Omega_2 = (dfSGN_Omega_2.Define("scale", "w*lumiIntegrated/3.")
        .Define("scaleFactor", ROOT.computeModelScaleOmega2, variablesOmega)
        .Define("goodMeson_pt_PRED", "scaleFactor[0]*goodMeson_pt[0]")
        .Define("Residual_old_pt", "goodMeson_pt - goodMeson_pt_GEN")
        .Define("Residual_new_pt", "goodMeson_pt_PRED - goodMeson_pt_GEN")
        .Define("HCandMass_varPRED", "compute_HiggsVars_var(goodMeson_pt_PRED, goodMeson_eta[0], goodMeson_phi[0], goodMeson_mass[0], goodPhotons_pt[0], goodPhotons_eta[0], goodPhotons_phi[0], 0)"))
    
    dfSGN_Phi3_0 = (dfSGN_Phi3_0.Define("scale", "w*lumiIntegrated/3.")
        .Define("scaleFactor", ROOT.computeModelScalePhi0, variablesPhi)
        .Define("goodMeson_pt_PRED", "scaleFactor[0]*goodMeson_pt[0]")
        .Define("Residual_old_pt", "goodMeson_pt - goodMeson_pt_GEN")
        .Define("Residual_new_pt", "goodMeson_pt_PRED - goodMeson_pt_GEN")
        .Define("HCandMass_varPRED", "compute_HiggsVars_var(goodMeson_pt_PRED, goodMeson_eta[0], goodMeson_phi[0], goodMeson_mass[0], goodPhotons_pt[0], goodPhotons_eta[0], goodPhotons_phi[0], 0)"))
    dfSGN_Phi3_1 = (dfSGN_Phi3_1.Define("scale", "w*lumiIntegrated/3.")
        .Define("scaleFactor", ROOT.computeModelScalePhi1, variablesPhi)
        .Define("goodMeson_pt_PRED", "scaleFactor[0]*goodMeson_pt[0]")
        .Define("Residual_old_pt", "goodMeson_pt - goodMeson_pt_GEN")
        .Define("Residual_new_pt", "goodMeson_pt_PRED - goodMeson_pt_GEN")
        .Define("HCandMass_varPRED", "compute_HiggsVars_var(goodMeson_pt_PRED, goodMeson_eta[0], goodMeson_phi[0], goodMeson_mass[0], goodPhotons_pt[0], goodPhotons_eta[0], goodPhotons_phi[0], 0)"))
    dfSGN_Phi3_2 = (dfSGN_Phi3_2.Define("scale", "w*lumiIntegrated/3.")
        .Define("scaleFactor", ROOT.computeModelScalePhi2, variablesPhi)
        .Define("goodMeson_pt_PRED", "scaleFactor[0]*goodMeson_pt[0]")
        .Define("Residual_old_pt", "goodMeson_pt - goodMeson_pt_GEN")
        .Define("Residual_new_pt", "goodMeson_pt_PRED - goodMeson_pt_GEN")
        .Define("HCandMass_varPRED", "compute_HiggsVars_var(goodMeson_pt_PRED, goodMeson_eta[0], goodMeson_phi[0], goodMeson_mass[0], goodPhotons_pt[0], goodPhotons_eta[0], goodPhotons_phi[0], 0)"))
    
    dfSGN_D0Star2_0 = (dfSGN_D0Star2_0.Define("scale", "w*lumiIntegrated/3.")
        .Define("scaleFactor", ROOT.computeModelScaleD0Star0, variablesD0Star)
        .Define("goodMeson_pt_PRED", "scaleFactor[0]*goodMeson_pt[0]")
        .Define("Residual_old_pt", "goodMeson_pt - goodMeson_pt_GEN")
        .Define("Residual_new_pt", "goodMeson_pt_PRED - goodMeson_pt_GEN")
        .Define("HCandMass_varPRED", "compute_HiggsVars_var(goodMeson_pt_PRED, goodMeson_eta[0], goodMeson_phi[0], goodMeson_mass[0], goodPhotons_pt[0], goodPhotons_eta[0], goodPhotons_phi[0], 0)"))
    dfSGN_D0Star2_1 = (dfSGN_D0Star2_1.Define("scale", "w*lumiIntegrated/3.")
        .Define("scaleFactor", ROOT.computeModelScaleD0Star1, variablesD0Star)
        .Define("goodMeson_pt_PRED", "scaleFactor[0]*goodMeson_pt[0]")
        .Define("Residual_old_pt", "goodMeson_pt - goodMeson_pt_GEN")
        .Define("Residual_new_pt", "goodMeson_pt_PRED - goodMeson_pt_GEN")
        .Define("HCandMass_varPRED", "compute_HiggsVars_var(goodMeson_pt_PRED, goodMeson_eta[0], goodMeson_phi[0], goodMeson_mass[0], goodPhotons_pt[0], goodPhotons_eta[0], goodPhotons_phi[0], 0)"))
    dfSGN_D0Star2_2 = (dfSGN_D0Star2_2.Define("scale", "w*lumiIntegrated/3.")
        .Define("scaleFactor", ROOT.computeModelScaleD0Star2, variablesD0Star)
        .Define("goodMeson_pt_PRED", "scaleFactor[0]*goodMeson_pt[0]")
        .Define("Residual_old_pt", "goodMeson_pt - goodMeson_pt_GEN")
        .Define("Residual_new_pt", "goodMeson_pt_PRED - goodMeson_pt_GEN")
        .Define("HCandMass_varPRED", "compute_HiggsVars_var(goodMeson_pt_PRED, goodMeson_eta[0], goodMeson_phi[0], goodMeson_mass[0], goodPhotons_pt[0], goodPhotons_eta[0], goodPhotons_phi[0], 0)"))
    
    dfSGN_D0Star3_0 = (dfSGN_D0Star3_0.Define("scale", "w*lumiIntegrated/3.")
        #.Define("scaleFactor", ROOT.computeModelScaleD0Star0, variablesD0Star)
        .Define("goodMeson_pt_PRED", "goodMeson_pt[0]")
        .Define("Residual_old_pt", "goodMeson_pt - goodMeson_pt_GEN")
        .Define("Residual_new_pt", "goodMeson_pt_PRED - goodMeson_pt_GEN")
        .Define("HCandMass_varPRED", "compute_HiggsVars_var(goodMeson_pt_PRED, goodMeson_eta[0], goodMeson_phi[0], goodMeson_mass[0], goodPhotons_pt[0], goodPhotons_eta[0], goodPhotons_phi[0], 0)"))
    dfSGN_D0Star3_1 = (dfSGN_D0Star3_1.Define("scale", "w*lumiIntegrated/3.")
        #.Define("scaleFactor", ROOT.computeModelScaleD0Star1, variablesD0Star)
        .Define("goodMeson_pt_PRED", "goodMeson_pt[0]")
        .Define("Residual_old_pt", "goodMeson_pt - goodMeson_pt_GEN")
        .Define("Residual_new_pt", "goodMeson_pt_PRED - goodMeson_pt_GEN")
        .Define("HCandMass_varPRED", "compute_HiggsVars_var(goodMeson_pt_PRED, goodMeson_eta[0], goodMeson_phi[0], goodMeson_mass[0], goodPhotons_pt[0], goodPhotons_eta[0], goodPhotons_phi[0], 0)"))
    dfSGN_D0Star3_2 = (dfSGN_D0Star3_2.Define("scale", "w*lumiIntegrated/3.")
        #.Define("scaleFactor", ROOT.computeModelScaleD0Star2, variablesD0Star)
        .Define("goodMeson_pt_PRED", "goodMeson_pt[0]")
        .Define("Residual_old_pt", "goodMeson_pt - goodMeson_pt_GEN")
        .Define("Residual_new_pt", "goodMeson_pt_PRED - goodMeson_pt_GEN")
        .Define("HCandMass_varPRED", "compute_HiggsVars_var(goodMeson_pt_PRED, goodMeson_eta[0], goodMeson_phi[0], goodMeson_mass[0], goodPhotons_pt[0], goodPhotons_eta[0], goodPhotons_phi[0], 0)"))
    
    channels = ["Phi3", "Omega", "D0Star_2body", "D0Star_3body"]
    channels_latex = ["#phi", "#omega", "D^{*0} 2-body", "D^{*0} 3-body"]
    dfsSGN = [dfSGN_Phi3, dfSGN_Omega, dfSGN_D0Star2, dfSGN_D0Star3]
    dfsSGN_0 = [dfSGN_Phi3_0, dfSGN_Omega_0, dfSGN_D0Star2_0, dfSGN_D0Star3_0]
    dfsSGN_1 = [dfSGN_Phi3_1, dfSGN_Omega_1, dfSGN_D0Star2_1, dfSGN_D0Star3_1]
    dfsSGN_2 = [dfSGN_Phi3_2, dfSGN_Omega_2, dfSGN_D0Star2_2, dfSGN_D0Star3_2]
    
    # Kinetic fit comparison --------------------------------------------------------------------------------------------
    xLabels = ["m_{#phi}^{diTrk, RECO} - m_{#phi}^{diTrk, GEN}", "m_{#omega}^{diTrk, RECO} - m_{#omega}^{diTrk, GEN}", "m_{D^{0}}^{RECO} - m_{D^{0}}^{GEN}", "m_{D^{0}}^{RECO} - m_{D^{0}}^{GEN}"]
    for i, c in enumerate(channels):
        fileName = "{}_kinematic_fit_residual.png".format(c)
        df = dfsSGN[i]
        options = {"title": "Ditrack mass residual {}".format(channels_latex[i]), "labelXAxis": xLabels[i], "labelYAxis": "Events", "xRange": (-0.1, 0.1)}
        nbins, xlow, xhigh = 500, -0.5, 0.5
        histograms = []
        name1 = "w/ kinematic fit"
        h1 = df.Histo1D(("hist", name1, nbins, xlow, xhigh), "DiffFittedMass", "scale").GetValue()
        name2 = "w/o kinematic fit"
        h2 = df.Histo1D(("hist", name2, nbins, xlow, xhigh), "DiffSumMass", "scale").GetValue()
        histograms.append((name1, h1))
        histograms.append((name2, h2))
        print("{} MASS STD SUM:\t".format(c), h2.GetStdDev()*1000)
        print("{} MASS STD FIT:\t".format(c), h1.GetStdDev()*1000, h1.GetStdDev()/h2.GetStdDev()-1)
        savePlot(histograms, fileName, options=options)

    # New full meson mass comparison --------------------------------------------------------------------------------------------
    xLabels = ["m_{#phi}^{RECO} - m_{#phi}^{GEN}", "m_{#omega}^{RECO} - m_{#omega}^{GEN}", "m_{D^{*0}}^{RECO} - m_{D^{*0}}^{GEN}"]
    channels_latex_bis = ["#phi", "#omega", "D^{*0} 3-body"]
    dfsSGN_bis = [dfSGN_Phi3, dfSGN_Omega, dfSGN_D0Star3]
    for i, c, in enumerate(["Phi3", "Omega", "D0Star_3body"]):
        fileName = "{}_fullmeson_mass_residual.png".format(c)
        df = dfsSGN_bis[i]
        options = {"title": "Full mass residual {}".format(channels_latex_bis[i]), "labelXAxis": xLabels[i], "labelYAxis": "Events", "xRange": (-0.6, 0.6)}
        nbins, xlow, xhigh = 100, -0.6, 0.6
        histograms = []
        name1 = "w/ pi0 mass"
        h1 = df.Histo1D(("hist", name1, nbins, xlow, xhigh), "DiffModifiedMass", "scale").GetValue()
        name2 = "w/o pi0 mass"
        h2 = df.Histo1D(("hist", name2, nbins, xlow, xhigh), "DiffRawMass", "scale").GetValue()
        histograms.append((name1, h1))
        histograms.append((name2, h2))
        print("{} MASS STD RAW:\t".format(c), h2.GetStdDev()*1000)
        print("{} MASS STD PI0:\t".format(c), h1.GetStdDev()*1000, h1.GetStdDev()/h2.GetStdDev()-1)
        savePlot(histograms, fileName, options=options)

    # Ditrack PT residuals --------------------------------------------------------------------------------------------
    fileName = "ditrack_residuals_pt.png"
    nbins, xlow, xhigh = 100, -3., 3.
    options = {"title": "Ditrack system p_{T} residual", "labelXAxis": "p_{T}^{dtk}(reco) - p_{T}^{dtk}(gen) [GeV]", "labelYAxis": "Events"}
    histograms = []
    name1 = "#phi"
    h1 = dfSGN_Phi3.Histo1D(("hist", name1, nbins, xlow, xhigh), "Residual_ditrk_pt").GetValue()
    h1.Scale(1/h1.GetEntries())
    name2 = "#omega"
    h2 = dfSGN_Omega.Histo1D(("hist", name2, nbins, xlow, xhigh), "Residual_ditrk_pt").GetValue()
    h2.Scale(1/h2.GetEntries())
    name3 = "D^{*0} 2-body"
    h3 = dfSGN_D0Star2.Histo1D(("hist", name3, nbins, xlow, xhigh), "Residual_ditrk_pt").GetValue()
    h3.Scale(1/h3.GetEntries())
    name4 = "D^{*0} 3-body"
    h4 = dfSGN_D0Star3.Histo1D(("hist", name4, nbins, xlow, xhigh), "Residual_ditrk_pt").GetValue()
    h4.Scale(1/h4.GetEntries())
    
    histograms.append((name1, h1))
    histograms.append((name2, h2))
    histograms.append((name3, h3))
    histograms.append((name4, h4))
    savePlot(histograms, fileName, options=options)

    # Ditrack Mass residuals --------------------------------------------------------------------------------------------
    fileName = "ditrack_residuals_mass.png"
    nbins, xlow, xhigh = 100, -0.2, 0.2
    options = {"title": "Ditrack system mass residual", "labelXAxis": "m^{dtk}(reco) - m^{dtk}(gen) [GeV]", "labelYAxis": "Events"}
    histograms = []
    name1 = "#phi"
    h1 = dfSGN_Phi3.Histo1D(("hist", name1, nbins, xlow, xhigh), "Residual_ditrk_mass").GetValue()
    h1.Scale(1/h1.GetEntries())
    name2 = "#omega"
    h2 = dfSGN_Omega.Histo1D(("hist", name2, nbins, xlow, xhigh), "Residual_ditrk_mass").GetValue()
    h2.Scale(1/h2.GetEntries())
    name3 = "D^{*0} 2-body"
    h3 = dfSGN_D0Star2.Histo1D(("hist", name3, nbins, xlow, xhigh), "Residual_ditrk_mass").GetValue()
    h3.Scale(1/h3.GetEntries())
    name4 = "D^{*0} 3-body"
    h4 = dfSGN_D0Star3.Histo1D(("hist", name4, nbins, xlow, xhigh), "Residual_ditrk_mass").GetValue()
    h4.Scale(1/h4.GetEntries())
    
    histograms.append((name1, h1))
    histograms.append((name2, h2))
    histograms.append((name3, h3))
    histograms.append((name4, h4))
    savePlot(histograms, fileName, options=options)

    # Ditrack Eta residuals --------------------------------------------------------------------------------------------
    fileName = "ditrack_residuals_eta.png"
    nbins, xlow, xhigh = 100, -0.004, 0.004
    options = {"title": "Ditrack system #eta residual", "labelXAxis": "#eta^{dtk}(reco) - #eta^{dtk}(gen)", "labelYAxis": "Events"}
    histograms = []
    name1 = "#phi"
    h1 = dfSGN_Phi3.Histo1D(("hist", name1, nbins, xlow, xhigh), "Residual_ditrk_eta").GetValue()
    h1.Scale(1/h1.GetEntries())
    name2 = "#omega"
    h2 = dfSGN_Omega.Histo1D(("hist", name2, nbins, xlow, xhigh), "Residual_ditrk_eta").GetValue()
    h2.Scale(1/h2.GetEntries())
    name3 = "D^{*0} 2-body"
    h3 = dfSGN_D0Star2.Histo1D(("hist", name3, nbins, xlow, xhigh), "Residual_ditrk_eta").GetValue()
    h3.Scale(1/h3.GetEntries())
    name4 = "D^{*0} 3-body"
    h4 = dfSGN_D0Star3.Histo1D(("hist", name4, nbins, xlow, xhigh), "Residual_ditrk_eta").GetValue()
    h4.Scale(1/h4.GetEntries())
    
    histograms.append((name1, h1))
    histograms.append((name2, h2))
    histograms.append((name3, h3))
    histograms.append((name4, h4))
    savePlot(histograms, fileName, options=options)

    # Ditrack Phi residuals --------------------------------------------------------------------------------------------
    fileName = "ditrack_residuals_phi.png"
    nbins, xlow, xhigh = 100, -0.004, 0.004
    options = {"title": "Ditrack system #phi residual", "labelXAxis": "#phi^{dtk}(reco) - #phi^{dtk}(gen)", "labelYAxis": "Events"}
    histograms = []
    name1 = "#phi"
    h1 = dfSGN_Phi3.Histo1D(("hist", name1, nbins, xlow, xhigh), "Residual_ditrk_phi").GetValue()
    h1.Scale(1/h1.GetEntries())
    name2 = "#omega"
    h2 = dfSGN_Omega.Histo1D(("hist", name2, nbins, xlow, xhigh), "Residual_ditrk_phi").GetValue()
    h2.Scale(1/h2.GetEntries())
    name3 = "D^{*0} 2-body"
    h3 = dfSGN_D0Star2.Histo1D(("hist", name3, nbins, xlow, xhigh), "Residual_ditrk_phi").GetValue()
    h3.Scale(1/h3.GetEntries())
    name4 = "D^{*0} 3-body"
    h4 = dfSGN_D0Star3.Histo1D(("hist", name4, nbins, xlow, xhigh), "Residual_ditrk_phi").GetValue()
    h4.Scale(1/h4.GetEntries())
    
    histograms.append((name1, h1))
    histograms.append((name2, h2))
    histograms.append((name3, h3))
    histograms.append((name4, h4))
    savePlot(histograms, fileName, options=options)

    # Full meson PT residuals --------------------------------------------------------------------------------------------
    fileName = "fullmeson_residuals_pt.png"
    nbins, xlow, xhigh = 100, -30., 30.
    options = {"title": "Full meson p_{T} residual", "labelXAxis": "p_{T}(reco) - p_{T}(gen) [GeV]", "labelYAxis": "Events"}
    histograms = []
    name1 = "#phi"
    h1 = dfSGN_Phi3.Histo1D(("hist", name1, nbins, xlow, xhigh), "Residual_old_pt").GetValue()
    h1.Scale(1/h1.GetEntries())
    name2 = "#omega"
    h2 = dfSGN_Omega.Histo1D(("hist", name2, nbins, xlow, xhigh), "Residual_old_pt").GetValue()
    h2.Scale(1/h2.GetEntries())
    name3 = "D^{*0} 2-body"
    h3 = dfSGN_D0Star2.Histo1D(("hist", name3, nbins, xlow, xhigh), "Residual_old_pt").GetValue()
    h3.Scale(1/h3.GetEntries())
    name4 = "D^{*0} 3-body"
    h4 = dfSGN_D0Star3.Histo1D(("hist", name4, nbins, xlow, xhigh), "Residual_old_pt").GetValue()
    h4.Scale(1/h4.GetEntries())
    
    histograms.append((name1, h1))
    histograms.append((name2, h2))
    histograms.append((name3, h3))
    histograms.append((name4, h4))
    savePlot(histograms, fileName, options=options)

    # Good Meson PT Phi --------------------------------------------------------------------------------------------
    for i, c in enumerate(channels):
        fileName = "{}_model_pt.png".format(c)
        df_0, df_1, df_2 = dfsSGN_0[i], dfsSGN_1[i], dfsSGN_2[i]
        nbins, xlow, xhigh = 100, 0., 150.
        options = {"title": "{} p_{{T}}".format(channels_latex[i]), "labelXAxis": "p_{T} [GeV]", "labelYAxis": "Events", "style": ["f", "l", "l"], "colors": [ROOT.kBlue - 10, ROOT.kRed + 1, ROOT.kGreen + 2]}
        histograms = []
        name1 = "Generation"
        h1 = df_0.Histo1D(("hist", name1, nbins, xlow, xhigh), "goodMeson_pt_GEN", "scale").GetValue()
        h1.Add(df_1.Histo1D(("hist", name1, nbins, xlow, xhigh), "goodMeson_pt_GEN", "scale").GetValue())
        h1.Add(df_2.Histo1D(("hist", name1, nbins, xlow, xhigh), "goodMeson_pt_GEN", "scale").GetValue())
        name2 = "Predicted"
        h2 = df_0.Histo1D(("hist", name2, nbins, xlow, xhigh), "goodMeson_pt_PRED", "scale").GetValue()
        h2.Add(df_1.Histo1D(("hist", name2, nbins, xlow, xhigh), "goodMeson_pt_PRED", "scale").GetValue())
        h2.Add(df_2.Histo1D(("hist", name2, nbins, xlow, xhigh), "goodMeson_pt_PRED", "scale").GetValue())
        name3 = "Reconstructed"
        h3 = df_0.Histo1D(("hist", name3, nbins, xlow, xhigh), "goodMeson_pt", "scale").GetValue()
        h3.Add(df_1.Histo1D(("hist", name3, nbins, xlow, xhigh), "goodMeson_pt", "scale").GetValue())
        h3.Add(df_2.Histo1D(("hist", name3, nbins, xlow, xhigh), "goodMeson_pt", "scale").GetValue())

        histograms.append((name1, h1))
        histograms.append((name2, h2))
        histograms.append((name3, h3))
        savePlot(histograms, fileName, options=options)

    # Good Meson PT Residuals --------------------------------------------------------------------------------------------
    for i, c in enumerate(channels):
        fileName = "{}_model_pt_residuals.png".format(c)
        df_0, df_1, df_2 = dfsSGN_0[i], dfsSGN_1[i], dfsSGN_2[i]
        nbins, xlow, xhigh = 100, -20., 20.
        options = {"title": "{} p_{{T}} residuals".format(channels_latex[i]), "labelXAxis": "p_{T} [GeV]", "labelYAxis": "Events"}
        histograms = []
        name1 = "Predicted"
        h1 = df_0.Histo1D(("hist", name1, nbins, xlow, xhigh), "Residual_new_pt", "scale").GetValue()
        h1.Add(df_1.Histo1D(("hist", name1, nbins, xlow, xhigh), "Residual_new_pt", "scale").GetValue())
        h1.Add(df_2.Histo1D(("hist", name1, nbins, xlow, xhigh), "Residual_new_pt", "scale").GetValue())
        name2 = "Reconstructed"
        h2 = df_0.Histo1D(("hist", name2, nbins, xlow, xhigh), "Residual_old_pt", "scale").GetValue()
        h2.Add(df_1.Histo1D(("hist", name2, nbins, xlow, xhigh), "Residual_old_pt", "scale").GetValue())
        h2.Add(df_2.Histo1D(("hist", name2, nbins, xlow, xhigh), "Residual_old_pt", "scale").GetValue())
        histograms.append((name1, h1))
        histograms.append((name2, h2))
        savePlot(histograms, fileName, options=options)

    print("Done!")