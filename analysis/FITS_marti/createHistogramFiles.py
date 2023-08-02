from prepareFits import *

if "/home/submit/pdmonte/CMSSW_10_6_27/src/Hrare2023/analysis/func_marti.so" not in ROOT.gSystem.GetLibraries():
    ROOT.gSystem.CompileMacro("/home/submit/pdmonte/CMSSW_10_6_27/src/Hrare2023/analysis/func_marti.cc","k")

if "/home/submit/pdmonte/CMSSW_10_6_27/src/Hrare2023/analysis/functions.so" not in ROOT.gSystem.GetLibraries():
    ROOT.gSystem.CompileMacro("/home/submit/pdmonte/CMSSW_10_6_27/src/Hrare2023/analysis/functions.cc","k")


def createAndSaveHistogramSignal(tag, mesonCat, year, date, filters=[], extraTitle=None, ditrack=False, regressionModel=None):
    """Creates a histogram and saves it to a file."""
    print('\033[1;36m' + "\n[createAndSaveHistogramSIG] ---------------------- Creating Histogram... --------------------" + '\033[0m')
    histogram = getHisto(200*10, 0., 200., date, numDict[mesonCat], tag, mesonCat, mesonLatex[mesonCat], year, filters, extraTitle, ditrack, regressionModel=regressionModel)
    #Save histogram
    name = getFullNameOfHistFile(mesonCat, cat, year, date, extraTitle=extraTitle)
    saveHistoToFile(histogram, name)
    print('\033[1;36m' + "[createAndSaveHistogramSIG] ------------------------ Histogram saved! -----------------------" + '\033[0m')
    print('\033[1;36m' + "[createAndSaveHistogramSIG] {}".format((" " + name[34:] + " ").center(65, "-") + '\033[0m'))


def createAndSaveHistogramBackground(tag, mesonCat, year, date, regressionModel=None):
    """Creates a histogram and saves it to a file."""
    print('\033[1;31m' + "\n[createAndSaveHistogramBKG] ---------------------- Creating Histogram... --------------------" + '\033[0m')
    histogram = getHisto(200, 0., 200., date, numDict["Background"], tag, mesonCat, mesonLatex[mesonCat], year, regressionModel=regressionModel)
    #Save histogram
    if regressionModel is None:
        extratitle="BKG"
    else:
        extratitle="BKG_regression"
    name = getFullNameOfHistFile(mesonCat, cat, year, date, extraTitle=extratitle)
    saveHistoToFile(histogram, name)
    print('\033[1;31m' + "[createAndSaveHistogramBKG] ------------------------ Histogram saved! -----------------------" + '\033[0m')
    print('\033[1;31m' + "[createAndSaveHistogramBKG] {}".format((" " + name[34:] + " ").center(65, "-")) + '\033[0m')


if __name__ == "__main__":

    cat = "GFcat"
    year = 2018
    date = "JUL31"


    #D0Star----------------------------------------------------------------------------------------
    mesonCat = "D0StarCat"
    #createAndSaveHistogramSignal(cat, mesonCat, year, date)
    '''
    filters = ["abs(goodMeson_eta) < 1.4"]
    extraTitle = "barrel meson"
    createAndSaveHistogramSignal(cat, mesonCat, year, date, filters=filters, extraTitle=extraTitle)

    filters = ["abs(goodPhotons_eta) < 1.4"]
    extraTitle = "barrel photon"
    createAndSaveHistogramSignal(cat, mesonCat, year, date, filters=filters, extraTitle=extraTitle)

    filters = ["abs(goodMeson_eta) < 1.4", "abs(goodPhotons_eta) < 1.4"]
    extraTitle = "barrel meson, barrel photon"
    createAndSaveHistogramSignal(cat, mesonCat, year, date, filters=filters, extraTitle=extraTitle)

    filters = ["abs(goodMeson_eta) > 1.4", "abs(goodPhotons_eta) < 1.4"]
    extraTitle = "endcap meson, barrel photon"
    createAndSaveHistogramSignal(cat, mesonCat, year, date, filters=filters, extraTitle=extraTitle)

    filters = ["abs(goodMeson_eta) < 1.4", "abs(goodPhotons_eta) > 1.4"]
    extraTitle = "barrel meson, endcap photon"
    createAndSaveHistogramSignal(cat, mesonCat, year, date, filters=filters, extraTitle=extraTitle)

    filters = ["abs(goodMeson_eta) > 1.4", "abs(goodPhotons_eta) > 1.4"]
    extraTitle = "endcap meson, endcap photon"
    createAndSaveHistogramSignal(cat, mesonCat, year, date, filters=filters, extraTitle=extraTitle)
    
    date = "JUN21"
    filters = ["Vec_i {static_cast<int>(getPt(GenPart_pt, GenPart_pdgId, GenPart_genPartIdxMother, 22, 423, 25).size())}"]
    extraTitle = "missing photon"
    createAndSaveHistogramSignal(cat, mesonCat, year, date, filters=filters, extraTitle=extraTitle, ditrack=True)
    filters = ["Vec_i {static_cast<int>(getPt(GenPart_pt, GenPart_pdgId, GenPart_genPartIdxMother, 111, 423, 25).size())}"]
    extraTitle = "missing pion"
    createAndSaveHistogramSignal(cat, mesonCat, year, date, filters=filters, extraTitle=extraTitle, ditrack=True)
    '''
    #Phi3------------------------------------------------------------------------------------------
    mesonCat = "Phi3Cat"
    s = '''
        TMVA::Experimental::RReader modelScale("{modelFileName}");
        computeModelScale = TMVA::Experimental::Compute<{numVars}, float>(modelScale);
        '''.format(modelFileName="/data/submit/pdmonte/TMVA_models/weightsVars/TMVARegression_BDTG_df15_dl511_v1_v35.weights.xml", numVars=15)

    ROOT.gInterpreter.ProcessLine(s)

    regressionModelPhi3 = (ROOT.computeModelScale, list(ROOT.modelScale.GetVariableNames()))
    createAndSaveHistogramSignal(cat, mesonCat, year, date, extraTitle="regression", regressionModel=regressionModelPhi3)
    createAndSaveHistogramSignal(cat, mesonCat, year, date)
    '''
    filters = ["abs(goodMeson_eta) < 1.4"]
    extraTitle = "barrel meson"
    createAndSaveHistogramSignal(cat, mesonCat, year, date, filters=filters, extraTitle=extraTitle)

    filters = ["abs(goodPhotons_eta) < 1.4"]
    extraTitle = "barrel photon"
    createAndSaveHistogramSignal(cat, mesonCat, year, date, filters=filters, extraTitle=extraTitle)

    filters = ["abs(goodMeson_eta) < 1.4", "abs(goodPhotons_eta) < 1.4"]
    extraTitle = "barrel meson, barrel photon"
    createAndSaveHistogramSignal(cat, mesonCat, year, date, filters=filters, extraTitle=extraTitle)

    filters = ["abs(goodMeson_eta) > 1.4", "abs(goodPhotons_eta) < 1.4"]
    extraTitle = "endcap meson, barrel photon"
    createAndSaveHistogramSignal(cat, mesonCat, year, date, filters=filters, extraTitle=extraTitle)

    filters = ["abs(goodMeson_eta) < 1.4", "abs(goodPhotons_eta) > 1.4"]
    extraTitle = "barrel meson, endcap photon"
    createAndSaveHistogramSignal(cat, mesonCat, year, date, filters=filters, extraTitle=extraTitle)

    filters = ["abs(goodMeson_eta) > 1.4", "abs(goodPhotons_eta) > 1.4"]
    extraTitle = "endcap meson, endcap photon"
    createAndSaveHistogramSignal(cat, mesonCat, year, date, filters=filters, extraTitle=extraTitle)
'''

    #BACKGROUND D0Star-----------------------------------------------------------------------------
    mesonCat = "D0StarCat"
    date = "JUN29"
    #createAndSaveHistogramBackground(cat, mesonCat, year, date)


    #BACKGROUND Phi3-------------------------------------------------------------------------------
    mesonCat = "Phi3Cat"
    date = "JUL31"
    createAndSaveHistogramBackground(cat, mesonCat, year, date, regressionModel=regressionModelPhi3)
    createAndSaveHistogramBackground(cat, mesonCat, year, date)
