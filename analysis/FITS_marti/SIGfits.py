import ROOT
from prepareFits import *

ROOT.gROOT.SetBatch()
ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit.so")

xlowRange = 100.
xhighRange = 150.

sig = "ggH"
workspaceName = 'WS_AUG24'

def fitSig(tag, mesonCat, year, date, extraTitle=None, regModelName=None):

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
    cb_mu = ROOT.RooRealVar('cb_mu_' + mesonCat + "_" + tag + '_' + sig, 'cb_mu', 125., 125-10., 125+10.)
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

    # -------------------------------------------------------------

    w = ROOT.RooWorkspace("w", "workspace")

    norm_SR = data_full.Integral(data_full.FindBin(xlowRange), data_full.FindBin(xhighRange))
    SIG_norm = ROOT.RooRealVar(model.GetName()+ "_norm", model.GetName()+ "_norm", norm_SR) # no range means constants

    # -----------------------------------------------------------------------------
    # Create workspace, import data and model

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


if __name__ == "__main__":

    cat = "GFcat"
    year = 2018
    date = "AUG24"


    #D0Star----------------------------------------------------------------------------------------
    mesonCat = "D0StarCat"
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
    date = "JUN21"
    extraTitle = "missing photon"
    fitSig(cat, mesonCat, year, date, extraTitle=extraTitle)
    extraTitle = "missing pion"
    fitSig(cat, mesonCat, year, date, extraTitle=extraTitle)

    '''
    #Phi3------------------------------------------------------------------------------------------
    mesonCat = "Phi3Cat"
    regModelName = "BDTG_df15_dl511_v7_v46"
    fitSig(cat, mesonCat, year, date, regModelName=regModelName)
    regModelName = "BDTG_df15_dl511_v0"
    fitSig(cat, mesonCat, year, date, regModelName=regModelName)
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