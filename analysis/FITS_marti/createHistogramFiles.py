from prepareFits import *

numDict = {"Background": [10, 11, 12, 13, 14], "OmegaCat": [1037], "D0StarCat": [1039], "Phi3Cat": [1040]}

mesonLatex = {"OmegaCat": "#omega", "D0StarCat": "D^{0*}", "Phi3Cat": "#phi"}


def createAndSaveHistogramSignal(tag, mesonCat, year, date, filters=[], extraTitle=None):
    """Creates a histogram and saves it to a file."""
    #Create Histogram
    histogram = getHisto(200*10, 0., 200., date, numDict[mesonCat], tag, mesonCat, mesonLatex[mesonCat], year, filters, extraTitle)
    #Save histogram
    saveHistoToFile(histogram, getFullNameOfHistFile(mesonCat, cat, year, date, extraTitle=extraTitle))
    print("[createAndSaveHistogram] ------------------------Histogram saved!-----------------------")


def createAndSaveHistogramBackground(tag, mesonCat, year, date):
    """Creates a histogram and saves it to a file."""
    #Create Histogram
    histogram = getHisto(250, 0., 200., date, numDict["Background"], tag, mesonCat, mesonLatex[mesonCat], year)
    #Save histogram
    saveHistoToFile(histogram, getFullNameOfHistFile(mesonCat, cat, year, date, extraTitle="BKG"))
    print("[createAndSaveHistogram] ------------------------Histogram saved!-----------------------")


if __name__ == "__main__":

    cat = "GFcat"
    year = 2018
    date = "JUN07"


    #D0Star----------------------------------------------------------------------------------------
    mesonCat = "D0StarCat"
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
    date = "MAY31"
    createAndSaveHistogramBackground(cat, mesonCat, year, date)


    #BACKGROUND Phi3-------------------------------------------------------------------------------
    mesonCat = "Phi3Cat"
    date = "MAY30"
    createAndSaveHistogramBackground(cat, mesonCat, year, date)
