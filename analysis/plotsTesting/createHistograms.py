import ROOT
ROOT.ROOT.EnableImplicitMT()

if "/home/submit/pdmonte/CMSSW_10_6_27/src/Hrare2023/analysis/func_marti.so" not in ROOT.gSystem.GetLibraries():
    ROOT.gSystem.CompileMacro("/home/submit/pdmonte/CMSSW_10_6_27/src/Hrare2023/analysis/func_marti.cc","k")

if "/home/submit/pdmonte/CMSSW_10_6_27/src/Hrare2023/analysis/functions.so" not in ROOT.gSystem.GetLibraries():
    ROOT.gSystem.CompileMacro("/home/submit/pdmonte/CMSSW_10_6_27/src/Hrare2023/analysis/functions.cc","k")

numDict = {"Background": [10, 11, 12, 13, 14], "OmegaCat": [1038], "Phi3Cat": [1039], "D0StarRhoCat": [1040], "D0StarCat": [1041]}

mesonLatex = {"OmegaCat": "#omega", "Phi3Cat": "#phi", "D0StarRhoCat": "D^{0*} (#rho)", "D0StarCat": "D^{0*}"}

variableNames = {"goodMeson_ditrk_mass": ["ditrack mass", "m [GeV]"],
                 "goodMeson_mass": ["full mass", "m [GeV]"],
                 "goodMeson_ditrk_pt": ["ditrack p_{T}", "p_{T} [GeV]"],
                 "goodMeson_pt": ["full p_{T}", "p_{T} [GeV]"],
                 "goodMeson_leadtrk_pt": ["leading track p_{T}", "p_{T} [GeV]"],
                 "goodMeson_subleadtrk_pt": ["subleading track p_{T}", "p_{T} [GeV]"],
                 "goodPhotons_pt": ["photon from H p_{T}", "p_{T} [GeV]"],
                 "goodMeson_DR": ["DR of ditrack", "DR [rad]"],
                 "HCandMass": ["H Cand mass", "m [GeV]"],
                 "HCandMassMissing": ["H Cand mass missing #gamma/#pi^{0}", "m [GeV]"]}


def getHistogram(nbins, xlow, xhigh, df, mesonCat, variable, level):
    print("[getHistogram] ------------------------Creating histogram {} {} {}-----------------------".format(mesonCat, variable, level))
    title = mesonLatex[mesonCat] + ": " + variableNames[variable][0] + ", " + level
    xAxisTitle = variableNames[variable][1]
    yAxisTitle = "Events/(" + str((xhigh - xlow)/nbins) + " " + variableNames[variable][1].split('[')[1].split(']')[0] + ")"

    extendedVariable = variable if level == "RECO" else variable + "_" + level

    #h = df.Define("good", "{0}[{0}>0]".format(extendedVariable)).Histo1D(("hist", title, nbins, xlow, xhigh), "good", "scale")

    if (level == "RECO"):
        if (variable == "HCandMass" or variable == "HCandMassMissing"):
            h = df.Filter("{0}>0".format(extendedVariable)).Histo1D(("hist", title, nbins, xlow, xhigh), extendedVariable, "scale")
        else:
            h = df.Define("good", "{0}[{0}>0]".format(extendedVariable)).Histo1D(("hist", title, nbins, xlow, xhigh), "good", "scale")
        h.SetFillColor(ROOT.kGreen-9)
    elif (level == "GEN"):
        h = df.Histo1D(("hist", title, nbins, xlow, xhigh), extendedVariable, "scale")
        h.SetFillColor(ROOT.kBlue-9)
    else:
        print("ERROR!")
        return
    h.SetLineColor(ROOT.kBlack)
    h.GetXaxis().SetTitle(xAxisTitle)
    h.GetYaxis().SetTitle(yAxisTitle)
    print("[getHistogram] ------------------------Histogram created!-----------------------")
    return ROOT.TH1D(h.GetValue())


if __name__ == "__main__":

    cat = "GFcat"
    year = 2018
    date = "JUN21"
    

    #D0Star----------------------------------------------------------------------------------------
    mesonCat = "D0StarCat"
    histograms = []
    numRows = 10
    height = numRows * 800
    cs_D0Star = ROOT.TCanvas("canvas_D0Star", "canvas", 2200, height)
    cs_D0Star.Divide(2, numRows)
    chain = ROOT.TChain("events")
    for num in numDict[mesonCat]:
        chain.Add("/data/submit/pdmonte/outputs/{}/{}/outname_mc{}_{}_{}_{}.root".format(date, year, num, cat, mesonCat, year))
    df_D0Star = ROOT.RDataFrame(chain)

    df_D0Star = df_D0Star.Define("scale", "w*lumiIntegrated")\
        .Define("goodMeson_ditrk_mass_GEN", "get2BodyPtEtaPhiM(GenPart_pt, GenPart_eta, GenPart_phi, GenPart_mass, GenPart_pdgId, GenPart_genPartIdxMother, -321, 211, 421, 423, 25)[3]")\
        .Define("goodMeson_ditrk_pt_GEN", "get2BodyPtEtaPhiM(GenPart_pt, GenPart_eta, GenPart_phi, GenPart_mass, GenPart_pdgId, GenPart_genPartIdxMother, -321, 211, 421, 423, 25)[0]")\
        .Define("goodMeson_leadtrk_pt_GEN", "getMaximum(getPt(GenPart_pt, GenPart_pdgId, GenPart_genPartIdxMother, -321, 421, 423, 25), getPt(GenPart_pt, GenPart_pdgId, GenPart_genPartIdxMother, 211, 421, 423, 25))")\
        .Define("goodMeson_subleadtrk_pt_GEN", "getMinimum(getPt(GenPart_pt, GenPart_pdgId, GenPart_genPartIdxMother, -321, 421, 423, 25), getPt(GenPart_pt, GenPart_pdgId, GenPart_genPartIdxMother, 211, 421, 423, 25))")\
        .Define("goodPhotons_pt_GEN", "getPt(GenPart_pt, GenPart_pdgId, GenPart_genPartIdxMother, 22, 25)")\
        .Define("goodMeson_DR_GEN", "getDR(GenPart_eta, GenPart_phi, GenPart_pdgId, GenPart_genPartIdxMother, -321, 421, 423, 25, 211, 421, 423, 25)")\
        .Define("goodMeson_mass_GEN", "getD0StarPtEtaPhiM(GenPart_pt, GenPart_eta, GenPart_phi, GenPart_mass, GenPart_pdgId, GenPart_genPartIdxMother)[3]")\
        .Define("goodMeson_pt_GEN", "getD0StarPtEtaPhiM(GenPart_pt, GenPart_eta, GenPart_phi, GenPart_mass, GenPart_pdgId, GenPart_genPartIdxMother)[0]")\
        .Define("HCandMass_GEN", "getHiggsPtEtaPhiM(GenPart_pt, GenPart_eta, GenPart_phi, GenPart_mass, GenPart_pdgId, GenPart_genPartIdxMother, 423, 25, 22, 25)[3]")\
        .Define("HCandMassMissing", "compute_HiggsVars_var(goodMeson_ditrk_pt[0],goodMeson_ditrk_eta[0],goodMeson_ditrk_phi[0],goodMeson_ditrk_mass[0],photon_pt,goodPhotons_eta[index_pair[1]],goodPhotons_phi[index_pair[1]],0)")\
        .Define("HCandMassMissing_GEN", "getHiggsPtEtaPhiMD0StarDitrack(GenPart_pt, GenPart_eta, GenPart_phi, GenPart_mass, GenPart_pdgId, GenPart_genPartIdxMother)[3]")


    nbins, xlow, xhigh = 200, 1.6, 2.1
    histograms.append(getHistogram(nbins, xlow, xhigh, df_D0Star, mesonCat, "goodMeson_ditrk_mass", "RECO"))
    p = cs_D0Star.cd(len(histograms))
    histograms[-1].Draw("hist")
    histograms.append(getHistogram(nbins, xlow, xhigh, df_D0Star, mesonCat, "goodMeson_ditrk_mass", "GEN"))
    p = cs_D0Star.cd(len(histograms))
    histograms[-1].Draw("hist")

    nbins, xlow, xhigh = 200, 0., 200.
    histograms.append(getHistogram(nbins, xlow, xhigh, df_D0Star, mesonCat, "goodMeson_ditrk_pt", "RECO"))
    p = cs_D0Star.cd(len(histograms))
    histograms[-1].Draw("hist")
    histograms.append(getHistogram(nbins, xlow, xhigh, df_D0Star, mesonCat, "goodMeson_ditrk_pt", "GEN"))
    p = cs_D0Star.cd(len(histograms))
    histograms[-1].Draw("hist")

    nbins, xlow, xhigh = 200, 0., 100.
    histograms.append(getHistogram(nbins, xlow, xhigh, df_D0Star, mesonCat, "goodMeson_leadtrk_pt", "RECO"))
    p = cs_D0Star.cd(len(histograms))
    histograms[-1].Draw("hist")
    histograms.append(getHistogram(nbins, xlow, xhigh, df_D0Star, mesonCat, "goodMeson_leadtrk_pt", "GEN"))
    p = cs_D0Star.cd(len(histograms))
    histograms[-1].Draw("hist")

    nbins, xlow, xhigh = 200, 0., 100.
    histograms.append(getHistogram(nbins, xlow, xhigh, df_D0Star, mesonCat, "goodMeson_subleadtrk_pt", "RECO"))
    p = cs_D0Star.cd(len(histograms))
    histograms[-1].Draw("hist")
    histograms.append(getHistogram(nbins, xlow, xhigh, df_D0Star, mesonCat, "goodMeson_subleadtrk_pt", "GEN"))
    p = cs_D0Star.cd(len(histograms))
    histograms[-1].Draw("hist")

    nbins, xlow, xhigh = 200, 0., 200.
    histograms.append(getHistogram(nbins, xlow, xhigh, df_D0Star, mesonCat, "goodPhotons_pt", "RECO"))
    p = cs_D0Star.cd(len(histograms))
    histograms[-1].Draw("hist")
    histograms.append(getHistogram(nbins, xlow, xhigh, df_D0Star, mesonCat, "goodPhotons_pt", "GEN"))
    p = cs_D0Star.cd(len(histograms))
    histograms[-1].Draw("hist")

    nbins, xlow, xhigh = 200, 0., 0.2
    histograms.append(getHistogram(nbins, xlow, xhigh, df_D0Star, mesonCat, "goodMeson_DR", "RECO"))
    p = cs_D0Star.cd(len(histograms))
    histograms[-1].Draw("hist")
    histograms.append(getHistogram(nbins, xlow, xhigh, df_D0Star, mesonCat, "goodMeson_DR", "GEN"))
    p = cs_D0Star.cd(len(histograms))
    histograms[-1].Draw("hist")

    nbins, xlow, xhigh = 200, 1.85, 2.15
    histograms.append(getHistogram(nbins, xlow, xhigh, df_D0Star, mesonCat, "goodMeson_mass", "RECO"))
    p = cs_D0Star.cd(len(histograms))
    histograms[-1].Draw("hist")
    histograms.append(getHistogram(nbins, xlow, xhigh, df_D0Star, mesonCat, "goodMeson_mass", "GEN"))
    p = cs_D0Star.cd(len(histograms))
    histograms[-1].Draw("hist")

    nbins, xlow, xhigh = 200, 0., 200.
    histograms.append(getHistogram(nbins, xlow, xhigh, df_D0Star, mesonCat, "goodMeson_pt", "RECO"))
    p = cs_D0Star.cd(len(histograms))
    histograms[-1].Draw("hist")
    histograms.append(getHistogram(nbins, xlow, xhigh, df_D0Star, mesonCat, "goodMeson_pt", "GEN"))
    p = cs_D0Star.cd(len(histograms))
    histograms[-1].Draw("hist")

    nbins, xlow, xhigh = 200, 105, 145
    histograms.append(getHistogram(nbins, xlow, xhigh, df_D0Star, mesonCat, "HCandMass", "RECO"))
    p = cs_D0Star.cd(len(histograms))
    histograms[-1].Draw("hist")
    histograms.append(getHistogram(nbins, xlow, xhigh, df_D0Star, mesonCat, "HCandMass", "GEN"))
    p = cs_D0Star.cd(len(histograms))
    histograms[-1].Draw("hist")

    nbins, xlow, xhigh = 200, 105, 145
    histograms.append(getHistogram(nbins, xlow, xhigh, df_D0Star, mesonCat, "HCandMassMissing", "RECO"))
    p = cs_D0Star.cd(len(histograms))
    histograms[-1].Draw("hist")
    histograms.append(getHistogram(nbins, xlow, xhigh, df_D0Star, mesonCat, "HCandMassMissing", "GEN"))
    p = cs_D0Star.cd(len(histograms))
    histograms[-1].Draw("hist")

    cs_D0Star.SaveAs("~/public_html/D0Star_RECO_vs_GEN.png")


    #Phi3----------------------------------------------------------------------------------------
    mesonCat = "Phi3Cat"
    histograms = []
    numRows = 10
    height = numRows * 800
    cs_Phi3 = ROOT.TCanvas("canvas_Phi3", "canvas", 2200, height)
    cs_Phi3.Divide(2, numRows)
    chain = ROOT.TChain("events")
    for num in numDict[mesonCat]:
        chain.Add("/data/submit/pdmonte/outputs/{}/{}/outname_mc{}_{}_{}_{}.root".format(date, year, num, cat, mesonCat, year))
    df_Phi3 = ROOT.RDataFrame(chain)

    df_Phi3 = df_Phi3.Define("scale", "w*lumiIntegrated")\
        .Define("goodMeson_ditrk_mass_GEN", "get2BodyPtEtaPhiM(GenPart_pt, GenPart_eta, GenPart_phi, GenPart_mass, GenPart_pdgId, GenPart_genPartIdxMother, -211, 211, 333, 25)[3]")\
        .Define("goodMeson_ditrk_pt_GEN", "get2BodyPtEtaPhiM(GenPart_pt, GenPart_eta, GenPart_phi, GenPart_mass, GenPart_pdgId, GenPart_genPartIdxMother, -211, 211, 333, 25)[0]")\
        .Define("goodMeson_leadtrk_pt_GEN", "getMaximum(getPt(GenPart_pt, GenPart_pdgId, GenPart_genPartIdxMother, 211, 333, 25), getPt(GenPart_pt, GenPart_pdgId, GenPart_genPartIdxMother, -211, 333, 25))")\
        .Define("goodMeson_subleadtrk_pt_GEN", "getMinimum(getPt(GenPart_pt, GenPart_pdgId, GenPart_genPartIdxMother, 211, 333, 25), getPt(GenPart_pt, GenPart_pdgId, GenPart_genPartIdxMother, -211, 333, 25))")\
        .Define("goodPhotons_pt_GEN", "getPt(GenPart_pt, GenPart_pdgId, GenPart_genPartIdxMother, 22, 25)")\
        .Define("goodMeson_DR_GEN", "getDR(GenPart_eta, GenPart_phi, GenPart_pdgId, GenPart_genPartIdxMother, -211, 333, 25, 211, 333, 25)")\
        .Define("goodMeson_mass_GEN", "get3BodyPtEtaPhiM(GenPart_pt, GenPart_eta, GenPart_phi, GenPart_mass, GenPart_pdgId, GenPart_genPartIdxMother, -211, 211, 111, 333, 25)[3]")\
        .Define("goodMeson_pt_GEN", "get3BodyPtEtaPhiM(GenPart_pt, GenPart_eta, GenPart_phi, GenPart_mass, GenPart_pdgId, GenPart_genPartIdxMother, -211, 211, 111, 333, 25)[0]")\
        .Define("HCandMass_GEN", "getHiggsPtEtaPhiM(GenPart_pt, GenPart_eta, GenPart_phi, GenPart_mass, GenPart_pdgId, GenPart_genPartIdxMother, 333, 25, 22, 25)[3]")\
        .Define("HCandMassMissing", "compute_HiggsVars_var(goodMeson_ditrk_pt[0],goodMeson_ditrk_eta[0],goodMeson_ditrk_phi[0],goodMeson_ditrk_mass[0],photon_pt,goodPhotons_eta[index_pair[1]],goodPhotons_phi[index_pair[1]],0)")\
        .Define("HCandMassMissing_GEN", "getHiggsPtEtaPhiMPhi3Ditrack(GenPart_pt, GenPart_eta, GenPart_phi, GenPart_mass, GenPart_pdgId, GenPart_genPartIdxMother)[3]")
    

    nbins, xlow, xhigh = 200, 0., 1.4
    histograms.append(getHistogram(nbins, xlow, xhigh, df_Phi3, mesonCat, "goodMeson_ditrk_mass", "RECO"))
    p = cs_Phi3.cd(len(histograms))
    histograms[-1].Draw("hist")
    histograms.append(getHistogram(nbins, xlow, xhigh, df_Phi3, mesonCat, "goodMeson_ditrk_mass", "GEN"))
    p = cs_Phi3.cd(len(histograms))
    histograms[-1].Draw("hist")

    nbins, xlow, xhigh = 200, 0., 200.
    histograms.append(getHistogram(nbins, xlow, xhigh, df_Phi3, mesonCat, "goodMeson_ditrk_pt", "RECO"))
    p = cs_Phi3.cd(len(histograms))
    histograms[-1].Draw("hist")
    histograms.append(getHistogram(nbins, xlow, xhigh, df_Phi3, mesonCat, "goodMeson_ditrk_pt", "GEN"))
    p = cs_Phi3.cd(len(histograms))
    histograms[-1].Draw("hist")

    nbins, xlow, xhigh = 200, 0., 100.
    histograms.append(getHistogram(nbins, xlow, xhigh, df_Phi3, mesonCat, "goodMeson_leadtrk_pt", "RECO"))
    p = cs_Phi3.cd(len(histograms))
    histograms[-1].Draw("hist")
    histograms.append(getHistogram(nbins, xlow, xhigh, df_Phi3, mesonCat, "goodMeson_leadtrk_pt", "GEN"))
    p = cs_Phi3.cd(len(histograms))
    histograms[-1].Draw("hist")

    nbins, xlow, xhigh = 200, 0., 100.
    histograms.append(getHistogram(nbins, xlow, xhigh, df_Phi3, mesonCat, "goodMeson_subleadtrk_pt", "RECO"))
    p = cs_Phi3.cd(len(histograms))
    histograms[-1].Draw("hist")
    histograms.append(getHistogram(nbins, xlow, xhigh, df_Phi3, mesonCat, "goodMeson_subleadtrk_pt", "GEN"))
    p = cs_Phi3.cd(len(histograms))
    histograms[-1].Draw("hist")

    nbins, xlow, xhigh = 200, 0., 200.
    histograms.append(getHistogram(nbins, xlow, xhigh, df_Phi3, mesonCat, "goodPhotons_pt", "RECO"))
    p = cs_Phi3.cd(len(histograms))
    histograms[-1].Draw("hist")
    histograms.append(getHistogram(nbins, xlow, xhigh, df_Phi3, mesonCat, "goodPhotons_pt", "GEN"))
    p = cs_Phi3.cd(len(histograms))
    histograms[-1].Draw("hist")

    nbins, xlow, xhigh = 200, 0., 0.2
    histograms.append(getHistogram(nbins, xlow, xhigh, df_Phi3, mesonCat, "goodMeson_DR", "RECO"))
    p = cs_Phi3.cd(len(histograms))
    histograms[-1].Draw("hist")
    histograms.append(getHistogram(nbins, xlow, xhigh, df_Phi3, mesonCat, "goodMeson_DR", "GEN"))
    p = cs_Phi3.cd(len(histograms))
    histograms[-1].Draw("hist")

    nbins, xlow, xhigh = 200, 0.6, 1.4
    histograms.append(getHistogram(nbins, xlow, xhigh, df_Phi3, mesonCat, "goodMeson_mass", "RECO"))
    p = cs_Phi3.cd(len(histograms))
    histograms[-1].Draw("hist")
    histograms.append(getHistogram(nbins, xlow, xhigh, df_Phi3, mesonCat, "goodMeson_mass", "GEN"))
    p = cs_Phi3.cd(len(histograms))
    histograms[-1].Draw("hist")

    nbins, xlow, xhigh = 200, 0., 200.
    histograms.append(getHistogram(nbins, xlow, xhigh, df_Phi3, mesonCat, "goodMeson_pt", "RECO"))
    p = cs_Phi3.cd(len(histograms))
    histograms[-1].Draw("hist")
    histograms.append(getHistogram(nbins, xlow, xhigh, df_Phi3, mesonCat, "goodMeson_pt", "GEN"))
    p = cs_Phi3.cd(len(histograms))
    histograms[-1].Draw("hist")

    nbins, xlow, xhigh = 200, 105, 145
    histograms.append(getHistogram(nbins, xlow, xhigh, df_Phi3, mesonCat, "HCandMass", "RECO"))
    p = cs_Phi3.cd(len(histograms))
    histograms[-1].Draw("hist")
    histograms.append(getHistogram(nbins, xlow, xhigh, df_Phi3, mesonCat, "HCandMass", "GEN"))
    p = cs_Phi3.cd(len(histograms))
    histograms[-1].Draw("hist")

    nbins, xlow, xhigh = 200, 50., 140
    histograms.append(getHistogram(nbins, xlow, xhigh, df_Phi3, mesonCat, "HCandMassMissing", "RECO"))
    p = cs_Phi3.cd(len(histograms))
    histograms[-1].Draw("hist")
    histograms.append(getHistogram(nbins, xlow, xhigh, df_Phi3, mesonCat, "HCandMassMissing", "GEN"))
    p = cs_Phi3.cd(len(histograms))
    histograms[-1].Draw("hist")

    cs_Phi3.SaveAs("~/public_html/Phi3_RECO_vs_GEN.png")


    #Omega----------------------------------------------------------------------------------------
    mesonCat = "OmegaCat"
    histograms = []
    numRows = 10
    height = numRows * 800
    cs_Omega = ROOT.TCanvas("canvas_Omega", "canvas", 2200, height)
    cs_Omega.Divide(2, numRows)
    chain = ROOT.TChain("events")
    for num in numDict[mesonCat]:
        chain.Add("/data/submit/pdmonte/outputs/{}/{}/outname_mc{}_{}_{}_{}.root".format(date, year, num, cat, mesonCat, year))
    df_Omega = ROOT.RDataFrame(chain)

    df_Omega = df_Omega.Define("scale", "w*lumiIntegrated")\
        .Define("goodMeson_ditrk_mass_GEN", "get2BodyPtEtaPhiM(GenPart_pt, GenPart_eta, GenPart_phi, GenPart_mass, GenPart_pdgId, GenPart_genPartIdxMother, -211, 211, 223, 25)[3]")\
        .Define("goodMeson_ditrk_pt_GEN", "get2BodyPtEtaPhiM(GenPart_pt, GenPart_eta, GenPart_phi, GenPart_mass, GenPart_pdgId, GenPart_genPartIdxMother, -211, 211, 223, 25)[0]")\
        .Define("goodMeson_leadtrk_pt_GEN", "getMaximum(getPt(GenPart_pt, GenPart_pdgId, GenPart_genPartIdxMother, 211, 223, 25), getPt(GenPart_pt, GenPart_pdgId, GenPart_genPartIdxMother, -211, 223, 25))")\
        .Define("goodMeson_subleadtrk_pt_GEN", "getMinimum(getPt(GenPart_pt, GenPart_pdgId, GenPart_genPartIdxMother, 211, 223, 25), getPt(GenPart_pt, GenPart_pdgId, GenPart_genPartIdxMother, -211, 223, 25))")\
        .Define("goodPhotons_pt_GEN", "getPt(GenPart_pt, GenPart_pdgId, GenPart_genPartIdxMother, 22, 25)")\
        .Define("goodMeson_DR_GEN", "getDR(GenPart_eta, GenPart_phi, GenPart_pdgId, GenPart_genPartIdxMother, -211, 223, 25, 211, 223, 25)")\
        .Define("goodMeson_mass_GEN", "get3BodyPtEtaPhiM(GenPart_pt, GenPart_eta, GenPart_phi, GenPart_mass, GenPart_pdgId, GenPart_genPartIdxMother, -211, 211, 111, 223, 25)[3]")\
        .Define("goodMeson_pt_GEN", "get3BodyPtEtaPhiM(GenPart_pt, GenPart_eta, GenPart_phi, GenPart_mass, GenPart_pdgId, GenPart_genPartIdxMother, -211, 211, 111, 223, 25)[0]")\
        .Define("HCandMass_GEN", "getHiggsPtEtaPhiM(GenPart_pt, GenPart_eta, GenPart_phi, GenPart_mass, GenPart_pdgId, GenPart_genPartIdxMother, 223, 25, 22, 25)[3]")\
        .Define("HCandMassMissing", "compute_HiggsVars_var(goodMeson_ditrk_pt[0],goodMeson_ditrk_eta[0],goodMeson_ditrk_phi[0],goodMeson_ditrk_mass[0],photon_pt,goodPhotons_eta[index_pair[1]],goodPhotons_phi[index_pair[1]],0)")\
        .Define("HCandMassMissing_GEN", "getHiggsPtEtaPhiMOmegaDitrack(GenPart_pt, GenPart_eta, GenPart_phi, GenPart_mass, GenPart_pdgId, GenPart_genPartIdxMother)[3]")
    

    nbins, xlow, xhigh = 200, 0., 1.4
    histograms.append(getHistogram(nbins, xlow, xhigh, df_Omega, mesonCat, "goodMeson_ditrk_mass", "RECO"))
    p = cs_Omega.cd(len(histograms))
    histograms[-1].Draw("hist")
    histograms.append(getHistogram(nbins, xlow, xhigh, df_Omega, mesonCat, "goodMeson_ditrk_mass", "GEN"))
    p = cs_Omega.cd(len(histograms))
    histograms[-1].Draw("hist")

    nbins, xlow, xhigh = 200, 0., 200.
    histograms.append(getHistogram(nbins, xlow, xhigh, df_Omega, mesonCat, "goodMeson_ditrk_pt", "RECO"))
    p = cs_Omega.cd(len(histograms))
    histograms[-1].Draw("hist")
    histograms.append(getHistogram(nbins, xlow, xhigh, df_Omega, mesonCat, "goodMeson_ditrk_pt", "GEN"))
    p = cs_Omega.cd(len(histograms))
    histograms[-1].Draw("hist")

    nbins, xlow, xhigh = 200, 0., 100.
    histograms.append(getHistogram(nbins, xlow, xhigh, df_Omega, mesonCat, "goodMeson_leadtrk_pt", "RECO"))
    p = cs_Omega.cd(len(histograms))
    histograms[-1].Draw("hist")
    histograms.append(getHistogram(nbins, xlow, xhigh, df_Omega, mesonCat, "goodMeson_leadtrk_pt", "GEN"))
    p = cs_Omega.cd(len(histograms))
    histograms[-1].Draw("hist")

    nbins, xlow, xhigh = 200, 0., 100.
    histograms.append(getHistogram(nbins, xlow, xhigh, df_Omega, mesonCat, "goodMeson_subleadtrk_pt", "RECO"))
    p = cs_Omega.cd(len(histograms))
    histograms[-1].Draw("hist")
    histograms.append(getHistogram(nbins, xlow, xhigh, df_Omega, mesonCat, "goodMeson_subleadtrk_pt", "GEN"))
    p = cs_Omega.cd(len(histograms))
    histograms[-1].Draw("hist")

    nbins, xlow, xhigh = 200, 0., 200.
    histograms.append(getHistogram(nbins, xlow, xhigh, df_Omega, mesonCat, "goodPhotons_pt", "RECO"))
    p = cs_Omega.cd(len(histograms))
    histograms[-1].Draw("hist")
    histograms.append(getHistogram(nbins, xlow, xhigh, df_Omega, mesonCat, "goodPhotons_pt", "GEN"))
    p = cs_Omega.cd(len(histograms))
    histograms[-1].Draw("hist")

    nbins, xlow, xhigh = 200, 0., 0.4
    histograms.append(getHistogram(nbins, xlow, xhigh, df_Omega, mesonCat, "goodMeson_DR", "RECO"))
    p = cs_Omega.cd(len(histograms))
    histograms[-1].Draw("hist")
    histograms.append(getHistogram(nbins, xlow, xhigh, df_Omega, mesonCat, "goodMeson_DR", "GEN"))
    p = cs_Omega.cd(len(histograms))
    histograms[-1].Draw("hist")

    nbins, xlow, xhigh = 200, 0.2, 1.4
    histograms.append(getHistogram(nbins, xlow, xhigh, df_Omega, mesonCat, "goodMeson_mass", "RECO"))
    p = cs_Omega.cd(len(histograms))
    histograms[-1].Draw("hist")
    histograms.append(getHistogram(nbins, xlow, xhigh, df_Omega, mesonCat, "goodMeson_mass", "GEN"))
    p = cs_Omega.cd(len(histograms))
    histograms[-1].Draw("hist")

    nbins, xlow, xhigh = 200, 0., 200.
    histograms.append(getHistogram(nbins, xlow, xhigh, df_Omega, mesonCat, "goodMeson_pt", "RECO"))
    p = cs_Omega.cd(len(histograms))
    histograms[-1].Draw("hist")
    histograms.append(getHistogram(nbins, xlow, xhigh, df_Omega, mesonCat, "goodMeson_pt", "GEN"))
    p = cs_Omega.cd(len(histograms))
    histograms[-1].Draw("hist")

    nbins, xlow, xhigh = 200, 105, 145
    histograms.append(getHistogram(nbins, xlow, xhigh, df_Omega, mesonCat, "HCandMass", "RECO"))
    p = cs_Omega.cd(len(histograms))
    histograms[-1].Draw("hist")
    histograms.append(getHistogram(nbins, xlow, xhigh, df_Omega, mesonCat, "HCandMass", "GEN"))
    p = cs_Omega.cd(len(histograms))
    histograms[-1].Draw("hist")

    nbins, xlow, xhigh = 200, 50., 140
    histograms.append(getHistogram(nbins, xlow, xhigh, df_Omega, mesonCat, "HCandMassMissing", "RECO"))
    p = cs_Omega.cd(len(histograms))
    histograms[-1].Draw("hist")
    histograms.append(getHistogram(nbins, xlow, xhigh, df_Omega, mesonCat, "HCandMassMissing", "GEN"))
    p = cs_Omega.cd(len(histograms))
    histograms[-1].Draw("hist")

    cs_Omega.SaveAs("~/public_html/Omega_RECO_vs_GEN.png")


    #D0StarRho----------------------------------------------------------------------------------------
    mesonCat = "D0StarRhoCat"
    histograms = []
    numRows = 10
    height = numRows * 800
    cs_D0StarRho = ROOT.TCanvas("canvas_D0StarRho", "canvas", 2200, height)
    cs_D0StarRho.Divide(2, numRows)
    chain = ROOT.TChain("events")
    for num in numDict[mesonCat]:
        chain.Add("/data/submit/pdmonte/outputs/{}/{}/outname_mc{}_{}_{}_{}.root".format(date, year, num, cat, mesonCat, year))
    df_D0StarRho = ROOT.RDataFrame(chain)

    df_D0StarRho = df_D0StarRho.Define("scale", "w*lumiIntegrated")\
        .Define("goodMeson_ditrk_mass_GEN", "get2BodyPtEtaPhiM(GenPart_pt, GenPart_eta, GenPart_phi, GenPart_mass, GenPart_pdgId, GenPart_genPartIdxMother, -321, 213, 421, 423, 25)[3]")\
        .Define("goodMeson_ditrk_pt_GEN", "get2BodyPtEtaPhiM(GenPart_pt, GenPart_eta, GenPart_phi, GenPart_mass, GenPart_pdgId, GenPart_genPartIdxMother, -321, 213, 421, 423, 25)[0]")\
        .Define("goodMeson_leadtrk_pt_GEN", "getMaximum(getPt(GenPart_pt, GenPart_pdgId, GenPart_genPartIdxMother, -321, 421, 423, 25), getPt(GenPart_pt, GenPart_pdgId, GenPart_genPartIdxMother, 213, 421, 423, 25))")\
        .Define("goodMeson_subleadtrk_pt_GEN", "getMinimum(getPt(GenPart_pt, GenPart_pdgId, GenPart_genPartIdxMother, -321, 421, 423, 25), getPt(GenPart_pt, GenPart_pdgId, GenPart_genPartIdxMother, 213, 421, 423, 25))")\
        .Define("goodPhotons_pt_GEN", "getPt(GenPart_pt, GenPart_pdgId, GenPart_genPartIdxMother, 22, 25)")\
        .Define("goodMeson_DR_GEN", "getDR(GenPart_eta, GenPart_phi, GenPart_pdgId, GenPart_genPartIdxMother, -321, 421, 423, 25, 213, 421, 423, 25)")\
        .Define("goodMeson_mass_GEN", "getD0StarPtEtaPhiM(GenPart_pt, GenPart_eta, GenPart_phi, GenPart_mass, GenPart_pdgId, GenPart_genPartIdxMother)[3]")\
        .Define("goodMeson_pt_GEN", "getD0StarPtEtaPhiM(GenPart_pt, GenPart_eta, GenPart_phi, GenPart_mass, GenPart_pdgId, GenPart_genPartIdxMother)[0]")\
        .Define("HCandMass_GEN", "getHiggsPtEtaPhiM(GenPart_pt, GenPart_eta, GenPart_phi, GenPart_mass, GenPart_pdgId, GenPart_genPartIdxMother, 423, 25, 22, 25)[3]")\
        .Define("HCandMassMissing", "compute_HiggsVars_var(goodMeson_ditrk_pt[0],goodMeson_ditrk_eta[0],goodMeson_ditrk_phi[0],goodMeson_ditrk_mass[0],photon_pt,goodPhotons_eta[index_pair[1]],goodPhotons_phi[index_pair[1]],0)")\
        .Define("HCandMassMissing_GEN", "getHiggsPtEtaPhiMD0StarDitrack(GenPart_pt, GenPart_eta, GenPart_phi, GenPart_mass, GenPart_pdgId, GenPart_genPartIdxMother)[3]")


    nbins, xlow, xhigh = 200, 1.6, 2.1
    histograms.append(getHistogram(nbins, xlow, xhigh, df_D0StarRho, mesonCat, "goodMeson_ditrk_mass", "RECO"))
    p = cs_D0StarRho.cd(len(histograms))
    histograms[-1].Draw("hist")
    histograms.append(getHistogram(nbins, xlow, xhigh, df_D0StarRho, mesonCat, "goodMeson_ditrk_mass", "GEN"))
    p = cs_D0StarRho.cd(len(histograms))
    histograms[-1].Draw("hist")

    nbins, xlow, xhigh = 200, 0., 200.
    histograms.append(getHistogram(nbins, xlow, xhigh, df_D0StarRho, mesonCat, "goodMeson_ditrk_pt", "RECO"))
    p = cs_D0StarRho.cd(len(histograms))
    histograms[-1].Draw("hist")
    histograms.append(getHistogram(nbins, xlow, xhigh, df_D0StarRho, mesonCat, "goodMeson_ditrk_pt", "GEN"))
    p = cs_D0StarRho.cd(len(histograms))
    histograms[-1].Draw("hist")

    nbins, xlow, xhigh = 200, 0., 100.
    histograms.append(getHistogram(nbins, xlow, xhigh, df_D0StarRho, mesonCat, "goodMeson_leadtrk_pt", "RECO"))
    p = cs_D0StarRho.cd(len(histograms))
    histograms[-1].Draw("hist")
    histograms.append(getHistogram(nbins, xlow, xhigh, df_D0StarRho, mesonCat, "goodMeson_leadtrk_pt", "GEN"))
    p = cs_D0StarRho.cd(len(histograms))
    histograms[-1].Draw("hist")

    nbins, xlow, xhigh = 200, 0., 100.
    histograms.append(getHistogram(nbins, xlow, xhigh, df_D0StarRho, mesonCat, "goodMeson_subleadtrk_pt", "RECO"))
    p = cs_D0StarRho.cd(len(histograms))
    histograms[-1].Draw("hist")
    histograms.append(getHistogram(nbins, xlow, xhigh, df_D0StarRho, mesonCat, "goodMeson_subleadtrk_pt", "GEN"))
    p = cs_D0StarRho.cd(len(histograms))
    histograms[-1].Draw("hist")

    nbins, xlow, xhigh = 200, 0., 200.
    histograms.append(getHistogram(nbins, xlow, xhigh, df_D0StarRho, mesonCat, "goodPhotons_pt", "RECO"))
    p = cs_D0StarRho.cd(len(histograms))
    histograms[-1].Draw("hist")
    histograms.append(getHistogram(nbins, xlow, xhigh, df_D0StarRho, mesonCat, "goodPhotons_pt", "GEN"))
    p = cs_D0StarRho.cd(len(histograms))
    histograms[-1].Draw("hist")

    nbins, xlow, xhigh = 200, 0., 0.2
    histograms.append(getHistogram(nbins, xlow, xhigh, df_D0StarRho, mesonCat, "goodMeson_DR", "RECO"))
    p = cs_D0StarRho.cd(len(histograms))
    histograms[-1].Draw("hist")
    histograms.append(getHistogram(nbins, xlow, xhigh, df_D0StarRho, mesonCat, "goodMeson_DR", "GEN"))
    p = cs_D0StarRho.cd(len(histograms))
    histograms[-1].Draw("hist")

    nbins, xlow, xhigh = 200, 1.85, 2.15
    histograms.append(getHistogram(nbins, xlow, xhigh, df_D0StarRho, mesonCat, "goodMeson_mass", "RECO"))
    p = cs_D0StarRho.cd(len(histograms))
    histograms[-1].Draw("hist")
    histograms.append(getHistogram(nbins, xlow, xhigh, df_D0StarRho, mesonCat, "goodMeson_mass", "GEN"))
    p = cs_D0StarRho.cd(len(histograms))
    histograms[-1].Draw("hist")

    nbins, xlow, xhigh = 200, 0., 200.
    histograms.append(getHistogram(nbins, xlow, xhigh, df_D0StarRho, mesonCat, "goodMeson_pt", "RECO"))
    p = cs_D0StarRho.cd(len(histograms))
    histograms[-1].Draw("hist")
    histograms.append(getHistogram(nbins, xlow, xhigh, df_D0StarRho, mesonCat, "goodMeson_pt", "GEN"))
    p = cs_D0StarRho.cd(len(histograms))
    histograms[-1].Draw("hist")

    nbins, xlow, xhigh = 200, 105, 145
    histograms.append(getHistogram(nbins, xlow, xhigh, df_D0StarRho, mesonCat, "HCandMass", "RECO"))
    p = cs_D0StarRho.cd(len(histograms))
    histograms[-1].Draw("hist")
    histograms.append(getHistogram(nbins, xlow, xhigh, df_D0StarRho, mesonCat, "HCandMass", "GEN"))
    p = cs_D0StarRho.cd(len(histograms))
    histograms[-1].Draw("hist")

    nbins, xlow, xhigh = 200, 105, 145
    histograms.append(getHistogram(nbins, xlow, xhigh, df_D0StarRho, mesonCat, "HCandMassMissing", "RECO"))
    p = cs_D0StarRho.cd(len(histograms))
    histograms[-1].Draw("hist")
    histograms.append(getHistogram(nbins, xlow, xhigh, df_D0StarRho, mesonCat, "HCandMassMissing", "GEN"))
    p = cs_D0StarRho.cd(len(histograms))
    histograms[-1].Draw("hist")

    cs_D0StarRho.SaveAs("~/public_html/D0StarRho_RECO_vs_GEN.png")