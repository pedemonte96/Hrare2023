import ROOT
import os
import json
from subprocess import call,check_output
import fnmatch
import glob
from XRootD import client
from XRootD.client.flags import DirListFlags
import subprocess

if "/functions.so" not in ROOT.gSystem.GetLibraries():
    ROOT.gSystem.CompileMacro("functions.cc","k")

import correctionlib
correctionlib.register_pyroot_binding()

def loadCorrectionSet(year):
    ROOT.gInterpreter.Load("config/mysf.so")
    ROOT.gInterpreter.Declare('#include "config/mysf.h"')
    ROOT.gInterpreter.ProcessLine('auto corr_sf = MyCorrections(%d);' % (year))

def getTriggerFromJson(overall, type, year ):

    for trigger in overall:
        if trigger['name'] == type and trigger['year'] == year: return trigger['definition']

def getMesonFromJson(overall, type, cat ):

    for meson in overall:
        if meson['name'] == type and meson['type'] == cat: return meson['definition']

def getMVAFromJson(overall, type, cat ):

    for meson in overall:
        if meson['name'] == type and meson['type'] == cat: return meson['file']

def loadJSON(fIn):

    if not os.path.isfile(fIn):
        print("JSON file %s does not exist" % fIn)
        return

    if not hasattr(ROOT, "jsonMap"):
        print("jsonMap not found in ROOT dict")
        return

    info = json.load(open(fIn))
    print("JSON file %s loaded" % fIn)
    for k,v in info.items():

        vec = ROOT.std.vector["std::pair<unsigned int, unsigned int>"]()
        for combo in v:
            pair = ROOT.std.pair["unsigned int", "unsigned int"](*[int(c) for c in combo])
            vec.push_back(pair)
            ROOT.jsonMap[int(k)] = vec

def findDataset(name):

    DASclient = "dasgoclient -query '%(query)s'"
    cmd= DASclient%{'query':'file dataset=%s'%name}
    print(cmd)
    check_output(cmd,shell=True)
    fileList=[ 'root://xrootd-cms.infn.it//'+x for x in check_output(cmd,shell=True).split() ]

    files_ROOT = ROOT.vector('string')()
    for f in fileList: files_ROOT.push_back(f)

    return files_ROOT

def findDIR(directory):

    print(directory)

    counter = 0
    rootFiles = ROOT.vector('string')()
    for root, directories, filenames in os.walk(directory):
        for f in filenames:

            counter+=1
            filePath = os.path.join(os.path.abspath(root), f)
            if "failed/" in filePath: continue
            if "log/" in filePath: continue
            rootFiles.push_back(filePath)
#            if counter>100: break
#            if counter>50: break
#            if counter>5: break

    return rootFiles

def readListFromFile(filename):

    rootFiles = ROOT.vector('string')()
    with open(filename, "r") as f:
        for item in f:
            rootFiles.push_back(item)

    return rootFiles


def findManyClient(basedir, regex):

    rootFiles = ROOT.vector('string')()

    directory = '/store/user/paus/nanohr/D01'
    fs = client.FileSystem('root://xrootd.cmsaf.mit.edu/')
    lsst = fs.dirlist(directory,DirListFlags.RECURSIVE)
#    lsst = fs.dirlist(directory)

    for e in lsst[1]:
        filePath  = e.name
        if fnmatch.fnmatch(filePath, regex):
            filename= 'root://xrootd.cmsaf.mit.edu/'+directory+e.name
            if "failed/" in filename: continue
            if "log/" in filename: continue
            if "tmp_" in filename: continue
            if ".txt" in filename: continue
            rootFiles.push_back(filename)

    return rootFiles

def findManyXRDFS(basedir, regex):

    server = "root://xrootd.cmsaf.mit.edu/"
    print("using ",server)
    print("regex=",regex)
    print("basedir=",basedir)

    command = f"xrdfs "+server+" ls -R /store/user/paus/nanohr/D01 | grep "+regex+" | grep '.root'"
    proc = subprocess.Popen(command, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, shell=True)
    result = proc.stdout.readlines()
    paths = [server + r.rstrip().decode("utf-8") for r in result]
    print(paths)
    print('RESULTS = ',len(result))

    rootFiles = ROOT.vector('string')()
    for f in paths:
        rootFiles.push_back(f)

    return rootFiles


def findMany(basedir, regex):

    if basedir[-1] == "/": basedir = basedir[:-1]
    regex = basedir + "/" + regex

    rootFiles = ROOT.vector('string')()
    for root, directories, filenames in os.walk(basedir):

        for f in filenames:

            filePath = os.path.join(os.path.abspath(root), f)
            if "failed/" in filePath: continue
            if "log/" in filePath: continue
            if fnmatch.fnmatch(filePath, regex): rootFiles.push_back(filePath)

    return rootFiles

def concatenate(result, tmp1):
    for f in tmp1:
        result.push_back(f)

def getMClist(year,sampleNOW):

    files = findDIR("{}".format(SwitchSample(sampleNOW)[0]))
    if sampleNOW==0:
            files1 = findDIR("{}".format(SwitchSample(1000)[0]))
            concatenate(files, files1)
    return files

def getDATAlist(year,type):

    if(year == 2018):
        loadJSON("/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions18/13TeV/Legacy_2018/Cert_314472-325175_13TeV_Legacy2018_Collisions18_JSON.txt")
    if(year == 2017):
        loadJSON("/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions17/13TeV/Legacy_2017/Cert_294927-306462_13TeV_UL2017_Collisions17_GoldenJSON.txt")
    if(year == 2016 or year == 12016):
        loadJSON("/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/Legacy_2016/Cert_271036-284044_13TeV_Legacy2016_Collisions16_JSON.txt")

    if(year == 2018 and type == -1):
        files = findMany("/mnt/T2_US_MIT/hadoop/cms/store/user/paus/nanohr/D01/","SingleMuon+Run2018A*")
    if(year == 2018 and type == -2):
        files = findMany("/mnt/T2_US_MIT/hadoop/cms/store/user/paus/nanohr/D01/","SingleMuon+Run2018B*")
    if(year == 2018 and type == -3):
        files = findMany("/mnt/T2_US_MIT/hadoop/cms/store/user/paus/nanohr/D01/","SingleMuon+Run2018C*")
    if(year == 2018 and type == -4):
        files = findMany("/mnt/T2_US_MIT/hadoop/cms/store/user/paus/nanohr/D01/","SingleMuon+Run2018D*")

    if(year == 2018 and type == -31):
        files = findMany("/mnt/T2_US_MIT/hadoop/cms/store/user/paus/nanohr/D01/","EGamma+Run2018A*")
    if(year == 2018 and type == -32):
        files = findMany("/mnt/T2_US_MIT/hadoop/cms/store/user/paus/nanohr/D01/","EGamma+Run2018B*")
    if(year == 2018 and type == -33):
        files = findMany("/mnt/T2_US_MIT/hadoop/cms/store/user/paus/nanohr/D01/","EGamma+Run2018C*")
    if(year == 2018 and type == -34):
        files = findMany("/mnt/T2_US_MIT/hadoop/cms/store/user/paus/nanohr/D01/","EGamma+Run2018D*")

    return files

def getSkims(argument,year,category):

    if(year == 2018):
        loadJSON("/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions18/13TeV/Legacy_2018/Cert_314472-325175_13TeV_Legacy2018_Collisions18_JSON.txt")
    if(year == 2017):
        loadJSON("/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions17/13TeV/Legacy_2017/Cert_294927-306462_13TeV_UL2017_Collisions17_GoldenJSON.txt")
    if(year == 2016 or year == 12016):
        loadJSON("/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/Legacy_2016/Cert_271036-284044_13TeV_Legacy2016_Collisions16_JSON.txt")

    dirScratch = "/scratch/submit/mariadlf/Hrare/SKIMS/D01"
    switch = {
        -1: (("SingleMuon+Run"+"A"),"SingleMuon"),
        -2: (("SingleMuon+Run"+"B"),"SingleMuon"),
        -3: (("SingleMuon+Run"+"C"),"SingleMuon"),
        -4: (("SingleMuon+Run"+"D"),"SingleMuon"),
        -5: (("SingleMuon+Run"+"E"),"SingleMuon"),
        -6: (("SingleMuon+Run"+"F"),"SingleMuon"),
        -7: (("SingleMuon+Run"+"G"),"SingleMuon"),
        -8: (("SingleMuon+Run"+"H"),"SingleMuon"),
        #
        -11: (("DoubleMuon+Run"+"A"),"DoubleMuon"),
        -12: (("DoubleMuon+Run"+"B"),"DoubleMuon"),
        -13: (("DoubleMuon+Run"+"C"),"DoubleMuon"),
        -14: (("DoubleMuon+Run"+"D"),"DoubleMuon"),
        -15: (("DoubleMuon+Run"+"E"),"DoubleMuon"),
        -16: (("DoubleMuon+Run"+"F"),"DoubleMuon"),
        -17: (("DoubleMuon+Run"+"G"),"DoubleMuon"),
        -18: (("DoubleMuon+Run"+"H"),"DoubleMuon"),        ,
        #
        -21: (("MuonEG+Run"+"A"),"MuonEG"),
        -22: (("MuonEG+Run"+"B"),"MuonEG"),
        -23: (("MuonEG+Run"+"C"),"MuonEG"),
        -24: (("MuonEG+Run"+"D"),"MuonEG"),
        -25: (("MuonEG+Run"+"E"),"MuonEG"),
        -26: (("MuonEG+Run"+"F"),"MuonEG"),
        -27: (("MuonEG+Run"+"G"),"MuonEG"),
        -28: (("MuonEG+Run"+"H"),"MuonEG"),
        #
        -31: (("EGamma+Run"+"A"),"EGamma"),
        -32: (("EGamma+Run"+"B"),"EGamma"),
        -33: (("EGamma+Run"+"C"),"EGamma"),
        -34: (("EGamma+Run"+"D"),"EGamma"),
        -35: (("EGamma+Run"+"E"),"EGamma"),
        -36: (("EGamma+Run"+"F"),"EGamma"),
        -37: (("EGamma+Run"+"G"),"EGamma"),
        -38: (("EGamma+Run"+"H"),"EGamma"),
        #
        -41: (("DoubleEG+Run"+"A"),"DoubleEG"),
        -42: (("DoubleEG+Run"+"B"),"DoubleEG"),
        -43: (("DoubleEG+Run"+"C"),"DoubleEG"),
        -43: (("DoubleEG+Run"+"C"),"DoubleEG"),
        -44: (("DoubleEG+Run"+"D"),"DoubleEG"),
        -45: (("DoubleEG+Run"+"E"),"DoubleEG"),
        -46: (("DoubleEG+Run"+"F"),"DoubleEG"),
        -47: (("DoubleEG+Run"+"G"),"DoubleEG"),
        -48: (("DoubleEG+Run"+"H"),"DoubleEG"),
        #
        -51: (("SingleElectron+Run"+"A"),"SingleElectron"),
        -52: (("SingleElectron+Run"+"B"),"SingleElectron"),
        -53: (("SingleElectron+Run"+"C"),"SingleElectron"),
        -54: (("SingleElectron+Run"+"D"),"SingleElectron"),
        -55: (("SingleElectron+Run"+"E"),"SingleElectron"),
        -56: (("SingleElectron+Run"+"F"),"SingleElectron"),
        -57: (("SingleElectron+Run"+"G"),"SingleElectron"),
        -58: (("SingleElectron+Run"+"H"),"SingleElectron"),
        #
        -61: (("Tau+Run"+"A"),"Tau"),
        -62: (("Tau+Run"+"B"),"Tau"),
        -63: (("Tau+Run"+"C"),"Tau"),
        -64: (("Tau+Run"+"D"),"Tau"),
        #
#        -71: (("SinglePhoton+Run"+"A"),"SinglePhoton"),
#        -72: (("SinglePhoton+Run"+"B"),"SinglePhoton"),
#        -73: (("SinglePhoton+Run"+"C"),"SinglePhoton"),
#        -74: (("SinglePhoton+Run"+"D"),"SinglePhoton"),
#        -75: (("SinglePhoton+Run"+"E"),"SinglePhoton"),
        -76: (("SinglePhoton+Run"+"F"),"SinglePhoton"), # only this used 
#        -77: (("SinglePhoton+Run"+"G"),"SinglePhoton"),
#        -78: (("SinglePhoton+Run"+"H"),"SinglePhoton"),
        #
        -81: (("SinglePhoton+Run"+"B-ver1-HIPM"),"SinglePhoton"),
        -82: (("SinglePhoton+Run"+"B-ver1-HIPM"),"SinglePhoton"),
        -83: (("SinglePhoton+Run"+"C-HIPM"),"SinglePhoton"),
        -84: (("SinglePhoton+Run"+"D-HIPM"),"SinglePhoton"),
        -85: (("SinglePhoton+Run"+"E-HIPM"),"SinglePhoton"),
        -86: (("SinglePhoton+Run"+"F-HIPM"),"SinglePhoton"),
    }

    tmp_pair = switch.get(argument, "regex, PDtype")
    finalDir = dirScratch+"/"+category+"/"+str(year)+"/"+tmp_pair[0]
    pair = (findDIR(finalDir),tmp_pair[1])
    return pair


def SwitchSample(argument,year):

    # cross section from  https://cms-gen-dev.cern.ch/xsdb
    dirT2 = "/mnt/T2_US_MIT/hadoop/cms/store/user/paus/nanohr/D01/"
    dirLocal = "/work/submit/mariadlf/Hrare/D01/2018/"

    campaign = ""
    if(year == 2018): campaign = "RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1*"
    if(year == 2017): campaign = "RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9*"
    if(year == 2016): campaign = "RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17*"
    if(year == 12016): campaign = "RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11*"

    switch = {
        ## SIGNAL
        1010: (dirT2+"VBF_HToPhiGamma_M125_TuneCP5_PSWeights_13TeV_powheg_pythia8+"+campaign,3781.7*0.49), #NNLO
        1011: (dirT2+"WplusH_WToLNu_HToPhiGamma_M125_TuneCP5_PSWeights_13TeV_powheg_pythia8+"+campaign,3*94.26*0.49), #xsec = 3*9.426E-02 (xsec*Wl) * BR(Hphigamma)=1 BR(phi->kk)=0.49
        1012: (dirT2+"WminusH_WToLNu_HToRhoGamma_M125_TuneCP5_PSWeights_13TeV_powheg_pythia8+"+campaign,3*59.83*0.49), #xsec = 3*5.983E-02 (xsecWl) * BR(Hphigamma)=1 BR(phi->kk)=0.49
        1013: (dirT2+"ZH_ZToLL_HToPhiGamma_M125_TuneCP5_PSWeights_13TeV_powheg_pythia8+"+campaign,3*(29.82 - 4.14)*0.49), #xsec = 3*9.426E-02 (xsec*Zll) * BR(Hphigamma)=1 BR(phi->kk)=0.49
        1014: (dirT2+"ggZH_ZToLL_HToPhiGamma_M125_TuneCP5_PSWeights_13TeV_powheg_pythia8+"+campaign,3*4.14*0.49), #xsec = 3*9.426E-02 (xsec*Zll) * BR(Hphigamma)=1 BR(phi->kk)=0.49
        1015: (dirT2+"ZH_ZToNuNu_HToPhiGamma_M125_TuneCP5_PSWeights_13TeV_powheg_pythia8+"+campaign,(177.6 - 24.5)*0.49), #xsec = 3*9.426E-02 (xsec*Zll) * BR(Hphigamma)=1 BR(phi->kk)=0.49
        1016: (dirT2+"ggZH_ZToNuNu_HToPhiGamma_M125_TuneCP5_PSWeights_13TeV_powheg_pythia8+"+campaign,24.5*0.49), #xsec = 3*9.426E-02 (xsec*Zll) * BR(Hphigamma)=1 BR(phi->kk)=0.49
        1017: (dirT2+"GluGlu_HToPhiGamma_M125_TuneCP5_PSWeights_13TeV_powheg_pythia8+"+campaign,46870*0.49), #xsec = 3*9.426E-02 (xsec*ggH) * BR(Hphigamma)=1 BR(phi->kk)=0.49
        #
        1020: (dirT2+"VBF_HToRhoGamma_M125_TuneCP5_PSWeights_13TeV_powheg_pythia8+"+campaign,3781.7), # xsec = 4pb * BR(Hrhogamma)=1 BR(rho->pipi)=1
        1021: (dirT2+"WplusH_WToLNu_HToRhoGamma_M125_TuneCP5_PSWeights_13TeV_powheg_pythia8+"+campaign,3*94.26), #xsec = 3*9.426E-02 (Wl) * BR(Hrhogamma)=1 BR(rho->pipi)=1
        1022: (dirT2+"WminusH_WToLNu_HToRhoGamma_M125_TuneCP5_PSWeights_13TeV_powheg_pythia8+"+campaign,3*59.83), #xsec = 3*5.983E-02 (Wl) * BR(Hrhogamma)=1 BR(rho->pipi)=1
        1023: (dirT2+"ZH_ZToLL_HToRhoGamma_M125_TuneCP5_PSWeights_13TeV_powheg_pythia8+"+campaign,3*(29.82 - 4.14)), #xsec = 3*9.426E-02 (xsec*Wl) * BR(Hrhogamma)=1 BR(rho->pipi)=1
        1024: (dirT2+"ggZH_ZToLL_HToRhoGamma_M125_TuneCP5_PSWeights_13TeV_powheg_pythia8+"+campaign,3*4.14), #xsec = 3*9.426E-02 (xsec*Wl) * BR(Hrhogamma)=1 BR(rho->pipi)=1
        1025: (dirT2+"ZH_ZToNuNu_HToRhoGamma_M125_TuneCP5_PSWeights_13TeV_powheg_pythia8+"+campaign,(177.6 - 24.5)), #xsec = 3*9.426E-02 (xsec*Wl) * BR(Hrhogamma)=1 BR(rho->pipi)=1
        1026: (dirT2+"ggZH_ZToNuNu_HToRhoGamma_M125_TuneCP5_PSWeights_13TeV_powheg_pythia8+"+campaign,24.5), #xsec = 3*9.426E-02 (xsec*Wl) * BR(Hrhogamma)=1 BR(rho->pipi)=1
        1027: (dirT2+"GluGlu_HToRhoGamma_M125_TuneCP5_PSWeights_13TeV_powheg_pythia8+"+campaign,46870), #xsec = 3*9.426E-02 (xsec*ggH) * BR(Hrhogamma)=1 BR(rho->pipi)=1
        ##
        1030: (dirT2+"ZH_HToJPsiG_JPsiToMuMu_TuneCP5_13TeV-madgraph-pythia8+"+campaign,6067*1000), #check xSEC
        ## SM-BKG
        0: (dirT2+"DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8+"+campaign,6067*1000), #NNLO
        1: (dirT2+"ZGToLLG_01J_5f_TuneCP5_13TeV-amcatnloFXFX-pythia8+"+campaign, 51.1*1000), #LO
        2: (dirT2+"WGToLNuG_01J_5f_TuneCP5_13TeV-amcatnloFXFX-pythia8+"+campaign, 191.0*1000), #LO
        3: (dirT2+"WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8+"+campaign,53870.0*1000), #LO
        4: (dirT2+"TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8+"+campaign,88.2*1000), #NNLO
        5: (dirT2+"TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8+"+campaign,365.3452*1000), #NNLO
        #
        6: (dirT2+"GJets_DR-0p4_HT-100To200_TuneCP5_13TeV-madgraphMLM-pythia8+"+campaign,5034*1000*1.26), #LO *1.26
        7: (dirT2+"GJets_DR-0p4_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8+"+campaign,1129*1000*1.26), #LO *1.26
        8: (dirT2+"GJets_DR-0p4_HT-400To600_TuneCP5_13TeV-madgraphMLM-pythia8+"+campaign,126.2*1000*1.26), #LO *1.26
        9: (dirT2+"GJets_DR-0p4_HT-600ToInf_TuneCP5_13TeV-madgraphMLM-pythia8+"+campaign,41.31*1000*1.26), #LO *1.26
        10: (dirT2+"GJets_HT-40To100_TuneCP5_13TeV-madgraphMLM-pythia8+"+campaign,18540.0*1000*1.26), #LO *1.26
        11: (dirT2+"GJets_HT-100To200_TuneCP5_13TeV-madgraphMLM-pythia8+"+campaignFIX,8644.0*1000*1.26), #LO *1.26
        12: (dirT2+"GJets_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8+"+campaign,2183.0*1000*1.26), #LO *1.26
        13: (dirT2+"GJets_HT-400To600_TuneCP5_13TeV-madgraphMLM-pythia8+"+campaign,260.2*1000*1.26), #LO *1.26
        14: (dirT2+"GJets_HT-600ToInf_TuneCP5_13TeV-madgraphMLM-pythia8+"+campaign,86.58*1000*1.26), #LO *1.26
        #
        15: (dirT2+"VBFGamma_5f_TuneCP5_DipoleRecoil_13TeV-madgraph-pythia8+"+campaign,21.09*1000), #LO
        #
        20: (dirT2+"QCD_Pt-30to50_EMEnriched_TuneCP5_13TeV-pythia8+"+campaign,6447000.0*1000*1.26), #LO *1.26
        21: (dirT2+"QCD_Pt-50to80_EMEnriched_TuneCP5_13TeV-pythia8+"+campaign,1988000.0*1000*1.26), #LO *1.26
        22: (dirT2+"QCD_Pt-80to120_EMEnriched_TuneCP5_13TeV-pythia8+"+campaign,367500.0*1000*1.26), #LO *1.26
        23: (dirT2+"QCD_Pt-120to170_EMEnriched_TuneCP5_13TeV-pythia8+"+campaign,66590.0*1000*1.26), #LO *1.26
        24: (dirT2+"QCD_Pt-170to300_EMEnriched_TuneCP5_13TeV-pythia8+"+campaign,16620.0*1000*1.26), #LO *1.26
        25: (dirT2+"QCD_Pt-300toInf_EMEnriched_TuneCP5_13TeV-pythia8+"+campaign,1104.0*1000*1.26), #LO *1.26
        #
        31: (dirT2+"WJetsToLNu_0J_TuneCP5_13TeV-amcatnloFXFX-pythia8+"+campaign,53330.0*1000), #LO
        32: (dirT2+"WJetsToLNu_1J_TuneCP5_13TeV-amcatnloFXFX-pythia8+"+campaign,8875.0*1000), #LO
        33: (dirT2+"WJetsToLNu_2J_TuneCP5_13TeV-amcatnloFXFX-pythia8+"+campaign,3338.0*1000), #LO
        34: (dirT2+"DYJetsToLL_0J_TuneCP5_13TeV-amcatnloFXFX-pythia8+"+campaign,5129.0*1000), #LO
        35: (dirT2+"DYJetsToLL_1J_TuneCP5_13TeV-amcatnloFXFX-pythia8+"+campaign,951.5*1000), #LO
        36: (dirT2+"DYJetsToLL_2J_TuneCP5_13TeV-amcatnloFXFX-pythia8+"+campaign,361.4*1000), #LO
        #
        37: (dirT2+"Z1JetsToNuNu_M-50_LHEFilterPtZ-50To150_MatchEWPDG20_TuneCP5_13TeV-amcatnloFXFX-pythia8+"+campaign,579.9*1000),
        38: (dirT2+"Z1JetsToNuNu_M-50_LHEFilterPtZ-150To250_MatchEWPDG20_TuneCP5_13TeV-amcatnloFXFX-pythia8+"+campaign,17.42*1000),
        39: (dirT2+"Z1JetsToNuNu_M-50_LHEFilterPtZ-250To400_MatchEWPDG20_TuneCP5_13TeV-amcatnloFXFX-pythia8+"+campaign,1.987*1000),
        40: (dirT2+"Z1JetsToNuNu_M-50_LHEFilterPtZ-400ToInf_MatchEWPDG20_TuneCP5_13TeV-amcatnloFXFX-pythia8+"+campaign,0.2179*1000),
        41: (dirT2+"Z2JetsToNuNu_M-50_LHEFilterPtZ-50To150_MatchEWPDG20_TuneCP5_13TeV-amcatnloFXFX-pythia8+"+campaign,312.5*1000),
        42: (dirT2+"Z2JetsToNuNu_M-50_LHEFilterPtZ-150To250_MatchEWPDG20_TuneCP5_13TeV-amcatnloFXFX-pythia8+"+campaign,30*1000),
        43: (dirT2+"Z2JetsToNuNu_M-50_LHEFilterPtZ-250To400_MatchEWPDG20_TuneCP5_13TeV-amcatnloFXFX-pythia8+"+campaign,4.98*1000),
        44: (dirT2+"Z2JetsToNuNu_M-50_LHEFilterPtZ-400ToInf_MatchEWPDG20_TuneCP5_13TeV-amcatnloFXFX-pythia8+"+campaign,0.8165*1000),
        #
        45: (dirT2+"WGammaToJJGamma_TuneCP5_13TeV-amcatnloFXFX-pythia8+"+campaign,8.635*1000),
        46: (dirT2+"ZGammaToJJGamma_TuneCP5_13TeV-amcatnloFXFX-pythia8+"+campaign,4.144*1000),
        47: (dirT2+"TTGJets_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8+"+campaign,3.757*1000),
        48: (dirT2+"ZGTo2NuG_TuneCP5_13TeV-amcatnloFXFX-pythia8+"+campaign,30.11*1000),
    }
    return switch.get(argument, "BKGdefault, xsecDefault")


def pickTRG(overall,year,PDType,isVBF,isW,isZ,isZinv):

    TRIGGER=''
    if(year == 2018 and isVBF):
        if (PDType== "EGamma"): TRIGGER=getTriggerFromJson(overall, "isVBF", year)
        elif (PDType== "NULL"): TRIGGER=getTriggerFromJson(overall, "isVBF", year)     # MC seems the same
    if(year == 2018 and isZinv):
        if (PDType== "TAU"): TRIGGER=getTriggerFromJson(overall, "isZinv", year)
        elif (PDType== "NULL"): TRIGGER=getTriggerFromJson(overall, "isZinv", year)     # MC seems the same
    if(year == 2017 and isVBF and PDType== "SinglePhoton"): TRIGGER=getTriggerFromJson(overall, "isVBF", year)

    if(year == 2018 and (isW or isZ)):

        if(PDType == "MuonEG"): TRIGGER = "{0}".format(getTriggerFromJson(overall, "muEG", year))
        elif (PDType == "DoubleMuon"): TRIGGER = "{0} and not {1}".format(getTriggerFromJson(overall, "diMU", year),getTriggerFromJson(overall, "muEG", year))
        elif (PDType == "SingleMuon"): TRIGGER = "{0} and not {1} and not {2}".format(getTriggerFromJson(overall, "oneMU", year),getTriggerFromJson(overall, "diMU", year),getTriggerFromJson(overall, "muEG", year))
        elif (PDType == "EGamma"): TRIGGER = "({0} or {1}) and not {2} and not {3} and not {4}".format(getTriggerFromJson(overall, "oneEL", year),getTriggerFromJson(overall, "diEL", year),getTriggerFromJson(overall, "oneMU", year),getTriggerFromJson(overall, "diMU", year),getTriggerFromJson(overall, "muEG", year))
        elif(year == 2018):
            TRIGGER = "{0} or {1} or {2} or {3} or {4}".format(getTriggerFromJson(overall, "oneEL", year),getTriggerFromJson(overall, "diEL", year),getTriggerFromJson(overall, "oneMU", year),getTriggerFromJson(overall, "diMU", year),getTriggerFromJson(overall, "muEG", year))
        else:
            print("PROBLEM with triggers!!!")

    return TRIGGER


def computeWeigths(df, files, sampleNOW, year, isMC):

    nevents = df.Count().GetValue()
    print("%s entries in the dataset" %nevents)

    if not isMC:
        return 1.
    else:
        rdf = ROOT.RDataFrame("Runs", files)
        genEventSumWeight = rdf.Sum("genEventSumw").GetValue()
        genEventSumNoWeight = rdf.Sum("genEventCount").GetValue()

        ## this is what we want to do:    lum*xsec/sumGenWeight
        weight = (SwitchSample(sampleNOW,year)[1] / genEventSumWeight)
#        weightApprox = (SwitchSample(sampleNOW,year)[1] / genEventSumNoWeight)
#        print('weight',weight )
#        print('weightApprox',weightApprox)
        lumiEq = (genEventSumNoWeight / SwitchSample(sampleNOW,year)[1])
        print("lumi equivalent fb %s" %lumiEq)

        return weight

def plot(h,filename,doLogX,color):

   ROOT.gStyle.SetOptStat(1);
   ROOT.gStyle.SetTextFont(42)
   c = ROOT.TCanvas("c", "", 800, 700)
   if doLogX: c.SetLogx();
#  c.SetLogy()

   h.SetTitle("")
   h.GetXaxis().SetTitleSize(0.04)
   h.GetYaxis().SetTitleSize(0.04)
   h.SetLineColor(color)

   h.Draw()

   label = ROOT.TLatex(); label.SetNDC(True)
   label.DrawLatex(0.175, 0.740, "#eta")
   label.DrawLatex(0.205, 0.775, "#rho,#omega")
   label.DrawLatex(0.270, 0.740, "#phi")
   label.SetTextSize(0.040); label.DrawLatex(0.100, 0.920, "#bf{CMS Simulation}")
   label.SetTextSize(0.030); label.DrawLatex(0.630, 0.920, "#sqrt{s} = 13 TeV, L_{int} = X fb^{-1}")

   print("saving file: {} ".format(filename))

   c.SaveAs(filename)
