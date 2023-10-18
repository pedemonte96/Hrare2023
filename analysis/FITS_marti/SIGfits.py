import ROOT
from prepareFits import *

ROOT.gROOT.SetBatch()
ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit.so")

xlowRange = 100.
xhighRange = 150.

sig = "ggH"
workspaceName = 'WS_SEP25'

def fitSig(tag, mesonCat, year, date, extraTitle=None, regModelName=None, doubleFit=False):

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

    if not doubleFit:#set workspace when not double fit
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
        print('INSIDE fitSig: integral signal = ',SIG_norm.Print())
        # Import data into the workspace
        getattr(w,'import')(data)

    #2Dfit---------------------------------------------------------------------------
    else:
        #Read Hist file saved
        data_full_doubleFit = getHistoFromFile(getFullNameOfHistFile(mesonCat, cat, year, date, doubleFit=doubleFit))
        print("[fitSig2D] ------------------------Histogram read!-----------------------")

        xlow2D, xhigh2D = doubleFitVar[mesonCat][3]

        x_doubleFit = ROOT.RooRealVar('m_meson', '{} [GeV]'.format(doubleFitVar[mesonCat][2]), xlow2D, xhigh2D)

        x_doubleFit.setRange("full", xlow2D, xhigh2D)

        data_doubleFit = ROOT.RooDataHist('datahist_' + mesonCat + '_' + tag + '_' + sig + "_doubleFit", 'data_doubleFit', ROOT.RooArgList(x_doubleFit), data_full_doubleFit)

        #Crystal ball definition --------------------------------------------------------------
        cb_mu_doubleFit = ROOT.RooRealVar('cb_mu_' + mesonCat + "_" + tag + '_' + sig + "_doubleFit", 'cb_mu_doubleFit', doubleFitVar[mesonCat][4], xlow2D, xhigh2D)
        cb_sigma_doubleFit = ROOT.RooRealVar('cb_sigma_' + mesonCat + "_" + tag + '_' + sig + "_doubleFit", 'cb_sigma_doubleFit', 0.03, 0., 0.5)
        cb_alphaL_doubleFit = ROOT.RooRealVar('cb_alphaL_' + mesonCat + "_" + tag + '_' + sig + "_doubleFit", 'cb_alphaL_doubleFit', 0., 3.)
        cb_alphaR_doubleFit = ROOT.RooRealVar('cb_alphaR_' + mesonCat + "_" + tag + '_' + sig + "_doubleFit", 'cb_alphaR_doubleFit', 0., 3.)
        cb_nL_doubleFit = ROOT.RooRealVar('cb_nL_' + mesonCat + "_" + tag + '_' + sig + "_doubleFit", 'cb_nL_doubleFit', 0., 30.)
        cb_nR_doubleFit = ROOT.RooRealVar('cb_nR_' + mesonCat + "_" + tag + '_' + sig + "_doubleFit", 'cb_nR_doubleFit', 0., 10.)

        pdf_crystalball_doubleFit = ROOT.RooDoubleCBFast('crystal_ball_' + mesonCat + "_" + tag + '_' + sig + "_doubleFit", 'crystal_ball_DF', x_doubleFit, cb_mu_doubleFit, cb_sigma_doubleFit, cb_alphaL_doubleFit, cb_nL_doubleFit, cb_alphaR_doubleFit, cb_nR_doubleFit)
        model_doubleFit = pdf_crystalball_doubleFit

        fitresults_doubleFit = model_doubleFit.fitTo(data_doubleFit, ROOT.RooFit.Minimizer("Minuit2"), ROOT.RooFit.Strategy(2), ROOT.RooFit.Range("full"), ROOT.RooFit.Save(ROOT.kTRUE))

        # Here we will plot the results
        canvas_doubleFit = ROOT.TCanvas("canvas_doubleFit", "canvas_doubleFit", 1600, 1600)

        canvas_doubleFit.cd()
        pad1_doubleFit = ROOT.TPad("Fit pad", "Fit pad", 0, 0.40, 1.0, 1.0)
        pad1_doubleFit.Draw()
        pad1_doubleFit.cd()
        title_doubleFit = "mMeson_" + mesonCat + "_" + tag + "_" + str(year)
        plotFrameWithNormRange_doubleFit = x_doubleFit.frame(ROOT.RooFit.Title(title_doubleFit))
        data_doubleFit.plotOn(plotFrameWithNormRange_doubleFit)
        model_doubleFit.plotOn(plotFrameWithNormRange_doubleFit, ROOT.RooFit.LineColor(2), ROOT.RooFit.Range("full"), ROOT.RooFit.NormRange("full"), ROOT.RooFit.LineStyle(10))
        model_doubleFit.paramOn(plotFrameWithNormRange_doubleFit, ROOT.RooFit.Layout(0.65, 0.99, 0.75))
        name_doubleFit = model_doubleFit.GetName() + "_Norm[m_meson]_Range[full]_NormRange[full]"
        chi2_doubleFit = plotFrameWithNormRange_doubleFit.chiSquare(name_doubleFit, "h_" + data_doubleFit.GetName(), fitresults_doubleFit.floatParsFinal().getSize()) #name1 is name of the model, "h_" + ... is name of the hist
        plotFrameWithNormRange_doubleFit.getAttText().SetTextSize(0.02)
        plotFrameWithNormRange_doubleFit.Draw()
        data_full_doubleFit.GetXaxis().SetRangeUser(xlow2D, xhigh2D)

        latex_doubleFit = ROOT.TLatex()
        latex_doubleFit.SetTextColor(ROOT.kRed)
        latex_doubleFit.SetTextSize(0.03)
        latex_doubleFit.SetTextAlign(12)
        latex_doubleFit.SetTextColor(ROOT.kRed)
        latex_doubleFit.SetTextAlign(12)
        latex_doubleFit.DrawLatexNDC(0.13, 0.865, "Crystal ball")
        latex_doubleFit.SetTextAlign(32)
        latex_doubleFit.DrawLatexNDC(0.39, 0.865, "#chi^{{2}}/ndof: {}".format(round(chi2_doubleFit, 2)))
        latex_doubleFit.SetTextColor(ROOT.kBlack)
        latex_doubleFit.SetTextAlign(12)
        latex_doubleFit.DrawLatexNDC(0.74, 0.865, "Entries:")
        latex_doubleFit.DrawLatexNDC(0.74, 0.825, "Mean:")
        latex_doubleFit.DrawLatexNDC(0.74, 0.785, "Std Dev:")
        latex_doubleFit.SetTextAlign(32)
        latex_doubleFit.DrawLatexNDC(0.89, 0.865, "{}".format(int(data_full_doubleFit.GetEntries())))
        latex_doubleFit.DrawLatexNDC(0.89, 0.825, "{}".format(round(data_full_doubleFit.GetMean(), 2)))
        latex_doubleFit.DrawLatexNDC(0.89, 0.785, "{}".format(round(data_full_doubleFit.GetStdDev(), 4)))

        canvas_doubleFit.cd()
        pad2_doubleFit = ROOT.TPad("Res pad", "Res pad", 0, 0.20, 1.0, 0.40)
        pad2_doubleFit.Draw()
        pad2_doubleFit.cd()
        residualsFrame_doubleFit = x_doubleFit.frame(ROOT.RooFit.Title("Residuals"))
        hresid_doubleFit = plotFrameWithNormRange_doubleFit.residHist()
        residualsFrame_doubleFit.addPlotable(hresid_doubleFit, "P")
        residualsFrame_doubleFit.Draw()
        
        canvas_doubleFit.cd()
        pad3_doubleFit = ROOT.TPad("Pull pad", "Pull pad", 0, 0, 1.0, 0.20)
        pad3_doubleFit.Draw()
        pad3_doubleFit.cd()
        pullFrame_doubleFit = x_doubleFit.frame(ROOT.RooFit.Title("Pull"))
        hpull_doubleFit = plotFrameWithNormRange_doubleFit.pullHist()
        pullFrame_doubleFit.addPlotable(hpull_doubleFit, "P")
        pullFrame_doubleFit.Draw()

        fileName_doubleFit = "~/public_html/fits/{}/{}".format(mesonCat[:-3], mesonCat)
        canvas_doubleFit.SaveAs(fileName_doubleFit + "_fit_2D.png")

        #Create 2D model
        pdf_2D = ROOT.RooProdPdf("pdf_2D_sgn", "", ROOT.RooArgList(model, model_doubleFit))

        #set workspace with double fit
        norm_SR = data_full.Integral(data_full.FindBin(xlowRange), data_full.FindBin(xhighRange))
        SIG_norm = ROOT.RooRealVar(pdf_2D.GetName()+ "_norm", pdf_2D.GetName()+ "_norm", norm_SR) # no range means constants

        # Import data and model
        cb_mu.setConstant()
        cb_sigma.setConstant()
        cb_alphaL.setConstant()
        cb_alphaR.setConstant()
        cb_nL.setConstant()
        cb_nR.setConstant()
        SIG_norm.setConstant()

        cb_mu_doubleFit.setConstant()
        cb_sigma_doubleFit.setConstant()
        cb_alphaL_doubleFit.setConstant()
        cb_alphaR_doubleFit.setConstant()
        cb_nL_doubleFit.setConstant()
        cb_nR_doubleFit.setConstant()

        # Import model and all its components into the workspace
        print("[fitSig] ------------------------getattr(w,'import')(model)-----------------------")
        getattr(w,'import')(pdf_2D)
        print("[fitSig] ------------------------getattr(w,'import')(SIG_norm)-----------------------")
        getattr(w,'import')(SIG_norm)
        print('INSIDE fitSig: integral signal = ',SIG_norm.Print())
        # Import data into the workspace
        getattr(w,'import')(data)
        getattr(w,'import')(data_doubleFit)


    # Print workspace contents for 1D/2D
    w.Print()

    # -----------------------------------------------------------------------------
    # Save workspace in file, create folder if it does not exist
    if not os.path.exists(workspaceName):
        os.mkdir(workspaceName)

    workspaceFileName = "Sgn_" + mesonCat[:-3] + "_" + tag + "_" + str(year)
    if regModelName is not None:
        workspaceFileName += "_" + regModelName

    w.writeToFile(workspaceName + "/" + workspaceFileName + "_workspace.root")#same name as 2D
    print('\033[1;36m' + "[fitSig] Fit done, workspace created!" + '\033[0m')


if __name__ == "__main__":

    cat = "GFcat"
    year = 2018
    date = "SEP25"


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
    for mesonCat in ["Phi3Cat", "OmegaCat", "D0StarCat"]:
        with open('models_{}.txt'.format(mesonCat[:-3]), 'r') as file:
            for line in file:
                regModelName = line.strip()
                if regModelName[0] != "#":
                    fitSig(cat, mesonCat, year, date, regModelName=regModelName, doubleFit=df)
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