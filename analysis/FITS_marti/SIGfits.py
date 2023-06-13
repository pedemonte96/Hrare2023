import ROOT
from prepareFits import *

ROOT.gROOT.SetBatch()
ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit.so")

xlowRange = 100.
xhighRange = 150.

sig = "ggH"


def fitSig(tag, mesonCat, year, date, extraTitle=None):

    print("[fitSig] Fitting Histogram {} {} {}...".format(mesonCat, cat, extraTitle))

    #Read Hist file saved

    data_full = getHistoFromFile(getFullNameOfHistFile(mesonCat, tag, year, date, extraTitle=extraTitle))
    print("[fitSig] ------------------------Histogram read!-----------------------")

    x = ROOT.RooRealVar('mh', 'm_{{#gamma, {0} }} [GeV]'.format(mesonLatex[mesonCat]), xlowRange, xhighRange)

    x.setRange("full", xlowRange, xhighRange)

    data = ROOT.RooDataHist('datahist' + tag + '_' + sig, 'data', ROOT.RooArgList(x), data_full)

    cb_mu = ROOT.RooRealVar('cb_mu_' + mesonCat + "_" + tag + '_' + sig, 'cb_mu', 125., 125-10., 125+10.)
    cb_sigma = ROOT.RooRealVar('cb_sigma_' + mesonCat + "_" + tag + '_' + sig, 'cb_sigma', 0., 5.)
    cb_alphaL = ROOT.RooRealVar('cb_alphaL_' + mesonCat + "_" + tag + '_' + sig, 'cb_alphaL', 0., 5.)
    cb_alphaR = ROOT.RooRealVar('cb_alphaR_' + mesonCat + "_" + tag + '_' + sig, 'cb_alphaR', 0., 5.)
    cb_nL = ROOT.RooRealVar('cb_nL_' + mesonCat + "_" + tag + '_' + sig, 'cb_nL', 0., 20.)
    cb_nR = ROOT.RooRealVar('cb_nR_' + mesonCat + "_" + tag + '_' + sig, 'cb_nR', 0., 20.)

    pdf_crystalball = ROOT.RooDoubleCBFast('crystal_ball_' + mesonCat + "_" + tag + '_' + sig, 'crystal_ball', x, cb_mu, cb_sigma, cb_alphaL, cb_nL, cb_alphaR, cb_nR)
    model = pdf_crystalball

    model.fitTo(data, ROOT.RooFit.Minimizer("Minuit2"), ROOT.RooFit.Strategy(2), ROOT.RooFit.Range("full"))

    # Here we will plot the results
    canvas = ROOT.TCanvas("canvas", "canvas", 1600, 1600)

    canvas.cd()
    pad1 = ROOT.TPad("Fit pad", "Fit pad", 0, 0.40, 1.0, 1.0)
    pad1.Draw()
    pad1.cd()
    title = "mH_" + mesonCat + "_" + tag + "_" + str(year)
    if extraTitle is not None:
        title += "_({})".format(extraTitle)
    plotFrameWithNormRange = x.frame(ROOT.RooFit.Title(title))
    data.plotOn(plotFrameWithNormRange)
    model.plotOn(plotFrameWithNormRange, ROOT.RooFit.LineColor(2), ROOT.RooFit.Range("full"), ROOT.RooFit.NormRange("full"), ROOT.RooFit.LineStyle(10))
    model.paramOn(plotFrameWithNormRange, ROOT.RooFit.Layout(0.65, 0.99, 0.75))
    plotFrameWithNormRange.getAttText().SetTextSize(0.02)
    plotFrameWithNormRange.Draw()

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

    fileName = "~/public_html/fits/{}/{}_fit.png".format(mesonCat[:-3], mesonCat)
    if extraTitle is not None:
        fileName = fileName[:-4] + "_" + extraTitle.replace(" ", "_").replace(",", "") + fileName[-4:]
    canvas.SaveAs(fileName)

    canvas2 = ROOT.TCanvas("canvas2", "canvas2", 1200, 800)
    data_full.Draw("hist")
    data_full.GetXaxis().SetRangeUser(xlowRange, xhighRange)
    fileName2 = "~/public_html/fits/{}/{}.png".format(mesonCat[:-3], mesonCat)
    if extraTitle is not None:
        fileName2 = fileName2[:-4] + "_" + extraTitle.replace(" ", "_").replace(",", "") + fileName2[-4:]
    canvas2.SaveAs(fileName2)


if __name__ == "__main__":
    print("Main SGNfits")

    cat = "GFcat"
    year = 2018
    date = "JUN07"

    mesonCat = "D0StarCat"
    fitSig(cat, mesonCat, year, date)
    extraTitle = "barrel meson, barrel photon"
    fitSig(cat, mesonCat, year, date, extraTitle=extraTitle)
    extraTitle = "endcap meson, barrel photon"
    fitSig(cat, mesonCat, year, date, extraTitle=extraTitle)
    extraTitle = "barrel meson, endcap photon"
    fitSig(cat, mesonCat, year, date, extraTitle=extraTitle)
    extraTitle = "endcap meson, endcap photon"
    fitSig(cat, mesonCat, year, date, extraTitle=extraTitle)
    extraTitle = "barrel meson"
    fitSig(cat, mesonCat, year, date, extraTitle=extraTitle)
    extraTitle = "barrel photon"
    fitSig(cat, mesonCat, year, date, extraTitle=extraTitle)


    mesonCat = "Phi3Cat"
    fitSig(cat, mesonCat, year, date)
