import ROOT
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
ROOT.ROOT.EnableImplicitMT()

if "/home/submit/pdmonte/CMSSW_10_6_27/src/Hrare2023/analysis/func_marti.so" not in ROOT.gSystem.GetLibraries():
    ROOT.gSystem.CompileMacro("/home/submit/pdmonte/CMSSW_10_6_27/src/Hrare2023/analysis/func_marti.cc","k")

if "/home/submit/pdmonte/CMSSW_10_6_27/src/Hrare2023/analysis/functions.so" not in ROOT.gSystem.GetLibraries():
    ROOT.gSystem.CompileMacro("/home/submit/pdmonte/CMSSW_10_6_27/src/Hrare2023/analysis/functions.cc","k")

date = "JUN29"

chain = ROOT.TChain("events")
chain.Add("/data/submit/pdmonte/outputs/{0}/2018/outname_mc1039_GFcat_Phi3Cat_2018.root".format(date))
df_SGN = ROOT.RDataFrame(chain)

print("hello world!")

df_SGN = df_SGN.Define("scale", "w*lumiIntegrated")\
            .Define("goodMeson_ditrk_mass_GEN", "get2BodyPtEtaPhiM(GenPart_pt, GenPart_eta, GenPart_phi, GenPart_mass, GenPart_pdgId, GenPart_genPartIdxMother, -211, 211, 333, 25)[3]")\
            .Define("goodMeson_ditrk_eta_GEN", "get2BodyPtEtaPhiM(GenPart_pt, GenPart_eta, GenPart_phi, GenPart_mass, GenPart_pdgId, GenPart_genPartIdxMother, -211, 211, 333, 25)[1]")\
            .Define("goodMeson_ditrk_phi_GEN", "get2BodyPtEtaPhiM(GenPart_pt, GenPart_eta, GenPart_phi, GenPart_mass, GenPart_pdgId, GenPart_genPartIdxMother, -211, 211, 333, 25)[2]")\
            .Define("goodMeson_ditrk_pt_GEN", "get2BodyPtEtaPhiM(GenPart_pt, GenPart_eta, GenPart_phi, GenPart_mass, GenPart_pdgId, GenPart_genPartIdxMother, -211, 211, 333, 25)[0]")\
            .Define("goodMeson_leadtrk_pt_GEN", "getMaximum(getPt(GenPart_pt, GenPart_pdgId, GenPart_genPartIdxMother, 211, 333, 25), getPt(GenPart_pt, GenPart_pdgId, GenPart_genPartIdxMother, -211, 333, 25))")\
            .Define("goodMeson_subleadtrk_pt_GEN", "getMinimum(getPt(GenPart_pt, GenPart_pdgId, GenPart_genPartIdxMother, 211, 333, 25), getPt(GenPart_pt, GenPart_pdgId, GenPart_genPartIdxMother, -211, 333, 25))")\
            .Define("goodPhotons_pt_GEN", "getPt(GenPart_pt, GenPart_pdgId, GenPart_genPartIdxMother, 22, 25)")\
            .Define("goodMeson_DR_GEN", "getDR(GenPart_eta, GenPart_phi, GenPart_pdgId, GenPart_genPartIdxMother, -211, 333, 25, 211, 333, 25)")\
            .Define("goodMeson_mass_GEN", "get3BodyPtEtaPhiM(GenPart_pt, GenPart_eta, GenPart_phi, GenPart_mass, GenPart_pdgId, GenPart_genPartIdxMother, -211, 211, 111, 333, 25)[3]")\
            .Define("goodMeson_pt_GEN", "get3BodyPtEtaPhiM(GenPart_pt, GenPart_eta, GenPart_phi, GenPart_mass, GenPart_pdgId, GenPart_genPartIdxMother, -211, 211, 111, 333, 25)[0]")\
            .Define("HCandMass_GEN", "getHiggsPtEtaPhiM(GenPart_pt, GenPart_eta, GenPart_phi, GenPart_mass, GenPart_pdgId, GenPart_genPartIdxMother, 333, 25, 22, 25)[3]")\
            .Define("HCandMassMissing", "compute_HiggsVars_var(goodMeson_ditrk_pt[0],goodMeson_ditrk_eta[0],goodMeson_ditrk_phi[0],goodMeson_ditrk_mass[0],photon_pt,goodPhotons_eta[index_pair[1]],goodPhotons_phi[index_pair[1]],0)")\
            .Define("HCandMassMissing_GEN", "getHiggsPtEtaPhiMPhi3Ditrack(GenPart_pt, GenPart_eta, GenPart_phi, GenPart_mass, GenPart_pdgId, GenPart_genPartIdxMother)[3]")\
            .Define("goodMeson_ditrk_pt_sum", "sum2Body(goodMeson_trk1_pt[0], goodMeson_trk1_eta[0], goodMeson_trk1_phi[0], pi1_mass, goodMeson_trk2_pt[0], goodMeson_trk2_eta[0], goodMeson_trk2_phi[0], pi1_mass).Pt()")\
            .Define("goodMeson_ditrk_eta_sum", "sum2Body(goodMeson_trk1_pt[0], goodMeson_trk1_eta[0], goodMeson_trk1_phi[0], pi1_mass, goodMeson_trk2_pt[0], goodMeson_trk2_eta[0], goodMeson_trk2_phi[0], pi1_mass).Eta()")\
            .Define("goodMeson_ditrk_phi_sum", "sum2Body(goodMeson_trk1_pt[0], goodMeson_trk1_eta[0], goodMeson_trk1_phi[0], pi1_mass, goodMeson_trk2_pt[0], goodMeson_trk2_eta[0], goodMeson_trk2_phi[0], pi1_mass).Phi()")\
            .Define("goodMeson_ditrk_mass_sum", "sum2Body(goodMeson_trk1_pt[0], goodMeson_trk1_eta[0], goodMeson_trk1_phi[0], pi1_mass, goodMeson_trk2_pt[0], goodMeson_trk2_eta[0], goodMeson_trk2_phi[0], pi1_mass).M()")\
            .Define("Diff_pt_original", "(goodMeson_ditrk_pt[0]-goodMeson_ditrk_pt_GEN)/goodMeson_ditrk_pt_GEN")\
            .Define("Diff_pt_sum", "(goodMeson_ditrk_pt_sum-goodMeson_ditrk_pt_GEN)/goodMeson_ditrk_pt_GEN")\
            .Define("Diff_eta_original", "(goodMeson_ditrk_eta[0]-goodMeson_ditrk_eta_GEN)/goodMeson_ditrk_eta_GEN")\
            .Define("Diff_eta_sum",     "(goodMeson_ditrk_eta_sum-goodMeson_ditrk_eta_GEN)/goodMeson_ditrk_eta_GEN")\
            .Define("Diff_phi_original", "(goodMeson_ditrk_phi[0]-goodMeson_ditrk_phi_GEN)/goodMeson_ditrk_phi_GEN")\
            .Define("Diff_phi_sum",     "(goodMeson_ditrk_phi_sum-goodMeson_ditrk_phi_GEN)/goodMeson_ditrk_phi_GEN")\
            .Define("Diff_mass_original", "(goodMeson_ditrk_mass[0]-goodMeson_ditrk_mass_GEN)/goodMeson_ditrk_mass_GEN")\
            .Define("Diff_mass_sum",     "(goodMeson_ditrk_mass_sum-goodMeson_ditrk_mass_GEN)/goodMeson_ditrk_mass_GEN")

cols = ["GenPart_pdgId", "GenPart_genPartIdxMother", "GenPart_pt", "GenPart_mass", "GenPart_eta", "GenPart_phi", "goodMeson_ditrk_mass_GEN", "goodMeson_ditrk_pt_GEN", "goodMeson_ditrk_eta_GEN", "goodMeson_ditrk_phi_GEN"]
x = df_SGN.AsNumpy(columns=cols)
pddf = pd.DataFrame(x)

print(pddf[pddf["goodMeson_ditrk_mass_GEN"] < 0.2])