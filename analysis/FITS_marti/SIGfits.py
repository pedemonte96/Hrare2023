import ROOT
from prepareFits import *

gROOT.SetBatch()
gSystem.Load("libHiggsAnalysisCombinedLimit.so")

xlowRange = 100.
xhighRange = 170.

x = ROOT.RooRealVar('mh', 'm_{#gamma,meson}', xlowRange, xhighRange)

x.setRange("full", xlowRange, xhighRange)
x.setRange("left", xlowRange, 115)
x.setRange("right", 135, xhighRange)


def fitSig(tag, mesonCat, year):
    
    sig =  "ggH"

    #data_full = getHisto(foo, 200*10, 0., 200., True, tag, mesonCat, True, sig)
    data_full = "getHistogram"

    x = ROOT.RooRealVar('mh', 'm_{#gamma,meson}', xlowRange, xhighRange)

    x.setRange("full", xlowRange, xhighRange)

    data = ROOT.RooDataHist('datahist' + tag + '_' + sig, 'data', ROOT.RooArgList(x), data_full)

    cb_mu = ROOT.RooRealVar('cb_mu' + mesonCat + tag + '_' + sig, 'cb_mu', 125., 125-10., 125+10.)
    cb_sigma = ROOT.RooRealVar('cb_sigma' + mesonCat + tag + '_' + sig, 'cb_sigma', 0., 3.)
    cb_alphaL = ROOT.RooRealVar('cb_alphaL' + mesonCat + tag + '_' + sig, 'cb_alphaL', 0., 5.)
    cb_alphaR = ROOT.RooRealVar('cb_alphaR' + mesonCat + tag + '_' + sig, 'cb_alphaR', 0., 5.)
    cb_nL = ROOT.RooRealVar('cb_nL' + mesonCat + tag + '_' + sig, 'cb_nL', 0., 30.)
    cb_nR = ROOT.RooRealVar('cb_nR' + mesonCat + tag + '_' + sig, 'cb_nR', 0., 15.)

    pdf_crystalball = ROOT.RooDoubleCBFast('crystal_ball' + mesonCat + tag + '_' + sig, 'crystal_ball', x, cb_mu, cb_sigma, cb_alphaL, cb_nL, cb_alphaR, cb_nR)
    model = pdf_crystalball

    model.fitTo(data, ROOT.RooFit.Minimizer("Minuit2"), ROOT.RooFit.Strategy(2), ROOT.RooFit.Range("full"))

    # Here we will plot the results
    canvas = ROOT.TCanvas("canvas", "canvas", 800, 800)

    titleSTR = "mH" + mesonCat + tag + "_" + str(year) + " -- "

    plotFrameWithNormRange = x.frame(ROOT.RooFit.Title(titleSTR))

    data.plotOn(plotFrameWithNormRange)
    model.plotOn(plotFrameWithNormRange, ROOT.RooFit.LineColor(2), ROOT.RooFit.Range("full"), ROOT.RooFit.NormRange("full"), ROOT.RooFit.LineStyle(10))
    model.paramOn(plotFrameWithNormRange, ROOT.RooFit.Layout(0.65, 0.99, 0.75))
    plotFrameWithNormRange.getAttText().SetTextSize(0.02)

    plotFrameWithNormRange.Draw()

    canvas.Draw()


if __name__ == "__main__":

    fitSig('_GFcat', '_D0StarCat', 2018)
