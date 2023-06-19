import ROOT
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#from collections import Counter
#import tqdm
ROOT.ROOT.EnableImplicitMT()

if "/home/submit/pdmonte/CMSSW_10_6_27/src/Hrare2023/analysis/func_marti.so" not in ROOT.gSystem.GetLibraries():
    ROOT.gSystem.CompileMacro("/home/submit/pdmonte/CMSSW_10_6_27/src/Hrare2023/analysis/func_marti.cc","k")

date = "MAY31"

chainSGN = ROOT.TChain("events")
#chainSGN.Add("/data/submit/pdmonte/outputs/{0}/2018/outname_mc1040_GFcat_Phi3Cat_2018.root".format(date))
chainSGN.Add("/data/submit/pdmonte/outputs/{0}/2018/outname_mc1039_GFcat_D0StarCat_2018.root".format(date))

df = ROOT.RDataFrame(chainSGN)

df = df.Define("D0GenPT", "getPt(GenPart_pt, GenPart_pdgId, GenPart_genPartIdxMother, 421, 423, 25)[0]")\
    .Define("D0GenPhi", "getEtaPhi(GenPart_eta, GenPart_phi, GenPart_pdgId, GenPart_genPartIdxMother, 421, 423, 25)[1]")\
    .Define("D0GenEta", "getEtaPhi(GenPart_eta, GenPart_phi, GenPart_pdgId, GenPart_genPartIdxMother, 421, 423, 25)[0]")\
    .Define("size", "goodMeson_pt.size()")


dfnew = df.Filter("size  == 2").Define("goodMesonImproved", "getFilteredGoodMeson(goodMeson, goodMeson_pt, goodMeson_vtx_prob)")

colsDiff = ["goodMeson", "goodMeson_pt", "goodMeson_eta", "goodMeson_phi", "goodMeson_iso", "goodMeson_mass",\
            "goodMeson_vtx_chi2dof", "goodMeson_vtx_prob", "goodMeson_sipPV", "goodMeson_bestVtx_X",\
           "goodMeson_bestVtx_Y", "goodMeson_bestVtx_Z", "goodMeson_trk1_pt", "goodMeson_trk2_pt",\
           "goodMeson_leadtrk_pt", "goodMeson_subleadtrk_pt", "goodMeson_threemass"]

colsDiff = ["goodMeson", "goodMesonImproved", "goodMeson_pt", "goodMeson_vtx_prob"]

cols = ["D0GenPT", "D0GenPhi", "D0GenEta"] + colsDiff

x = dfnew.AsNumpy(columns=cols)

pddf = pd.DataFrame(x)

print(pddf.head())
