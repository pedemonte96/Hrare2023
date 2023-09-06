import ROOT
ROOT.ROOT.EnableImplicitMT()

if "/home/submit/pdmonte/CMSSW_10_6_27/src/Hrare2023/analysis/func_marti.so" not in ROOT.gSystem.GetLibraries():
    ROOT.gSystem.CompileMacro("/home/submit/pdmonte/CMSSW_10_6_27/src/Hrare2023/analysis/func_marti.cc","k")

if "/home/submit/pdmonte/CMSSW_10_6_27/src/Hrare2023/analysis/functions.so" not in ROOT.gSystem.GetLibraries():
    ROOT.gSystem.CompileMacro("/home/submit/pdmonte/CMSSW_10_6_27/src/Hrare2023/analysis/functions.cc","k")

numDict = {"Background": [10, 11, 12, 13, 14], "OmegaCat": [1038], "Phi3Cat": [1039], "D0StarRhoCat": [1040], "D0StarCat": [1041]}

mesonLatex = {"OmegaCat": "#omega", "Phi3Cat": "#phi", "D0StarRhoCat": "D^{0*} (#rho)", "D0StarCat": "D^{0*}"}

colors = {"RECO": "\033[1;36m", "GEN": "\033[1;34m", "BKG": "\033[1;31m", "NC": "\033[0m", "YELLOW": "\033[1;33m"}

variableNames = {"goodMeson_ditrk_mass": ["ditrack mass", "m [GeV]", "GeV"],
                 "goodMeson_mass": ["full mass", "m [GeV]", "GeV"],
                 "goodMeson_ditrk_pt": ["ditrack p_{T}", "p_{T} [GeV]", "GeV"],
                 "goodMeson_pt": ["full p_{T}", "p_{T} [GeV]", "GeV"],
                 "goodMeson_Nphotons": ["Num photons", "#", ""],
                 "goodMeson_leadtrk_pt": ["leading track p_{T}", "p_{T} [GeV]", "GeV"],
                 "goodMeson_subleadtrk_pt": ["subleading track p_{T}", "p_{T} [GeV]", "GeV"],
                 "goodPhotons_pt": ["photon from H p_{T}", "p_{T} [GeV]", "GeV"],
                 "goodMeson_DR": ["DR of ditrack", "DR [rad]", "rad"],
                 "HCandMassFilt": ["H Cand mass", "m [GeV]", "GeV"],
                 "HCandMassMissing": ["H Cand mass missing #gamma/#pi^{0}", "m [GeV]", "GeV"],
                 "goodMeson_iso": ["isolation", "Iso", ""]}


def getHistogram(nbins, xlow, xhigh, df, mesonCat, variable, level):
    text = " Creating histogram {} {} {} ".format(mesonCat, variable, level).center(70, "-")
    print(colors[level] + "[getHistogram]{}".format(text) + colors["NC"])
    title = mesonLatex[mesonCat] + ": " + variableNames[variable][0] + ", " + level
    xAxisTitle = variableNames[variable][1]
    yAxisTitle = "Events/(" + str(round((xhigh - xlow)/nbins, 5)) + " " + variableNames[variable][2] + ")"

    extendedVariable = variable + "_" + level if level == "GEN" else variable

    #h = df.Define("good", "{0}[{0}>0]".format(extendedVariable)).Histo1D(("hist", title, nbins, xlow, xhigh), "good", "scale")

    if (level == "RECO" or level == "BKG"):
        h = df.Define("good", "{0}[{0}>0]".format(extendedVariable)).Histo1D(("hist", title, nbins, xlow, xhigh), "good", "scale")
        if(variable == "goodMeson_Nphotons"):
            h = df.Define("good", "{0}[{0}>=-1]".format(extendedVariable)).Histo1D(("hist", title, nbins, xlow, xhigh), "good", "scale")
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
    text = " Histogram created! ".center(70, "-")
    print(colors[level] + "[getHistogram]{}".format(text) + colors["NC"])
    return ROOT.TH1D(h.GetValue())


def makePlots(cat, mesonCat, year, date, background):

    text = " Making plots for {} {} ".format(mesonCat, date).center(70, "~")
    print(colors["YELLOW"] + "[makePlots]~~~{}".format(text) + colors["NC"])

    numRows = 12
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
        df_BKG = (df_BKG.Define("scale", "w*lumiIntegrated")
            .Define("HCandMassFilt", "Vec_f {HCandMass}")
            .Define("HCandMassMissing", "Vec_f {compute_HiggsVars_var(goodMeson_ditrk_pt[0],goodMeson_ditrk_eta[0],goodMeson_ditrk_phi[0],goodMeson_ditrk_mass[0],photon_pt,goodPhotons_eta[index_pair[1]],goodPhotons_phi[index_pair[1]],0)}"))

    if (mesonCat == "D0StarCat"):
        df_SGN = (df_SGN.Define("scale", "w*lumiIntegrated")
            .Define("HCandMassFilt", "Vec_f {HCandMass}")
            .Define("HCandMassFilt_GEN", "getHiggsPtEtaPhiM(GenPart_pt, GenPart_eta, GenPart_phi, GenPart_mass, GenPart_pdgId, GenPart_genPartIdxMother, 423, 25, 22, 25)[3]")
            .Define("HCandMassMissing", "Vec_f {compute_HiggsVars_var(goodMeson_ditrk_pt[0],goodMeson_ditrk_eta[0],goodMeson_ditrk_phi[0],goodMeson_ditrk_mass[0],photon_pt,goodPhotons_eta[index_pair[1]],goodPhotons_phi[index_pair[1]],0)}")
            .Define("HCandMassMissing_GEN", "getHiggsPtEtaPhiMD0StarDitrack(GenPart_pt, GenPart_eta, GenPart_phi, GenPart_mass, GenPart_pdgId, GenPart_genPartIdxMother)[3]"))
    elif (mesonCat == "Phi3Cat"):
        df_SGN = (df_SGN.Define("scale", "w*lumiIntegrated")
            .Define("HCandMassFilt", "Vec_f {HCandMass}")
            .Define("HCandMassFilt_GEN", "getHiggsPtEtaPhiM(GenPart_pt, GenPart_eta, GenPart_phi, GenPart_mass, GenPart_pdgId, GenPart_genPartIdxMother, 333, 25, 22, 25)[3]")
            .Define("HCandMassMissing", "Vec_f {compute_HiggsVars_var(goodMeson_ditrk_pt[0],goodMeson_ditrk_eta[0],goodMeson_ditrk_phi[0],goodMeson_ditrk_mass[0],photon_pt,goodPhotons_eta[index_pair[1]],goodPhotons_phi[index_pair[1]],0)}")
            .Define("HCandMassMissing_GEN", "getHiggsPtEtaPhiMPhi3Ditrack(GenPart_pt, GenPart_eta, GenPart_phi, GenPart_mass, GenPart_pdgId, GenPart_genPartIdxMother)[3]"))
    elif (mesonCat == "OmegaCat"):
        df_SGN = (df_SGN.Define("scale", "w*lumiIntegrated")
            .Define("HCandMassFilt", "Vec_f {HCandMass}")
            .Define("HCandMassFilt_GEN", "getHiggsPtEtaPhiM(GenPart_pt, GenPart_eta, GenPart_phi, GenPart_mass, GenPart_pdgId, GenPart_genPartIdxMother, 223, 25, 22, 25)[3]")
            .Define("HCandMassMissing", "Vec_f {compute_HiggsVars_var(goodMeson_ditrk_pt[0],goodMeson_ditrk_eta[0],goodMeson_ditrk_phi[0],goodMeson_ditrk_mass[0],photon_pt,goodPhotons_eta[index_pair[1]],goodPhotons_phi[index_pair[1]],0)}")
            .Define("HCandMassMissing_GEN", "getHiggsPtEtaPhiMOmegaDitrack(GenPart_pt, GenPart_eta, GenPart_phi, GenPart_mass, GenPart_pdgId, GenPart_genPartIdxMother)[3]"))
    elif (mesonCat == "D0StarRhoCat"):
        df_SGN = (df_SGN.Define("scale", "w*lumiIntegrated")
            .Define("HCandMassFilt", "Vec_f {HCandMass}")
            .Define("HCandMassFilt_GEN", "getHiggsPtEtaPhiM(GenPart_pt, GenPart_eta, GenPart_phi, GenPart_mass, GenPart_pdgId, GenPart_genPartIdxMother, 423, 25, 22, 25)[3]")
            .Define("HCandMassMissing", "Vec_f {compute_HiggsVars_var(goodMeson_ditrk_pt[0],goodMeson_ditrk_eta[0],goodMeson_ditrk_phi[0],goodMeson_ditrk_mass[0],photon_pt,goodPhotons_eta[index_pair[1]],goodPhotons_phi[index_pair[1]],0)}")
            .Define("HCandMassMissing_GEN", "getHiggsPtEtaPhiMD0StarDitrack(GenPart_pt, GenPart_eta, GenPart_phi, GenPart_mass, GenPart_pdgId, GenPart_genPartIdxMother)[3]"))
        
    
    nbins, xlow, xhigh, variable = 200, 1.65, 2.05, "goodMeson_ditrk_mass"
    if (mesonCat == "Phi3Cat"):
        xlow, xhigh = 0.2, 1.0
    elif (mesonCat == "OmegaCat"):
        xlow, xhigh = 0.2, 0.8
    elif (mesonCat == "D0StarRhoCat"):
        xlow, xhigh = 0.4, 2.00
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

    nbins, xlow, xhigh, variable = 200, 0., 0.15, "goodMeson_DR"
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
    if (mesonCat == "Phi3Cat"):
        xlow, xhigh = 0.6, 1.3
    elif (mesonCat == "OmegaCat"):
        xlow, xhigh = 0.3, 1.3
    elif (mesonCat == "D0StarRhoCat"):
        xlow, xhigh = 0.6, 2.30
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

    nbins, xlow, xhigh, variable = 9, -1., 8., "goodMeson_Nphotons"
    histograms.append(getHistogram(nbins, xlow, xhigh, df_SGN, mesonCat, variable, "RECO"))
    p = cs.cd(len(histograms))
    histograms[-1].Draw("hist")
    histograms.append(0)
    p = cs.cd(len(histograms))
    #histograms[-1].Draw("hist")
    if background:
        histograms.append(getHistogram(nbins, xlow, xhigh, df_BKG, mesonCat, variable, "BKG"))
        p = cs.cd(len(histograms))
        histograms[-1].Draw("hist")

    nbins, xlow, xhigh, variable = 200, 105, 145, "HCandMassFilt"
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

    nbins, xlow, xhigh, variable = 200, 105, 135, "HCandMassMissing"
    if (mesonCat == "Phi3Cat" or mesonCat == "OmegaCat" or mesonCat == "D0StarRhoCat"):
        xlow, xhigh = 50, 140
    histograms.append(getHistogram(nbins, xlow, xhigh, df_SGN, mesonCat, variable, "RECO"))
    p = cs.cd(len(histograms))
    histograms[-1].Draw("hist")
    if (mesonCat == "D0StarCat" or mesonCat == "D0StarRhoCat"):
        #Stack
        h_ph_RECO=df_SGN.Filter("getPt(GenPart_pt, GenPart_pdgId, GenPart_genPartIdxMother, 22, 423, 25).size() == 1").Histo1D(("hist", "title", nbins, xlow, xhigh), variable, "scale")
        h_pi_RECO=df_SGN.Filter("getPt(GenPart_pt, GenPart_pdgId, GenPart_genPartIdxMother, 111, 423, 25).size() == 1").Histo1D(("hist", "title", nbins, xlow, xhigh), variable, "scale")
        h_ph_RECO.SetFillColor(ROOT.kGreen-2)
        h_ph_RECO.SetLineColor(ROOT.kBlack)
        h_pi_RECO.SetFillColor(ROOT.kGreen-9)
        h_pi_RECO.SetLineColor(ROOT.kBlack)

        stackRECO = ROOT.THStack("stack", mesonLatex[mesonCat] + ": " + variableNames[variable][0] + ", " + "RECO")
        stackRECO.Add(h_ph_RECO.GetValue())
        stackRECO.Add(h_pi_RECO.GetValue())
        stackRECO.Draw("hist same")
        #ROOT.gStyle.SetLegendBorderSize(0)
        legendRECO = ROOT.TLegend(0.78, 0.42, 0.98, 0.775)
        legendRECO.AddEntry(h_ph_RECO.GetValue(), "#splitline{{#splitline{{#scale[1.4]{{Missing #gamma}}}}{{Entries:  {0}}}}}{{#splitline{{Mean:     {1}}}{{Std Dev: {2}}}}}".format(int(h_ph_RECO.GetEntries()), round(h_ph_RECO.GetMean(), 1), round(h_ph_RECO.GetStdDev(), 3)), "f")
        legendRECO.AddEntry(h_pi_RECO.GetValue(), "#splitline{{#scale[1.4]{{Missing #pi^{{0}}}}}}{{#splitline{{Entries:  {0}}}{{#splitline{{Mean:     {1}}}{{Std Dev: {2}}}}}}}".format(int(h_pi_RECO.GetEntries()), round(h_pi_RECO.GetMean(), 1), round(h_pi_RECO.GetStdDev(), 3)), "f")
        legendRECO.SetEntrySeparation(0.79)
        legendRECO.SetMargin(0.42)
        legendRECO.Draw()
        #ROOT.gStyle.SetLegendBorderSize(1)

    histograms.append(getHistogram(nbins, xlow, xhigh, df_SGN, mesonCat, variable, "GEN"))
    p = cs.cd(len(histograms))
    histograms[-1].Draw("hist")
    if (mesonCat == "D0StarCat" or mesonCat == "D0StarRhoCat"):
        #Stack
        h_ph_GEN=df_SGN.Filter("getPt(GenPart_pt, GenPart_pdgId, GenPart_genPartIdxMother, 22, 423, 25).size() == 1").Histo1D(("hist", "title", nbins, xlow, xhigh), variable + "_GEN", "scale")
        h_pi_GEN=df_SGN.Filter("getPt(GenPart_pt, GenPart_pdgId, GenPart_genPartIdxMother, 111, 423, 25).size() == 1").Histo1D(("hist", "title", nbins, xlow, xhigh), variable + "_GEN", "scale")
        h_ph_GEN.SetFillColor(ROOT.kBlue-2)
        h_ph_GEN.SetLineColor(ROOT.kBlack)
        h_pi_GEN.SetFillColor(ROOT.kBlue-9)
        h_pi_GEN.SetLineColor(ROOT.kBlack)

        stackGEN = ROOT.THStack("stack", mesonLatex[mesonCat] + ": " + variableNames[variable][0] + ", " + "GEN")
        stackGEN.Add(h_ph_GEN.GetValue())
        stackGEN.Add(h_pi_GEN.GetValue())
        stackGEN.Draw("hist same")
        #ROOT.gStyle.SetLegendBorderSize(0)
        legendGEN = ROOT.TLegend(0.78, 0.42, 0.98, 0.775)
        legendGEN.AddEntry(h_ph_GEN.GetValue(), "#splitline{{#splitline{{#scale[1.4]{{Missing #gamma}}}}{{Entries:  {0}}}}}{{#splitline{{Mean:     {1}}}{{Std Dev: {2}}}}}".format(int(h_ph_GEN.GetEntries()), round(h_ph_GEN.GetMean(), 1), round(h_ph_GEN.GetStdDev(), 3)), "f")
        legendGEN.AddEntry(h_pi_GEN.GetValue(), "#splitline{{#scale[1.4]{{Missing #pi^{{0}}}}}}{{#splitline{{Entries:  {0}}}{{#splitline{{Mean:     {1}}}{{Std Dev: {2}}}}}}}".format(int(h_pi_GEN.GetEntries()), round(h_pi_GEN.GetMean(), 1), round(h_pi_GEN.GetStdDev(), 3)), "f")
        legendGEN.SetEntrySeparation(0.79)
        legendGEN.SetMargin(0.42)
        legendGEN.Draw()
        #ROOT.gStyle.SetLegendBorderSize(1)
    
    if background:
        histograms.append(getHistogram(nbins, xlow, xhigh, df_BKG, mesonCat, variable, "BKG"))
        p = cs.cd(len(histograms))
        histograms[-1].Draw("hist")

    nbins, xlow, xhigh, variable = 200, 0.0, 1.20, "goodMeson_iso"
    histograms.append(getHistogram(nbins, xlow, xhigh, df_SGN, mesonCat, variable, "RECO"))
    p = cs.cd(len(histograms))
    p.SetLogy()
    histograms[-1].Draw("hist")
    histograms.append(0)
    p = cs.cd(len(histograms))
    #histograms[-1].Draw("hist")
    if background:
        histograms.append(getHistogram(nbins, xlow, xhigh, df_BKG, mesonCat, variable, "BKG"))
        p = cs.cd(len(histograms))
        p.SetLogy()
        histograms[-1].Draw("hist")

    cs.SaveAs("~/public_html/{}_RECO_vs_GEN.png".format(mesonCat[:-3]))
    text = " Done! ".center(70, "~")
    print(colors["YELLOW"] + "[makePlots]~~~{}".format(text) + colors["NC"] + "\n")
    

if __name__ == "__main__":

    background = True

    cat = "GFcat"
    year = 2018
    date = "AUG24"

    #D0Star--------------------------------------------------------------------------------------
    #background = False
    mesonCat = "D0StarCat"
    #makePlots(cat, mesonCat, year, date, background)

    #Phi3----------------------------------------------------------------------------------------
    #background = False
    mesonCat = "Phi3Cat"
    #makePlots(cat, mesonCat, year, date, background)

    #Omega---------------------------------------------------------------------------------------
    #background = False
    mesonCat = "OmegaCat"
    #makePlots(cat, mesonCat, year, date, background)

    #D0StarRho-----------------------------------------------------------------------------------
    #background = False
    mesonCat = "D0StarRhoCat"
    #makePlots(cat, mesonCat, year, date, background)
    