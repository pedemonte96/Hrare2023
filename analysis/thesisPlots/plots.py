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
    modelNameD0Star3 = "BDTG_df15_dl3684_v0_v1_opt18920"

    date = "OCT27"

    # READ FILES --------------------------------------------------------------------------------------------------------------------------
    #ggH ----------------------------------------------------------------------------------------------------------------------------------
    chainSGN_Phi3 = ROOT.TChain("events")
    chainSGN_Omega = ROOT.TChain("events")
    chainSGN_D0Star2 = ROOT.TChain("events")
    chainSGN_D0Star3 = ROOT.TChain("events")
    chainSGN_Phi3.Add("/data/submit/pdmonte/outputs/{0}/2018/outname_mc{1}_GFcat_{2}_2018.root".format(date, 1039, "Phi3Cat"))
    chainSGN_Omega.Add("/data/submit/pdmonte/outputs/{0}/2018/outname_mc{1}_GFcat_{2}_2018.root".format(date, 1038, "OmegaCat"))
    chainSGN_D0Star2.Add("/data/submit/pdmonte/outputs/{0}/2018/outname_mc{1}_GFcat_{2}_2018.root".format(date, 1041, "D0StarCat"))
    chainSGN_D0Star3.Add("/data/submit/pdmonte/outputs/{0}/2018/outname_mc{1}_GFcat_{2}_2018.root".format(date, 1040, "D0StarRhoCat"))
    dfSGN_Phi3 = ROOT.RDataFrame(chainSGN_Phi3)
    dfSGN_Omega = ROOT.RDataFrame(chainSGN_Omega)
    dfSGN_D0Star2 = ROOT.RDataFrame(chainSGN_D0Star2)
    dfSGN_D0Star3 = ROOT.RDataFrame(chainSGN_D0Star3)

    #ggH REGRESSION -----------------------------------------------------------------------------------------------------------------------
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

    #VBF ----------------------------------------------------------------------------------------------------------------------------------
    chainSGN_Phi3_VBF = ROOT.TChain("events")
    chainSGN_Omega_VBF = ROOT.TChain("events")
    chainSGN_D0Star2_VBF = ROOT.TChain("events")
    chainSGN_D0Star3_VBF = ROOT.TChain("events")
    chainSGN_Phi3_VBF.Add("/data/submit/pdmonte/outputs/{0}/2018/outname_mc{1}_GFcat_{2}_2018.root".format(date, 1069, "Phi3Cat"))
    chainSGN_Omega_VBF.Add("/data/submit/pdmonte/outputs/{0}/2018/outname_mc{1}_GFcat_{2}_2018.root".format(date, 1068, "OmegaCat"))
    chainSGN_D0Star2_VBF.Add("/data/submit/pdmonte/outputs/{0}/2018/outname_mc{1}_GFcat_{2}_2018.root".format(date, 1071, "D0StarCat"))
    chainSGN_D0Star3_VBF.Add("/data/submit/pdmonte/outputs/{0}/2018/outname_mc{1}_GFcat_{2}_2018.root".format(date, 1070, "D0StarRhoCat"))
    dfSGN_Phi3_VBF = ROOT.RDataFrame(chainSGN_Phi3_VBF)
    dfSGN_Omega_VBF = ROOT.RDataFrame(chainSGN_Omega_VBF)
    dfSGN_D0Star2_VBF = ROOT.RDataFrame(chainSGN_D0Star2_VBF)
    dfSGN_D0Star3_VBF = ROOT.RDataFrame(chainSGN_D0Star3_VBF)

    #VBF REGRESSION (TODO) ----------------------------------------------------------------------------------------------------------------

    #BKG ----------------------------------------------------------------------------------------------------------------------------------
    chainBKG_Omega = ROOT.TChain("events")
    chainBKG_Omega.Add("/data/submit/pdmonte/outputs/{0}/2018/outname_mc10_GFcat_{1}_2018.root".format(date, "OmegaCat"))
    chainBKG_Omega.Add("/data/submit/pdmonte/outputs/{0}/2018/outname_mc11_GFcat_{1}_2018.root".format(date, "OmegaCat"))
    chainBKG_Omega.Add("/data/submit/pdmonte/outputs/{0}/2018/outname_mc12_GFcat_{1}_2018.root".format(date, "OmegaCat"))
    chainBKG_Omega.Add("/data/submit/pdmonte/outputs/{0}/2018/outname_mc13_GFcat_{1}_2018.root".format(date, "OmegaCat"))
    chainBKG_Omega.Add("/data/submit/pdmonte/outputs/{0}/2018/outname_mc14_GFcat_{1}_2018.root".format(date, "OmegaCat"))
    dfBKG_Omega = ROOT.RDataFrame(chainBKG_Omega)

    chainBKG_Phi3 = ROOT.TChain("events")
    chainBKG_Phi3.Add("/data/submit/pdmonte/outputs/{0}/2018/outname_mc10_GFcat_{1}_2018.root".format(date, "Phi3Cat"))
    chainBKG_Phi3.Add("/data/submit/pdmonte/outputs/{0}/2018/outname_mc11_GFcat_{1}_2018.root".format(date, "Phi3Cat"))
    chainBKG_Phi3.Add("/data/submit/pdmonte/outputs/{0}/2018/outname_mc12_GFcat_{1}_2018.root".format(date, "Phi3Cat"))
    chainBKG_Phi3.Add("/data/submit/pdmonte/outputs/{0}/2018/outname_mc13_GFcat_{1}_2018.root".format(date, "Phi3Cat"))
    chainBKG_Phi3.Add("/data/submit/pdmonte/outputs/{0}/2018/outname_mc14_GFcat_{1}_2018.root".format(date, "Phi3Cat"))
    dfBKG_Phi3 = ROOT.RDataFrame(chainBKG_Phi3)

    chainBKG_D0Star2 = ROOT.TChain("events")
    chainBKG_D0Star2.Add("/data/submit/pdmonte/outputs/{0}/2018/outname_mc10_GFcat_{1}_2018.root".format(date, "D0StarCat"))
    chainBKG_D0Star2.Add("/data/submit/pdmonte/outputs/{0}/2018/outname_mc11_GFcat_{1}_2018.root".format(date, "D0StarCat"))
    chainBKG_D0Star2.Add("/data/submit/pdmonte/outputs/{0}/2018/outname_mc12_GFcat_{1}_2018.root".format(date, "D0StarCat"))
    chainBKG_D0Star2.Add("/data/submit/pdmonte/outputs/{0}/2018/outname_mc13_GFcat_{1}_2018.root".format(date, "D0StarCat"))
    chainBKG_D0Star2.Add("/data/submit/pdmonte/outputs/{0}/2018/outname_mc14_GFcat_{1}_2018.root".format(date, "D0StarCat"))
    dfBKG_D0Star2 = ROOT.RDataFrame(chainBKG_D0Star2)

    chainBKG_D0Star3 = ROOT.TChain("events")
    chainBKG_D0Star3.Add("/data/submit/pdmonte/outputs/{0}/2018/outname_mc10_GFcat_{1}_2018.root".format(date, "D0StarRhoCat"))
    chainBKG_D0Star3.Add("/data/submit/pdmonte/outputs/{0}/2018/outname_mc11_GFcat_{1}_2018.root".format(date, "D0StarRhoCat"))
    chainBKG_D0Star3.Add("/data/submit/pdmonte/outputs/{0}/2018/outname_mc12_GFcat_{1}_2018.root".format(date, "D0StarRhoCat"))
    chainBKG_D0Star3.Add("/data/submit/pdmonte/outputs/{0}/2018/outname_mc13_GFcat_{1}_2018.root".format(date, "D0StarRhoCat"))
    chainBKG_D0Star3.Add("/data/submit/pdmonte/outputs/{0}/2018/outname_mc14_GFcat_{1}_2018.root".format(date, "D0StarRhoCat"))
    dfBKG_D0Star3 = ROOT.RDataFrame(chainBKG_D0Star3)

    #DATA ---------------------------------------------------------------------------------------------------------------------------------
    chainDATA_Omega = ROOT.TChain("events")
    chainDATA_Omega.Add("/data/submit/pdmonte/outputs/{0}/2018/outname_mc-62_GFcat_{1}_2018.root".format(date, "OmegaCat"))
    chainDATA_Omega.Add("/data/submit/pdmonte/outputs/{0}/2018/outname_mc-63_GFcat_{1}_2018.root".format(date, "OmegaCat"))
    chainDATA_Omega.Add("/data/submit/pdmonte/outputs/{0}/2018/outname_mc-64_GFcat_{1}_2018.root".format(date, "OmegaCat"))
    dfDATA_Omega = ROOT.RDataFrame(chainDATA_Omega)

    chainDATA_Phi3 = ROOT.TChain("events")
    chainDATA_Phi3.Add("/data/submit/pdmonte/outputs/{0}/2018/outname_mc-62_GFcat_{1}_2018.root".format(date, "Phi3Cat"))
    chainDATA_Phi3.Add("/data/submit/pdmonte/outputs/{0}/2018/outname_mc-63_GFcat_{1}_2018.root".format(date, "Phi3Cat"))
    chainDATA_Phi3.Add("/data/submit/pdmonte/outputs/{0}/2018/outname_mc-64_GFcat_{1}_2018.root".format(date, "Phi3Cat"))
    dfDATA_Phi3 = ROOT.RDataFrame(chainDATA_Phi3)

    chainDATA_D0Star2 = ROOT.TChain("events")
    chainDATA_D0Star2.Add("/data/submit/pdmonte/outputs/{0}/2018/outname_mc-62_GFcat_{1}_2018.root".format(date, "D0StarCat"))
    chainDATA_D0Star2.Add("/data/submit/pdmonte/outputs/{0}/2018/outname_mc-63_GFcat_{1}_2018.root".format(date, "D0StarCat"))
    chainDATA_D0Star2.Add("/data/submit/pdmonte/outputs/{0}/2018/outname_mc-64_GFcat_{1}_2018.root".format(date, "D0StarCat"))
    dfDATA_D0Star2 = ROOT.RDataFrame(chainDATA_D0Star2)

    chainDATA_D0Star3 = ROOT.TChain("events")
    chainDATA_D0Star3.Add("/data/submit/pdmonte/outputs/{0}/2018/outname_mc-62_GFcat_{1}_2018.root".format(date, "D0StarRhoCat"))
    chainDATA_D0Star3.Add("/data/submit/pdmonte/outputs/{0}/2018/outname_mc-63_GFcat_{1}_2018.root".format(date, "D0StarRhoCat"))
    chainDATA_D0Star3.Add("/data/submit/pdmonte/outputs/{0}/2018/outname_mc-64_GFcat_{1}_2018.root".format(date, "D0StarRhoCat"))
    dfDATA_D0Star3 = ROOT.RDataFrame(chainDATA_D0Star3)

    # DEFINE NEW COLUMNS ------------------------------------------------------------------------------------------------------------------
    #ggH ----------------------------------------------------------------------------------------------------------------------------------
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
    
    #ggH REGRESSION -----------------------------------------------------------------------------------------------------------------------
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
    s += '''
    TMVA::Experimental::RReader modelScaleD0StarRho0("/data/submit/pdmonte/TMVA_models/weightsOpts/TMVARegression_{modelName}_{channel}_0.weights.xml");
    computeModelScaleD0StarRho0 = TMVA::Experimental::Compute<{numVarsTotal}, float>(modelScaleD0StarRho0);
    TMVA::Experimental::RReader modelScaleD0StarRho1("/data/submit/pdmonte/TMVA_models/weightsOpts/TMVARegression_{modelName}_{channel}_1.weights.xml");
    computeModelScaleD0StarRho1 = TMVA::Experimental::Compute<{numVarsTotal}, float>(modelScaleD0StarRho1);
    TMVA::Experimental::RReader modelScaleD0StarRho2("/data/submit/pdmonte/TMVA_models/weightsOpts/TMVARegression_{modelName}_{channel}_2.weights.xml");
    computeModelScaleD0StarRho2 = TMVA::Experimental::Compute<{numVarsTotal}, float>(modelScaleD0StarRho2);
    '''.format(modelName=modelNameD0Star3, channel="d0starrho", numVarsTotal=getTotalNumVars(modelNameD0Star3))
    ROOT.gInterpreter.ProcessLine(s)
    variablesOmega = list(ROOT.modelScaleOmega0.GetVariableNames())
    variablesPhi = list(ROOT.modelScalePhi0.GetVariableNames())
    variablesD0Star = list(ROOT.modelScaleD0Star0.GetVariableNames())
    variablesD0StarRho = list(ROOT.modelScaleD0StarRho0.GetVariableNames())

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
        .Define("scaleFactor", ROOT.computeModelScaleD0StarRho0, variablesD0StarRho)
        .Define("goodMeson_pt_PRED", "scaleFactor[0]*goodMeson_pt[0]")
        .Define("Residual_old_pt", "goodMeson_pt - goodMeson_pt_GEN")
        .Define("Residual_new_pt", "goodMeson_pt_PRED - goodMeson_pt_GEN")
        .Define("HCandMass_varPRED", "compute_HiggsVars_var(goodMeson_pt_PRED, goodMeson_eta[0], goodMeson_phi[0], goodMeson_mass[0], goodPhotons_pt[0], goodPhotons_eta[0], goodPhotons_phi[0], 0)"))
    dfSGN_D0Star3_1 = (dfSGN_D0Star3_1.Define("scale", "w*lumiIntegrated/3.")
        .Define("scaleFactor", ROOT.computeModelScaleD0StarRho1, variablesD0StarRho)
        .Define("goodMeson_pt_PRED", "scaleFactor[0]*goodMeson_pt[0]")
        .Define("Residual_old_pt", "goodMeson_pt - goodMeson_pt_GEN")
        .Define("Residual_new_pt", "goodMeson_pt_PRED - goodMeson_pt_GEN")
        .Define("HCandMass_varPRED", "compute_HiggsVars_var(goodMeson_pt_PRED, goodMeson_eta[0], goodMeson_phi[0], goodMeson_mass[0], goodPhotons_pt[0], goodPhotons_eta[0], goodPhotons_phi[0], 0)"))
    dfSGN_D0Star3_2 = (dfSGN_D0Star3_2.Define("scale", "w*lumiIntegrated/3.")
        .Define("scaleFactor", ROOT.computeModelScaleD0StarRho2, variablesD0StarRho)
        .Define("goodMeson_pt_PRED", "scaleFactor[0]*goodMeson_pt[0]")
        .Define("Residual_old_pt", "goodMeson_pt - goodMeson_pt_GEN")
        .Define("Residual_new_pt", "goodMeson_pt_PRED - goodMeson_pt_GEN")
        .Define("HCandMass_varPRED", "compute_HiggsVars_var(goodMeson_pt_PRED, goodMeson_eta[0], goodMeson_phi[0], goodMeson_mass[0], goodPhotons_pt[0], goodPhotons_eta[0], goodPhotons_phi[0], 0)"))
    
    #VBF (TODO) ---------------------------------------------------------------------------------------------------------------------------
    dfSGN_Phi3_VBF = (dfSGN_Phi3_VBF.Define("scale", "w*lumiIntegrated"))
    dfSGN_Omega_VBF = (dfSGN_Omega_VBF.Define("scale", "w*lumiIntegrated"))
    dfSGN_D0Star2_VBF = (dfSGN_D0Star2_VBF.Define("scale", "w*lumiIntegrated"))
    dfSGN_D0Star3_VBF = (dfSGN_D0Star3_VBF.Define("scale", "w*lumiIntegrated"))
                  
    #VBF REGRESSION (TODO) ----------------------------------------------------------------------------------------------------------------
    
    #BKG ----------------------------------------------------------------------------------------------------------------------------------
    dfBKG_Omega = (dfBKG_Omega.Define("scale", "w*lumiIntegrated")
                    .Define("scaleFactor0", ROOT.computeModelScaleOmega0, variablesOmega)
                    .Define("scaleFactor1", ROOT.computeModelScaleOmega1, variablesOmega)
                    .Define("scaleFactor2", ROOT.computeModelScaleOmega2, variablesOmega)
                    .Define("goodMeson_pt_PRED", "(scaleFactor0[0]*goodMeson_pt[0] + scaleFactor1[0]*goodMeson_pt[0] + scaleFactor2[0]*goodMeson_pt[0])/3")
                    .Define("HCandMass_varPRED", "compute_HiggsVars_var(goodMeson_pt_PRED, goodMeson_eta[0], goodMeson_phi[0], goodMeson_mass[0], goodPhotons_pt[0], goodPhotons_eta[0], goodPhotons_phi[0], 0)"))
    dfBKG_Phi3 = (dfBKG_Phi3.Define("scale", "w*lumiIntegrated")
                    .Define("scaleFactor0", ROOT.computeModelScalePhi0, variablesPhi)
                    .Define("scaleFactor1", ROOT.computeModelScalePhi1, variablesPhi)
                    .Define("scaleFactor2", ROOT.computeModelScalePhi2, variablesPhi)
                    .Define("goodMeson_pt_PRED", "(scaleFactor0[0]*goodMeson_pt[0] + scaleFactor1[0]*goodMeson_pt[0] + scaleFactor2[0]*goodMeson_pt[0])/3")
                    .Define("HCandMass_varPRED", "compute_HiggsVars_var(goodMeson_pt_PRED, goodMeson_eta[0], goodMeson_phi[0], goodMeson_mass[0], goodPhotons_pt[0], goodPhotons_eta[0], goodPhotons_phi[0], 0)"))
    dfBKG_D0Star2 = (dfBKG_D0Star2.Define("scale", "w*lumiIntegrated")
                    .Define("scaleFactor0", ROOT.computeModelScaleD0Star0, variablesD0Star)
                    .Define("scaleFactor1", ROOT.computeModelScaleD0Star1, variablesD0Star)
                    .Define("scaleFactor2", ROOT.computeModelScaleD0Star2, variablesD0Star)
                    .Define("goodMeson_pt_PRED", "(scaleFactor0[0]*goodMeson_pt[0] + scaleFactor1[0]*goodMeson_pt[0] + scaleFactor2[0]*goodMeson_pt[0])/3")
                    .Define("HCandMass_varPRED", "compute_HiggsVars_var(goodMeson_pt_PRED, goodMeson_eta[0], goodMeson_phi[0], goodMeson_mass[0], goodPhotons_pt[0], goodPhotons_eta[0], goodPhotons_phi[0], 0)"))
    dfBKG_D0Star3 = (dfBKG_D0Star3.Define("scale", "w*lumiIntegrated")
                    .Define("scaleFactor0", ROOT.computeModelScaleD0StarRho0, variablesD0StarRho)
                    .Define("scaleFactor1", ROOT.computeModelScaleD0StarRho1, variablesD0StarRho)
                    .Define("scaleFactor2", ROOT.computeModelScaleD0StarRho2, variablesD0StarRho)
                    .Define("goodMeson_pt_PRED", "(scaleFactor0[0]*goodMeson_pt[0] + scaleFactor1[0]*goodMeson_pt[0] + scaleFactor2[0]*goodMeson_pt[0])/3")
                    .Define("HCandMass_varPRED", "compute_HiggsVars_var(goodMeson_pt_PRED, goodMeson_eta[0], goodMeson_phi[0], goodMeson_mass[0], goodPhotons_pt[0], goodPhotons_eta[0], goodPhotons_phi[0], 0)"))
   
    #DATA ---------------------------------------------------------------------------------------------------------------------------------
    dfDATA_Omega = (dfDATA_Omega.Define("scale", "w*lumiIntegrated")
                    .Define("scaleFactor0", ROOT.computeModelScaleOmega0, variablesOmega)
                    .Define("scaleFactor1", ROOT.computeModelScaleOmega1, variablesOmega)
                    .Define("scaleFactor2", ROOT.computeModelScaleOmega2, variablesOmega)
                    .Define("goodMeson_pt_PRED", "(scaleFactor0[0]*goodMeson_pt[0] + scaleFactor1[0]*goodMeson_pt[0] + scaleFactor2[0]*goodMeson_pt[0])/3")
                    .Define("HCandMass_varPRED", "compute_HiggsVars_var(goodMeson_pt_PRED, goodMeson_eta[0], goodMeson_phi[0], goodMeson_mass[0], goodPhotons_pt[0], goodPhotons_eta[0], goodPhotons_phi[0], 0)"))
    dfDATA_Phi3 = (dfDATA_Phi3.Define("scale", "w*lumiIntegrated")
                    .Define("scaleFactor0", ROOT.computeModelScalePhi0, variablesPhi)
                    .Define("scaleFactor1", ROOT.computeModelScalePhi1, variablesPhi)
                    .Define("scaleFactor2", ROOT.computeModelScalePhi2, variablesPhi)
                    .Define("goodMeson_pt_PRED", "(scaleFactor0[0]*goodMeson_pt[0] + scaleFactor1[0]*goodMeson_pt[0] + scaleFactor2[0]*goodMeson_pt[0])/3")
                    .Define("HCandMass_varPRED", "compute_HiggsVars_var(goodMeson_pt_PRED, goodMeson_eta[0], goodMeson_phi[0], goodMeson_mass[0], goodPhotons_pt[0], goodPhotons_eta[0], goodPhotons_phi[0], 0)"))
    dfDATA_D0Star2 = (dfDATA_D0Star2.Define("scale", "w*lumiIntegrated")
                    .Define("scaleFactor0", ROOT.computeModelScaleD0Star0, variablesD0Star)
                    .Define("scaleFactor1", ROOT.computeModelScaleD0Star1, variablesD0Star)
                    .Define("scaleFactor2", ROOT.computeModelScaleD0Star2, variablesD0Star)
                    .Define("goodMeson_pt_PRED", "(scaleFactor0[0]*goodMeson_pt[0] + scaleFactor1[0]*goodMeson_pt[0] + scaleFactor2[0]*goodMeson_pt[0])/3")
                    .Define("HCandMass_varPRED", "compute_HiggsVars_var(goodMeson_pt_PRED, goodMeson_eta[0], goodMeson_phi[0], goodMeson_mass[0], goodPhotons_pt[0], goodPhotons_eta[0], goodPhotons_phi[0], 0)"))
    dfDATA_D0Star3 = (dfDATA_D0Star3.Define("scale", "w*lumiIntegrated")
                    .Define("scaleFactor0", ROOT.computeModelScaleD0StarRho0, variablesD0StarRho)
                    .Define("scaleFactor1", ROOT.computeModelScaleD0StarRho1, variablesD0StarRho)
                    .Define("scaleFactor2", ROOT.computeModelScaleD0StarRho2, variablesD0StarRho)
                    .Define("goodMeson_pt_PRED", "(scaleFactor0[0]*goodMeson_pt[0] + scaleFactor1[0]*goodMeson_pt[0] + scaleFactor2[0]*goodMeson_pt[0])/3")
                    .Define("HCandMass_varPRED", "compute_HiggsVars_var(goodMeson_pt_PRED, goodMeson_eta[0], goodMeson_phi[0], goodMeson_mass[0], goodPhotons_pt[0], goodPhotons_eta[0], goodPhotons_phi[0], 0)"))
    
    #Define useful lists ------------------------------------------------------------------------------------------------------------------
    channels = ["Phi3", "Omega", "D0Star_2body", "D0Star_3body"]
    channels_latex = ["#phi", "#omega", "D^{*0}", "D^{*0}"]
    channels_latex_titles = ["#phi", "#omega", "D^{*0} 2-body", "D^{*0} 3-body"]
    dfsSGN = [dfSGN_Phi3, dfSGN_Omega, dfSGN_D0Star2, dfSGN_D0Star3]
    dfsSGN_VBF = [dfSGN_Phi3_VBF, dfSGN_Omega_VBF, dfSGN_D0Star2_VBF, dfSGN_D0Star3_VBF]
    dfsBKG = [dfBKG_Phi3, dfBKG_Omega, dfBKG_D0Star2, dfBKG_D0Star3]
    dfsDATA = [dfDATA_Phi3, dfDATA_Omega, dfDATA_D0Star2, dfDATA_D0Star3]
    dfsSGN_0 = [dfSGN_Phi3_0, dfSGN_Omega_0, dfSGN_D0Star2_0, dfSGN_D0Star3_0]
    dfsSGN_1 = [dfSGN_Phi3_1, dfSGN_Omega_1, dfSGN_D0Star2_1, dfSGN_D0Star3_1]
    dfsSGN_2 = [dfSGN_Phi3_2, dfSGN_Omega_2, dfSGN_D0Star2_2, dfSGN_D0Star3_2]

    massRanges = {"Phi3": (0.80, 1.20), "Omega": (0.60, 0.96), "D0Star_2body": (1.80, 1.93), "D0Star_3body": (1.40, 2.20)}
    slicingVals = {}
    for k in massRanges:
        width = massRanges[k][1] - massRanges[k][0]
        slicingVals[k] = [massRanges[k][0] + width/4., massRanges[k][0] + width/2., massRanges[k][0] + width*3/4.,]
    print(slicingVals)
    slicingVals = {"Phi3": [0.9174, 0.9875, 1.032], "Omega": [0.725, 0.77, 0.81], "D0Star_2body": [1.854, 1.865, 1.876], "D0Star_3body": [1.780, 1.850, 1.920]}
    cutVariables = {"Phi3": "goodMeson_mass", "Omega": "goodMeson_mass", "D0Star_2body": "goodMeson_ditrk_mass", "D0Star_3body": "goodMeson_mass"}

    plotKinematicFitResidual = False
    plotFullMesonMassResidual = False
    plotDitrackResiduals = False
    plotFullMesonPtResiduals = False
    plotModelsPt = False
    plotModelsPtResiduals = False
    plotGeneralData = False
    plotFullMesonPtData = False
    plotHCandMass = True
    plotSlicesSignal = False
    plotSlicesBackground = False
    plotFits = False

    # -------------------------------------------------------------------------------------------------------------------------------------
    # START PLOTTING ----------------------------------------------------------------------------------------------------------------------
    # -------------------------------------------------------------------------------------------------------------------------------------

    if plotKinematicFitResidual:
        # Kinematic fit comparison --------------------------------------------------------------------------------------------
        xLabels = ["m_{#phi}^{diTrk, RECO} - m_{#phi}^{diTrk, GEN} [GeV]", "m_{#omega}^{diTrk, RECO} - m_{#omega}^{diTrk, GEN} [GeV]", "m_{D^{*0}}^{diTrk, RECO} - m_{D^{*0}}^{diTrk, GEN} [GeV]", "m_{D^{*0}}^{diTrk, RECO} - m_{D^{*0}}^{diTrk, GEN} [GeV]"]
        for i, c in enumerate(channels):
            fileName = "{}_kinematic_fit_residual.png".format(c)
            df = dfsSGN[i]
            options = {"labelXAxis": xLabels[i], "labelYAxis": "Events", "xRange": (-0.1, 0.1), "data": False}
            nbins, xlow, xhigh = 500, -0.5, 0.5
            histograms = []
            name1 = "w/ kin. fit"
            h1 = df.Histo1D(("hist", name1, nbins, xlow, xhigh), "DiffFittedMass", "scale").GetValue()
            name2 = "w/o kin. fit"
            h2 = df.Histo1D(("hist", name2, nbins, xlow, xhigh), "DiffSumMass", "scale").GetValue()
            histograms.append((name1, h1))
            histograms.append((name2, h2))
            print("{} MASS STD SUM:\t".format(c), h2.GetStdDev()*1000)
            print("{} MASS STD FIT:\t".format(c), h1.GetStdDev()*1000, h1.GetStdDev()/h2.GetStdDev()-1)
            savePlot(histograms, fileName, options=options)

    if plotFullMesonMassResidual:
        # New full meson mass comparison --------------------------------------------------------------------------------------------
        xLabels = ["m_{#phi}^{RECO} - m_{#phi}^{GEN} [GeV]", "m_{#omega}^{RECO} - m_{#omega}^{GEN} [GeV]", "m_{D^{*0}}^{RECO} - m_{D^{*0}}^{GEN} [GeV]"]
        channels_latex_bis = ["#phi", "#omega", "D^{*0} 3-body"]
        dfsSGN_bis = [dfSGN_Phi3, dfSGN_Omega, dfSGN_D0Star3]
        for i, c, in enumerate(["Phi3", "Omega", "D0Star_3body"]):
            fileName = "{}_fullmeson_mass_residual.png".format(c)
            df = dfsSGN_bis[i]
            options = {"labelXAxis": xLabels[i], "labelYAxis": "Events", "xRange": (-0.5, 0.5), "data": False}
            nbins, xlow, xhigh = 120, -0.6, 0.6
            histograms = []
            name1 = "w/ #pi^{0} mass"
            h1 = df.Histo1D(("hist", name1, nbins, xlow, xhigh), "DiffModifiedMass", "scale").GetValue()
            name2 = "w/o #pi^{0} mass"
            h2 = df.Histo1D(("hist", name2, nbins, xlow, xhigh), "DiffRawMass", "scale").GetValue()
            histograms.append((name1, h1))
            histograms.append((name2, h2))
            print("{} MASS STD RAW:\t".format(c), h2.GetStdDev()*1000)
            print("{} MASS STD PI0:\t".format(c), h1.GetStdDev()*1000, h1.GetStdDev()/h2.GetStdDev()-1)
            savePlot(histograms, fileName, options=options)

    if plotDitrackResiduals:
        # Ditrack PT residuals --------------------------------------------------------------------------------------------
        fileName = "ditrack_residuals_pt.png"
        nbins, xlow, xhigh = 100, -3., 3.
        options = {"labelXAxis": "p_{T}^{diTrk, RECO} - p_{T}^{diTrk, GEN} [GeV]", "labelYAxis": "Frequency", "data": False}
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
        options = {"labelXAxis": "m^{diTrk, RECO} - m^{diTrk, GEN} [GeV]", "labelYAxis": "Frequency", "data": False}
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
        options = {"labelXAxis": "#eta^{diTrk, RECO} - #eta^{diTrk, GEN}", "labelYAxis": "Frequency", "data": False}
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
        options = {"labelXAxis": "#phi^{diTrk, RECO} - #phi^{diTrk, GEN}", "labelYAxis": "Frequency", "data": False}
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

    if plotFullMesonPtResiduals:
        # Full meson PT residuals --------------------------------------------------------------------------------------------
        fileName = "fullmeson_residuals_pt.png"
        nbins, xlow, xhigh = 100, -30., 30.
        options = {"labelXAxis": "p_{T}^{RECO} - p_{T}^{GEN} [GeV]", "labelYAxis": "Frequency", "data": False}
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

    if plotModelsPt:
        # Good Meson PT Phi --------------------------------------------------------------------------------------------
        for i, c in enumerate(channels):
            fileName = "{}_model_pt.png".format(c)
            df_0, df_1, df_2 = dfsSGN_0[i], dfsSGN_1[i], dfsSGN_2[i]
            nbins, xlow, xhigh = 100, 0., 150.
            options = {"labelXAxis": "p_{T} [GeV]", "labelYAxis": "Events", "style": ["f", "l", "l"], "colors": [ROOT.kSpring + 1, ROOT.kRed + 1, ROOT.kBlue], "data": False}
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

    if plotModelsPtResiduals:
        # Good Meson PT Residuals --------------------------------------------------------------------------------------------
        for i, c in enumerate(channels):
            fileName = "{}_model_pt_residuals.png".format(c)
            df_0, df_1, df_2 = dfsSGN_0[i], dfsSGN_1[i], dfsSGN_2[i]
            nbins, xlow, xhigh = 100, -20., 20.
            options = {"labelXAxis": "p_{T} - p_{T}^{GEN} [GeV]", "labelYAxis": "Events", "data": False}
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

    if plotGeneralData:
        # Good Meson General plots (wihtout PT) --------------------------------------------------------------------------------------------
        variables = ["goodMeson_ditrk_mass", "goodMeson_mass", "goodPhotons_pt", "goodMeson_leadtrk_pt", "goodMeson_subleadtrk_pt"]
        variablesTitle = ["Ditrack mass", "Mass", "Photon from PV", "Leading track p_{T}", "Subleading track p_{T}"]
        variablesFileName = ["ditrk_mass", "mass", "photon_pt", "lead_pt", "sublead_pt"]
        variablesXRange = {"Phi3": [(0.2, 1.0), (0.6, 1.4), (0, 160), (0, 80), (0, 50)],
                            "Omega": [(0.2, 1.0), (0.4, 1.2), (0, 160), (0, 80), (0, 50)],
                            "D0Star_2body": [(1.70, 2.10), (1.30, 2.50), (0, 160), (0, 80), (0, 50)],
                            "D0Star_3body": [(0.40, 2.00), (1.30, 2.50), (0, 160), (0, 80), (0, 50)]}
        
        for j, c in enumerate(channels):
            dfSGN = dfsSGN[j]
            dfSGN_VBF = dfsSGN_VBF[j]
            dfBKG = dfsBKG[j]
            dfDATA = dfsDATA[j]
            variablesXLabel = ["m^{{diTrk}}_{{{meson}}} [GeV]".format(meson=channels_latex[j]), "m_{{{meson}}} [GeV]".format(meson=channels_latex[j]), "p_{T}^{#gamma} [GeV]", "p_{{T, {meson}}}^{{lead}} [GeV]".format(meson=channels_latex[j]), "p_{{T, {meson}}}^{{subLead}} [GeV]".format(meson=channels_latex[j])]
            print(variablesXLabel)
            for i, var in enumerate(variables):
                fileName = "{}_{}.png".format(c, variablesFileName[i])
                options = {"labelXAxis": variablesXLabel[i], "labelYAxis": "Events", "style": ["f", "l", "p"], "colors": [ROOT.kOrange - 9, ROOT.kRed + 1, ROOT.kBlack], "data": True}
                nbins, xlow, xhigh = 100, variablesXRange[c][i][0], variablesXRange[c][i][1]
                histograms = []
                name1 = "#gamma + jets"
                h1 = dfBKG.Histo1D(("hist", name1, nbins, xlow, xhigh), var, "scale").GetValue()
                name2 = "ggH MC ({})".format(channels_latex_titles[j])
                h2 = dfSGN.Histo1D(("hist", name2, nbins, xlow, xhigh), var, "scale").GetValue()
                h2.Add(dfSGN_VBF.Histo1D(("hist", name2, nbins, xlow, xhigh), var, "scale").GetValue())

                name3 = "Data"
                h3 = dfDATA.Histo1D(("hist", name3, nbins, xlow, xhigh), var, "scale").GetValue()

                integralBKG = h1.Integral(h1.FindBin(xlow), h1.FindBin(xhigh))
                integralSGN = h2.Integral(h2.FindBin(xlow), h2.FindBin(xhigh))
                integralDAT = h3.Integral(h3.FindBin(xlow), h3.FindBin(xhigh))
                h2.Scale(integralDAT/integralSGN)
                #add data
                histograms.append((name1, h1))
                histograms.append((name2, h2))
                histograms.append((name3, h3))
                savePlot(histograms, fileName, options=options)

    if plotFullMesonPtData:
        # Good Meson PT with regression --------------------------------------------------------------------------------------------
        for i, c in enumerate(channels):
            fileName = "{}_pt.png".format(c)
            df_0, df_1, df_2 = dfsSGN_0[i], dfsSGN_1[i], dfsSGN_2[i]
            dfBKG = dfsBKG[i]
            dfDATA = dfsDATA[i]
            nbins, xlow, xhigh = 100, 0., 160.
            options = {"labelXAxis": "p_{T} [GeV]", "labelYAxis": "Events", "style": ["f", "l", "p"], "colors": [ROOT.kOrange - 9, ROOT.kRed + 1, ROOT.kBlack], "data": True}
            histograms = []
            name1 = "#gamma + jets"
            h1 = dfBKG.Histo1D(("hist", name1, nbins, xlow, xhigh), "goodMeson_pt_PRED", "scale").GetValue()
            name2 = "ggH MC ({})".format(channels_latex_titles[i])
            h2 = df_0.Histo1D(("hist", name2, nbins, xlow, xhigh), "goodMeson_pt_PRED", "scale").GetValue()
            h2.Add(df_1.Histo1D(("hist", name2, nbins, xlow, xhigh), "goodMeson_pt_PRED", "scale").GetValue())
            h2.Add(df_2.Histo1D(("hist", name2, nbins, xlow, xhigh), "goodMeson_pt_PRED", "scale").GetValue())
            # todo change with real VBF
            h2_vbf = df_0.Histo1D(("hist", name2, nbins, xlow, xhigh), "goodMeson_pt_PRED", "scale").GetValue()
            h2_vbf.Add(df_1.Histo1D(("hist", name2, nbins, xlow, xhigh), "goodMeson_pt_PRED", "scale").GetValue())
            h2_vbf.Add(df_2.Histo1D(("hist", name2, nbins, xlow, xhigh), "goodMeson_pt_PRED", "scale").GetValue())
            h2_vbf.Scale(1/13.)
            h2.Add(h2_vbf)

            name3 = "Data"
            h3 = dfDATA.Histo1D(("hist", name3, nbins, xlow, xhigh), "goodMeson_pt_PRED", "scale").GetValue()

            integralBKG = h1.Integral(h1.FindBin(xlow), h1.FindBin(xhigh))
            integralSGN = h2.Integral(h2.FindBin(xlow), h2.FindBin(xhigh))
            h2.Scale(integralBKG/integralSGN)
            #add data
            histograms.append((name1, h1))
            histograms.append((name2, h2))
            histograms.append((name3, h3))
            savePlot(histograms, fileName, options=options)

    if plotHCandMass:
        # HCandVar with regression --------------------------------------------------------------------------------------------
        for i, c in enumerate(channels):
            fileName = "{}_HiggsMass.png".format(c)
            df_0, df_1, df_2 = dfsSGN_0[i], dfsSGN_1[i], dfsSGN_2[i]
            dfBKG = dfsBKG[i]
            dfDATA = dfsDATA[i]
            nbins, xlow, xhigh = 100, 0., 180.
            options = {"labelXAxis": "m^{{H}}_{{#gamma{}}} [GeV]".format(channels_latex[i]), "labelYAxis": "Events", "style": ["f", "f", "f", "p"], "colors": [ROOT.kOrange - 9, ROOT.kRed - 7, ROOT.kRed + 2, ROOT.kBlack], "logScale": True, "HCandMass": True, "data": True}
            histograms = []
            name1 = "#gamma + jets"
            h1 = dfBKG.Histo1D(("hist", name1, nbins, xlow, xhigh), "HCandMass_varPRED", "scale").GetValue()
            name2 = "qqH MC ({})".format(channels_latex_titles[i])#VBF
            h2 = df_0.Histo1D(("hist", name2, nbins, xlow, xhigh), "HCandMass_varPRED", "scale").GetValue()
            h2.Add(df_1.Histo1D(("hist", name2, nbins, xlow, xhigh), "HCandMass_varPRED", "scale").GetValue())
            h2.Add(df_2.Histo1D(("hist", name2, nbins, xlow, xhigh), "HCandMass_varPRED", "scale").GetValue())
            h2.Scale(1/13.)
            name3 = "ggH MC ({})".format(channels_latex_titles[i])
            h3 = df_0.Histo1D(("hist", name3, nbins, xlow, xhigh), "HCandMass_varPRED", "scale").GetValue()
            h3.Add(df_1.Histo1D(("hist", name3, nbins, xlow, xhigh), "HCandMass_varPRED", "scale").GetValue())
            h3.Add(df_2.Histo1D(("hist", name3, nbins, xlow, xhigh), "HCandMass_varPRED", "scale").GetValue())
            
            name4 = "Data"
            h4 = dfDATA.Filter("HCandMass_varPRED < 115 || HCandMass_varPRED > 135").Histo1D(("hist", name4, nbins, xlow, xhigh), "HCandMass_varPRED", "scale").GetValue()

            #integralBKG = h1.Integral(h1.FindBin(xlow), h1.FindBin(xhigh))
            #integralSGN = h2.Integral(h2.FindBin(xlow), h2.FindBin(xhigh))
            #h2.Scale(integralBKG/integralSGN)
            #add data
            histograms.append((name1, h1))
            histograms.append((name2, h2))
            histograms.append((name3, h3))
            histograms.append((name4, h4))
            savePlot(histograms, fileName, options=options)

    if plotSlicesSignal:
        # Slices of HCandVar Signal --------------------------------------------------------------------------------------------
        for i, c in enumerate(channels):
            fileName = "{}_fit_SGN_MH_sliced.png".format(c)
            df_0, df_1, df_2 = dfsSGN_0[i], dfsSGN_1[i], dfsSGN_2[i]
            nbins, xlow, xhigh = 60, 110., 140.
            options = {"labelXAxis": "m^{{H}}_{{#gamma{}}} [GeV]".format(channels_latex[i]), "labelYAxis": "Events", "style": ["f", "l", "l", "l", "l"], "colors": [ROOT.kRed - 10, ROOT.kRed + 2, ROOT.kBlue, ROOT.kGreen + 3, ROOT.kOrange + 9], "data": False}
            histograms = []
            name1 = "Total ggH MC ({})".format(channels_latex_titles[i])
            h1 = df_0.Histo1D(("hist", name1, nbins, xlow, xhigh), "HCandMass_varPRED", "scale").GetValue()
            h1.Add(df_1.Histo1D(("hist", name1, nbins, xlow, xhigh), "HCandMass_varPRED", "scale").GetValue())
            h1.Add(df_2.Histo1D(("hist", name1, nbins, xlow, xhigh), "HCandMass_varPRED", "scale").GetValue())
            name2 = "Slice 1"
            h2 = df_0.Filter("{var}[0] < {val1}".format(var=cutVariables[c], val1=slicingVals[c][0])).Histo1D(("hist", name2, nbins, xlow, xhigh), "HCandMass_varPRED", "scale").GetValue()
            h2.Add(df_1.Filter("{var}[0] < {val1}".format(var=cutVariables[c], val1=slicingVals[c][0])).Histo1D(("hist", name2, nbins, xlow, xhigh), "HCandMass_varPRED", "scale").GetValue())
            h2.Add(df_2.Filter("{var}[0] < {val1}".format(var=cutVariables[c], val1=slicingVals[c][0])).Histo1D(("hist", name2, nbins, xlow, xhigh), "HCandMass_varPRED", "scale").GetValue())
            name3 = "Slice 2"
            h3 = df_0.Filter("{var}[0] > {val1} && {var}[0] < {val2}".format(var=cutVariables[c], val1=slicingVals[c][0], val2=slicingVals[c][1])).Histo1D(("hist", name3, nbins, xlow, xhigh), "HCandMass_varPRED", "scale").GetValue()
            h3.Add(df_1.Filter("{var}[0] > {val1} && {var}[0] < {val2}".format(var=cutVariables[c], val1=slicingVals[c][0], val2=slicingVals[c][1])).Histo1D(("hist", name3, nbins, xlow, xhigh), "HCandMass_varPRED", "scale").GetValue())
            h3.Add(df_2.Filter("{var}[0] > {val1} && {var}[0] < {val2}".format(var=cutVariables[c], val1=slicingVals[c][0], val2=slicingVals[c][1])).Histo1D(("hist", name3, nbins, xlow, xhigh), "HCandMass_varPRED", "scale").GetValue())
            name4 = "Slice 3"
            h4 = df_0.Filter("{var}[0] > {val1} && {var}[0] < {val2}".format(var=cutVariables[c], val1=slicingVals[c][1], val2=slicingVals[c][2])).Histo1D(("hist", name4, nbins, xlow, xhigh), "HCandMass_varPRED", "scale").GetValue()
            h4.Add(df_1.Filter("{var}[0] > {val1} && {var}[0] < {val2}".format(var=cutVariables[c], val1=slicingVals[c][1], val2=slicingVals[c][2])).Histo1D(("hist", name4, nbins, xlow, xhigh), "HCandMass_varPRED", "scale").GetValue())
            h4.Add(df_2.Filter("{var}[0] > {val1} && {var}[0] < {val2}".format(var=cutVariables[c], val1=slicingVals[c][1], val2=slicingVals[c][2])).Histo1D(("hist", name4, nbins, xlow, xhigh), "HCandMass_varPRED", "scale").GetValue())
            name5 = "Slice 4"
            h5 = df_0.Filter("{var}[0] > {val1}".format(var=cutVariables[c], val1=slicingVals[c][2])).Histo1D(("hist", name5, nbins, xlow, xhigh), "HCandMass_varPRED", "scale").GetValue()
            h5.Add(df_1.Filter("{var}[0] > {val1}".format(var=cutVariables[c], val1=slicingVals[c][2])).Histo1D(("hist", name5, nbins, xlow, xhigh), "HCandMass_varPRED", "scale").GetValue())
            h5.Add(df_2.Filter("{var}[0] > {val1}".format(var=cutVariables[c], val1=slicingVals[c][2])).Histo1D(("hist", name5, nbins, xlow, xhigh), "HCandMass_varPRED", "scale").GetValue())
            
            h2.Scale(h1.Integral()/h2.Integral())
            h3.Scale(h1.Integral()/h3.Integral())
            h4.Scale(h1.Integral()/h4.Integral())
            h5.Scale(h1.Integral()/h5.Integral())
            print(c)
            print(h1.GetEntries(), h1.GetEntries()/4.)
            print(h2.GetEntries())
            print(h3.GetEntries())
            print(h4.GetEntries())
            print(h5.GetEntries())

            histograms.append((name1, h1))
            histograms.append((name2, h2))
            histograms.append((name3, h3))
            histograms.append((name4, h4))
            histograms.append((name5, h5))
            savePlot(histograms, fileName, options=options)

    if plotSlicesBackground:
        # Slices of HCandVar Background --------------------------------------------------------------------------------------------
        for i, c in enumerate(channels):
            fileName = "{}_fit_BKG_MH_sliced.png".format(c)
            dfBKG = dfsBKG[i]
            nbins, xlow, xhigh = 20, 100., 160.
            options = {"labelXAxis": "m^{{H}}_{{#gamma{}}} [GeV]".format(channels_latex[i]), "labelYAxis": "Events", "style": ["f", "l", "l", "l", "l"], "colors": [ROOT.kOrange - 9, ROOT.kRed + 2, ROOT.kBlue, ROOT.kGreen + 3, ROOT.kOrange + 9], "data": False}
            histograms = []
            name1 = "Total #gamma + jets"
            h1 = dfBKG.Histo1D(("hist", name1, nbins, xlow, xhigh), "HCandMass_varPRED", "scale").GetValue()
            name2 = "Slice 1"
            h2 = dfBKG.Filter("{var}[0] < {val1}".format(var=cutVariables[c], val1=slicingVals[c][0])).Histo1D(("hist", name2, nbins, xlow, xhigh), "HCandMass_varPRED", "scale").GetValue()
            name3 = "Slice 2"
            h3 = dfBKG.Filter("{var}[0] > {val1} && {var}[0] < {val2}".format(var=cutVariables[c], val1=slicingVals[c][0], val2=slicingVals[c][1])).Histo1D(("hist", name3, nbins, xlow, xhigh), "HCandMass_varPRED", "scale").GetValue()
            name4 = "Slice 3"
            h4 = dfBKG.Filter("{var}[0] > {val1} && {var}[0] < {val2}".format(var=cutVariables[c], val1=slicingVals[c][1], val2=slicingVals[c][2])).Histo1D(("hist", name4, nbins, xlow, xhigh), "HCandMass_varPRED", "scale").GetValue()
            name5 = "Slice 4"
            h5 = dfBKG.Filter("{var}[0] > {val1}".format(var=cutVariables[c], val1=slicingVals[c][2])).Histo1D(("hist", name5, nbins, xlow, xhigh), "HCandMass_varPRED", "scale").GetValue()
            
            h2.Scale(h1.Integral()/h2.Integral())
            h3.Scale(h1.Integral()/h3.Integral())
            h4.Scale(h1.Integral()/h4.Integral())
            h5.Scale(h1.Integral()/h5.Integral())
            print(c)
            print(h1.GetEntries(), h1.GetEntries()/4.)
            print(h2.GetEntries())
            print(h3.GetEntries())
            print(h4.GetEntries())
            print(h5.GetEntries())

            histograms.append((name1, h1))
            histograms.append((name2, h2))
            histograms.append((name3, h3))
            histograms.append((name4, h4))
            histograms.append((name5, h5))
            savePlot(histograms, fileName, options=options)

    print("Done!")