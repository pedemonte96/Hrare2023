from prepareFits import *

if "/home/submit/pdmonte/CMSSW_10_6_27/src/Hrare2023/analysis/func_marti.so" not in ROOT.gSystem.GetLibraries():
    ROOT.gSystem.CompileMacro("/home/submit/pdmonte/CMSSW_10_6_27/src/Hrare2023/analysis/func_marti.cc","k")

if "/home/submit/pdmonte/CMSSW_10_6_27/src/Hrare2023/analysis/functions.so" not in ROOT.gSystem.GetLibraries():
    ROOT.gSystem.CompileMacro("/home/submit/pdmonte/CMSSW_10_6_27/src/Hrare2023/analysis/functions.cc","k")


def createAndSaveHistogramSignal(tag, mesonCat, year, date, filters=[], extraTitle=None, ditrack=False):
    """Creates a histogram and saves it to a file."""
    #Create Histogram
    histogram = getHisto(200*10, 0., 200., date, numDict[mesonCat], tag, mesonCat, mesonLatex[mesonCat], year, filters, extraTitle, ditrack)
    #Save histogram
    saveHistoToFile(histogram, getFullNameOfHistFile(mesonCat, cat, year, date, extraTitle=extraTitle))
    print("[createAndSaveHistogram] ------------------------Histogram saved!-----------------------")


def createAndSaveHistogramBackground(tag, mesonCat, year, date):
    """Creates a histogram and saves it to a file."""
    #Create Histogram
    histogram = getHisto(200, 0., 200., date, numDict["Background"], tag, mesonCat, mesonLatex[mesonCat], year)
    #Save histogram
    saveHistoToFile(histogram, getFullNameOfHistFile(mesonCat, cat, year, date, extraTitle="BKG"))
    print("[createAndSaveHistogram] ------------------------Histogram saved!-----------------------")


if __name__ == "__main__":

    cat = "GFcat"
    year = 2018
    date = "JUN14"


    #D0Star----------------------------------------------------------------------------------------
    mesonCat = "D0StarCat"
    '''createAndSaveHistogramSignal(cat, mesonCat, year, date)

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
    createAndSaveHistogramSignal(cat, mesonCat, year, date, filters=filters, extraTitle=extraTitle)'''
    
    date = "JUN21"
    filters = ["Vec_i {static_cast<int>(getPt(GenPart_pt, GenPart_pdgId, GenPart_genPartIdxMother, 22, 423, 25).size())}"]
    #filters = ["abs(goodMeson_eta) > 1.4", "abs(goodPhotons_eta) > 1.4"]
    extraTitle = "missing photon"
    createAndSaveHistogramSignal(cat, mesonCat, year, date, filters=filters, extraTitle=extraTitle, ditrack=True)
    filters = ["Vec_i {static_cast<int>(getPt(GenPart_pt, GenPart_pdgId, GenPart_genPartIdxMother, 111, 423, 25).size())}"]
    #filters = ["abs(goodMeson_eta) > 1.4", "abs(goodPhotons_eta) > 1.4"]
    extraTitle = "missing pion"
    createAndSaveHistogramSignal(cat, mesonCat, year, date, filters=filters, extraTitle=extraTitle, ditrack=True)

    '''
    #Phi3------------------------------------------------------------------------------------------
    mesonCat = "Phi3Cat"
    createAndSaveHistogramSignal(cat, mesonCat, year, date)

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


    #BACKGROUND D0Star-----------------------------------------------------------------------------
    mesonCat = "D0StarCat"
    date = "JUN14"
    createAndSaveHistogramBackground(cat, mesonCat, year, date)


    #BACKGROUND Phi3-------------------------------------------------------------------------------
    mesonCat = "Phi3Cat"
    date = "JUN14"
    createAndSaveHistogramBackground(cat, mesonCat, year, date)
    '''