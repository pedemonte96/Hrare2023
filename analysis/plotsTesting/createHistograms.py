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

    extendedVariable = variable + "_" + level if level == "GEN" else variable

    #h = df.Define("good", "{0}[{0}>0]".format(extendedVariable)).Histo1D(("hist", title, nbins, xlow, xhigh), "good", "scale")

    if (level == "RECO" or level == "BKG"):
        if (variable == "HCandMass" or variable == "HCandMassMissing"):
            h = df.Filter("{0}>0".format(extendedVariable)).Histo1D(("hist", title, nbins, xlow, xhigh), extendedVariable, "scale")
        else:
            h = df.Define("good", "{0}[{0}>0]".format(extendedVariable)).Histo1D(("hist", title, nbins, xlow, xhigh), "good", "scale")
        
        if (level == "RECO"):
            h.SetFillColor(ROOT.kGreen-9)
        elif (level == "BKG"):
            h.SetFillColor(ROOT.kRed-9)
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


def makePlots(cat, mesonCat, year, date, background):

    numRows = 10
    numCols = 3 if background else 2
    height = numRows * 800
    width = numCols * 850

    histograms = []

    cs = ROOT.TCanvas("canvas", "canvas", width, height)
    cs.Divide(numCols, numRows)

    chainSGN = ROOT.TChain("events")
    for num in numDict[mesonCat]:
        chainSGN.Add("/data/submit/pdmonte/outputs/{}/{}/outname_mc{}_{}_{}_{}.root".format(date, year, num, cat, mesonCat, year))
    df_SGN = ROOT.RDataFrame(chainSGN)

    if background:
        chainBKG = ROOT.TChain("events")
        for num in numDict["Background"]:
            chainBKG.Add("/data/submit/pdmonte/outputs/{}/{}/outname_mc{}_{}_{}_{}.root".format(date, year, num, cat, mesonCat, year))
        df_BKG = ROOT.RDataFrame(chainBKG)
        df_BKG = df_BKG.Define("scale", "w*lumiIntegrated")\
            .Define("HCandMassMissing", "compute_HiggsVars_var(goodMeson_ditrk_pt[0],goodMeson_ditrk_eta[0],goodMeson_ditrk_phi[0],goodMeson_ditrk_mass[0],photon_pt,goodPhotons_eta[index_pair[1]],goodPhotons_phi[index_pair[1]],0)")

    if (mesonCat == "D0StarCat"):
        df_SGN = df_SGN.Define("scale", "w*lumiIntegrated")\
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
    elif (mesonCat == "Phi3Cat"):
        df_SGN = df_SGN.Define("scale", "w*lumiIntegrated")\
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
    elif (mesonCat == "OmegaCat"):
        df_SGN = df_SGN.Define("scale", "w*lumiIntegrated")\
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
    elif (mesonCat == "D0StarRhoCat"):
        df_SGN = df_SGN.Define("scale", "w*lumiIntegrated")\
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
        
    
    nbins, xlow, xhigh, variable = 200, 1.6, 2.1, "goodMeson_ditrk_mass"
    if (mesonCat == "Phi3Cat" or mesonCat == "OmegaCat"):
        xlow, xhigh = 0.0, 1.4
    histograms.append(getHistogram(nbins, xlow, xhigh, df_SGN, mesonCat, variable, "RECO"))
    p = cs.cd(len(histograms))
    histograms[-1].Draw("hist")
    histograms.append(getHistogram(nbins, xlow, xhigh, df_SGN, mesonCat, variable, "GEN"))
    p = cs.cd(len(histograms))
    histograms[-1].Draw("hist")
    if background:
        histograms.append(getHistogram(nbins, xlow, xhigh, df_BKG, mesonCat, variable, "BKG"))
        p = cs.cd(len(histograms))
        histograms[-1].Draw("hist")

    nbins, xlow, xhigh, variable = 200, 0., 200., "goodMeson_ditrk_pt"
    histograms.append(getHistogram(nbins, xlow, xhigh, df_SGN, mesonCat, variable, "RECO"))
    p = cs.cd(len(histograms))
    histograms[-1].Draw("hist")
    histograms.append(getHistogram(nbins, xlow, xhigh, df_SGN, mesonCat, variable, "GEN"))
    p = cs.cd(len(histograms))
    histograms[-1].Draw("hist")
    if background:
        histograms.append(getHistogram(nbins, xlow, xhigh, df_BKG, mesonCat, variable, "BKG"))
        p = cs.cd(len(histograms))
        histograms[-1].Draw("hist")

    nbins, xlow, xhigh, variable = 200, 0., 100., "goodMeson_leadtrk_pt"
    histograms.append(getHistogram(nbins, xlow, xhigh, df_SGN, mesonCat, variable, "RECO"))
    p = cs.cd(len(histograms))
    histograms[-1].Draw("hist")
    histograms.append(getHistogram(nbins, xlow, xhigh, df_SGN, mesonCat, variable, "GEN"))
    p = cs.cd(len(histograms))
    histograms[-1].Draw("hist")
    if background:
        histograms.append(getHistogram(nbins, xlow, xhigh, df_BKG, mesonCat, variable, "BKG"))
        p = cs.cd(len(histograms))
        histograms[-1].Draw("hist")

    nbins, xlow, xhigh, variable = 200, 0., 100., "goodMeson_subleadtrk_pt"
    histograms.append(getHistogram(nbins, xlow, xhigh, df_SGN, mesonCat, variable, "RECO"))
    p = cs.cd(len(histograms))
    histograms[-1].Draw("hist")
    histograms.append(getHistogram(nbins, xlow, xhigh, df_SGN, mesonCat, variable, "GEN"))
    p = cs.cd(len(histograms))
    histograms[-1].Draw("hist")
    if background:
        histograms.append(getHistogram(nbins, xlow, xhigh, df_BKG, mesonCat, variable, "BKG"))
        p = cs.cd(len(histograms))
        histograms[-1].Draw("hist")

    nbins, xlow, xhigh, variable = 200, 0., 200., "goodPhotons_pt"
    histograms.append(getHistogram(nbins, xlow, xhigh, df_SGN, mesonCat, variable, "RECO"))
    p = cs.cd(len(histograms))
    histograms[-1].Draw("hist")
    histograms.append(getHistogram(nbins, xlow, xhigh, df_SGN, mesonCat, variable, "GEN"))
    p = cs.cd(len(histograms))
    histograms[-1].Draw("hist")
    if background:
        histograms.append(getHistogram(nbins, xlow, xhigh, df_BKG, mesonCat, variable, "BKG"))
        p = cs.cd(len(histograms))
        histograms[-1].Draw("hist")

    nbins, xlow, xhigh, variable = 200, 0., 0.2, "goodMeson_DR"
    histograms.append(getHistogram(nbins, xlow, xhigh, df_SGN, mesonCat, variable, "RECO"))
    p = cs.cd(len(histograms))
    histograms[-1].Draw("hist")
    histograms.append(getHistogram(nbins, xlow, xhigh, df_SGN, mesonCat, variable, "GEN"))
    p = cs.cd(len(histograms))
    histograms[-1].Draw("hist")
    if background:
        histograms.append(getHistogram(nbins, xlow, xhigh, df_BKG, mesonCat, variable, "BKG"))
        p = cs.cd(len(histograms))
        histograms[-1].Draw("hist")

    nbins, xlow, xhigh, variable = 200, 1.85, 2.15, "goodMeson_mass"
    if (mesonCat == "Phi3Cat" or mesonCat == "OmegaCat"):
        xlow, xhigh = 0.6, 1.4
    histograms.append(getHistogram(nbins, xlow, xhigh, df_SGN, mesonCat, variable, "RECO"))
    p = cs.cd(len(histograms))
    histograms[-1].Draw("hist")
    histograms.append(getHistogram(nbins, xlow, xhigh, df_SGN, mesonCat, variable, "GEN"))
    p = cs.cd(len(histograms))
    histograms[-1].Draw("hist")
    if background:
        histograms.append(getHistogram(nbins, xlow, xhigh, df_BKG, mesonCat, variable, "BKG"))
        p = cs.cd(len(histograms))
        histograms[-1].Draw("hist")

    nbins, xlow, xhigh, variable = 200, 0., 200., "goodMeson_pt"
    histograms.append(getHistogram(nbins, xlow, xhigh, df_SGN, mesonCat, variable, "RECO"))
    p = cs.cd(len(histograms))
    histograms[-1].Draw("hist")
    histograms.append(getHistogram(nbins, xlow, xhigh, df_SGN, mesonCat, variable, "GEN"))
    p = cs.cd(len(histograms))
    histograms[-1].Draw("hist")
    if background:
        histograms.append(getHistogram(nbins, xlow, xhigh, df_BKG, mesonCat, variable, "BKG"))
        p = cs.cd(len(histograms))
        histograms[-1].Draw("hist")

    nbins, xlow, xhigh, variable = 200, 105, 145, "HCandMass"
    histograms.append(getHistogram(nbins, xlow, xhigh, df_SGN, mesonCat, variable, "RECO"))
    p = cs.cd(len(histograms))
    histograms[-1].Draw("hist")
    histograms.append(getHistogram(nbins, xlow, xhigh, df_SGN, mesonCat, variable, "GEN"))
    p = cs.cd(len(histograms))
    histograms[-1].Draw("hist")
    if background:
        histograms.append(getHistogram(nbins, xlow, xhigh, df_BKG, mesonCat, variable, "BKG"))
        p = cs.cd(len(histograms))
        histograms[-1].Draw("hist")

    nbins, xlow, xhigh, variable = 200, 105, 145, "HCandMassMissing"
    if (mesonCat == "Phi3Cat" or mesonCat == "OmegaCat"):
        xlow, xhigh = 50, 140
    histograms.append(getHistogram(nbins, xlow, xhigh, df_SGN, mesonCat, variable, "RECO"))
    p = cs.cd(len(histograms))
    histograms[-1].Draw("hist")
    histograms.append(getHistogram(nbins, xlow, xhigh, df_SGN, mesonCat, variable, "GEN"))
    p = cs.cd(len(histograms))
    histograms[-1].Draw("hist")
    if background:
        histograms.append(getHistogram(nbins, xlow, xhigh, df_BKG, mesonCat, variable, "BKG"))
        p = cs.cd(len(histograms))
        histograms[-1].Draw("hist")

    cs.SaveAs("~/public_html/{}_RECO_vs_GEN.png".format(mesonCat[:-3]))
    

if __name__ == "__main__":

    background = True

    cat = "GFcat"
    year = 2018
    date = "JUN21"  

    #D0Star----------------------------------------------------------------------------------------
    mesonCat = "D0StarCat"
    makePlots(cat, mesonCat, year, date, background)

    #Phi3----------------------------------------------------------------------------------------
    mesonCat = "Phi3Cat"
    makePlots(cat, mesonCat, year, date, background)

    background = False

    #Omega----------------------------------------------------------------------------------------
    mesonCat = "OmegaCat"
    makePlots(cat, mesonCat, year, date, background)

    #D0StarRho----------------------------------------------------------------------------------------
    mesonCat = "D0StarRhoCat"
    #makePlots(cat, mesonCat, year, date, background)
    