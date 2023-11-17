from prepareFits import *

if "/home/submit/pdmonte/CMSSW_10_6_27/src/Hrare2023/analysis/func_marti.so" not in ROOT.gSystem.GetLibraries():
    ROOT.gSystem.CompileMacro("/home/submit/pdmonte/CMSSW_10_6_27/src/Hrare2023/analysis/func_marti.cc","k")

if "/home/submit/pdmonte/CMSSW_10_6_27/src/Hrare2023/analysis/functions.so" not in ROOT.gSystem.GetLibraries():
    ROOT.gSystem.CompileMacro("/home/submit/pdmonte/CMSSW_10_6_27/src/Hrare2023/analysis/functions.cc","k")



tag = "GFcat"

def createAndSaveHistogramSignal(mesonCat, year, date, filters=[], extraTitle=None, ditrack=False, regModelName=None, doubleFit=False):
    """Creates a histogram and saves it to a file."""
    print('\033[1;36m' + "\n[createAndSaveHistogramSIG] ---------------------- Creating Histogram... --------------------" + '\033[0m')
    if regModelName == "RECO":
        regModelName = None

    if not doubleFit:
        histogram = getHisto(200*2, 0., 200., date, numDict[mesonCat], tag, mesonCat, mesonLatex[mesonCat], year, filters, extraTitle, ditrack, regModelName=regModelName)
        #Save histogram
        name = getFullNameOfHistFile(mesonCat, tag, year, date, extraTitle=extraTitle, regModelName=regModelName)
    else:
        histogram = get2DHisto(200*2, 0., 200., 50, date, numDict[mesonCat], tag, mesonCat, mesonLatex[mesonCat], year, extraTitle, regModelName=regModelName)
        #Save histogram
        name = getFullNameOfHistFile(mesonCat, tag, year, date, extraTitle=extraTitle, regModelName=regModelName, doubleFit=True)
    
    saveHistoToFile(histogram, name)
    print('\033[1;36m' + "[createAndSaveHistogramSIG] ------------------------ Histogram saved! -----------------------" + '\033[0m')
    print('\033[1;36m' + "[createAndSaveHistogramSIG] {}".format((" " + name[34:] + " ").center(65, "-") + '\033[0m'))


def createAndSaveHistogramBackground(mesonCat, year, date, regModelName=None, doubleFit=False):
    """Creates a histogram and saves it to a file."""
    print('\033[1;31m' + "\n[createAndSaveHistogramBKG] ---------------------- Creating Histogram... --------------------" + '\033[0m')
    if regModelName == "RECO":
        regModelName = None

    if not doubleFit:
        histogram = getHisto(200*1, 0., 200., date, numDict["Background"], tag, mesonCat, mesonLatex[mesonCat], year, regModelName=regModelName)
        #Save histogram
        name = getFullNameOfHistFile(mesonCat, tag, year, date, extraTitle="BKG", regModelName=regModelName)
    else:
        histogram = get2DHisto(200*1, 0., 200., 50, date, numDict["Background"], tag, mesonCat, mesonLatex[mesonCat], year, extraTitle="BKG", regModelName=regModelName)
        #Save histogram
        name = getFullNameOfHistFile(mesonCat, tag, year, date, extraTitle="BKG", regModelName=regModelName, doubleFit=True)

    saveHistoToFile(histogram, name)
    print('\033[1;31m' + "[createAndSaveHistogramBKG] ------------------------ Histogram saved! -----------------------" + '\033[0m')
    print('\033[1;31m' + "[createAndSaveHistogramBKG] {}".format((" " + name[34:] + " ").center(65, "-")) + '\033[0m')


if __name__ == "__main__":

    year = 2018
    date = "NOV05"


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
    df = False
    mesonCat = "Phi3Cat"
    mesonCat = "OmegaCat"
    #mesonCat = "D0StarCat"
    #f = open("commands_temp_createHists.txt", "a")
    for df in [True]:
        for mesonCat in ["Phi3Cat", "OmegaCat", "D0StarCat", "D0StarRhoCat"]:
        #for mesonCat in ["D0StarRhoCat"]:
            with open('models_{}.txt'.format(mesonCat[:-3]), 'r') as file:
                for line in file:
                    regModelName = line.strip()
                    if regModelName[0] != "#":
                        createAndSaveHistogramSignal(mesonCat, year, date, regModelName=regModelName, doubleFit=df)
                        #createAndSaveHistogramBackground(mesonCat, year, date, regModelName=regModelName, doubleFit=df)
                        #comm = "{modelNameAbb}_{mesonCatAbb}_{df}::: python createHistogramFilesStandalone.py -m {modelName} -c {mesonCat} -y {year} -d {date} -f {doubleFit}"\
                        #    .format(modelNameAbb=regModelName[-5:], mesonCatAbb=mesonCat[:-3], df=int(df), modelName=regModelName, mesonCat=mesonCat, year=year, date=date, doubleFit=df)
                        #f.write(comm + "\n")
    #f.close()

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
