import ROOT
from prepareFits import *

ROOT.gROOT.SetBatch()
ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit.so")

xlowRange = 100.
xhighRange = 150.

sig = "ggH"
workspaceName = 'WS_SEP25'

def fitBkg(tag, mesonCat, year, date, extraTitle=None, regModelName=None, doubleFit=False):

    if regModelName == "RECO":
        regModelName = None

    verbString = "[fitBkg] Fitting Histogram {} {} {}".format(mesonCat, cat, date)
    if regModelName is not None:
        verbString += " {}".format(regModelName)
    if extraTitle is not None:
        verbString += " {}".format(extraTitle)
    verbString += "..."
    print('\033[1;31m' + verbString + '\033[0m')

    if extraTitle is None:
        extraTitle = "BKG"
    else:
        extraTitle = "BKG_{}".format(extraTitle)
    
    #Read Hist file saved
    data_full = getHistoFromFile(getFullNameOfHistFile(mesonCat, tag, year, date, extraTitle=extraTitle, regModelName=regModelName))
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
    model.plotOn(plotFrameWithNormRange, ROOT.RooFit.Components(model.GetName()), ROOT.RooFit.Range("full"), ROOT.RooFit.NormRange("full"), ROOT.RooFit.LineColor(ROOT.kRed))
    model2.plotOn(plotFrameWithNormRange, ROOT.RooFit.Components(model2.GetName()), ROOT.RooFit.Range("full"), ROOT.RooFit.NormRange("full"), ROOT.RooFit.LineColor(ROOT.kBlue))
    name1 = model.GetName() + "_Norm[mh]_Comp[" + model.GetName() + "]_Range[full]_NormRange[full]"
    name2 = model2.GetName() + "_Norm[mh]_Comp[" + model2.GetName() + "]_Range[full]_NormRange[full]"
    chi2_1 = plotFrameWithNormRange.chiSquare(name1, "h_" + data.GetName(), fitresults.floatParsFinal().getSize()) #name1 is name of the model, "h_" + ... is name of the hist
    chi2_2 = plotFrameWithNormRange.chiSquare(name2, "h_" + data.GetName(), fitresults2.floatParsFinal().getSize())
    print('----------------------------------------')
    print(model2.GetName(), "    chi2/ndof=",round(chi2_2,2), " ndof", fitresults2.floatParsFinal().getSize())
    print(model.GetName(), "    chi2/ndof=",round(chi2_1,2), " ndof", fitresults.floatParsFinal().getSize())
    print('----------------------------------------')
    plotFrameWithNormRange.Draw()
    data_full.GetXaxis().SetRangeUser(xlowRange, xhighRange)

    latex = ROOT.TLatex()
    latex.SetTextSize(0.03)
    latex.SetTextColor(ROOT.kRed)
    latex.SetTextAlign(12)
    latex.DrawLatexNDC(0.13, 0.865, model.GetName())
    latex.SetTextAlign(32)
    latex.DrawLatexNDC(0.49, 0.865, "#chi^{{2}}/ndof: {}".format(round(chi2_1, 2)))
    latex.SetTextColor(ROOT.kBlue)
    latex.SetTextAlign(12)
    latex.DrawLatexNDC(0.13, 0.825, model2.GetName())
    latex.SetTextAlign(32)
    latex.DrawLatexNDC(0.49, 0.825, "#chi^{{2}}/ndof: {}".format(round(chi2_2, 2)))
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
    residualsFrame1 = x.frame(ROOT.RooFit.Title("Residuals model 1"))
    hresid1 = plotFrameWithNormRange.residHist("h_" + data.GetName(), name1)
    residualsFrame1.addPlotable(hresid1, "P")
    residualsFrame1.Draw()
    
    canvas.cd()
    pad3 = ROOT.TPad("Pull pad", "Pull pad", 0, 0, 1.0, 0.20)
    pad3.Draw()
    pad3.cd()
    residualsFrame2 = x.frame(ROOT.RooFit.Title("Residuals model 2"))
    hresid2 = plotFrameWithNormRange.residHist("h_" + data.GetName(), name2)
    residualsFrame2.addPlotable(hresid2, "P")
    residualsFrame2.Draw()

    fileName = "~/public_html/fits/{}/{}".format(mesonCat[:-3], mesonCat)
    if regModelName is not None:
        fileName += "_" + regModelName
    if extraTitle is not None:
        fileName += "_" + extraTitle.replace(" ", "_").replace(",", "")
    canvas.SaveAs(fileName + "_fit.png")

    # Create workspace
    w = ROOT.RooWorkspace("w", "workspace")

    if not doubleFit:#set workspace when not double fit
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

    #2Dfit---------------------------------------------------------------------------
    else:
        #Read Hist file saved
        data_full_doubleFit = getHistoFromFile(getFullNameOfHistFile(mesonCat, tag, year, date, extraTitle=extraTitle, doubleFit=doubleFit))
        print("[fitBkg2D] ------------------------Histogram read!-----------------------")

        xlow2D, xhigh2D = doubleFitVar[mesonCat][3]

        x_doubleFit = ROOT.RooRealVar('m_meson', '{} [GeV]'.format(doubleFitVar[mesonCat][2]), xlow2D, xhigh2D)

        x_doubleFit.setRange("full", xlow2D, xhigh2D)

        data_doubleFit = ROOT.RooDataHist('datahist_' + mesonCat + '_' + tag + "_doubleFit", 'data_doubleFit', ROOT.RooArgList(x_doubleFit), data_full_doubleFit)

        #BERN law -----------------------------------------------------------------------------
        bern_c0_doubleFit = ROOT.RooRealVar('bern_c0_' + mesonCat + "_" + tag + "_doubleFit", 'bern_c0_doubleFit', 0.50, 0., 1.0)
        bern_c1_doubleFit = ROOT.RooRealVar('bern_c1_' + mesonCat + "_" + tag + "_doubleFit", 'bern_c1_doubleFit', 0.10, 0., 1.0)
        bern_c2_doubleFit = ROOT.RooRealVar('bern_c2_' + mesonCat + "_" + tag + "_doubleFit", 'bern_c2_doubleFit', 0.10, 0., 1.0)
        bern_c3_doubleFit = ROOT.RooRealVar('bern_c3_' + mesonCat + "_" + tag + "_doubleFit", 'bern_c3_doubleFit', 0.01, 0., 0.1)
        bern_c4_doubleFit = ROOT.RooRealVar('bern_c4_' + mesonCat + "_" + tag + "_doubleFit", 'bern_c4_doubleFit', 0.50, 0., 5.0)
        bern_c5_doubleFit = ROOT.RooRealVar('bern_c5_' + mesonCat + "_" + tag + "_doubleFit", 'bern_c5_doubleFit', 0.01, 0., 0.1)

        pdf_bern0_doubleFit = ROOT.RooBernstein('bern0_' + mesonCat + "_" + tag + "_doubleFit", 'bern0_doubleFit', x_doubleFit, ROOT.RooArgList(bern_c0_doubleFit))
        pdf_bern1_doubleFit = ROOT.RooBernstein('bern1_' + mesonCat + "_" + tag + "_doubleFit", 'bern1_doubleFit', x_doubleFit, ROOT.RooArgList(bern_c0_doubleFit, bern_c1_doubleFit))
        pdf_bern2_doubleFit = ROOT.RooBernstein('bern2_' + mesonCat + "_" + tag + "_doubleFit", 'bern2_doubleFit', x_doubleFit, ROOT.RooArgList(bern_c0_doubleFit, bern_c1_doubleFit, bern_c2_doubleFit))
        pdf_bern3_doubleFit = ROOT.RooBernstein('bern3_' + mesonCat + "_" + tag + "_doubleFit", 'bern3_doubleFit', x_doubleFit, ROOT.RooArgList(bern_c0_doubleFit, bern_c1_doubleFit, bern_c2_doubleFit, bern_c3_doubleFit))
        pdf_bern4_doubleFit = ROOT.RooBernstein('bern4_' + mesonCat + "_" + tag + "_doubleFit", 'bern4_doubleFit', x_doubleFit, ROOT.RooArgList(bern_c0_doubleFit, bern_c1_doubleFit, bern_c2_doubleFit, bern_c3_doubleFit, bern_c4_doubleFit))
        pdf_bern5_doubleFit = ROOT.RooBernstein('bern5_' + mesonCat + "_" + tag + "_doubleFit", 'bern5_doubleFit', x_doubleFit, ROOT.RooArgList(bern_c0_doubleFit, bern_c1_doubleFit, bern_c2_doubleFit, bern_c3_doubleFit, bern_c4_doubleFit, bern_c5_doubleFit))

        #CHEBYCHEV law ------------------------------------------------------------------------
        chebychev_c0_doubleFit = ROOT.RooRealVar('chebychev_c0_' + mesonCat + "_" + tag + "_doubleFit", 'chebychev_c0_doubleFit', 1.08, -1.1, 10.)
        chebychev_c1_doubleFit = ROOT.RooRealVar('chebychev_c1_' + mesonCat + "_" + tag + "_doubleFit", 'chebychev_c1_doubleFit', 0.40, -1.0, 1.0)
        chebychev_c2_doubleFit = ROOT.RooRealVar('chebychev_c2_' + mesonCat + "_" + tag + "_doubleFit", 'chebychev_c2_doubleFit', 0.01, -0.1, 0.1)
        chebychev_c3_doubleFit = ROOT.RooRealVar('chebychev_c3_' + mesonCat + "_" + tag + "_doubleFit", 'chebychev_c3_doubleFit', 0.00, -1.0, 1.0)
        chebychev_c4_doubleFit = ROOT.RooRealVar('chebychev_c4_' + mesonCat + "_" + tag + "_doubleFit", 'chebychev_c4_doubleFit', 0.00, -1.0, 1.0)

        pdf_chebychev1_doubleFit = ROOT.RooChebychev("chebychev1_" + mesonCat + "_" + tag + "_doubleFit", "chebychev1_doubleFit", x_doubleFit, ROOT.RooArgList(chebychev_c0_doubleFit, chebychev_c1_doubleFit))
        pdf_chebychev2_doubleFit = ROOT.RooChebychev("chebychev2_" + mesonCat + "_" + tag + "_doubleFit", "chebychev2_doubleFit", x_doubleFit, ROOT.RooArgList(chebychev_c0_doubleFit, chebychev_c1_doubleFit, chebychev_c2_doubleFit))
        pdf_chebychev3_doubleFit = ROOT.RooChebychev("chebychev3_" + mesonCat + "_" + tag + "_doubleFit", "chebychev3_doubleFit", x_doubleFit, ROOT.RooArgList(chebychev_c0_doubleFit, chebychev_c1_doubleFit, chebychev_c2_doubleFit, chebychev_c3_doubleFit))
        pdf_chebychev4_doubleFit = ROOT.RooChebychev("chebychev4_" + mesonCat + "_" + tag + "_doubleFit", "chebychev4_doubleFit", x_doubleFit, ROOT.RooArgList(chebychev_c0_doubleFit, chebychev_c1_doubleFit, chebychev_c2_doubleFit, chebychev_c3_doubleFit, chebychev_c4_doubleFit))

        #--------------------------------------------------------------------------------------

        storedPdfs_doubleFit = ROOT.RooArgList("store_" + mesonCat + "_" + tag + "_doubleFit")

        #For ggH:
        model_doubleFit = pdf_bern4_doubleFit
        model2_doubleFit = pdf_chebychev4_doubleFit

        fitresults_doubleFit = model_doubleFit.fitTo(data_doubleFit, ROOT.RooFit.Minimizer("Minuit2"), ROOT.RooFit.Strategy(2), ROOT.RooFit.Range("full"), ROOT.RooFit.Save(ROOT.kTRUE))
        fitresults2_doubleFit = model2_doubleFit.fitTo(data_doubleFit, ROOT.RooFit.Minimizer("Minuit2"), ROOT.RooFit.Strategy(2), ROOT.RooFit.Range("full"), ROOT.RooFit.Save(ROOT.kTRUE))
        storedPdfs_doubleFit.add(model_doubleFit)
        storedPdfs_doubleFit.add(model2_doubleFit)

        # Here we will plot the results
        canvas_doubleFit = ROOT.TCanvas("canvas", "canvas", 1600, 1600)

        canvas_doubleFit.cd()
        pad1_doubleFit = ROOT.TPad("Fit pad", "Fit pad", 0, 0.40, 1.0, 1.0)
        pad1_doubleFit.Draw()
        pad1_doubleFit.cd()
        title_doubleFit = "mMeson_" + mesonCat + "_" + tag + "_" + str(year)
        if extraTitle is not None:
            title_doubleFit += "_({})".format(extraTitle)
        plotFrameWithNormRange_doubleFit = x_doubleFit.frame(ROOT.RooFit.Title(title_doubleFit))
        data_doubleFit.plotOn(plotFrameWithNormRange_doubleFit)
        model_doubleFit.plotOn(plotFrameWithNormRange_doubleFit, ROOT.RooFit.Components(model_doubleFit.GetName()), ROOT.RooFit.Range("full"), ROOT.RooFit.NormRange("full"), ROOT.RooFit.LineColor(ROOT.kRed))
        model2_doubleFit.plotOn(plotFrameWithNormRange_doubleFit, ROOT.RooFit.Components(model2_doubleFit.GetName()), ROOT.RooFit.Range("full"), ROOT.RooFit.NormRange("full"), ROOT.RooFit.LineColor(ROOT.kBlue))
        name1_doubleFit = model_doubleFit.GetName() + "_Norm[m_meson]_Comp[" + model_doubleFit.GetName() + "]_Range[full]_NormRange[full]"
        name2_doubleFit = model2_doubleFit.GetName() + "_Norm[m_meson]_Comp[" + model2_doubleFit.GetName() + "]_Range[full]_NormRange[full]"
        chi2_1_doubleFit = plotFrameWithNormRange_doubleFit.chiSquare(name1_doubleFit, "h_" + data_doubleFit.GetName(), fitresults_doubleFit.floatParsFinal().getSize()) #name1 is name of the model, "h_" + ... is name of the hist
        chi2_2_doubleFit = plotFrameWithNormRange_doubleFit.chiSquare(name2_doubleFit, "h_" + data_doubleFit.GetName(), fitresults2_doubleFit.floatParsFinal().getSize())
        print('----------------------------------------')
        print(model2_doubleFit.GetName(), "    chi2/ndof=",round(chi2_2_doubleFit,2), " ndof", fitresults2_doubleFit.floatParsFinal().getSize())
        print(model_doubleFit.GetName(), "    chi2/ndof=",round(chi2_1_doubleFit,2), " ndof", fitresults_doubleFit.floatParsFinal().getSize())
        print('----------------------------------------')
        plotFrameWithNormRange_doubleFit.Draw()
        data_full_doubleFit.GetXaxis().SetRangeUser(xlow2D, xhigh2D)

        latex_doubleFit = ROOT.TLatex()
        latex_doubleFit.SetTextSize(0.03)
        latex_doubleFit.SetTextColor(ROOT.kRed)
        latex_doubleFit.SetTextAlign(12)
        latex_doubleFit.DrawLatexNDC(0.13, 0.865, model_doubleFit.GetName())
        latex_doubleFit.SetTextAlign(32)
        latex_doubleFit.DrawLatexNDC(0.49, 0.865, "#chi^{{2}}/ndof: {}".format(round(chi2_1_doubleFit, 2)))
        latex_doubleFit.SetTextColor(ROOT.kBlue)
        latex_doubleFit.SetTextAlign(12)
        latex_doubleFit.DrawLatexNDC(0.13, 0.825, model2_doubleFit.GetName())
        latex_doubleFit.SetTextAlign(32)
        latex_doubleFit.DrawLatexNDC(0.49, 0.825, "#chi^{{2}}/ndof: {}".format(round(chi2_2_doubleFit, 2)))
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
        residualsFrame1_doubleFit = x_doubleFit.frame(ROOT.RooFit.Title("Residuals model 1"))
        hresid1_doubleFit = plotFrameWithNormRange_doubleFit.residHist("h_" + data_doubleFit.GetName(), name1_doubleFit)
        residualsFrame1_doubleFit.addPlotable(hresid1_doubleFit, "P")
        residualsFrame1_doubleFit.Draw()
        
        canvas_doubleFit.cd()
        pad3_doubleFit = ROOT.TPad("Pull pad", "Pull pad", 0, 0, 1.0, 0.20)
        pad3_doubleFit.Draw()
        pad3_doubleFit.cd()
        residualsFrame2_doubleFit = x_doubleFit.frame(ROOT.RooFit.Title("Residuals model 2"))
        hresid2_doubleFit = plotFrameWithNormRange_doubleFit.residHist("h_" + data_doubleFit.GetName(), name2_doubleFit)
        residualsFrame2_doubleFit.addPlotable(hresid2_doubleFit, "P")
        residualsFrame2_doubleFit.Draw()

        fileName_doubleFit = "~/public_html/fits/{}/{}".format(mesonCat[:-3], mesonCat)
        if extraTitle is not None:
            fileName_doubleFit += "_" + extraTitle.replace(" ", "_").replace(",", "")
        canvas_doubleFit.SaveAs(fileName_doubleFit + "_fit_2D.png")

        #Create 2D model
        storedPdfs_doubleFit_ext = ROOT.RooArgList("store_" + mesonCat + "_" + tag + "_doubleFit_ext")
        pdf_2D = ROOT.RooProdPdf("pdf_2d", "", ROOT.RooArgList(model, model_doubleFit))
        pdf_2D2 = ROOT.RooProdPdf("pdf_2d2", "", ROOT.RooArgList(model2, model2_doubleFit))
        storedPdfs_doubleFit_ext.add(pdf_2D)
        storedPdfs_doubleFit_ext.add(pdf_2D2)

        norm_range = data_full.Integral(data_full.FindBin(xlowRange), data_full.FindBin(xhighRange))
        BKG_norm = ROOT.RooRealVar("multipdf_"+mesonCat+"_"+tag+"_bkg"+"_norm", model.GetName()+"_norm", norm_range, 0.5*norm_range, 2*norm_range)

        pdf_cat = ROOT.RooCategory("pdfindex_"+mesonCat+"_"+tag,"pdfindex"+"_"+mesonCat+"_"+tag)
        pdf_bkg = ROOT.RooMultiPdf("multipdf_"+mesonCat+"_"+tag+"_bkg","multipdf",pdf_cat,storedPdfs_doubleFit_ext)
        getattr(w,'import')(pdf_bkg)

        # Import model_norm
        getattr(w,'import')(BKG_norm)
        print("integral BKG",BKG_norm.Print())

        # Import data into the workspace
        getattr(w,'import')(data)
        getattr(w,'import')(data_doubleFit)

    # Print workspace contents for 1D/2D
    w.Print()

    # -----------------------------------------------------------------------------
    # Save workspace in file, create folder if it does not exist
    if not os.path.exists(workspaceName):
        os.mkdir(workspaceName)

    workspaceFileName = "Bkg_" + mesonCat[:-3] + "_" + tag + "_" + str(year)
    if regModelName is not None:
        workspaceFileName += "_" + regModelName

    w.writeToFile(workspaceName + "/" + workspaceFileName + "_workspace.root")#same name as 2D
    print('\033[1;31m' + "[fitBkg] Fit done, workspace created!" + '\033[0m')


if __name__ == "__main__":

    cat = "GFcat"
    year = 2018
    date = "SEP25"


    #BACKGROUND D0Star-----------------------------------------------------------------------------

    #BACKGROUND Phi3-------------------------------------------------------------------------------
    df = False
    mesonCat = "Phi3Cat"
    #mesonCat = "OmegaCat"
    #mesonCat = "D0StarCat"
    for mesonCat in ["Phi3Cat", "OmegaCat", "D0StarCat"]:
        with open('models_{}.txt'.format(mesonCat[:-3]), 'r') as file:
            for line in file:
                regModelName = line.strip()
                if regModelName[0] != "#":
                    fitBkg(cat, mesonCat, year, date, regModelName=regModelName, doubleFit=df)
    #fitBkg(cat, mesonCat, year, date)
