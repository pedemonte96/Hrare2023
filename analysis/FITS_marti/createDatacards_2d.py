#!env python
import ROOT
import sys, os
import re
#from array import array
import math
from optparse import OptionParser, OptionGroup

ROOT.gROOT.SetBatch()

parser = OptionParser()

parser.add_option("", "--inputFileSIG",     type='string', help="Input ROOT file signal model. [%default]", default="WS_JUL06/Signal_GFcat_D0StarCat_2018_workspace.root")
parser.add_option("", "--inputFileBKG",     type='string', help="Input ROOT file background model. [%default]", default="WS_JUL06/Bkg_GFcat_D0StarCat_2018_workspace.root")
parser.add_option("-c", "--whichCat",       type='string', help="Which category (GFcat, Wcat, Zcat Zinvcatm, VBFcat)", default="GFcat")
parser.add_option("-m", "--whichMeson",     type='string', help="Which meson (Phi3Cat, OmegaCat or D0StarCat)", default="D0StarCat")
parser.add_option("-o", "--output",         type='string', help="Output ROOT file. [%default]", default="WS_JUL06/workspace_STAT_D0StarCat_2018.root")
parser.add_option("-d", "--dataCardName",   type='string', help="Output txt file. [%default]", default="WS_JUL06/datacard_STAT_D0StarCat_2018.txt")

opts, args = parser.parse_args()

sys.argv = []

doSyst = True
MultiPdf = True

############ CONFIGURABLES ###########

if MultiPdf:
    BkgPdf={
        'Vcat': 'multipdf_' + opts.whichMeson,
        'Wcat': 'multipdf_' + opts.whichMeson,
        'Zcat': 'multipdf_' + opts.whichMeson,
        'VBFcat': 'multipdf_' + opts.whichMeson,
        'Zinvcat': 'multipdf_' + opts.whichMeson,
        'VBFcatlow': 'multipdf_' + opts.whichMeson,
        'GFcat': 'multipdf_' + opts.whichMeson,
    }
else:
    BkgPdf={
        'Vcat': 'exp1_' + opts.whichMeson,
        'Wcat': 'exp1_' + opts.whichMeson,
        'Zcat': 'exp1_' + opts.whichMeson,
        'VBFcat': 'bxg_' + opts.whichMeson,
        'Zinvcat': 'exp1_' + opts.whichMeson,
        'VBFcatlow': 'bxg_' + opts.whichMeson,
        'GFcat': 'bxg_' + opts.whichMeson,
    }

SigPdf={
    'Vcat': 'crystal_ball_' + opts.whichMeson,
    'Wcat': 'crystal_ball_' + opts.whichMeson,
    'Zcat': 'crystal_ball_' + opts.whichMeson,
    'VBFcat': 'crystal_ball_' + opts.whichMeson,
    'Zinvcat': 'crystal_ball_' + opts.whichMeson,
    'VBFcatlow': 'crystal_ball_' + opts.whichMeson,
    'GFcat': 'crystal_ball_' + opts.whichMeson,
}

ENUM={
    'ggH': 0,
    'VBFH': -1,
    'WH': -2,
    'ZH': -3,
    'ZinvH': -4,
    'WHl': -5,
    'ZHl': -6,
}

QCDscale={
    'ggH': '0.961/1.0039',
    'VBFH': '0.997/1.004',
    'WH': '0.993/1.006',
    'ZH': '0.995/1.005',
    'ZinvH': '0.995/1.005',
    'WHl': '0.993/1.006',
    'ZHl': '0.995/1.005',
}

pdf_Higgs={
    'ggH': '0.968/1.032',
    'VBFH': '0.979/1.021',
    'WH': '0.98/1.020',
    'ZH': '0.981/1.019', #assume the majority is not ggZH
    'ZinvH': '0.981/1.019', #assume the majority is not ggZH
    'WHl': '0.98/1.020',
    'ZHl': '0.981/1.019', #assume the majority is not ggZH
}

lumi={
    '_2016': '1.007',
    '_2017': '1.008',
    '_2018': '1.011',
}


def addSystematics(systname, systtype, value, whichProc, category, mcAll, datacard):

    datacard.write(systname + " \t" + systtype)
    for cat in category:
        #print("addSys cat", cat)
        for proc in mcAll:
            #print("addSys proc", proc)
            if (proc == whichProc): datacard.write("\t" + value)
            else: datacard.write("\t-")
    datacard.write("\n")


if __name__ == "__main__":
    #################### cat and processes ####################
    #print(opts.whichCat)

    if opts.whichCat=='GFcat':
        sigAll = ['ggH']
        mcAll = ['ggH', 'bkg']
        category = ['GFcat']
    else: raise ValueError("Category {} not supported.".format(opts.whichCat))
    
    #################### OPEN OUTPUT ####################
    w = ROOT.RooWorkspace("w","w")

    #################### DATACARD ####################
    datName = opts.dataCardName

    numChannel = len(mcAll) - 1
    print("-> Opening datacard: {}".format(datName))
    datacard = open(datName,"w")
    datacard.write("-------------------------------------\n")
    datacard.write("imax "+str(len(category))+" number of channels\n")
    datacard.write("jmax "+ str(numChannel)+" number of background minus 1\n")
    datacard.write("kmax * number of nuisance parameters\n")
    datacard.write("-------------------------------------\n")

    #################### IMPORT DATA ####################
    w.factory("mh[100,150]") # RooRealVar
    mh = w.var("mh")
    arglist_obs = ROOT.RooArgList(mh)
    argset_obs = ROOT.RooArgSet(mh)

    w.factory("m_meson[0.71,1.21]") # RooRealVar
    m_meson = w.var("m_meson")
    arglist_obs = ROOT.RooArgList(m_meson)
    argset_obs = ROOT.RooArgSet(m_meson)

    #################### Import SIGNAL/BKG CONTRIBUTIONS ####################
    fSigIn = ROOT.TFile.Open(opts.inputFileSIG,"READ")
    if fSigIn == None: raise FileNotFoundError("ERROR: file {} not found.".format(opts.inputFileSIG))

    fBkgIn = ROOT.TFile.Open(opts.inputFileBKG,"READ")
    if fBkgIn == None: raise FileNotFoundError("ERROR: file {} not found.".format(opts.inputFileBKG))

    for cat in category:
        for proc in mcAll:
            if proc == 'bkg':
                wInput = fBkgIn.Get("w")
                name = BkgPdf[cat] + "_" + cat + "_" + proc
                nameNorm = name + "_norm"
            else:
                wInput = fSigIn.Get("w")
                name = SigPdf[cat] + "_" + cat + "_" + proc
                name = "pdf_2D_sgn"
                nameNorm = name + "_norm"
            print("proc=", proc, " cat=", cat, " name=", name)
            func = wInput.pdf(name)
            if func == None: raise IOError("Unable to get func" + name)
            getattr(w,'import')(func)
            print("here----------------------")
            print(nameNorm)
            print("here----------------------")
            funcNorm = wInput.var(nameNorm)
            if funcNorm == None: raise IOError("Unable to get func normalization " + nameNorm)
            getattr(w,'import')(funcNorm)

            datacard.write("shapes")
            datacard.write("\t" + proc )
            datacard.write("\t" + cat )
            #if proc == 'bkg': datacard.write("\t" + opts.inputFileBKG )
            #else: datacard.write("\t" + opts.inputFileSIG )
            datacard.write("\t" + opts.output )
            datacard.write("\tw:" + name )
            datacard.write("\n")

        wInput = fBkgIn.Get("w")
        wInput.Print()
        hist_data = wInput.data("datahist_" + opts.whichMeson + '_' + cat)
        hist_data_doubleFit = wInput.data("datahist_" + opts.whichMeson + '_' + cat + "_doubleFit")
        print("datahist_" + opts.whichMeson + '_' + cat)
        hist_data.SetName("observed_data")
        hist_data_doubleFit.SetName("observed_data_doubleFit")
        print(hist_data)
        #this line produces segmentation violation after closing file w
        getattr(w,'import')(hist_data)
        getattr(w,'import')(hist_data_doubleFit)
        
        datacard.write("shapes")
        datacard.write("\tdata_obs" )
        datacard.write("\t" + cat )
        datacard.write("\t" + opts.output )
        datacard.write("\tw:" + "observed_data")
        #datacard.write("\t" + opts.inputFileBKG )
        #datacard.write("\tw:" + "datahist_" + opts.whichMeson + '_' + cat)
        datacard.write("\n")
    
    #################### OBSERVATION ####################
    datacard.write("-------------------------------------\n")
    datacard.write("bin")
    for cat in category:
        datacard.write("\t"+cat)
    datacard.write("\n")
    datacard.write("observation")
    for cat in category:
        datacard.write("\t-1")
    datacard.write("\n")

    #################### RATE ####################
    datacard.write("-------------------------------------\n")
    datacard.write("bin\t")
    for cat in category:    
        for proc in mcAll:
            datacard.write("\t"+cat)
    datacard.write("\n")
    datacard.write("process\t")
    for cat in category:    
        for proc in mcAll:
            datacard.write("\t"+proc)
    datacard.write("\n")
    datacard.write("process\t")
    for cat in category:
        for proc in mcAll: ## TRICK, put the only signal first
            if (proc=='bkg'): datacard.write("\t1")
            else: datacard.write("\t%d"%ENUM[proc])
    datacard.write("\n")
    datacard.write("rate\t")
    for cat in category:
        for proc in mcAll:
            if (proc=='bkg'): datacard.write("\t1")
            else: datacard.write("\t0.001")
    datacard.write("\n")

    #################### SYST ####################
    datacard.write("-------------------------------------\n")
    datacard.write("lumi_13TeV \tlnN ")
    for cat in category:
        for proc in mcAll:
            if (proc=='bkg'): datacard.write("\t-")
            else: datacard.write("\t%.3f"%(1.025) )
        datacard.write("\n")

    if doSyst:
        datacard.write("CMS_photonID \tlnN ")
        for cat in category:
            for proc in mcAll:
                if (proc=='bkg'): datacard.write("\t-")
                else: datacard.write("\t%.3f"%(1.01) )
            datacard.write("\n")

        datacard.write("CMS_prefiring \tlnN ")
        for cat in category:
            for proc in mcAll:
                if (proc=='bkg'): datacard.write("\t-")
                else: datacard.write("\t%.3f"%(1.005) )
            datacard.write("\n")

        datacard.write("CMS_pileup  \tlnN ")
        for cat in category:
            for proc in mcAll:
                if (proc=='bkg'): datacard.write("\t-")
                else: datacard.write("\t%.3f"%(1.01) )
            datacard.write("\n")

        for proc in mcAll:
            #print("proc", proc)
            if (proc=='bkg'): continue
            else:
                # theo
                addSystematics("QCDscale_" + proc, 'lnN', QCDscale[proc], proc, category, mcAll, datacard)
                addSystematics("pdf_Higgs_" + proc, 'lnN', pdf_Higgs[proc], proc, category, mcAll, datacard)

    #################### PDF index ####################
    datacard.write("-------------------------------------\n")

    if MultiPdf:
        pdfindexSTR = 'pdfindex_' + opts.whichMeson + "_" + opts.whichCat
        datacard.write("\n")
        datacard.write("%s discrete\n"%pdfindexSTR)

    #################### DONE ####################
    #w.Print()
    w.writeToFile(opts.output)
    del w #solves segfault. Bug in ROOT v6.14, fixed in v6.20
    print("->Done")