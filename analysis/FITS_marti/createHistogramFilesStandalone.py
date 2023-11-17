from prepareFits import *
import argparse

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
        histogram = getHisto(200*5, 0., 200., date, numDict[mesonCat], tag, mesonCat, mesonLatex[mesonCat], year, filters, extraTitle, ditrack, regModelName=regModelName)
        #Save histogram
        name = getFullNameOfHistFile(mesonCat, tag, year, date, extraTitle=extraTitle, regModelName=regModelName)
    else:
        histogram = get2DHisto(200*5, 0., 200., 100, date, numDict[mesonCat], tag, mesonCat, mesonLatex[mesonCat], year, extraTitle, regModelName=regModelName)
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


parser = argparse.ArgumentParser(description="Famous Submitter")
parser.add_argument("-m", "--modelName", type=str, required=True, help="Input the model name (e.g. BDTG_df55_dl12_v1_v13).")
parser.add_argument("-c", "--mesonCat", type=str, required=True, help="Channel (e.g. phi, omega, d0starrho, d0star).")
parser.add_argument("-y", "--year", type=int, required=True, help="Year of data (eg. 2018).")
parser.add_argument("-d", "--date", type=str, required=True, help="Year of data (eg. NOV05).")
parser.add_argument("-f", "--doubleFit", type=str, required=True, help="Double fit or not (true/false)")
options = parser.parse_args()

is2Dfit = options.doubleFit.lower() == 'true'
    
createAndSaveHistogramSignal(options.mesonCat, options.year, options.date, regModelName=options.modelName, doubleFit=is2Dfit)
createAndSaveHistogramBackground(options.mesonCat, options.year, options.date, regModelName=options.modelName, doubleFit=is2Dfit)
