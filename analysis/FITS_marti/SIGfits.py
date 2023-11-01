import ROOT
from prepareFits import *

ROOT.gROOT.SetBatch()
ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit.so")

xlowRange = 100.
xhighRange = 160.

sig = "ggH"
workspaceName = 'WS_OCT25'

def fitSig(tag, mesonCat, year, date, extraTitle=None, regModelName=None):

    if regModelName == "RECO":
        regModelName = None

    verbString = "[fitSig] Fitting Histogram {} {} {}".format(mesonCat, cat, date)
    if regModelName is not None:
        verbString += " {}".format(regModelName)
    if extraTitle is not None:
        verbString += " {}".format(extraTitle)
    verbString += "..."
    print('\033[1;36m' + verbString + '\033[0m')






    #Read Hist file saved
    data_full = getHistoFromFile(getFullNameOfHistFile(mesonCat, cat, year, date, extraTitle=extraTitle, regModelName=regModelName))
    print("[fitSig] ------------------------Histogram read!-----------------------")

    x = ROOT.RooRealVar('mh', 'm_{{#gamma, {0} }} [GeV]'.format(mesonLatex[mesonCat]), xlowRange, xhighRange)

    x.setRange("full", xlowRange, xhighRange)

    data = ROOT.RooDataHist('datahist_' + mesonCat + '_' + tag + '_' + sig, 'data', ROOT.RooArgList(x), data_full)

    #Crystal ball definition --------------------------------------------------------------
    cb_mu = ROOT.RooRealVar('cb_mu_' + mesonCat + "_" + tag + '_' + sig, 'cb_mu', 124.7, 125-10., 125+10.)
    cb_sigma = ROOT.RooRealVar('cb_sigma_' + mesonCat + "_" + tag + '_' + sig, 'cb_sigma', 1.5, 0., 5.)
    cb_alphaL = ROOT.RooRealVar('cb_alphaL_' + mesonCat + "_" + tag + '_' + sig, 'cb_alphaL', 0., 5.)
    cb_alphaR = ROOT.RooRealVar('cb_alphaR_' + mesonCat + "_" + tag + '_' + sig, 'cb_alphaR', 0., 5.)
    cb_nL = ROOT.RooRealVar('cb_nL_' + mesonCat + "_" + tag + '_' + sig, 'cb_nL', 0., 50.)
    cb_nR = ROOT.RooRealVar('cb_nR_' + mesonCat + "_" + tag + '_' + sig, 'cb_nR', 0., 50.)

    pdf_crystalball = ROOT.RooDoubleCBFast('crystal_ball_' + mesonCat + "_" + tag + '_' + sig, 'crystal_ball', x, cb_mu, cb_sigma, cb_alphaL, cb_nL, cb_alphaR, cb_nR)
    model = pdf_crystalball

    fitresults = model.fitTo(data, ROOT.RooFit.Minimizer("Minuit2"), ROOT.RooFit.Strategy(2), ROOT.RooFit.Range("full"), ROOT.RooFit.Save(ROOT.kTRUE))

    # Here we will plot the results
    canvas = ROOT.TCanvas("canvas", "canvas", 1600, 1600)

    canvas.cd()
    pad1 = ROOT.TPad("Fit pad", "Fit pad", 0, 0.40, 1.0, 1.0)
    pad1.Draw()
    pad1.cd()
    title = "mH_" + mesonCat + "_" + tag + "_" + str(year)
    if regModelName is not None:
        title += "_({})".format(regModelName)
    if extraTitle is not None:
        title += "_({})".format(extraTitle)
    plotFrameWithNormRange = x.frame(ROOT.RooFit.Title(title))
    data.plotOn(plotFrameWithNormRange)
    model.plotOn(plotFrameWithNormRange, ROOT.RooFit.LineColor(2), ROOT.RooFit.Range("full"), ROOT.RooFit.NormRange("full"), ROOT.RooFit.LineStyle(10))
    model.paramOn(plotFrameWithNormRange, ROOT.RooFit.Layout(0.65, 0.99, 0.75))
    name = model.GetName() + "_Norm[mh]_Range[full]_NormRange[full]"
    chi2 = plotFrameWithNormRange.chiSquare(name, "h_" + data.GetName(), fitresults.floatParsFinal().getSize()) #name1 is name of the model, "h_" + ... is name of the hist
    plotFrameWithNormRange.getAttText().SetTextSize(0.02)
    plotFrameWithNormRange.Draw()
    data_full.GetXaxis().SetRangeUser(xlowRange, xhighRange)

    latex = ROOT.TLatex()
    latex.SetTextColor(ROOT.kRed)
    latex.SetTextSize(0.03)
    latex.SetTextAlign(12)
    latex.SetTextColor(ROOT.kRed)
    latex.SetTextAlign(12)
    latex.DrawLatexNDC(0.13, 0.865, "Crystal ball")
    latex.SetTextAlign(32)
    latex.DrawLatexNDC(0.39, 0.865, "#chi^{{2}}/ndof: {}".format(round(chi2, 2)))
    latex.SetTextColor(ROOT.kBlack)
    latex.SetTextAlign(12)
    latex.DrawLatexNDC(0.74, 0.865, "Entries:")
    latex.DrawLatexNDC(0.74, 0.825, "Mean:")
    latex.DrawLatexNDC(0.74, 0.785, "Std Dev:")
    latex.SetTextAlign(32)
    latex.DrawLatexNDC(0.89, 0.865, "{}".format(int(data_full.GetEntries())))
    latex.DrawLatexNDC(0.89, 0.825, "{}".format(round(data_full.GetMean(), 2)))
    latex.DrawLatexNDC(0.89, 0.785, "{}".format(round(data_full.GetStdDev(), 4)))

    canvas.cd()
    pad2 = ROOT.TPad("Res pad", "Res pad", 0, 0.20, 1.0, 0.40)
    pad2.Draw()
    pad2.cd()
    residualsFrame = x.frame(ROOT.RooFit.Title("Residuals"))
    hresid = plotFrameWithNormRange.residHist()
    residualsFrame.addPlotable(hresid, "P")
    residualsFrame.Draw()
    
    canvas.cd()
    pad3 = ROOT.TPad("Pull pad", "Pull pad", 0, 0, 1.0, 0.20)
    pad3.Draw()
    pad3.cd()
    pullFrame = x.frame(ROOT.RooFit.Title("Pull"))
    hpull = plotFrameWithNormRange.pullHist()
    pullFrame.addPlotable(hpull, "P")
    pullFrame.Draw()

    fileName = "~/public_html/fits/{}/{}".format(mesonCat[:-3], mesonCat)
    if regModelName is not None:
        fileName += "_" + regModelName
    if extraTitle is not None:
        fileName += "_" + extraTitle.replace(" ", "_").replace(",", "")
    canvas.SaveAs(fileName + "_fit.png")

    # Create workspace
    w = ROOT.RooWorkspace("w", "workspace")

    norm_SR = data_full.Integral(data_full.FindBin(xlowRange), data_full.FindBin(xhighRange))
    SIG_norm = ROOT.RooRealVar(model.GetName()+ "_norm", model.GetName()+ "_norm", norm_SR) # no range means constants

    # Import data and model
    cb_mu.setConstant()
    cb_sigma.setConstant()
    cb_alphaL.setConstant()
    cb_alphaR.setConstant()
    cb_nL.setConstant()
    cb_nR.setConstant()
    SIG_norm.setConstant()

    # Import model and all its components into the workspace
    print("[fitSig] ------------------------getattr(w,'import')(model)-----------------------")
    getattr(w,'import')(model)
    print("[fitSig] ------------------------getattr(w,'import')(SIG_norm)-----------------------")
    getattr(w,'import')(SIG_norm)
    print('INSIDE fitSig: integral signal value = ', norm_SR)
    print('INSIDE fitSig: integral signal = ', SIG_norm.Print())
    # Import data into the workspace
    getattr(w,'import')(data)

    # Print workspace contents
    w.Print()

    # -----------------------------------------------------------------------------
    # Save workspace in file, create folder if it does not exist
    if not os.path.exists(workspaceName):
        os.mkdir(workspaceName)

    workspaceFileName = "Sgn_" + mesonCat[:-3] + "_" + tag + "_" + str(year)
    if regModelName is not None:
        workspaceFileName += "_" + regModelName

    w.writeToFile(workspaceName + "/" + workspaceFileName + "_workspace.root")
    print('\033[1;36m' + "[fitSig] Fit done, workspace created!" + '\033[0m')


def fitSig2D(tag, mesonCat, year, date, extraTitle=None, regModelName=None):

    if regModelName == "RECO":
        regModelName = None

    verbString = "[fitSig2D] Fitting Histogram {} {} {}".format(mesonCat, cat, date)
    if regModelName is not None:
        verbString += " {}".format(regModelName)
    if extraTitle is not None:
        verbString += " {}".format(extraTitle)
    verbString += "..."
    print('\033[1;36m' + verbString + '\033[0m')

    #Read Hist file saved
    data_full = getHistoFromFile(getFullNameOfHistFile(mesonCat, cat, year, date, extraTitle=extraTitle, regModelName=regModelName, doubleFit=True))

    print("[fitSig2D] ------------------------Histogram read!-----------------------")

    ylowRange, yhighRange = doubleFitVar[mesonCat][3]

    x = ROOT.RooRealVar('mh', 'm_{{#gamma, {0} }} [GeV]'.format(mesonLatex[mesonCat]), xlowRange, xhighRange)
    y = ROOT.RooRealVar('mmeson', '{0} [GeV]'.format(doubleFitVar[mesonCat][2]), ylowRange, yhighRange)

    x.setRange("full", xlowRange, xhighRange)
    y.setRange("full", ylowRange, yhighRange)

    data = ROOT.RooDataHist('datahist_' + mesonCat + '_' + tag + '_' + sig, 'data', ROOT.RooArgList(x, y), data_full)

    #Crystal ball definition (Higgs mass) --------------------------------------------------------------
    cb_mh_mu = ROOT.RooRealVar('cb_mh_mu_' + mesonCat + "_" + tag + '_' + sig, 'cb_mh_mu', 124.7, 125-10., 125+10.)
    cb_mh_sigma = ROOT.RooRealVar('cb_mh_sigma_' + mesonCat + "_" + tag + '_' + sig, 'cb_mh_sigma', 1.5, 0., 5.)
    cb_mh_alphaL = ROOT.RooRealVar('cb_mh_alphaL_' + mesonCat + "_" + tag + '_' + sig, 'cb_mh_alphaL', 0., 5.)
    cb_mh_alphaR = ROOT.RooRealVar('cb_mh_alphaR_' + mesonCat + "_" + tag + '_' + sig, 'cb_mh_alphaR', 0., 5.)
    cb_mh_nL = ROOT.RooRealVar('cb_mh_nL_' + mesonCat + "_" + tag + '_' + sig, 'cb_mh_nL', 0., 50.)
    cb_mh_nR = ROOT.RooRealVar('cb_mh_nR_' + mesonCat + "_" + tag + '_' + sig, 'cb_mh_nR', 0., 50.)
     #Crystal ball definition (Meson mass) --------------------------------------------------------------
    cb_mm_mu = ROOT.RooRealVar('cb_mm_mu_' + mesonCat + "_" + tag + '_' + sig, 'cb_mm_mu', doubleFitVar[mesonCat][4], ylowRange, yhighRange)
    cb_mm_sigma = ROOT.RooRealVar('cb_mm_sigma_' + mesonCat + "_" + tag + '_' + sig, 'cb_mm_sigma', 0.03, 0., 0.5)
    cb_mm_alphaL = ROOT.RooRealVar('cb_mm_alphaL_' + mesonCat + "_" + tag + '_' + sig, 'cb_mm_alphaL', 0., 3.)
    cb_mm_alphaR = ROOT.RooRealVar('cb_mm_alphaR_' + mesonCat + "_" + tag + '_' + sig, 'cb_mm_alphaR', 0., 3.)
    cb_mm_nL = ROOT.RooRealVar('cb_mm_nL_' + mesonCat + "_" + tag + '_' + sig, 'cb_mm_nL', 0., 30.)
    cb_mm_nR = ROOT.RooRealVar('cb_mm_nR_' + mesonCat + "_" + tag + '_' + sig, 'cb_mm_nR', 0., 10.)

    pdf_crystalball_mh = ROOT.RooDoubleCBFast('crystal_ball_' + mesonCat + "_" + tag + '_' + sig + "_mh", 'crystal_ball_mh', x, cb_mh_mu, cb_mh_sigma, cb_mh_alphaL, cb_mh_nL, cb_mh_alphaR, cb_mh_nR)
    pdf_crystalball_mm = ROOT.RooDoubleCBFast('crystal_ball_' + mesonCat + "_" + tag + '_' + sig + "_mm", 'crystal_ball_mm', y, cb_mm_mu, cb_mm_sigma, cb_mm_alphaL, cb_mm_nL, cb_mm_alphaR, cb_mm_nR)
    model2D = ROOT.RooProdPdf("pdf_2d_signal_" + mesonCat + "_" + tag + '_' + sig, "pdf_2d_signal", ROOT.RooArgList(pdf_crystalball_mh, pdf_crystalball_mm))

    fitresults = model2D.fitTo(data, ROOT.RooFit.Minimizer("Minuit2"), ROOT.RooFit.Strategy(2), ROOT.RooFit.Range("full"), ROOT.RooFit.Save(ROOT.kTRUE))
    
    # Here we will plot the results
    # Projection of the HiggsCandMass
    canvasMH = ROOT.TCanvas("canvasMH", "canvasMH", 1600, 1600)

    canvasMH.cd()
    pad1 = ROOT.TPad("Fit pad", "Fit pad", 0, 0.40, 1.0, 1.0)
    pad1.Draw()
    pad1.cd()
    titleMH = "mH_" + mesonCat + "_" + tag + "_" + str(year)
    if regModelName is not None:
        titleMH += "_({})".format(regModelName)
    if extraTitle is not None:
        titleMH += "_({})".format(extraTitle)
    plotFrameWithNormRangeMH = x.frame(ROOT.RooFit.Title(titleMH))
    data.plotOn(plotFrameWithNormRangeMH)
    model2D.plotOn(plotFrameWithNormRangeMH, ROOT.RooFit.LineColor(2), ROOT.RooFit.Range("full"), ROOT.RooFit.NormRange("full"), ROOT.RooFit.LineStyle(10))
    model2D.paramOn(plotFrameWithNormRangeMH, ROOT.RooFit.Layout(0.65, 0.99, 0.75))
    print(plotFrameWithNormRangeMH.Print("V"))
    name = model2D.GetName() + "_Int[mmeson]_Norm[mh,mmeson]_Range[full]_NormRange[full]"
    chi2 = plotFrameWithNormRangeMH.chiSquare(name, "h_" + data.GetName(), fitresults.floatParsFinal().getSize()) #name1 is name of the model, "h_" + ... is name of the hist
    plotFrameWithNormRangeMH.getAttText().SetTextSize(0.02)
    plotFrameWithNormRangeMH.Draw()
    data_full.GetXaxis().SetRangeUser(xlowRange, xhighRange)

    latexMH = ROOT.TLatex()
    latexMH.SetTextColor(ROOT.kRed)
    latexMH.SetTextSize(0.03)
    latexMH.SetTextAlign(12)
    latexMH.SetTextColor(ROOT.kRed)
    latexMH.SetTextAlign(12)
    latexMH.DrawLatexNDC(0.13, 0.865, "Crystal ball")
    latexMH.SetTextAlign(32)
    latexMH.DrawLatexNDC(0.39, 0.865, "#chi^{{2}}/ndof: {}".format(round(chi2, 2)))
    latexMH.SetTextColor(ROOT.kBlack)
    latexMH.SetTextAlign(12)
    latexMH.DrawLatexNDC(0.74, 0.865, "Entries:")
    latexMH.DrawLatexNDC(0.74, 0.825, "Mean:")
    latexMH.DrawLatexNDC(0.74, 0.785, "Std Dev:")
    latexMH.SetTextAlign(32)
    latexMH.DrawLatexNDC(0.89, 0.865, "{}".format(int(data_full.GetEntries())))
    latexMH.DrawLatexNDC(0.89, 0.825, "{}".format(round(data_full.GetMean(1), 2)))
    latexMH.DrawLatexNDC(0.89, 0.785, "{}".format(round(data_full.GetStdDev(1), 4)))

    canvasMH.cd()
    pad2 = ROOT.TPad("Res pad", "Res pad", 0, 0.20, 1.0, 0.40)
    pad2.Draw()
    pad2.cd()
    residualsFrame = x.frame(ROOT.RooFit.Title("Residuals"))
    hresid = plotFrameWithNormRangeMH.residHist()
    residualsFrame.addPlotable(hresid, "P")
    residualsFrame.Draw()
    
    canvasMH.cd()
    pad3 = ROOT.TPad("Pull pad", "Pull pad", 0, 0, 1.0, 0.20)
    pad3.Draw()
    pad3.cd()
    pullFrame = x.frame(ROOT.RooFit.Title("Pull"))
    hpull = plotFrameWithNormRangeMH.pullHist()
    pullFrame.addPlotable(hpull, "P")
    pullFrame.Draw()

    fileName = "~/public_html/fits/{}/{}".format(mesonCat[:-3], mesonCat)
    if regModelName is not None:
        fileName += "_" + regModelName
    if extraTitle is not None:
        fileName += "_" + extraTitle.replace(" ", "_").replace(",", "")
    canvasMH.SaveAs(fileName + "_2Dfit_MH.png")

    # Projection of the MesonMass
    canvasMM = ROOT.TCanvas("canvasMM", "canvasMM", 1600, 1600)

    canvasMM.cd()
    pad1 = ROOT.TPad("Fit pad", "Fit pad", 0, 0.40, 1.0, 1.0)
    pad1.Draw()
    pad1.cd()
    titleMM = "mM_" + mesonCat + "_" + tag + "_" + str(year)
    if regModelName is not None:
        titleMM += "_({})".format(regModelName)
    if extraTitle is not None:
        titleMM += "_({})".format(extraTitle)
    plotFrameWithNormRangeMM = y.frame(ROOT.RooFit.Title(titleMM))
    data.plotOn(plotFrameWithNormRangeMM)
    model2D.plotOn(plotFrameWithNormRangeMM, ROOT.RooFit.LineColor(2), ROOT.RooFit.Range("full"), ROOT.RooFit.NormRange("full"), ROOT.RooFit.LineStyle(10))
    model2D.paramOn(plotFrameWithNormRangeMM, ROOT.RooFit.Layout(0.65, 0.99, 0.75))
    print(plotFrameWithNormRangeMM.Print("V"))
    name = model2D.GetName() + "_Int[mh]_Norm[mh,mmeson]_Range[full]_NormRange[full]"
    chi2 = plotFrameWithNormRangeMM.chiSquare(name, "h_" + data.GetName(), fitresults.floatParsFinal().getSize()) #name1 is name of the model, "h_" + ... is name of the hist
    plotFrameWithNormRangeMM.getAttText().SetTextSize(0.02)
    plotFrameWithNormRangeMM.Draw()
    data_full.GetYaxis().SetRangeUser(ylowRange, yhighRange)

    latexMM = ROOT.TLatex()
    latexMM.SetTextColor(ROOT.kRed)
    latexMM.SetTextSize(0.03)
    latexMM.SetTextAlign(12)
    latexMM.SetTextColor(ROOT.kRed)
    latexMM.SetTextAlign(12)
    latexMM.DrawLatexNDC(0.13, 0.865, "Crystal ball")
    latexMM.SetTextAlign(32)
    latexMM.DrawLatexNDC(0.39, 0.865, "#chi^{{2}}/ndof: {}".format(round(chi2, 2)))
    latexMM.SetTextColor(ROOT.kBlack)
    latexMM.SetTextAlign(12)
    latexMM.DrawLatexNDC(0.74, 0.865, "Entries:")
    latexMM.DrawLatexNDC(0.74, 0.825, "Mean:")
    latexMM.DrawLatexNDC(0.74, 0.785, "Std Dev:")
    latexMM.SetTextAlign(32)
    latexMM.DrawLatexNDC(0.89, 0.865, "{}".format(int(data_full.GetEntries())))
    latexMM.DrawLatexNDC(0.89, 0.825, "{}".format(round(data_full.GetMean(2), 2)))
    latexMM.DrawLatexNDC(0.89, 0.785, "{}".format(round(data_full.GetStdDev(2), 4)))

    canvasMM.cd()
    pad2 = ROOT.TPad("Res pad", "Res pad", 0, 0.20, 1.0, 0.40)
    pad2.Draw()
    pad2.cd()
    residualsFrame = y.frame(ROOT.RooFit.Title("Residuals"))
    hresid = plotFrameWithNormRangeMM.residHist()
    residualsFrame.addPlotable(hresid, "P")
    residualsFrame.Draw()
    
    canvasMM.cd()
    pad3 = ROOT.TPad("Pull pad", "Pull pad", 0, 0, 1.0, 0.20)
    pad3.Draw()
    pad3.cd()
    pullFrame = y.frame(ROOT.RooFit.Title("Pull"))
    hpull = plotFrameWithNormRangeMM.pullHist()
    pullFrame.addPlotable(hpull, "P")
    pullFrame.Draw()

    fileName = "~/public_html/fits/{}/{}".format(mesonCat[:-3], mesonCat)
    if regModelName is not None:
        fileName += "_" + regModelName
    if extraTitle is not None:
        fileName += "_" + extraTitle.replace(" ", "_").replace(",", "")
    canvasMM.SaveAs(fileName + "_2Dfit_MM.png")

    # Create workspace
    w = ROOT.RooWorkspace("w", "workspace")

    norm_SR = data_full.Integral(data_full.GetXaxis().FindBin(xlowRange), data_full.GetXaxis().FindBin(xhighRange), data_full.GetYaxis().FindBin(ylowRange), data_full.GetYaxis().FindBin(yhighRange))
    SIG_norm = ROOT.RooRealVar(model2D.GetName()+ "_norm", model2D.GetName()+ "_norm", norm_SR) # no range means constants

    # Import data and model
    cb_mh_mu.setConstant()
    cb_mh_sigma.setConstant()
    cb_mh_alphaL.setConstant()
    cb_mh_alphaR.setConstant()
    cb_mh_nL.setConstant()
    cb_mh_nR.setConstant()
    cb_mm_mu.setConstant()
    cb_mm_sigma.setConstant()
    cb_mm_alphaL.setConstant()
    cb_mm_alphaR.setConstant()
    cb_mm_nL.setConstant()
    cb_mm_nR.setConstant()
    SIG_norm.setConstant()

    # Import model and all its components into the workspace
    print("[fitSig2D] ------------------------getattr(w,'import')(model)-----------------------")
    getattr(w,'import')(model2D)
    print("[fitSig2D] ------------------------getattr(w,'import')(SIG_norm)-----------------------")
    getattr(w,'import')(SIG_norm)
    print('INSIDE fitSig2D: integral signal value = ', norm_SR)
    print('INSIDE fitSig2D: integral signal = ', SIG_norm.Print())
    # Import data into the workspace
    getattr(w,'import')(data)

    # Print workspace contents
    w.Print()

    # -----------------------------------------------------------------------------
    # Save workspace in file, create folder if it does not exist
    if not os.path.exists(workspaceName):
        os.mkdir(workspaceName)

    workspaceFileName = "Sgn_" + mesonCat[:-3] + "_" + tag + "_" + str(year)
    if regModelName is not None:
        workspaceFileName += "_" + regModelName

    w.writeToFile(workspaceName + "/" + workspaceFileName + "_2D_workspace.root")
    print('\033[1;36m' + "[fitSig2D] Fit done, workspace created!" + '\033[0m')


if __name__ == "__main__":

    cat = "GFcat"
    year = 2018
    date = "OCT27"


    #D0Star----------------------------------------------------------------------------------------
    '''
    extraTitle = "barrel meson"
    fitSig(cat, mesonCat, year, date, extraTitle=extraTitle)
    extraTitle = "barrel photon"
    fitSig(cat, mesonCat, year, date, extraTitle=extraTitle)
    extraTitle = "barrel meson, barrel photon"
    fitSig(cat, mesonCat, year, date, extraTitle=extraTitle)
    extraTitle = "endcap meson, barrel photon"
    fitSig(cat, mesonCat, year, date, extraTitle=extraTitle)
    extraTitle = "barrel meson, endcap photon"
    fitSig(cat, mesonCat, year, date, extraTitle=extraTitle)
    extraTitle = "endcap meson, endcap photon"
    fitSig(cat, mesonCat, year, date, extraTitle=extraTitle)
    date = "JUN21"
    extraTitle = "missing photon"
    fitSig(cat, mesonCat, year, date, extraTitle=extraTitle)
    extraTitle = "missing pion"
    fitSig(cat, mesonCat, year, date, extraTitle=extraTitle)

    '''
    #Phi3------------------------------------------------------------------------------------------
    df = False
    mesonCat = "Phi3Cat"
    #mesonCat = "OmegaCat"
    #mesonCat = "D0StarCat"
    for mesonCat in ["Phi3Cat", "OmegaCat", "D0StarCat", "D0StarRhoCat"]:
    #for mesonCat in ["Phi3Cat"]:
        with open('models_{}.txt'.format(mesonCat[:-3]), 'r') as file:
            for line in file:
                regModelName = line.strip()
                if regModelName[0] != "#":
                    fitSig(cat, mesonCat, year, date, regModelName=regModelName)
                    #fitSig2D(cat, mesonCat, year, date, regModelName=regModelName)
        #fitSig(cat, mesonCat, year, date)

    '''
    extraTitle = "barrel meson"
    fitSig(cat, mesonCat, year, date, extraTitle=extraTitle)
    extraTitle = "barrel photon"
    fitSig(cat, mesonCat, year, date, extraTitle=extraTitle)
    extraTitle = "barrel meson, barrel photon"
    fitSig(cat, mesonCat, year, date, extraTitle=extraTitle)
    extraTitle = "endcap meson, barrel photon"
    fitSig(cat, mesonCat, year, date, extraTitle=extraTitle)
    extraTitle = "barrel meson, endcap photon"
    fitSig(cat, mesonCat, year, date, extraTitle=extraTitle)
    extraTitle = "endcap meson, endcap photon"
    fitSig(cat, mesonCat, year, date, extraTitle=extraTitle)
    '''