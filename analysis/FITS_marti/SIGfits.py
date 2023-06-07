import ROOT
from prepareFits import *

ROOT.gROOT.SetBatch()
ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit.so")

xlowRange = 100.
xhighRange = 150.

numDictSignal = {"OmegaCat": 1037, "D0StarCat": 1039, "Phi3Cat": 1040}

mesonLatex = {"OmegaCat": "#omega", "D0StarCat": "D^{0*}", "Phi3Cat": "#phi"}

sig = "ggH"

#x = ROOT.RooRealVar('mh', 'm_{#gamma,meson}', xlowRange, xhighRange)

#x.setRange("full", xlowRange, xhighRange)
#x.setRange("left", xlowRange, 115)
#x.setRange("right", 135, xhighRange)


def fitSig(tag, mesonCat, year):

    print("Main fitSignal")

    data_full = getHisto(200*10, 0., 200., numDictSignal[mesonCat], tag, mesonCat, year)

    x = ROOT.RooRealVar('mh', 'm_{{#gamma, {0} }}'.format(mesonLatex[mesonCat]), xlowRange, xhighRange)

    x.setRange("full", xlowRange, xhighRange)

    data = ROOT.RooDataHist('datahist' + tag + '_' + sig, 'data', ROOT.RooArgList(x), data_full)

    cb_mu = ROOT.RooRealVar('cb_mu_' + mesonCat + "_" + tag + '_' + sig, 'cb_mu', 125., 125-10., 125+10.)
    cb_sigma = ROOT.RooRealVar('cb_sigma_' + mesonCat + "_" + tag + '_' + sig, 'cb_sigma', 0., 5.)
    cb_alphaL = ROOT.RooRealVar('cb_alphaL_' + mesonCat + "_" + tag + '_' + sig, 'cb_alphaL', 0., 5.)
    cb_alphaR = ROOT.RooRealVar('cb_alphaR_' + mesonCat + "_" + tag + '_' + sig, 'cb_alphaR', 0., 5.)
    cb_nL = ROOT.RooRealVar('cb_nL_' + mesonCat + "_" + tag + '_' + sig, 'cb_nL', 0., 20.)
    cb_nR = ROOT.RooRealVar('cb_nR_' + mesonCat + "_" + tag + '_' + sig, 'cb_nR', 0., 20.)

    pdf_crystalball = ROOT.RooDoubleCBFast('crystal_ball' + mesonCat + "_" + tag + '_' + sig, 'crystal_ball', x, cb_mu, cb_sigma, cb_alphaL, cb_nL, cb_alphaR, cb_nR)
    model = pdf_crystalball

    model.fitTo(data, ROOT.RooFit.Minimizer("Minuit2"), ROOT.RooFit.Strategy(2), ROOT.RooFit.Range("full"))

    # Here we will plot the results
    canvas = ROOT.TCanvas("canvas", "canvas", 1600, 1600)

    canvas.cd()
    pad1 = ROOT.TPad("Fit pad", "Fit pad", 0, 0.40, 1.0, 1.0)
    pad1.Draw()
    pad1.cd()
    plotFrameWithNormRange = x.frame(ROOT.RooFit.Title("mH_" + mesonCat + "_" + tag + "_" + str(year)))
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

    canvas.SaveAs("~/public_html/fits/{}_fit.png".format(mesonCat))

    canvas2 = ROOT.TCanvas("canvas2", "canvas2", 1200, 800)
    data_full.Draw("hist")
    data_full.GetXaxis().SetRangeUser(xlowRange, xhighRange)
    canvas2.SaveAs("~/public_html/fits/{}.png".format(mesonCat))


if __name__ == "__main__":
    print("Main sigfits")
    fitSig('GFcat', 'D0StarCat', 2018)
    fitSig('GFcat', 'Phi3Cat', 2018)
