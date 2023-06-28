import ROOT
ROOT.ROOT.EnableImplicitMT()

numDict = {"Background": [10, 11, 12, 13, 14], "OmegaCat": [1038], "Phi3Cat": [1039], "D0StarCat": [1041]}

mesonLatex = {"OmegaCat": "#omega", "D0StarCat": "D^{0*}", "Phi3Cat": "#phi"}


def getHisto(nbin, xlow, xhigh, date, nums, cat, mesonCat, mesonLatex, year, filters=[], extraTitle=None, ditrack=False):
    """Creates a histogram based on specified parameters using ROOT's RDataFrame. Optional filters and extra title strings."""

    print("[getHisto] Creating Histogram {} {} {}...".format(mesonCat, cat, extraTitle))

    chain = ROOT.TChain("events")
    for num in nums:
        chain.Add("/data/submit/pdmonte/outputs/{}/{}/outname_mc{}_{}_{}_{}.root".format(date, year, num, cat, mesonCat, year))

    df = ROOT.RDataFrame(chain)
    
    for i in range(len(filters)):
        filterName = "filter_" + str(i)
        df = df.Define(filterName, filters[i]).Filter("Sum({})>0".format(filterName))

    title = "Higgs candidate mass for {}, reconstruction".format(mesonLatex)
    if extraTitle is not None:
        title += " ({})".format(extraTitle)

    if ditrack:
        h = df.Define("scale", "w*lumiIntegrated").Define("HCandMassMissing", "compute_HiggsVars_var(goodMeson_ditrk_pt[0],goodMeson_ditrk_eta[0],goodMeson_ditrk_phi[0],goodMeson_ditrk_mass[0],photon_pt,goodPhotons_eta[index_pair[1]],goodPhotons_phi[index_pair[1]],0)").Histo1D(("m_{H}", title, nbin, xlow, xhigh), "HCandMassMissing", "scale")
    else:
        h = df.Define("scale", "w*lumiIntegrated").Histo1D(("m_{H}", title, nbin, xlow, xhigh), "HCandMass", "scale")
    #h = df.Define("scale", "w*lumiIntegrated").Histo1D(("m_{H}", title, nbin, xlow, xhigh), "HCandMassVtxCorr", "scale")

    h.GetXaxis().SetTitle('m_{{#gamma, {0} }} [GeV]'.format(mesonLatex))
    h.GetYaxis().SetTitle("Events")

    h.SetFillColor(ROOT.kGreen-6)
    h.SetLineColor(ROOT.kBlack)

    print("[getHisto] -------------------------------------Histogram created!----------------------")

    return ROOT.TH1D(h.GetValue())


def getHistoFromFile(fileName):
    """Reads a histogram object from a ROOT file specified by `fileName`."""
    # Read using python 2.7.14 and ROOT 6.14
    infile = ROOT.TFile.Open(fileName, "read")
    h = infile.Get("myhisto")
    #Hist is associated with file and becomes None when file is destroyed. This line is to disassociate them
    h.SetDirectory(0)
    return h
    """
    # This is for python 3.11 and ROOT 6.28
    with ROOT.TFile(fileName, "read") as infile:
        h = infile.Get("myhisto")
        #Hist is associated with file and becomes None when file is destroyed. This line is to disassociate them
        h.SetDirectory(0)
        return h
    """


def saveHistoToFile(h, fileName):
    """Saves a histogram object `h` to a ROOT file specified by `fileName`."""
    # Save using python 3.11 and ROOT 6.28
    with ROOT.TFile(fileName, "RECREATE") as outfile:
        outfile.WriteObject(h, "myhisto")


def getFullNameOfHistFile(mesonCat, cat, year, date, extraTitle=None):
    """Generates the full file name for a histogram file based on the provided parameters."""
    fileName = "HCandMassHist_" + mesonCat[:-3] + "_" + cat[:-3] + "_" + str(year) + "_" + date + ".root"
    if extraTitle is not None:
        fileName = fileName[:-5] + "__" + extraTitle.replace(" ", "_").replace(",", "") + fileName[-5:]
    return "/data/submit/pdmonte/outHistsFits/" + fileName
