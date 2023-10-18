import ROOT
import os
#ROOT.ROOT.EnableImplicitMT()

numDict = {"Background": [10, 11, 12, 13, 14], "OmegaCat": [1038], "Phi3Cat": [1039], "D0StarCat": [1041]}

mesonLatex = {"OmegaCat": "#omega", "D0StarCat": "D^{0*}", "Phi3Cat": "#phi"}

mesonChannel = {"OmegaCat": "omega", "D0StarCat": "d0star", "Phi3Cat": "phi"}

#title, variable, xaxis label, range, max
doubleFitVar = {"OmegaCat": ["Full meson mass", "goodMeson_mass", "m_{#omega}", (0.57, 1.0), 0.7873],
                "Phi3Cat": ["Full meson mass", "goodMeson_mass", "m_{#phi}", (0.71, 1.21), 1.023],
                 "D0StarCat": ["Ditrack mass", "goodMeson_ditrk_mass", "m_{D^{0}}", (1.805, 1.925), 1.865]}


def getNumVarsFromCode(code):
    nVars = 0
    while(code > 0):
        nVars += int(code%2)
        code = int(code/2)
    return nVars


def getTotalNumVars(modelName):
    splitted = modelName.split("_")
    numVars = getNumVarsFromCode(int(splitted[1].replace("df", "")))
    numVars += getNumVarsFromCode(int(splitted[2].replace("dl", "")))
    numVars += len(splitted) - 3
    if "opt" in modelName:
        numVars -= 1
    return numVars


def getHisto(nbin, xlow, xhigh, date, nums, cat, mesonCat, mesonLatex, year, filters=[], extraTitle=None, ditrack=False, regModelName=None):
    """Creates a histogram based on specified parameters using ROOT's RDataFrame. Optional filters and extra title strings."""

    verbString = "[getHisto] Creating Histogram {} {} {}".format(mesonCat, cat, date)
    if regModelName is not None:
        verbString += " {}".format(regModelName)
    if extraTitle is not None:
        verbString += " {}".format(extraTitle)
    verbString += "..."
    print(verbString)

    title = "Higgs candidate mass for {}, reconstruction".format(mesonLatex)
    if regModelName is not None:
        title += " ({})".format(regModelName)
    if extraTitle is not None:
        title += " ({})".format(extraTitle)

    if regModelName is None:
        #No regression model
        chain = ROOT.TChain("events")
        for num in nums:
            chain.Add("/data/submit/pdmonte/outputs/{}/{}/outname_mc{}_{}_{}_{}.root".format(date, year, num, cat, mesonCat, year))

        df = ROOT.RDataFrame(chain)
        for i in range(len(filters)):
            filterName = "filter_" + str(i)
            df = df.Define(filterName, filters[i]).Filter("Sum({})>0".format(filterName))
        if ditrack:
            h = df.Define("scale", "w*lumiIntegrated").Define("HCandMassMissing", "compute_HiggsVars_var(goodMeson_ditrk_pt[0],goodMeson_ditrk_eta[0],goodMeson_ditrk_phi[0],goodMeson_ditrk_mass[0],photon_pt,goodPhotons_eta[index_pair[1]],goodPhotons_phi[index_pair[1]],0)").Histo1D(("m_{H}", title, nbin, xlow, xhigh), "HCandMassMissing", "scale").GetValue()
        else:
            h = df.Define("scale", "w*lumiIntegrated").Histo1D(("m_{H}", title, nbin, xlow, xhigh), "HCandMass", "scale").GetValue()
    else:
        #With a regression model to correct the PT of the meson
        #Load models
        variableName = regModelName + "_" + mesonChannel[mesonCat] + "_"
        variableName += "BKG" if len(nums) > 1 else "SGN"
        #print(variableName)

        s = '''
        TMVA::Experimental::RReader {variableName}Reader0("/data/submit/pdmonte/TMVA_models/weightsOpts2/TMVARegression_{modelName}_{channel}_0.weights.xml");
        {variableName}0 = TMVA::Experimental::Compute<{numVarsTotal}, float>({variableName}Reader0);
        TMVA::Experimental::RReader {variableName}Reader1("/data/submit/pdmonte/TMVA_models/weightsOpts2/TMVARegression_{modelName}_{channel}_1.weights.xml");
        {variableName}1 = TMVA::Experimental::Compute<{numVarsTotal}, float>({variableName}Reader1);
        TMVA::Experimental::RReader {variableName}Reader2("/data/submit/pdmonte/TMVA_models/weightsOpts2/TMVARegression_{modelName}_{channel}_2.weights.xml");
        {variableName}2 = TMVA::Experimental::Compute<{numVarsTotal}, float>({variableName}Reader2);
        '''.format(modelName=regModelName, channel=mesonChannel[mesonCat], numVarsTotal=getTotalNumVars(regModelName), variableName=variableName)

        ROOT.gInterpreter.ProcessLine(s)
        variables = list(getattr(ROOT, variableName + "Reader0").GetVariableNames())
        #print(variables)
        
        if len(nums) > 1:#BKG
            chainBKG = ROOT.TChain("events")
            for num in nums:
                chainBKG.Add("/data/submit/pdmonte/outputs/{}/{}/outname_mc{}_{}_{}_{}.root".format(date, year, num, cat, mesonCat, year))
            dfBKG = ROOT.RDataFrame(chainBKG)
            dfBKG = (dfBKG.Define("scale", "w*lumiIntegrated")
                    .Define("scaleFactor0", getattr(ROOT, variableName + "0"), variables)
                    .Define("scaleFactor1", getattr(ROOT, variableName + "1"), variables)
                    .Define("scaleFactor2", getattr(ROOT, variableName + "2"), variables)
                    #.Define("scaleFactor0", ROOT.computeModelScale0, variables)
                    #.Define("scaleFactor1", ROOT.computeModelScale1, variables)
                    #.Define("scaleFactor2", ROOT.computeModelScale2, variables)
                    .Define("goodMeson_pt_PRED", "(scaleFactor0[0]*goodMeson_pt[0] + scaleFactor1[0]*goodMeson_pt[0] + scaleFactor2[0]*goodMeson_pt[0])/3")
                    .Define("HCandMass_varPRED", "compute_HiggsVars_var(goodMeson_pt_PRED, goodMeson_eta[0], goodMeson_phi[0], goodMeson_mass[0], goodPhotons_pt[0], goodPhotons_eta[0], goodPhotons_phi[0], 0)"))
            h = dfBKG.Histo1D(("m_{H}", title, nbin, xlow, xhigh), "HCandMass_varPRED", "scale").GetValue()

        else:#SGN
            chainSGN0 = ROOT.TChain("events")
            chainSGN1 = ROOT.TChain("events")
            chainSGN2 = ROOT.TChain("events")
            chainSGN0.Add("/data/submit/pdmonte/outputs/{}/{}/outname_mc{}_{}_{}_{}_sample0.root".format(date, year, nums[0], cat, mesonCat, year))
            chainSGN1.Add("/data/submit/pdmonte/outputs/{}/{}/outname_mc{}_{}_{}_{}_sample1.root".format(date, year, nums[0], cat, mesonCat, year))
            chainSGN2.Add("/data/submit/pdmonte/outputs/{}/{}/outname_mc{}_{}_{}_{}_sample2.root".format(date, year, nums[0], cat, mesonCat, year))
            dfSGN0 = ROOT.RDataFrame(chainSGN0)
            dfSGN1 = ROOT.RDataFrame(chainSGN1)
            dfSGN2 = ROOT.RDataFrame(chainSGN2)
            #need to divide scale factor by 3 in each sample to be able to add all together
            dfSGN0 = (dfSGN0.Define("scale", "w*lumiIntegrated/3.")
                    .Define("scaleFactor", getattr(ROOT, variableName + "0"), variables)
                    #.Define("scaleFactor", ROOT.computeModelScale0, variables)
                    .Define("goodMeson_pt_PRED", "scaleFactor[0]*goodMeson_pt[0]")
                    .Define("HCandMass_varPRED", "compute_HiggsVars_var(goodMeson_pt_PRED, goodMeson_eta[0], goodMeson_phi[0], goodMeson_mass[0], goodPhotons_pt[0], goodPhotons_eta[0], goodPhotons_phi[0], 0)"))
            dfSGN1 = (dfSGN1.Define("scale", "w*lumiIntegrated/3.")
                    .Define("scaleFactor", getattr(ROOT, variableName + "1"), variables)
                    #.Define("scaleFactor", ROOT.computeModelScale1, variables)
                    .Define("goodMeson_pt_PRED", "scaleFactor[0]*goodMeson_pt[0]")
                    .Define("HCandMass_varPRED", "compute_HiggsVars_var(goodMeson_pt_PRED, goodMeson_eta[0], goodMeson_phi[0], goodMeson_mass[0], goodPhotons_pt[0], goodPhotons_eta[0], goodPhotons_phi[0], 0)"))
            dfSGN2 = (dfSGN2.Define("scale", "w*lumiIntegrated/3.")
                    .Define("scaleFactor", getattr(ROOT, variableName + "2"), variables)
                    #.Define("scaleFactor", ROOT.computeModelScale2, variables)
                    .Define("goodMeson_pt_PRED", "scaleFactor[0]*goodMeson_pt[0]")
                    .Define("HCandMass_varPRED", "compute_HiggsVars_var(goodMeson_pt_PRED, goodMeson_eta[0], goodMeson_phi[0], goodMeson_mass[0], goodPhotons_pt[0], goodPhotons_eta[0], goodPhotons_phi[0], 0)"))
            
            h = dfSGN0.Histo1D(("m_{H}", title, nbin, xlow, xhigh), "HCandMass_varPRED", "scale").GetValue()
            h.Add(dfSGN1.Histo1D(("m_{H}", title, nbin, xlow, xhigh), "HCandMass_varPRED", "scale").GetValue())
            h.Add(dfSGN2.Histo1D(("m_{H}", title, nbin, xlow, xhigh), "HCandMass_varPRED", "scale").GetValue())

    h.GetXaxis().SetTitle('m_{{#gamma, {0} }} [GeV]'.format(mesonLatex))
    h.GetYaxis().SetTitle("Events")
    h.SetFillColor(ROOT.kGreen-6)
    h.SetLineColor(ROOT.kBlack)

    print("[getHisto] ---------------------------------------- Histogram created! ----------------------")

    return ROOT.TH1D(h)


def getHistoDoubleFit(nbin, date, nums, cat, mesonCat, mesonLatex, year):
    """Creates a histogram based on specified parameters using ROOT's RDataFrame. Optional filters and extra title strings."""

    verbString = "[getHistoDoubleFit] Creating Histogram {} {} {}...".format(mesonCat, cat, date)
    print(verbString)

    title = "{} for {}, reconstruction".format(doubleFitVar[mesonCat][0], mesonLatex)

    xlow, xhigh = doubleFitVar[mesonCat][3]

    chain = ROOT.TChain("events")
    for num in nums:
        chain.Add("/data/submit/pdmonte/outputs/{}/{}/outname_mc{}_{}_{}_{}.root".format(date, year, num, cat, mesonCat, year))

    df = ROOT.RDataFrame(chain)
    h = df.Define("scale", "w*lumiIntegrated").Histo1D((doubleFitVar[mesonCat][0], title, nbin, xlow, xhigh), doubleFitVar[mesonCat][1], "scale").GetValue()
    
    h.GetXaxis().SetTitle('{} [GeV]'.format(doubleFitVar[mesonCat][2]))
    h.GetYaxis().SetTitle("Events")
    h.SetFillColor(ROOT.kGreen-6)
    h.SetLineColor(ROOT.kBlack)

    print("[getHistoDoubleFit] ---------------------------------------- Histogram created! ----------------------")

    return ROOT.TH1D(h)


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


def getFullNameOfHistFile(mesonCat, cat, year, date, extraTitle=None, regModelName=None, doubleFit=False):
    """Generates the full file name for a histogram file based on the provided parameters."""
    fileName = "HCandMassHist_" + mesonCat[:-3] + "_" + cat[:-3] + "_" + str(year) + "_" + date
    if regModelName is not None:
        fileName += "_" + regModelName
    if extraTitle is not None:
        fileName += "_" + extraTitle.replace(" ", "_").replace(",", "")
    if doubleFit:
        fileName += "_2D"
    return "/data/submit/pdmonte/outHistsFits/" + fileName + ".root"
