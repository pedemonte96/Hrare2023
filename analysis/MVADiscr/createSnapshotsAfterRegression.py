import ROOT

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


def getCatNumModel(channel):
    modelNamePhi3 =     "BDTG_df13_dl3620_v0_v1_opt70035"
    modelNameOmega =    "BDTG_df13_dl3620_v0_v1_opt72810"
    modelNameD0Star2 =  "BDTG_df7_dl3684_v0_v1_opt75239"
    modelNameD0Star3 =  "BDTG_df15_dl3684_v0_v1_opt76387"
    if (channel == "omega"):
        return "OmegaCat", 1038, modelNameOmega
    elif (channel == "phi"):
        return "Phi3Cat", 1039, modelNamePhi3
    elif (channel == "d0starrho"):
        return "D0StarRhoCat", 1040, modelNameD0Star3
    elif (channel == "d0star"):
        return "D0StarCat", 1041, modelNameD0Star2
    else:
        raise Exception("Wrong channel.")


def createSnapshotAfterRegression(channel, date):
    mesonCat, mesonNum, modelName = getCatNumModel(channel)
    print(channel, date, mesonCat, mesonNum, modelName)

    variableName = modelName + "_" + mesonCat

    s = '''
    TMVA::Experimental::RReader {variableName}Reader0("/data/submit/pdmonte/TMVA_models/weightsOptsFinal/TMVARegression_{modelName}_{channel}_ggh_0.weights.xml");
    {variableName}0 = TMVA::Experimental::Compute<{numVarsTotal}, float>({variableName}Reader0);
    TMVA::Experimental::RReader {variableName}Reader1("/data/submit/pdmonte/TMVA_models/weightsOptsFinal/TMVARegression_{modelName}_{channel}_ggh_1.weights.xml");
    {variableName}1 = TMVA::Experimental::Compute<{numVarsTotal}, float>({variableName}Reader1);
    TMVA::Experimental::RReader {variableName}Reader2("/data/submit/pdmonte/TMVA_models/weightsOptsFinal/TMVARegression_{modelName}_{channel}_ggh_2.weights.xml");
    {variableName}2 = TMVA::Experimental::Compute<{numVarsTotal}, float>({variableName}Reader2);
    '''.format(modelName=modelName, channel=channel, numVarsTotal=getTotalNumVars(modelName), variableName=variableName)

    ROOT.gInterpreter.ProcessLine(s)
    variables = list(getattr(ROOT, variableName + "Reader0").GetVariableNames())

    chainSGN0 = ROOT.TChain("events")
    chainSGN1 = ROOT.TChain("events")
    chainSGN2 = ROOT.TChain("events")
    chainSGN0.Add("/data/submit/pdmonte/outputs/{0}/2018/outname_mc{1}_GFcat_{2}_2018_sample0.root".format(date, mesonNum, mesonCat))
    chainSGN1.Add("/data/submit/pdmonte/outputs/{0}/2018/outname_mc{1}_GFcat_{2}_2018_sample1.root".format(date, mesonNum, mesonCat))
    chainSGN2.Add("/data/submit/pdmonte/outputs/{0}/2018/outname_mc{1}_GFcat_{2}_2018_sample2.root".format(date, mesonNum, mesonCat))

    dfSGN0 = ROOT.RDataFrame(chainSGN0)
    dfSGN1 = ROOT.RDataFrame(chainSGN1)
    dfSGN2 = ROOT.RDataFrame(chainSGN2)

    dfSGN0 = (dfSGN0.Define("scale", "w*lumiIntegrated/3.")
            .Define("HCandMass_GEN", "compute_HiggsVars_var(goodMeson_pt_GEN, goodMeson_eta_GEN, goodMeson_phi_GEN, goodMeson_mass_GEN, goodPhotons_pt_GEN, goodPhotons_eta_GEN, goodPhotons_phi_GEN, 0)")
            .Define("HCandMass_varGEN", "compute_HiggsVars_var(goodMeson_pt_GEN, goodMeson_eta[0], goodMeson_phi[0], goodMeson_mass[0], goodPhotons_pt[0], goodPhotons_eta[0], goodPhotons_phi[0], 0)")
            .Define("scaleFactor", getattr(ROOT, variableName + "0"), variables)
            .Define("goodMeson_pt_PRED", "scaleFactor[0]*goodMeson_pt[0]")
            .Define("HCandMass_varPRED", "compute_HiggsVars_var(goodMeson_pt_PRED, goodMeson_eta[0], goodMeson_phi[0], goodMeson_mass[0], goodPhotons_pt[0], goodPhotons_eta[0], goodPhotons_phi[0], 0)")
            .Define("HCandPt_varPRED", "compute_HiggsVars_var(goodMeson_pt_PRED, goodMeson_eta[0], goodMeson_phi[0], goodMeson_mass[0], goodPhotons_pt[0], goodPhotons_eta[0], goodPhotons_phi[0], 1)"))
    dfSGN1 = (dfSGN1.Define("scale", "w*lumiIntegrated/3.")
            .Define("HCandMass_GEN", "compute_HiggsVars_var(goodMeson_pt_GEN, goodMeson_eta_GEN, goodMeson_phi_GEN, goodMeson_mass_GEN, goodPhotons_pt_GEN, goodPhotons_eta_GEN, goodPhotons_phi_GEN, 0)")
            .Define("HCandMass_varGEN", "compute_HiggsVars_var(goodMeson_pt_GEN, goodMeson_eta[0], goodMeson_phi[0], goodMeson_mass[0], goodPhotons_pt[0], goodPhotons_eta[0], goodPhotons_phi[0], 0)")
            .Define("scaleFactor", getattr(ROOT, variableName + "1"), variables)
            .Define("goodMeson_pt_PRED", "scaleFactor[0]*goodMeson_pt[0]")
            .Define("HCandMass_varPRED", "compute_HiggsVars_var(goodMeson_pt_PRED, goodMeson_eta[0], goodMeson_phi[0], goodMeson_mass[0], goodPhotons_pt[0], goodPhotons_eta[0], goodPhotons_phi[0], 0)")
            .Define("HCandPt_varPRED", "compute_HiggsVars_var(goodMeson_pt_PRED, goodMeson_eta[0], goodMeson_phi[0], goodMeson_mass[0], goodPhotons_pt[0], goodPhotons_eta[0], goodPhotons_phi[0], 1)"))
    dfSGN2 = (dfSGN2.Define("scale", "w*lumiIntegrated/3.")
            .Define("HCandMass_GEN", "compute_HiggsVars_var(goodMeson_pt_GEN, goodMeson_eta_GEN, goodMeson_phi_GEN, goodMeson_mass_GEN, goodPhotons_pt_GEN, goodPhotons_eta_GEN, goodPhotons_phi_GEN, 0)")
            .Define("HCandMass_varGEN", "compute_HiggsVars_var(goodMeson_pt_GEN, goodMeson_eta[0], goodMeson_phi[0], goodMeson_mass[0], goodPhotons_pt[0], goodPhotons_eta[0], goodPhotons_phi[0], 0)")
            .Define("scaleFactor", getattr(ROOT, variableName + "2"), variables)
            .Define("goodMeson_pt_PRED", "scaleFactor[0]*goodMeson_pt[0]")
            .Define("HCandMass_varPRED", "compute_HiggsVars_var(goodMeson_pt_PRED, goodMeson_eta[0], goodMeson_phi[0], goodMeson_mass[0], goodPhotons_pt[0], goodPhotons_eta[0], goodPhotons_phi[0], 0)")
            .Define("HCandPt_varPRED", "compute_HiggsVars_var(goodMeson_pt_PRED, goodMeson_eta[0], goodMeson_phi[0], goodMeson_mass[0], goodPhotons_pt[0], goodPhotons_eta[0], goodPhotons_phi[0], 1)"))

    chainBKG = ROOT.TChain("events")
    chainBKG.Add("/data/submit/pdmonte/outputs/{0}/2018/outname_mc10_GFcat_{1}_2018.root".format(date, mesonCat))
    chainBKG.Add("/data/submit/pdmonte/outputs/{0}/2018/outname_mc11_GFcat_{1}_2018.root".format(date, mesonCat))
    chainBKG.Add("/data/submit/pdmonte/outputs/{0}/2018/outname_mc12_GFcat_{1}_2018.root".format(date, mesonCat))
    chainBKG.Add("/data/submit/pdmonte/outputs/{0}/2018/outname_mc13_GFcat_{1}_2018.root".format(date, mesonCat))
    chainBKG.Add("/data/submit/pdmonte/outputs/{0}/2018/outname_mc14_GFcat_{1}_2018.root".format(date, mesonCat))

    dfBKG = ROOT.RDataFrame(chainBKG)
    dfBKG = (dfBKG.Define("scale", "w*lumiIntegrated")
            .Define("scaleFactor0", getattr(ROOT, variableName + "0"), variables)
            .Define("scaleFactor1", getattr(ROOT, variableName + "1"), variables)
            .Define("scaleFactor2", getattr(ROOT, variableName + "2"), variables)
            .Define("goodMeson_pt_PRED", "(scaleFactor0[0]*goodMeson_pt[0] + scaleFactor1[0]*goodMeson_pt[0] + scaleFactor2[0]*goodMeson_pt[0])/3")
            .Define("HCandMass_varPRED", "compute_HiggsVars_var(goodMeson_pt_PRED, goodMeson_eta[0], goodMeson_phi[0], goodMeson_mass[0], goodPhotons_pt[0], goodPhotons_eta[0], goodPhotons_phi[0], 0)")
            .Define("HCandPt_varPRED", "compute_HiggsVars_var(goodMeson_pt_PRED, goodMeson_eta[0], goodMeson_phi[0], goodMeson_mass[0], goodPhotons_pt[0], goodPhotons_eta[0], goodPhotons_phi[0], 1)"))
    
    outputFile0 = "/data/submit/pdmonte/outputs/{0}/2018/outname_mc{1}_GFcat_{2}_2018_sample0_after.root".format(date, mesonNum, mesonCat)
    dfSGN0.Snapshot("events", outputFile0)
    print("Channel {}, SGN 1 snapshot done!".format(channel))
    outputFile1 = "/data/submit/pdmonte/outputs/{0}/2018/outname_mc{1}_GFcat_{2}_2018_sample1_after.root".format(date, mesonNum, mesonCat)
    dfSGN1.Snapshot("events", outputFile1)
    print("Channel {}, SGN 2 snapshot done!".format(channel))
    outputFile2 = "/data/submit/pdmonte/outputs/{0}/2018/outname_mc{1}_GFcat_{2}_2018_sample2_after.root".format(date, mesonNum, mesonCat)
    dfSGN2.Snapshot("events", outputFile2)
    print("Channel {}, SGN 3 snapshot done!".format(channel))
    outputFileBKG = "/data/submit/pdmonte/outputs/{0}/2018/outname_mc{1}_GFcat_{2}_2018_after.root".format(date, 0, mesonCat)
    dfBKG.Snapshot("events", outputFileBKG)
    print("Channel {}, BKG snapshot done!".format(channel))


if __name__ == "__main__":

    date = "NOV05"
    for channel in ["omega", "phi", "d0starrho", "d0star"]:
        createSnapshotAfterRegression(channel, date)
