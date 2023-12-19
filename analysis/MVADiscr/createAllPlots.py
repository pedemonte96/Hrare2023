import ROOT
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
ROOT.ROOT.EnableImplicitMT()

colors = {"GREEN": "\033[1;36m", "BLUE": "\033[1;34m", "RED": "\033[1;31m", "NC": "\033[0m", "YELLOW": "\033[1;33m"}

cols = {"DeepMETResolutionTune_phi" : [-4, 4, False],
"DeepMETResolutionTune_pt" : [0, 100, False],
"HCandMass" : [0, 200, False],
"HCandPT" : [0, 200, False],
"PV_npvsGood" : [0, 50, False],
"SoftActivityJetNjets5" : [0, 10, False],
"classify" : [0, 6, False],
"dEtaGammaMesonCand" : [-1, 3, False],
"dPhiGammaMesonCand" : [0.5, 3.5, False],
"delta_eta_goodMeson_ditrk_goodPhoton" : [-4, 4, False],
"delta_phi_goodMeson_ditrk_goodPhoton" : [0, 6, False],
"goodMeson_DR" : [0.0, 0.1, False],
"goodMeson_Nphotons" : [0, 6, False],
"goodMeson_bestVtx_R" : [0, 1, False],
"goodMeson_bestVtx_X" : [-1, 1, False],
"goodMeson_bestVtx_Y" : [-1, 1, False],
"goodMeson_bestVtx_Z" : [-20, 20, False],
"goodMeson_bestVtx_idx" : [-1, 5, False],
"goodMeson_ditrk_mass" : [0, 1, False],
"goodMeson_ditrk_pt" : [0, 150, False],
"goodMeson_eta" : [-3, 3, False],
"goodMeson_iso" : [0.9, 1.01, True],
"goodMeson_leadtrk_pt" : [0, 150, False],
"goodMeson_mass" : [0, 2, False],
"goodMeson_massErr" : [0.0, 0.05, False],
"goodMeson_mass_raw" : [0, 2, False],
"goodMeson_phi" : [-4, 4, False],
"goodMeson_photon1_DR" : [0.0, 0.1, False],
"goodMeson_photon1_eta" : [-3, 3, False],
"goodMeson_photon1_phi" : [-4, 4, False],
"goodMeson_photon1_pt" : [0, 100, False],
"goodMeson_pt" : [0, 150, False],
"goodMeson_sipPV" : [0, 10, False],
"goodMeson_subleadtrk_pt" : [0, 80, False],
"goodMeson_trk1_eta" : [-3, 3, False],
"goodMeson_trk1_phi" : [-4, 4, False],
"goodMeson_trk1_pt" : [0, 100, False],
"goodMeson_trk2_eta" : [-3, 3, False],
"goodMeson_trk2_phi" : [-4, 4, False],
"goodMeson_trk2_pt" : [0, 100, False],
"goodMeson_vtx_chi2dof" : [0, 10, False],
"goodMeson_vtx_prob" : [0, 1, False],
"goodPhotons_energyErr" : [0, 8, False],
"goodPhotons_eta" : [-3, 3, False],
"goodPhotons_hoe" : [-0.001, 0.05, True],
"goodPhotons_mvaID" : [0, 1, False],
"goodPhotons_pfRelIso03_all" : [-0.001, 0.1, True],
"goodPhotons_phi" : [-4, 4, False],
"goodPhotons_pt" : [0, 150, False],
"goodPhotons_r9" : [0.85, 1.05, False],
"goodPhotons_sieie" : [0, 0.03, True],
"nGoodJets" : [0, 8, False],
"nPhoton" : [0, 6, False],
"sigmaHCandMass_Rel2" : [-0.00, 0.015, True],
"var0_input_pred" : [0, 4, False],
"var10_input_pred" : [0, 150, False],
"var11_input_pred" : [0, 1, False],
"var12_input_pred" : [1, 3, False],
"var13_input_pred" : [0.0, 0.02, False],
"var14_input_pred" : [0.0, 0.02, False],
"var1_input_pred" : [1, 3.0, False],
"var2_input_pred" : [0, 150, False],
"var3_input_pred" : [20, 200, False],
"var4_input_pred" : [0, 2, False],
"var5_input_pred" : [0, 8, False],
"var6_input_pred" : [0, 150, False],
"var7_input_pred" : [40, 200, False],
"var8_input_pred" : [0, 2, False],
"var9_input_pred" : [0, 150, False],
"phi_bestVtx_X" : [-1, 1, False],
"phi_bestVtx_Y" : [-1, 1, False],
"phi_bestVtx_Z" : [-10, 10, False],
"phi_ds_cosAlphaXY" : [-1, 1, True],
"phi_ds_eta" : [-3, 3, False],
"phi_ds_phi" : [-4, 4, True],
"phi_ds_pion_eta" : [-3, 3, True],
"phi_ds_pion_phi" : [-4, 4, True],
"phi_ds_pion_pt" : [-2, 10, True],
"phi_ds_pt" : [0, 50, True],
"phi_ds_sipBS" : [0, 80, False],
"phi_ds_sipPV" : [0, 10, False],
"phi_ds_slxy" : [-2, 4, True],
"phi_ds_vtx_chi2dof" : [-1, 5, True],
"phi_ds_vtx_prob" : [-1, 1, True],
"phi_iso" : [-0, 1, False],
"phi_isoNeuHad" : [0, 1, False],
"phi_isoPho" : [0, 1, False],
"phi_kin_cosAlphaXY" : [-1, 1, True],
"phi_kin_eta" : [-3, 3, False],
"phi_kin_lxy" : [0, 3, False],
"phi_kin_phi" : [-4, 4, False],
"phi_kin_pt" : [0, 50, False],
"phi_kin_sipBS" : [0, 80, False],
"phi_kin_sipPV" : [0, 10, False],
"phi_kin_slxy" : [-1, 10, False],
"phi_kin_vtx_chi2dof" : [0, 10, False],
"phi_kin_vtx_prob" : [0, 1, False],
"phi_mass" : [0.9, 1.2, False],
"phi_trk1_eta" : [-3, 3, False],
"phi_trk1_phi" : [-4, 4, False],
"phi_trk1_pt" : [0, 20, False],
"phi_trk1_sip" : [0, 8, False],
"phi_trk2_eta" : [-3, 3, False],
"phi_trk2_phi" : [-4, 4, False],
"phi_trk2_pt" : [0, 20, False],
"phi_trk2_sip" : [0, 8, False],
"phi_bestVtx_idx" : [0, 10, False],
"boostedTau_chargedIso" : [0, 8, True],
"boostedTau_eta" : [-3, 3, False],
"boostedTau_leadTkDeltaEta" : [-0.1, 0.1, False],
"boostedTau_leadTkDeltaPhi" : [-0.1, 0.1, False],
"boostedTau_leadTkPtOverTauPt" : [0, 1.2, False],
"boostedTau_mass" : [0, 2, False],
"boostedTau_neutralIso" : [0, 10, True],
"boostedTau_phi" : [-4, 4, False],
"boostedTau_photonsOutsideSignalCone" : [0, 10, True],
"boostedTau_pt" : [0, 150, False],
"boostedTau_puCorr" : [0, 80, False],
"boostedTau_rawIso" : [0, 10, True],
"boostedTau_rawIsodR03" : [0, 10, True],
"boostedTau_rawMVAnewDM2017v2" : [-1, 1, False],
"boostedTau_rawMVAoldDM2017v2" : [-1, 1, True],
"boostedTau_rawMVAoldDMdR032017v2" : [-1, 1, True],
"nTau" : [-1, 4, False],
"Tau_chargedIso" : [0, 8, True],
"Tau_dxy" : [-0.02, 0.02, False],
"Tau_dz" : [-0.04, 0.04, False],
"Tau_eta" : [-3, 3, False],
"Tau_leadTkDeltaEta" : [-0.06, 0.06, False],
"Tau_leadTkDeltaPhi" : [-0.06, 0.06, False],
"Tau_leadTkPtOverTauPt" : [0, 1.2, False],
"Tau_mass" : [0, 2, False],
"Tau_neutralIso" : [0, 10, True],
"Tau_phi" : [-4, 4, False],
"Tau_photonsOutsideSignalCone" : [0, 10, True],
"Tau_pt" : [0, 150, False],
"Tau_puCorr" : [0, 80, False],
"Tau_rawDeepTau2017v2p1VSe" : [0, 1, True],
"Tau_rawDeepTau2017v2p1VSjet" : [0, 1, False],
"Tau_rawDeepTau2017v2p1VSmu" : [0, 1, True],
"Tau_rawIso" : [0, 10, True],
"Tau_rawIsodR03" : [0, 10, True],
"Tau_decayMode" : [-2, 8, False],
"Tau_jetIdx" : [-2, 8, False],
"Tau_idDecayModeOldDMs" : [0, 2, False],
"CaloMET_phi" : [-4, 4, False],
"CaloMET_pt" : [0, 150, False],
"ChsMET_phi" : [-4, 4, False],
"ChsMET_pt" : [0, 150, False],
"nCorrT1METJet" : [0, 20, False],
"CorrT1METJet_area" : [0, 1, False],
"CorrT1METJet_eta" : [-3, 3, False],
"CorrT1METJet_phi" : [-4, 4, False],
"CorrT1METJet_rawPt" : [0, 40, False],
"DeepMETResponseTune_phi" : [-4, 4, False],
"DeepMETResponseTune_pt" : [0, 100, False],
"FsrPhoton_eta" : [-3, 3, False],
"FsrPhoton_phi" : [-4, 4, False],
"FsrPhoton_pt" : [0, 150, False],
"FsrPhoton_relIso03" : [0, 2, False],
"nIsoTrack" : [0, 10, False],
"IsoTrack_dxy" : [-3, 3, False],
"IsoTrack_dz" : [-20, 20, False],
"IsoTrack_eta" : [-3, 3, False],
"IsoTrack_pfRelIso03_all" : [0, 5, False],
"IsoTrack_pfRelIso03_chg" : [0, 0.3, False],
"IsoTrack_phi" : [-4, 4, False],
"IsoTrack_pt" : [0, 150, False],
"IsoTrack_miniPFRelIso_all" : [0, 5, False],
"IsoTrack_miniPFRelIso_chg" : [0, 0.3, False],
"MET_MetUnclustEnUpDeltaX" : [-20, 20, False],
"MET_MetUnclustEnUpDeltaY" : [-20, 20, False],
"MET_covXX" : [0, 1000, False],
"MET_covXY" : [-300, 300, False],
"MET_covYY" : [0, 1000, False],
"MET_phi" : [-4, 4, False],
"MET_pt" : [0, 150, False],
"MET_significance" : [0, 10, False],
"Photon_dEsigmaDown" : [-0.1, 0.1, False],
"Photon_dEsigmaUp" : [-0.1, 0.1, False],
"Photon_energyErr" : [0, 10, False],
"Photon_eta" : [-3, 3, False],
"Photon_hoe" : [0, 1, False],
"Photon_mvaID" : [-1, 1, True],
"Photon_mvaID_Fall17V1p1" : [-1, 1, True],
"Photon_pfRelIso03_all" : [0, 4, False],
"Photon_pfRelIso03_chg" : [0, 2, False],
"Photon_phi" : [-4, 4, False],
"Photon_r9" : [0, 2, True],
"Photon_sieie" : [0, 0.1, True],
"Photon_x_calo" : [-200, 200, False],
"Photon_y_calo" : [-200, 200, False],
"Photon_z_calo" : [-400, 400, False],
"Photon_cutBased" : [0, 4, False],
"Photon_jetIdx" : [-1, 10, False],
"Photon_isScEtaEB" : [0, 2, False],
"Photon_isScEtaEE" : [0, 2, False],
"Photon_pixelSeed" : [0, 2, False],
"Pileup_nTrueInt" : [0, 60, False],
"Pileup_nPU" : [0, 80, False],
"Pileup_sumEOOT" : [0, 1000, False],
"Pileup_sumLOOT" : [0, 200, False],
"PuppiMET_phi" : [-4, 4, False],
"PuppiMET_pt" : [0, 150, False],
"PuppiMET_sumEt" : [80, 1000, False],
"SoftActivityJet_eta" : [-3, 3, False],
"SoftActivityJet_phi" : [-4, 4, False],
"SoftActivityJet_pt" : [0, 70, False],
"SoftActivityJetHT" : [0, 200, False],
"SoftActivityJetHT10" : [0, 200, False],
"SoftActivityJetHT2" : [0, 200, False],
"SoftActivityJetHT5" : [0, 200, False],
"SoftActivityJetNjets10" : [0, 10, False],
"SoftActivityJetNjets2" : [0, 30, False],
"nSubJet" : [-10, 10, False],
"SubJet_eta" : [-3, 3, False],
"SubJet_mass" : [0, 10, False],
"SubJet_n2b1" : [-1, 1, True],
"SubJet_n3b1" : [-1, 5, True],
"SubJet_phi" : [-4, 4, False],
"SubJet_pt" : [0, 200, False],
"SubJet_tau1" : [0, 0.4, False],
"TkMET_phi" : [-4, 4, False],
"TkMET_pt" : [0, 150, False],
"TkMET_sumEt" : [40, 1000, False],
"nTrigObj" : [0, 12, False],
"TrigObj_pt" : [0, 200, False],
"TrigObj_eta" : [-3, 3, False],
"TrigObj_phi" : [-4, 4, False],
"TrigObj_l1pt" : [0, 200, False],
"OtherPV_z" : [-10, 10, False],
"PV_ndof" : [0, 300, False],
"PV_x" : [0.0, 0.02, False],
"PV_y" : [0.03, 0.055, False],
"PV_z" : [-10, 10, False],
"PV_chi2" : [0, 2, False],
"PV_score" : [0, 10000, False],
"PV_npvs" : [0, 50, False],
"nSV" : [-1, 10, False],
"SV_dlen" : [0, 20, False],
"SV_dlenSig" : [0, 20, False],
"SV_dxy" : [0, 6, False],
"SV_dxySig" : [0, 60, False],
"SV_pAngle" : [2.5, 3.2, False],
"SV_charge" : [-6, 6, False],
"SV_chi2" : [0, 10, False],
"SV_eta" : [-3, 3, False],
"SV_mass" : [0, 5, False],
"SV_ndof" : [-1, 10, False],
"SV_phi" : [-4, 4, False],
"SV_pt" : [0, 70, False],
"SV_x" : [-4, 4, False],
"SV_y" : [-4, 4, False],
"SV_z" : [-10, 10, False],
"SV_ntracks" : [0, 8, False]}


if "/home/submit/pdmonte/CMSSW_10_6_27/src/Hrare2023/analysis/func_marti.so" not in ROOT.gSystem.GetLibraries():
    ROOT.gSystem.CompileMacro("/home/submit/pdmonte/CMSSW_10_6_27/src/Hrare2023/analysis/func_marti.cc","k")

if "/home/submit/pdmonte/CMSSW_10_6_27/src/Hrare2023/analysis/functions.so" not in ROOT.gSystem.GetLibraries():
    ROOT.gSystem.CompileMacro("/home/submit/pdmonte/CMSSW_10_6_27/src/Hrare2023/analysis/functions.cc","k")


def getSgnBkgChains(channel, date):
    print(colors["RED"] + " Getting RDataFrames for {} ".format(channel).center(100, "~") + colors["NC"])
    if (channel == "omega"):
        cat, numMeson =  "OmegaCat", 1038
    elif (channel == "phi"):
        cat, numMeson =  "Phi3Cat", 1039
    elif (channel == "d0starrho"):
        cat, numMeson =  "D0StarRhoCat", 1040
    elif (channel == "d0star"):
        cat, numMeson =  "D0StarCat", 1041
    else:
        raise Exception("Wrong channel.")

    chainSGN = ROOT.TChain("events")
    chainBKG = ROOT.TChain("events")

    chainSGN.Add("/data/submit/pdmonte/outputs/{0}/2018/outname_mc{1}_GFcat_{2}_2018.root".format(date, numMeson, cat))
    chainBKG.Add("/data/submit/pdmonte/outputs/{0}/2018/outname_mc10_GFcat_{1}_2018.root".format(date, cat))
    chainBKG.Add("/data/submit/pdmonte/outputs/{0}/2018/outname_mc11_GFcat_{1}_2018.root".format(date, cat))
    chainBKG.Add("/data/submit/pdmonte/outputs/{0}/2018/outname_mc12_GFcat_{1}_2018.root".format(date, cat))
    chainBKG.Add("/data/submit/pdmonte/outputs/{0}/2018/outname_mc13_GFcat_{1}_2018.root".format(date, cat))
    chainBKG.Add("/data/submit/pdmonte/outputs/{0}/2018/outname_mc14_GFcat_{1}_2018.root".format(date, cat))

    print(colors["RED"] + " Done! ".center(100, "~") + colors["NC"] + "\n")

    return chainSGN, chainBKG


def plotHistogram(var, dfSGN, dfBKG, nbins=100, xlow=0, xhigh=100, doLog=False):
    print(colors["GREEN"] + " Plotting {} ".format(var).center(100, "~") + colors["NC"])
    canvas = ROOT.TCanvas("canvas", "canvas", 600, 600)

    hs = dfSGN.Histo1D(("hist", var, nbins, xlow, xhigh), var, "scale")
    hs.SetFillColorAlpha(ROOT.kGreen-9, 0.20)
    hs.SetLineColor(ROOT.kGreen+2)
    hs.SetLineWidth(2)
    hs.SetFillStyle(4050)

    hb = dfBKG.Histo1D(("hist", var, nbins, xlow, xhigh), var, "scale")
    hb.SetFillColorAlpha(ROOT.kRed-9, 0.20)
    hb.SetLineColor(ROOT.kRed+2)
    #hb.SetLineColor(ROOT.kBlue+2)
    hb.SetLineWidth(2)
    hb.SetFillStyle(4050)

    hb.Scale(1/hb.Integral())
    hs.Scale(1/hs.Integral())

    stack = ROOT.THStack("stack", var)
    stack.Add(hb.GetValue())
    stack.Add(hs.GetValue())
    stack.Draw("hist nostack")
    stack.GetYaxis().SetTitle("Frequency")

    print("Signal mean:     {:.3f}\t StdDev: {:.3f}".format(hs.GetMean(), hs.GetStdDev()))
    print("Background mean: {:.3f}\t StdDev: {:.3f}".format(hb.GetMean(), hb.GetStdDev()))
    text = ROOT.TLatex()
    text.SetNDC()
    text.SetTextSize(0.03)
    xSp1, xSp2, xSp3, xSp4 = 0.13, 0.22, 0.45, 0.69
    text.SetTextFont(62)
    text.DrawLatex(xSp1, 0.87, "SGN:")
    text.DrawLatex(xSp1, 0.84, "BKG:")
    text.SetTextFont(42)
    text.DrawLatex(xSp2, 0.87, "Mean: {:+.3f}".format(hs.GetMean()))
    text.DrawLatex(xSp3, 0.87, "StdDev: {:.3f}".format(hs.GetStdDev()))
    text.DrawLatex(xSp4, 0.87, "nEvents: {}".format(int(hs.GetEntries())))
    
    text.DrawLatex(xSp2, 0.84, "Mean: {:+.3f}".format(hb.GetMean()))
    text.DrawLatex(xSp3, 0.84, "StdDev: {:.3f}".format(hb.GetStdDev()))
    text.DrawLatex(xSp4, 0.84, "nEvents: {}".format(int(hb.GetEntries())))

    if doLog:
        canvas.SetLogy()
    canvas.SaveAs("/home/submit/pdmonte/public_html/MVA_plots/{}.png".format(var))
    print(colors["GREEN"] + " Done! ".center(100, "~") + colors["NC"] + "\n")
    return var, [hs.GetMean(), hb.GetMean(), hs.GetStdDev(), hb.GetStdDev()]


if __name__ == "__main__":
    means = {}
    date = "NOV05"
    chainsig, chainbkg = getSgnBkgChains("phi", date)

    dfs = ROOT.RDataFrame(chainsig)
    dfb = ROOT.RDataFrame(chainbkg)

    dfs = (dfs.Define("scale", "w*lumiIntegrated"))
    dfb = (dfb.Define("scale", "w*lumiIntegrated"))

    c = 0
    for column, range in cols.items():
        k, v = plotHistogram(column, dfs, dfb, xlow=range[0], xhigh=range[1], doLog=range[2])
        means[k] = v
        c += 1
        if c > 500:
            break

    print(colors["BLUE"] + " Sorted Signal mean ".center(100, "~") + colors["NC"] + "\n")
    for a in sorted(means.items(), key=lambda x:x[1][0]):
        print(a)

    print(colors["BLUE"] + " Sorted StdDev ".center(100, "~") + colors["NC"] + "\n")
    for a in sorted(means.items(), key=lambda x:(x[1][2] + x[1][3])/2.):
        print(a)

    print(colors["BLUE"] + " Sorted Diff Means ".center(100, "~") + colors["NC"] + "\n")
    for a in sorted(means.items(), key=lambda x:abs(x[1][0] - x[1][1])*2/(x[1][2] + x[1][3])):
        print(a)

    print(len(means))