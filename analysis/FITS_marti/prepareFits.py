import ROOT
import math
import os
#ROOT.ROOT.EnableImplicitMT()

numDict = {"Background": [10, 11, 12, 13, 14], "Data": [-62, -63, -64], "OmegaCat": [1038], "Phi3Cat": [1039], "D0StarRhoCat": [1040], "D0StarCat": [1041]}

numVBFDict = {"OmegaCat": 1068, "Phi3Cat": 1069, "D0StarRhoCat": 1070, "D0StarCat": 1071}

mesonLatex = {"OmegaCat": "#omega", "D0StarCat": "D^{0*}", "Phi3Cat": "#phi", "D0StarRhoCat": "D^{0*}"}

mesonChannel = {"OmegaCat": "omega", "D0StarCat": "d0star", "Phi3Cat": "phi", "D0StarRhoCat": "d0starrho"}

#title, variable, xaxis label, range, peak
doubleFitVar = {"OmegaCat": ["Full meson mass", "goodMeson_mass", "m_{#omega}", (0.6001, 0.8399), 0.789],
                "Phi3Cat": ["Full meson mass", "goodMeson_mass", "m_{#phi}", (0.8001, 1.0799), 1.025],
                "D0StarCat": ["Ditrack mass", "goodMeson_ditrk_mass", "m_{D^{0}}", (1.8201, 1.9099), 1.865],
                "D0StarRhoCat": ["Full meson mass", "goodMeson_mass", "m_{D^{*0}}", (1.6001, 1.9999), 1.865]}

prodCat = "ggh"


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

    if len(nums) > 1:#BKG
        nums = numDict["Data"]

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
        TMVA::Experimental::RReader {variableName}Reader0("/data/submit/pdmonte/TMVA_models/weightsOptsFinalBis2/TMVARegression_{modelName}_{channel}_{prodCat}_0.weights.xml");
        {variableName}0 = TMVA::Experimental::Compute<{numVarsTotal}, float>({variableName}Reader0);
        TMVA::Experimental::RReader {variableName}Reader1("/data/submit/pdmonte/TMVA_models/weightsOptsFinalBis2/TMVARegression_{modelName}_{channel}_{prodCat}_1.weights.xml");
        {variableName}1 = TMVA::Experimental::Compute<{numVarsTotal}, float>({variableName}Reader1);
        TMVA::Experimental::RReader {variableName}Reader2("/data/submit/pdmonte/TMVA_models/weightsOptsFinalBis2/TMVARegression_{modelName}_{channel}_{prodCat}_2.weights.xml");
        {variableName}2 = TMVA::Experimental::Compute<{numVarsTotal}, float>({variableName}Reader2);
        '''.format(modelName=regModelName, channel=mesonChannel[mesonCat], prodCat=prodCat, numVarsTotal=getTotalNumVars(regModelName), variableName=variableName)

        ROOT.gInterpreter.ProcessLine(s)
        variables = list(getattr(ROOT, variableName + "Reader0").GetVariableNames())
        #print(variables)
        
        if len(nums) > 1:#BKG
            nums = numDict["Data"]
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
            #VBF
            chainSGN_VBF = ROOT.TChain("events")
            chainSGN_VBF.Add("/data/submit/pdmonte/outputs/{}/{}/outname_mc{}_{}_{}_{}.root".format(date, year, numVBFDict[mesonCat], cat, mesonCat, year))
            dfSGN_VBF = ROOT.RDataFrame(chainSGN_VBF)
            dfSGN_VBF = (dfSGN_VBF.Define("scale", "w*lumiIntegrated")
                    .Define("scaleFactor0", getattr(ROOT, variableName + "0"), variables)
                    .Define("scaleFactor1", getattr(ROOT, variableName + "1"), variables)
                    .Define("scaleFactor2", getattr(ROOT, variableName + "2"), variables)
                    .Define("goodMeson_pt_PRED", "(scaleFactor0[0]*goodMeson_pt[0] + scaleFactor1[0]*goodMeson_pt[0] + scaleFactor2[0]*goodMeson_pt[0])/3")
                    .Define("HCandMass_varPRED", "compute_HiggsVars_var(goodMeson_pt_PRED, goodMeson_eta[0], goodMeson_phi[0], goodMeson_mass[0], goodPhotons_pt[0], goodPhotons_eta[0], goodPhotons_phi[0], 0)"))
            h.Add(dfSGN_VBF.Histo1D(("m_{H}", title, nbin, xlow, xhigh), "HCandMass_varPRED", "scale").GetValue())

    h.GetXaxis().SetTitle('m_{{#gamma, {0} }} [GeV]'.format(mesonLatex))
    h.GetYaxis().SetTitle("Events")
    h.SetFillColor(ROOT.kGreen-6)
    h.SetLineColor(ROOT.kBlack)

    print("[getHisto] ---------------------------------------- Histogram created! ----------------------")

    return ROOT.TH1D(h)


def get2DHisto(nbinHiggs, xlow, xhigh, nbinMeson, date, nums, cat, mesonCat, mesonLatex, year, extraTitle=None, regModelName=None):
    """Creates a 2D histogram based on specified parameters using ROOT's RDataFrame."""

    verbString = "[get2DHisto] Creating Histogram {} {} {}".format(mesonCat, cat, date)
    if regModelName is not None:
        verbString += " {}".format(regModelName)
    if extraTitle is not None:
        verbString += " {}".format(extraTitle)
    verbString += "..."
    print(verbString)

    title = "Higgs candidate mass vs meson mass for {}, reconstruction".format(mesonLatex)
    if regModelName is not None:
        title += " ({})".format(regModelName)
    if extraTitle is not None:
        title += " ({})".format(extraTitle)

    yAxisVariable = doubleFitVar[mesonCat][1]
    ylow, yhigh = doubleFitVar[mesonCat][3]
    #nbinMeson = int(math.ceil((yhigh - ylow)/0.005)) if len(nums) > 1 else int(math.ceil((yhigh - ylow)/0.001))
    if len(nums) > 1:#BKG
        nums = numDict["Data"]

    if regModelName is None:
        #No regression model
        chain = ROOT.TChain("events")
        for num in nums:
            chain.Add("/data/submit/pdmonte/outputs/{}/{}/outname_mc{}_{}_{}_{}.root".format(date, year, num, cat, mesonCat, year))

        df = ROOT.RDataFrame(chain)
        #Create signal/Bkg 2D with no model
        h = df.Define("scale", "w*lumiIntegrated").Histo2D(("m_{H}_vs_m_{M}", title, nbinHiggs, xlow, xhigh, nbinMeson, ylow, yhigh), "HCandMass", yAxisVariable, "scale").GetValue()
    else:
        #With a regression model to correct the PT of the meson
        #Load models
        variableName = regModelName + "_" + mesonChannel[mesonCat] + "_"
        variableName += "BKG" if len(nums) > 1 else "SGN"
        #print(variableName)

        s = '''
        TMVA::Experimental::RReader {variableName}Reader0("/data/submit/pdmonte/TMVA_models/weightsOptsFinalBis2/TMVARegression_{modelName}_{channel}_{prodCat}_0.weights.xml");
        {variableName}0 = TMVA::Experimental::Compute<{numVarsTotal}, float>({variableName}Reader0);
        TMVA::Experimental::RReader {variableName}Reader1("/data/submit/pdmonte/TMVA_models/weightsOptsFinalBis2/TMVARegression_{modelName}_{channel}_{prodCat}_1.weights.xml");
        {variableName}1 = TMVA::Experimental::Compute<{numVarsTotal}, float>({variableName}Reader1);
        TMVA::Experimental::RReader {variableName}Reader2("/data/submit/pdmonte/TMVA_models/weightsOptsFinalBis2/TMVARegression_{modelName}_{channel}_{prodCat}_2.weights.xml");
        {variableName}2 = TMVA::Experimental::Compute<{numVarsTotal}, float>({variableName}Reader2);
        '''.format(modelName=regModelName, channel=mesonChannel[mesonCat], prodCat=prodCat, numVarsTotal=getTotalNumVars(regModelName), variableName=variableName)

        ROOT.gInterpreter.ProcessLine(s)
        variables = list(getattr(ROOT, variableName + "Reader0").GetVariableNames())
        #print(variables)
        
        if len(nums) > 1:#BKG
            nums = numDict["Data"]
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
            #change this to 2D
            h = dfBKG.Histo2D(("m_{H}_vs_m_{M}", title, nbinHiggs, xlow, xhigh, nbinMeson, ylow, yhigh), "HCandMass_varPRED", yAxisVariable, "scale").GetValue()

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
            
            h = dfSGN0.Histo2D(("m_{H}_vs_m_{M}", title, nbinHiggs, xlow, xhigh, nbinMeson, ylow, yhigh), "HCandMass_varPRED", yAxisVariable, "scale").GetValue()
            h.Add(dfSGN1.Histo2D(("m_{H}_vs_m_{M}", title, nbinHiggs, xlow, xhigh, nbinMeson, ylow, yhigh), "HCandMass_varPRED", yAxisVariable, "scale").GetValue())
            h.Add(dfSGN2.Histo2D(("m_{H}_vs_m_{M}", title, nbinHiggs, xlow, xhigh, nbinMeson, ylow, yhigh), "HCandMass_varPRED", yAxisVariable, "scale").GetValue())

            #VBF
            chainSGN_VBF = ROOT.TChain("events")
            chainSGN_VBF.Add("/data/submit/pdmonte/outputs/{}/{}/outname_mc{}_{}_{}_{}.root".format(date, year, numVBFDict[mesonCat], cat, mesonCat, year))
            dfSGN_VBF = ROOT.RDataFrame(chainSGN_VBF)
            dfSGN_VBF = (dfSGN_VBF.Define("scale", "w*lumiIntegrated")
                    .Define("scaleFactor0", getattr(ROOT, variableName + "0"), variables)
                    .Define("scaleFactor1", getattr(ROOT, variableName + "1"), variables)
                    .Define("scaleFactor2", getattr(ROOT, variableName + "2"), variables)
                    .Define("goodMeson_pt_PRED", "(scaleFactor0[0]*goodMeson_pt[0] + scaleFactor1[0]*goodMeson_pt[0] + scaleFactor2[0]*goodMeson_pt[0])/3")
                    .Define("HCandMass_varPRED", "compute_HiggsVars_var(goodMeson_pt_PRED, goodMeson_eta[0], goodMeson_phi[0], goodMeson_mass[0], goodPhotons_pt[0], goodPhotons_eta[0], goodPhotons_phi[0], 0)"))
            h.Add(dfSGN_VBF.Histo2D(("m_{H}_vs_m_{M}", title, nbinHiggs, xlow, xhigh, nbinMeson, ylow, yhigh), "HCandMass_varPRED", yAxisVariable, "scale").GetValue())

    h.GetXaxis().SetTitle('m_{{#gamma, {0} }} [GeV]'.format(mesonLatex))
    h.GetYaxis().SetTitle('{0} [GeV]'.format(doubleFitVar[mesonCat][2]))
    h.GetZaxis().SetTitle("Events")

    print(nbinMeson)

    print("[get2DHisto] ---------------------------------------- Histogram created! ----------------------")

    return ROOT.TH2D(h)


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


def getNameOfHistFileSimple(mesonCat, cat, year, date, extraTitle=None, regModelName=None, doubleFit=False):
    """Generates the full file name for a histogram file based on the provided parameters."""
    fileName = "HCandMassHist_" + mesonCat[:-3] + "_" + cat[:-3] + "_" + str(year) + "_" + date
    if regModelName is not None:
        fileName += "_" + regModelName
    if extraTitle is not None:
        fileName += "_" + extraTitle.replace(" ", "_").replace(",", "")
    if doubleFit:
        fileName += "_2D"
    return fileName


def plotHist(nameRootFile, nameOutDraw, is2D=False, xAxisRange=None, yAxisRange=None):
    print("[plotHist] START")
    cs = ROOT.TCanvas("canvas", "canvas", 800, 800)
    h = getHistoFromFile(nameRootFile)
    if xAxisRange:
        h.GetXaxis().SetRangeUser(xAxisRange[0], xAxisRange[1])
    if yAxisRange:
        h.GetYaxis().SetRangeUser(yAxisRange[0], yAxisRange[1])
    
    if is2D:
        h.SetContour(100)
        h.Draw("colz")
        cs.SaveAs("~/public_html/fits/testing/{}.png".format(nameOutDraw))
        csX = ROOT.TCanvas("canvas", "canvas", 800, 800)
        h.ProjectionX().Draw("hist")
        csX.SaveAs("~/public_html/fits/testing/{}_X.png".format(nameOutDraw))
        csY = ROOT.TCanvas("canvas", "canvas", 800, 800)
        h.ProjectionY().Draw("hist")
        csY.SaveAs("~/public_html/fits/testing/{}_Y.png".format(nameOutDraw))
    else:
        h.Draw("hist")
        cs.SaveAs("~/public_html/fits/testing/{}.png".format(nameOutDraw))
    print("[plotHist] END")
