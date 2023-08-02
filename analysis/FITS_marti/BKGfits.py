import ROOT
from prepareFits import *

ROOT.gROOT.SetBatch()
ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit.so")

xlowRange = 100.
xhighRange = 150.

workspaceName = 'WS_JUL06'


def fitBkg(tag, mesonCat, year, date, extraTitle=None):

    print('\033[1;31m' + "[fitBkg] Fitting Histogram {} {} {} {} BKG...".format(mesonCat, cat, date, extraTitle) + '\033[0m')

    #Read Hist file saved
    if extraTitle is None:
        extratitle="BKG"
    else:
        extratitle="BKG_{}".format(extraTitle)
    data_full = getHistoFromFile(getFullNameOfHistFile(mesonCat, tag, year, date, extraTitle=extratitle))
    print("[fitBkg] ------------------------Histogram read!-----------------------")

    x = ROOT.RooRealVar('mh', 'm_{{#gamma, {0} }} [GeV]'.format(mesonLatex[mesonCat]), xlowRange, xhighRange)

    x.setRange("full", xlowRange, xhighRange)

    data = ROOT.RooDataHist('datahist_' + mesonCat + '_' + tag, 'data', ROOT.RooArgList(x), data_full)

    #BERN law -----------------------------------------------------------------------------
    bern_c0 = ROOT.RooRealVar('bern_c0_' + mesonCat + "_" + tag, 'bern_c0', 0.50, 0., 1.0)
    bern_c1 = ROOT.RooRealVar('bern_c1_' + mesonCat + "_" + tag, 'bern_c1', 0.10, 0., 1.0)
    bern_c2 = ROOT.RooRealVar('bern_c2_' + mesonCat + "_" + tag, 'bern_c2', 0.10, 0., 1.0)
    bern_c3 = ROOT.RooRealVar('bern_c3_' + mesonCat + "_" + tag, 'bern_c3', 0.01, 0., 0.1)
    bern_c4 = ROOT.RooRealVar('bern_c4_' + mesonCat + "_" + tag, 'bern_c4', 0.50, 0., 5.0)
    bern_c5 = ROOT.RooRealVar('bern_c5_' + mesonCat + "_" + tag, 'bern_c5', 0.01, 0., 0.1)

    pdf_bern0 = ROOT.RooBernstein('bern0_' + mesonCat + "_" + tag, 'bern0', x, ROOT.RooArgList(bern_c0))
    pdf_bern1 = ROOT.RooBernstein('bern1_' + mesonCat + "_" + tag, 'bern1', x, ROOT.RooArgList(bern_c0, bern_c1))
    pdf_bern2 = ROOT.RooBernstein('bern2_' + mesonCat + "_" + tag, 'bern2', x, ROOT.RooArgList(bern_c0, bern_c1, bern_c2))
    pdf_bern3 = ROOT.RooBernstein('bern3_' + mesonCat + "_" + tag, 'bern3', x, ROOT.RooArgList(bern_c0, bern_c1, bern_c2, bern_c3))
    pdf_bern4 = ROOT.RooBernstein('bern4_' + mesonCat + "_" + tag, 'bern4', x, ROOT.RooArgList(bern_c0, bern_c1, bern_c2, bern_c3, bern_c4))
    pdf_bern5 = ROOT.RooBernstein('bern5_' + mesonCat + "_" + tag, 'bern5', x, ROOT.RooArgList(bern_c0, bern_c1, bern_c2, bern_c3, bern_c4, bern_c5))

    #CHEBYCHEV law ------------------------------------------------------------------------
    chebychev_c0 = ROOT.RooRealVar('chebychev_c0_' + mesonCat + "_" + tag, 'chebychev_c0', 1.08, -1.1, 10.)
    chebychev_c1 = ROOT.RooRealVar('chebychev_c1_' + mesonCat + "_" + tag, 'chebychev_c1', 0.40, -1.0, 1.0)
    chebychev_c2 = ROOT.RooRealVar('chebychev_c2_' + mesonCat + "_" + tag, 'chebychev_c2', 0.01, -0.1, 0.1)
    chebychev_c3 = ROOT.RooRealVar('chebychev_c3_' + mesonCat + "_" + tag, 'chebychev_c3', 0.00, -1.0, 1.0)

    pdf_chebychev1 = ROOT.RooChebychev("chebychev1_" + mesonCat + "_" + tag, "chebychev1", x, ROOT.RooArgList(chebychev_c0, chebychev_c1))
    pdf_chebychev2 = ROOT.RooChebychev("chebychev2_" + mesonCat + "_" + tag, "chebychev2", x, ROOT.RooArgList(chebychev_c0, chebychev_c1, chebychev_c2))
    pdf_chebychev3 = ROOT.RooChebychev("chebychev3_" + mesonCat + "_" + tag, "chebychev3", x, ROOT.RooArgList(chebychev_c0, chebychev_c1, chebychev_c2, chebychev_c3))

    #GAUSS law ----------------------------------------------------------------------------
    gauss_mu = ROOT.RooRealVar('gauss_mu_' + mesonCat + "_" + tag, 'gauss_mu', 10.0, 0.0, 30.)
    gauss_sigma = ROOT.RooRealVar('gauss_sigma_' + mesonCat + "_" + tag, 'gauss_sigma', 10.0, 2.0, 30.)
    pdf_gauss = ROOT.RooGaussian('gauss_' + mesonCat + "_" + tag, 'gauss', x , gauss_mu, gauss_sigma)

    #POW law ------------------------------------------------------------------------------
    formula_pow1 = 'TMath::Power(@0, @1)'
    formula_pow2 = '(1.-@1)*TMath::Power(@0,@2) + @1*TMath::Power(@0,@3)'
    formula_pow3 = '(1.-@1-@2)*TMath::Power(@0,@3) + @1*TMath::Power(@0,@4) + @2*TMath::Power(@0,@5)'

    pow_frac1 = ROOT.RooRealVar('frac1', 'frac1', 0.01, 0., 1.)
    pow_frac2 = ROOT.RooRealVar('frac2', 'frac2', 0.01, 0., 1.)
    pow_p1 = ROOT.RooRealVar('p1', 'p1', -2.555, -10., 0.)
    pow_p2 = ROOT.RooRealVar('p2', 'p2', -8., -10., 0.)
    pow_p3 = ROOT.RooRealVar('p3', 'p3', -10., -10., 0.)

    pdf_pow1 = ROOT.RooGenericPdf('pow1', 'pow1', formula_pow1, ROOT.RooArgList(x, pow_p1))
    pdf_pow2 = ROOT.RooGenericPdf('pow2', 'pow2', formula_pow2, ROOT.RooArgList(x, pow_frac1, pow_p1, pow_p2))
    pdf_pow3 = ROOT.RooGenericPdf('pow3', 'pow3', formula_pow3, ROOT.RooArgList(x, pow_frac1, pow_frac2, pow_p1, pow_p2, pow_p3))

    #EXP law ------------------------------------------------------------------------------
    exp_p1 = ROOT.RooRealVar('exp_p1_' + mesonCat + "_" + tag, 'exp_p1', -0.1, -10, 0)
    exp_p2 = ROOT.RooRealVar('exp_p2_' + mesonCat + "_" + tag, 'exp_p2', -1e-2, -10, 0)
    exp_p3 = ROOT.RooRealVar('exp_p3_' + mesonCat + "_" + tag, 'exp_p3', -1e-3, -10, 0)
    exp_c1 = ROOT.RooRealVar('exp_c1_' + mesonCat + "_" + tag, 'exp_c1', 0., 1.)
    exp_c2 = ROOT.RooRealVar('exp_c2_' + mesonCat + "_" + tag, 'exp_c2', 0., 1.)
    exp_c3 = ROOT.RooRealVar('exp_c3_' + mesonCat + "_" + tag, 'exp_c3', 0., 1.)

    pdf_exp1 = ROOT.RooExponential('exp1_' + mesonCat + "_" + tag, 'exp1', x, exp_p1)
    pdf_single_exp2 = ROOT.RooExponential('single_exp2_' + mesonCat + "_" + tag, 'single_exp2', x, exp_p2)
    pdf_single_exp3 = ROOT.RooExponential('single_exp3_' + mesonCat + "_" + tag, 'single_exp3', x, exp_p3)
    pdf_exp2 = ROOT.RooAddPdf('exp2_' + mesonCat + "_" + tag, 'exp2', ROOT.RooArgList(pdf_exp1, pdf_single_exp2), ROOT.RooArgList(exp_c1, exp_c2))
    pdf_exp3 = ROOT.RooAddPdf('exp3_' + mesonCat + "_" + tag, 'exp3', ROOT.RooArgList(pdf_exp1, pdf_single_exp2, pdf_single_exp3), ROOT.RooArgList(exp_c1, exp_c2, exp_c3))
    pdf_exp1_conv_gauss = ROOT.RooFFTConvPdf('exp1_conv_gauss_' + mesonCat + "_" + tag, 'exp1 (X) gauss', x, pdf_exp1, pdf_gauss)

    #--------------------------------------------------------------------------------------

    storedPdfs = ROOT.RooArgList("store_" + mesonCat + "_" + tag)

    #For ggH:
    model = pdf_bern3
    model2 = pdf_chebychev3

    fitresults = model.fitTo(data, ROOT.RooFit.Minimizer("Minuit2"), ROOT.RooFit.Strategy(2), ROOT.RooFit.Range("full"), ROOT.RooFit.Save(ROOT.kTRUE))
    fitresults2 = model2.fitTo(data, ROOT.RooFit.Minimizer("Minuit2"), ROOT.RooFit.Strategy(2), ROOT.RooFit.Range("full"), ROOT.RooFit.Save(ROOT.kTRUE))
    storedPdfs.add(model)
    storedPdfs.add(model2)

    # Here we will plot the results
    canvas = ROOT.TCanvas("canvas", "canvas", 1600, 960)

    #canvas.cd()
    #pad1 = ROOT.TPad("Fit pad", "Fit pad", 0, 0.40, 1.0, 1.0)
    #pad1.Draw()
    #pad1.cd()
    plotFrameWithNormRange = x.frame(ROOT.RooFit.Title("mH_" + mesonCat + "_" + tag + "_" + str(year) + "_" + extratitle))
    data.plotOn(plotFrameWithNormRange)
    model.plotOn(plotFrameWithNormRange, ROOT.RooFit.Components(model.GetName()), ROOT.RooFit.Range("full"), ROOT.RooFit.NormRange("full"), ROOT.RooFit.LineColor(ROOT.kRed))
    model2.plotOn(plotFrameWithNormRange, ROOT.RooFit.Components(model2.GetName()), ROOT.RooFit.Range("full"), ROOT.RooFit.NormRange("full"), ROOT.RooFit.LineColor(ROOT.kBlue))
    name1 = model.GetName() + "_Norm[mh]_Comp[" + model.GetName() + "]_Range[full]_NormRange[full]"
    name2 = model2.GetName() + "_Norm[mh]_Comp[" + model2.GetName() + "]_Range[full]_NormRange[full]"
    chi2_1 = plotFrameWithNormRange.chiSquare(name1, "h_" + data.GetName(), fitresults.floatParsFinal().getSize())
    chi2_2 = plotFrameWithNormRange.chiSquare(name2, "h_" + data.GetName(), fitresults2.floatParsFinal().getSize())

    print('----------------------------------------')
    print(model2.GetName(), "    chi2/ndof=",round(chi2_2,2), " ndof", fitresults2.floatParsFinal().getSize())
    print(model.GetName(), "    chi2/ndof=",round(chi2_1,2), " ndof", fitresults.floatParsFinal().getSize())
    print('----------------------------------------')

    plotFrameWithNormRange.Draw()

    latex = ROOT.TLatex()
    latex.SetTextColor(ROOT.kRed)
    latex.SetTextSize(0.03)
    #latex.DrawLatex(102, + 1.00*data_full.GetMaximum(), model.GetName())
    latex.DrawLatexNDC(0.14, 0.84, model.GetName())
    latex.SetTextColor(ROOT.kBlue)
    latex.DrawLatexNDC(0.14, 0.79, model2.GetName())

    canvas.SaveAs("~/public_html/fits/{}/{}_fit_{}.png".format(mesonCat[:-3], mesonCat, extratitle))

    # -------------------------------------------------------------

    w = ROOT.RooWorkspace("w", "workspace")

    norm_range = data_full.Integral(data_full.FindBin(xlowRange), data_full.FindBin(xhighRange))
    BKG_norm = ROOT.RooRealVar("multipdf_"+mesonCat+"_"+tag+"_bkg"+"_norm", model.GetName()+"_norm", norm_range, 0.5*norm_range, 2*norm_range)

    pdf_cat = ROOT.RooCategory("pdfindex_"+mesonCat+"_"+tag,"pdfindex"+"_"+mesonCat+"_"+tag)
    pdf_bkg = ROOT.RooMultiPdf("multipdf_"+mesonCat+"_"+tag+"_bkg","multipdf",pdf_cat,storedPdfs)
    getattr(w,'import')(pdf_bkg)

    # Import model_norm
    getattr(w,'import')(BKG_norm)
    print("integral BKG",BKG_norm.Print())

    # Import data into the workspace
    getattr(w,'import')(data)

    # Print workspace contents
    w.Print()

    # -----------------------------------------------------------------------------
    # Save workspace in file
    w.writeToFile(workspaceName+"/Bkg_"+mesonCat[:-3]+"_"+tag+"_"+str(year)+"_workspace.root")
    print('\033[1;31m' + "[fitBkg] Fit done, workspace created!" + '\033[0m')


if __name__ == "__main__":

    cat = "GFcat"
    year = 2018


    #BACKGROUND D0Star-----------------------------------------------------------------------------
    mesonCat = "D0StarCat"
    date = "JUN29"
    #fitBkg(cat, mesonCat, year, date)


    #BACKGROUND Phi3-------------------------------------------------------------------------------
    mesonCat = "Phi3Cat"
    date = "JUL31"
    fitBkg(cat, mesonCat, year, date, extraTitle="regression")
    fitBkg(cat, mesonCat, year, date)
