import ROOT
from prepareFits import *
import random

ROOT.gROOT.SetBatch()
ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit.so")

xlowRange = 100.
xhighRange = 160.

# (init, low, high)
fitInitVals = {"Phi3Cat": { "bern_mh": [(0.2, -2.0, 2.0), (0.5, -2.0, 2.0), (0.00, -2.0, 2.0), (0.00, -2.0, 2.0), (0.00, -2.0, 2.0), (0.00, -2.0, 2.0)],
                                "cheb_mh": [(-0.641, -1.0, 1.0), (-0.188, -1.0, 1.0), (0.156, -1.0, 1.0), (0.006, -1.0, 1.0), (-0.045, -1.0, 1.0), (0.00, -1.0, 1.0)],
                                "bern_mm": [(0.14, -1.0, 1.0), (0.05, -1.0, 1.0), (0.15, -1.0, 1.0), (0.07, -1.0, 1.0), (0.01, -1.0, 1.0), (0.01, -1.0, 1.0)],
                                "cheb_mm": [(1.08, -1.0, 10.0), (0.40, -1.0, 1.0), (0.01, -1.0, 1.0), (0.00, -1.0, 1.0), (0.00, -1.0, 1.0), (0.00, -1.0, 1.0)]},
                "OmegaCat": {   "bern_mh": [(0.2, -2.0, 2.0), (0.5, -2.0, 2.0), (0.00, -2.0, 2.0), (0.00, -2.0, 2.0), (0.00, -2.0, 2.0), (0.00, -2.0, 2.0)],
                                "cheb_mh": [(-0.03, -2.0, 2.0), (0.29, -2.0, 2.0), (0.005, -2.0, 2.0), (-0.03, -2.0, 2.0), (-0.00, -2.0, 2.0), (0.00, -2.0, 2.0)],
                                "bern_mm": [(0.14, -1.0, 1.0), (0.05, -1.0, 1.0), (0.15, -1.0, 1.0), (0.07, -1.0, 1.0), (0.01, -1.0, 1.0), (0.01, -1.0, 1.0)],
                                "cheb_mm": [(1.08, -1.0, 10.0), (0.40, -1.0, 1.0), (0.01, -1.0, 1.0), (0.00, -1.0, 1.0), (0.00, -1.0, 1.0), (0.00, -1.0, 1.0)]},
                "D0StarCat": {  "bern_mh": [(0.14, -1.0, 1.0), (0.05, -1.0, 1.0), (0.15, -1.0, 1.0), (0.07, -1.0, 1.0), (0.01, -1.0, 1.0), (0.01, -1.0, 1.0)],
                                "cheb_mh": [(1.00, -1.0, 10.0), (0.24, -1.0, 1.0), (-0.20, -1.0, 1.0), (-0.18, -1.0, 1.0), (-0.43, -1.0, 1.0), (0.00, -1.0, 1.0)],
                                "bern_mm": [(0.14, -1.0, 1.0), (0.05, -1.0, 1.0), (0.15, -1.0, 1.0), (0.07, -1.0, 1.0), (0.01, -1.0, 1.0), (0.01, -1.0, 1.0)],
                                "cheb_mm": [(1.08, -1.0, 10.0), (0.40, -1.0, 1.0), (0.01, -1.0, 1.0), (0.00, -1.0, 1.0), (0.00, -1.0, 1.0), (0.00, -1.0, 1.0)]},
                "D0StarRhoCat":{"bern_mh": [(0.04, -1.0, 1.0), (0.14, -1.0, 1.0), (0.06, -1.0, 1.0), (0.04, -1.0, 1.0), (0.01, -1.0, 1.0), (0.01, -1.0, 1.0)],
                                "cheb_mh": [(-0.1, -1.0, 10.0), (-0.3, -1.0, 1.0), (0.1, -1.0, 1.0), (0.02, -1.0, 1.0), (0.75, -1.0, 1.0), (0.00, -1.0, 1.0)],
                                "bern_mm": [(0.14, -1.0, 1.0), (0.05, -1.0, 1.0), (0.15, -1.0, 1.0), (0.07, -1.0, 1.0), (0.01, -1.0, 1.0), (0.01, -1.0, 1.0)],
                                "cheb_mm": [(1.08, -1.0, 10.0), (0.40, -1.0, 1.0), (0.01, -1.0, 1.0), (0.00, -1.0, 1.0), (0.00, -1.0, 1.0), (0.00, -1.0, 1.0)]}}

sig = "ggH"
workspaceName = 'WS_NOV16'


def rndInits(init):
    for key in init:
        for pol in init[key]:
            for i, e in enumerate(init[key][pol]):
                mean = e[0]
                sig = (e[2] - e[1])/5.
                lw = e[1] + random.gauss(0, 0.3)
                hg = e[2] + random.gauss(0, 0.3)
                while lw > hg:
                    lw = e[1] + random.gauss(0, 0.3)
                    hg = e[2] + random.gauss(0, 0.3)
                nv = random.gauss(mean, sig)
                while nv > e[2] or nv < e[1]:
                    nv = random.gauss(mean, sig)
                init[key][pol][i] = (nv, lw, hg)

    return init


def fitBkg(tag, mesonCat, year, date, extraTitle=None, regModelName=None):

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
    bern_c0 = ROOT.RooRealVar('bern_c0_' + mesonCat + "_" + tag, 'bern_c0', fitInitVals[mesonCat]["bern_mh"][0][0], fitInitVals[mesonCat]["bern_mh"][0][1], fitInitVals[mesonCat]["bern_mh"][0][2])
    bern_c1 = ROOT.RooRealVar('bern_c1_' + mesonCat + "_" + tag, 'bern_c1', fitInitVals[mesonCat]["bern_mh"][1][0], fitInitVals[mesonCat]["bern_mh"][1][1], fitInitVals[mesonCat]["bern_mh"][1][2])
    bern_c2 = ROOT.RooRealVar('bern_c2_' + mesonCat + "_" + tag, 'bern_c2', fitInitVals[mesonCat]["bern_mh"][2][0], fitInitVals[mesonCat]["bern_mh"][2][1], fitInitVals[mesonCat]["bern_mh"][2][2])
    bern_c3 = ROOT.RooRealVar('bern_c3_' + mesonCat + "_" + tag, 'bern_c3', fitInitVals[mesonCat]["bern_mh"][3][0], fitInitVals[mesonCat]["bern_mh"][3][1], fitInitVals[mesonCat]["bern_mh"][3][2])
    bern_c4 = ROOT.RooRealVar('bern_c4_' + mesonCat + "_" + tag, 'bern_c4', fitInitVals[mesonCat]["bern_mh"][4][0], fitInitVals[mesonCat]["bern_mh"][4][1], fitInitVals[mesonCat]["bern_mh"][4][2])
    bern_c5 = ROOT.RooRealVar('bern_c5_' + mesonCat + "_" + tag, 'bern_c5', fitInitVals[mesonCat]["bern_mh"][5][0], fitInitVals[mesonCat]["bern_mh"][5][1], fitInitVals[mesonCat]["bern_mh"][5][2])

    bern_c0_mod = ROOT.RooRealVar('bern_c0_mod' + mesonCat + "_" + tag, 'bern_c0_mod', 0.39, 0.0, 1.0)
    bern_c1_mod = ROOT.RooRealVar('bern_c1_mod_' + mesonCat + "_" + tag, 'bern_c1_mod', 0.059, -0.1, 0.52)
    pdf_bern1_mod = ROOT.RooBernstein('bern0_mod_' + mesonCat + "_" + tag, 'bern0_mod', x, ROOT.RooArgList(bern_c0_mod, bern_c1_mod))
    pdf_bern0 = ROOT.RooBernstein('bern0_' + mesonCat + "_" + tag, 'bern0', x, ROOT.RooArgList(bern_c0))
    pdf_bern1 = ROOT.RooBernstein('bern1_' + mesonCat + "_" + tag, 'bern1', x, ROOT.RooArgList(bern_c0, bern_c1))
    pdf_bern2 = ROOT.RooBernstein('bern2_' + mesonCat + "_" + tag, 'bern2', x, ROOT.RooArgList(bern_c0, bern_c1, bern_c2))
    pdf_bern3 = ROOT.RooBernstein('bern3_' + mesonCat + "_" + tag, 'bern3', x, ROOT.RooArgList(bern_c0, bern_c1, bern_c2, bern_c3))
    pdf_bern4 = ROOT.RooBernstein('bern4_' + mesonCat + "_" + tag, 'bern4', x, ROOT.RooArgList(bern_c0, bern_c1, bern_c2, bern_c3, bern_c4))
    pdf_bern5 = ROOT.RooBernstein('bern5_' + mesonCat + "_" + tag, 'bern5', x, ROOT.RooArgList(bern_c0, bern_c1, bern_c2, bern_c3, bern_c4, bern_c5))

    #CHEBYCHEV law ------------------------------------------------------------------------
    chebychev_c0 = ROOT.RooRealVar('chebychev_c0_' + mesonCat + "_" + tag, 'chebychev_c0', fitInitVals[mesonCat]["cheb_mh"][0][0], fitInitVals[mesonCat]["cheb_mh"][0][1], fitInitVals[mesonCat]["cheb_mh"][0][2])
    chebychev_c1 = ROOT.RooRealVar('chebychev_c1_' + mesonCat + "_" + tag, 'chebychev_c1', fitInitVals[mesonCat]["cheb_mh"][1][0], fitInitVals[mesonCat]["cheb_mh"][1][1], fitInitVals[mesonCat]["cheb_mh"][1][2])
    chebychev_c2 = ROOT.RooRealVar('chebychev_c2_' + mesonCat + "_" + tag, 'chebychev_c2', fitInitVals[mesonCat]["cheb_mh"][2][0], fitInitVals[mesonCat]["cheb_mh"][2][1], fitInitVals[mesonCat]["cheb_mh"][2][2])
    chebychev_c3 = ROOT.RooRealVar('chebychev_c3_' + mesonCat + "_" + tag, 'chebychev_c3', fitInitVals[mesonCat]["cheb_mh"][3][0], fitInitVals[mesonCat]["cheb_mh"][3][1], fitInitVals[mesonCat]["cheb_mh"][3][2])
    chebychev_c4 = ROOT.RooRealVar('chebychev_c4_' + mesonCat + "_" + tag, 'chebychev_c4', fitInitVals[mesonCat]["cheb_mh"][4][0], fitInitVals[mesonCat]["cheb_mh"][4][1], fitInitVals[mesonCat]["cheb_mh"][4][2])
    chebychev_c5 = ROOT.RooRealVar('chebychev_c5_' + mesonCat + "_" + tag, 'chebychev_c5', fitInitVals[mesonCat]["cheb_mh"][5][0], fitInitVals[mesonCat]["cheb_mh"][5][1], fitInitVals[mesonCat]["cheb_mh"][5][2])

    pdf_chebychev1 = ROOT.RooChebychev("chebychev1_" + mesonCat + "_" + tag, "chebychev1", x, ROOT.RooArgList(chebychev_c0, chebychev_c1))
    pdf_chebychev2 = ROOT.RooChebychev("chebychev2_" + mesonCat + "_" + tag, "chebychev2", x, ROOT.RooArgList(chebychev_c0, chebychev_c1, chebychev_c2))
    pdf_chebychev3 = ROOT.RooChebychev("chebychev3_" + mesonCat + "_" + tag, "chebychev3", x, ROOT.RooArgList(chebychev_c0, chebychev_c1, chebychev_c2, chebychev_c3))
    pdf_chebychev4 = ROOT.RooChebychev("chebychev4_" + mesonCat + "_" + tag, "chebychev4", x, ROOT.RooArgList(chebychev_c0, chebychev_c1, chebychev_c2, chebychev_c3, chebychev_c4))
    pdf_chebychev5 = ROOT.RooChebychev("chebychev5_" + mesonCat + "_" + tag, "chebychev5", x, ROOT.RooArgList(chebychev_c0, chebychev_c1, chebychev_c2, chebychev_c3, chebychev_c4, chebychev_c5))

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

    if mesonCat in ["Phi3Cat", "OmegaCat"]:
        model = pdf_bern4
        model2 = pdf_chebychev4
    else:
        model = pdf_bern3
        model2 = pdf_chebychev3

    fitresults = model.fitTo(data, ROOT.RooFit.Minimizer("Minuit2"), ROOT.RooFit.Strategy(2), ROOT.RooFit.Range("full"), ROOT.RooFit.Save(ROOT.kTRUE))
    fitresults2 = model2.fitTo(data, ROOT.RooFit.Minimizer("Minuit2"), ROOT.RooFit.Strategy(2), ROOT.RooFit.Range("full"), ROOT.RooFit.Save(ROOT.kTRUE))
    title = "mH_" + mesonCat + "_" + tag + "_" + str(year)
    if regModelName is not None:
        title += "_({})".format(regModelName)
    if extraTitle is not None:
        title += "_({})".format(extraTitle)
    plotFrameWithNormRange = x.frame(ROOT.RooFit.Title(title))
    name1 = model.GetName() + "_Norm[mh]_Comp[" + model.GetName() + "]_Range[full]_NormRange[full]"
    name2 = model2.GetName() + "_Norm[mh]_Comp[" + model2.GetName() + "]_Range[full]_NormRange[full]"
    
    storedPdfs = ROOT.RooArgList("store_" + mesonCat + "_" + tag)
    storedPdfs.add(model)
    storedPdfs.add(model2)

    data.plotOn(plotFrameWithNormRange)
    model.plotOn(plotFrameWithNormRange, ROOT.RooFit.Components(model.GetName()), ROOT.RooFit.Range("full"), ROOT.RooFit.NormRange("full"), ROOT.RooFit.LineColor(ROOT.kRed))
    model2.plotOn(plotFrameWithNormRange, ROOT.RooFit.Components(model2.GetName()), ROOT.RooFit.Range("full"), ROOT.RooFit.NormRange("full"), ROOT.RooFit.LineColor(ROOT.kBlue))
    model.paramOn(plotFrameWithNormRange, ROOT.RooFit.Layout(0.10, 0.40, 0.5))

    chi2_1 = plotFrameWithNormRange.chiSquare(name1, "h_" + data.GetName(), fitresults.floatParsFinal().getSize()) #name1 is name of the model, "h_" + ... is name of the hist
    chi2_2 = plotFrameWithNormRange.chiSquare(name2, "h_" + data.GetName(), fitresults2.floatParsFinal().getSize())

    # Here we will plot the results
    canvas = ROOT.TCanvas("canvas", "canvas", 1600, 1600)
    canvas.cd()
    pad1 = ROOT.TPad("Fit pad", "Fit pad", 0, 0.40, 1.0, 1.0)
    pad1.Draw()
    pad1.cd()

    #hist1 = plotFrameWithNormRange.getCurve(name1)
    #hist2 = plotFrameWithNormRange.getCurve(name2)
    #hist1.Print()
    #print(type(hist1))
    #f = ROOT.TFile("/data/submit/pdmonte/thesisFitRootFiles/{}_curve.root".format(getNameOfHistFileSimple(mesonCat, cat, year, date, extraTitle=extraTitle, regModelName=regModelName)),"RECREATE")
    #f.WriteObject(hist1, "curve1")
    #f.WriteObject(hist2, "curve2")
    #f.Close()
    #f = ROOT.TFile("/data/submit/pdmonte/thesisFitRootFiles/{}_hist.root".format(getNameOfHistFileSimple(mesonCat, cat, year, date, extraTitle=extraTitle, regModelName=regModelName)),"RECREATE")
    #f.WriteObject(data, "hist")
    #f.Close()

    print('----------------------------------------')
    print(model2.GetName(), "    chi2/ndof=",round(chi2_2,2), " ndof", fitresults2.floatParsFinal().getSize())
    print(model.GetName(), "    chi2/ndof=",round(chi2_1,2), " ndof", fitresults.floatParsFinal().getSize())
    print('----------------------------------------')
    plotFrameWithNormRange.Draw()
    plotFrameWithNormRange.getAttText().SetTextSize(0.02)
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

    norm_range = data_full.Integral(data_full.FindBin(xlowRange), data_full.FindBin(xhighRange))
    BKG_norm = ROOT.RooRealVar("multipdf_"+mesonCat+"_"+tag+"_bkg"+"_norm", model.GetName()+"_norm", norm_range, 0.5*norm_range, 2*norm_range)

    pdf_cat = ROOT.RooCategory("pdfindex_"+mesonCat+"_"+tag,"pdfindex"+"_"+mesonCat+"_"+tag)
    pdf_bkg = ROOT.RooMultiPdf("multipdf_"+mesonCat+"_"+tag+"_bkg","multipdf",pdf_cat,storedPdfs)
    getattr(w,'import')(pdf_bkg)

    # Import model_norm
    getattr(w,'import')(BKG_norm)
    print("integral BKG", BKG_norm.Print())

    # Import data into the workspace
    getattr(w,'import')(data)
    
    # Print workspace contents
    w.Print()

    # -----------------------------------------------------------------------------
    # Save workspace in file, create folder if it does not exist
    if not os.path.exists(workspaceName):
        os.mkdir(workspaceName)

    workspaceFileName = "Bkg_" + mesonCat[:-3] + "_" + tag + "_" + str(year)
    if regModelName is not None:
        workspaceFileName += "_" + regModelName

    w.writeToFile(workspaceName + "/" + workspaceFileName + "_workspace.root")
    print('\033[1;31m' + "[fitBkg] Fit done, workspace created!" + '\033[0m')









def fitBkg2D(tag, mesonCat, year, date, extraTitle=None, regModelName=None):

    if regModelName == "RECO":
        regModelName = None

    verbString = "[fitBkg2D] Fitting Histogram {} {} {}".format(mesonCat, cat, date)
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
    data_full = getHistoFromFile(getFullNameOfHistFile(mesonCat, tag, year, date, extraTitle=extraTitle, regModelName=regModelName, doubleFit=True))
    print("[fitBkg2D] ------------------------Histogram read!-----------------------")

    ylowRange, yhighRange = doubleFitVar[mesonCat][3]

    x = ROOT.RooRealVar('mh', 'm_{{#gamma, {0} }} [GeV]'.format(mesonLatex[mesonCat]), xlowRange, xhighRange)
    y = ROOT.RooRealVar('mmeson', '{0} [GeV]'.format(doubleFitVar[mesonCat][2]), ylowRange, yhighRange)

    x.setRange("full", xlowRange, xhighRange)
    y.setRange("full", ylowRange, yhighRange)

    data = ROOT.RooDataHist('datahist_' + mesonCat + '_' + tag, 'data', ROOT.RooArgList(x, y), data_full)

    #BERN law (Higgs mass) -----------------------------------------------------------------------------
    bern_mh_c0_mod = ROOT.RooRealVar('bern_mh_c0_mod_' + mesonCat + "_" + tag, 'bern_mh_c0', 0.10, -1., 1.0)
    bern_mh_c0 = ROOT.RooRealVar('bern_mh_c0_' + mesonCat + "_" + tag, 'bern_mh_c0', fitInitVals[mesonCat]["bern_mh"][0][0], fitInitVals[mesonCat]["bern_mh"][0][1], fitInitVals[mesonCat]["bern_mh"][0][2])
    bern_mh_c1 = ROOT.RooRealVar('bern_mh_c1_' + mesonCat + "_" + tag, 'bern_mh_c1', fitInitVals[mesonCat]["bern_mh"][1][0], fitInitVals[mesonCat]["bern_mh"][1][1], fitInitVals[mesonCat]["bern_mh"][1][2])
    bern_mh_c2 = ROOT.RooRealVar('bern_mh_c2_' + mesonCat + "_" + tag, 'bern_mh_c2', fitInitVals[mesonCat]["bern_mh"][2][0], fitInitVals[mesonCat]["bern_mh"][2][1], fitInitVals[mesonCat]["bern_mh"][2][2])
    bern_mh_c3 = ROOT.RooRealVar('bern_mh_c3_' + mesonCat + "_" + tag, 'bern_mh_c3', fitInitVals[mesonCat]["bern_mh"][3][0], fitInitVals[mesonCat]["bern_mh"][3][1], fitInitVals[mesonCat]["bern_mh"][3][2])
    bern_mh_c4 = ROOT.RooRealVar('bern_mh_c4_' + mesonCat + "_" + tag, 'bern_mh_c4', fitInitVals[mesonCat]["bern_mh"][4][0], fitInitVals[mesonCat]["bern_mh"][4][1], fitInitVals[mesonCat]["bern_mh"][4][2])
    bern_mh_c5 = ROOT.RooRealVar('bern_mh_c5_' + mesonCat + "_" + tag, 'bern_mh_c5', fitInitVals[mesonCat]["bern_mh"][5][0], fitInitVals[mesonCat]["bern_mh"][5][1], fitInitVals[mesonCat]["bern_mh"][5][2])

    pdf_bern0_mh_mod = ROOT.RooBernstein('bern0_mod_' + mesonCat + "_" + tag + "_mh", 'bern0_mh', x, ROOT.RooArgList(bern_mh_c0_mod))
    pdf_bern0_mh = ROOT.RooBernstein('bern0_' + mesonCat + "_" + tag + "_mh", 'bern0_mh', x, ROOT.RooArgList(bern_mh_c0))
    pdf_bern1_mh = ROOT.RooBernstein('bern1_' + mesonCat + "_" + tag + "_mh", 'bern1_mh', x, ROOT.RooArgList(bern_mh_c0, bern_mh_c1))
    pdf_bern2_mh = ROOT.RooBernstein('bern2_' + mesonCat + "_" + tag + "_mh", 'bern2_mh', x, ROOT.RooArgList(bern_mh_c0, bern_mh_c1, bern_mh_c2))
    pdf_bern3_mh = ROOT.RooBernstein('bern3_' + mesonCat + "_" + tag + "_mh", 'bern3_mh', x, ROOT.RooArgList(bern_mh_c0, bern_mh_c1, bern_mh_c2, bern_mh_c3))
    pdf_bern4_mh = ROOT.RooBernstein('bern4_' + mesonCat + "_" + tag + "_mh", 'bern4_mh', x, ROOT.RooArgList(bern_mh_c0, bern_mh_c1, bern_mh_c2, bern_mh_c3, bern_mh_c4))
    pdf_bern5_mh = ROOT.RooBernstein('bern5_' + mesonCat + "_" + tag + "_mh", 'bern5_mh', x, ROOT.RooArgList(bern_mh_c0, bern_mh_c1, bern_mh_c2, bern_mh_c3, bern_mh_c4, bern_mh_c5))

    #CHEBYCHEV law (Higgs mass) ------------------------------------------------------------------------
    chebychev_mh_c0 = ROOT.RooRealVar('chebychev_mh_c0_' + mesonCat + "_" + tag, 'chebychev_mh_c0', fitInitVals[mesonCat]["cheb_mh"][0][0], fitInitVals[mesonCat]["cheb_mh"][0][1], fitInitVals[mesonCat]["cheb_mh"][0][2])
    chebychev_mh_c1 = ROOT.RooRealVar('chebychev_mh_c1_' + mesonCat + "_" + tag, 'chebychev_mh_c1', fitInitVals[mesonCat]["cheb_mh"][1][0], fitInitVals[mesonCat]["cheb_mh"][1][1], fitInitVals[mesonCat]["cheb_mh"][1][2])
    chebychev_mh_c2 = ROOT.RooRealVar('chebychev_mh_c2_' + mesonCat + "_" + tag, 'chebychev_mh_c2', fitInitVals[mesonCat]["cheb_mh"][2][0], fitInitVals[mesonCat]["cheb_mh"][2][1], fitInitVals[mesonCat]["cheb_mh"][2][2])
    chebychev_mh_c3 = ROOT.RooRealVar('chebychev_mh_c3_' + mesonCat + "_" + tag, 'chebychev_mh_c3', fitInitVals[mesonCat]["cheb_mh"][3][0], fitInitVals[mesonCat]["cheb_mh"][3][1], fitInitVals[mesonCat]["cheb_mh"][3][2])
    chebychev_mh_c4 = ROOT.RooRealVar('chebychev_mh_c4_' + mesonCat + "_" + tag, 'chebychev_mh_c4', fitInitVals[mesonCat]["cheb_mh"][4][0], fitInitVals[mesonCat]["cheb_mh"][4][1], fitInitVals[mesonCat]["cheb_mh"][4][2])
    chebychev_mh_c5 = ROOT.RooRealVar('chebychev_mh_c5_' + mesonCat + "_" + tag, 'chebychev_mh_c5', fitInitVals[mesonCat]["cheb_mh"][5][0], fitInitVals[mesonCat]["cheb_mh"][5][1], fitInitVals[mesonCat]["cheb_mh"][5][2])

    pdf_chebychev1_mh = ROOT.RooChebychev("chebychev1_" + mesonCat + "_" + tag + "_mh", "chebychev1_mh", x, ROOT.RooArgList(chebychev_mh_c0, chebychev_mh_c1))
    pdf_chebychev2_mh = ROOT.RooChebychev("chebychev2_" + mesonCat + "_" + tag + "_mh", "chebychev2_mh", x, ROOT.RooArgList(chebychev_mh_c0, chebychev_mh_c1, chebychev_mh_c2))
    pdf_chebychev3_mh = ROOT.RooChebychev("chebychev3_" + mesonCat + "_" + tag + "_mh", "chebychev3_mh", x, ROOT.RooArgList(chebychev_mh_c0, chebychev_mh_c1, chebychev_mh_c2, chebychev_mh_c3))
    pdf_chebychev4_mh = ROOT.RooChebychev("chebychev4_" + mesonCat + "_" + tag + "_mh", "chebychev4_mh", x, ROOT.RooArgList(chebychev_mh_c0, chebychev_mh_c1, chebychev_mh_c2, chebychev_mh_c3, chebychev_mh_c4))
    pdf_chebychev5_mh = ROOT.RooChebychev("chebychev5_" + mesonCat + "_" + tag + "_mh", "chebychev5_mh", x, ROOT.RooArgList(chebychev_mh_c0, chebychev_mh_c1, chebychev_mh_c2, chebychev_mh_c3, chebychev_mh_c4, chebychev_mh_c5))

    #BERN law (Meson mass) -----------------------------------------------------------------------------
    bern_mm_c0 = ROOT.RooRealVar('bern_mm_c0_' + mesonCat + "_" + tag, 'bern_mm_c0', fitInitVals[mesonCat]["bern_mm"][0][0], fitInitVals[mesonCat]["bern_mm"][0][1], fitInitVals[mesonCat]["bern_mm"][0][2])
    bern_mm_c1 = ROOT.RooRealVar('bern_mm_c1_' + mesonCat + "_" + tag, 'bern_mm_c1', fitInitVals[mesonCat]["bern_mm"][1][0], fitInitVals[mesonCat]["bern_mm"][1][1], fitInitVals[mesonCat]["bern_mm"][1][2])
    bern_mm_c2 = ROOT.RooRealVar('bern_mm_c2_' + mesonCat + "_" + tag, 'bern_mm_c2', fitInitVals[mesonCat]["bern_mm"][2][0], fitInitVals[mesonCat]["bern_mm"][2][1], fitInitVals[mesonCat]["bern_mm"][2][2])
    bern_mm_c3 = ROOT.RooRealVar('bern_mm_c3_' + mesonCat + "_" + tag, 'bern_mm_c3', fitInitVals[mesonCat]["bern_mm"][3][0], fitInitVals[mesonCat]["bern_mm"][3][1], fitInitVals[mesonCat]["bern_mm"][3][2])
    bern_mm_c4 = ROOT.RooRealVar('bern_mm_c4_' + mesonCat + "_" + tag, 'bern_mm_c4', fitInitVals[mesonCat]["bern_mm"][4][0], fitInitVals[mesonCat]["bern_mm"][4][1], fitInitVals[mesonCat]["bern_mm"][4][2])
    bern_mm_c5 = ROOT.RooRealVar('bern_mm_c5_' + mesonCat + "_" + tag, 'bern_mm_c5', fitInitVals[mesonCat]["bern_mm"][5][0], fitInitVals[mesonCat]["bern_mm"][5][1], fitInitVals[mesonCat]["bern_mm"][5][2])

    pdf_bern0_mm = ROOT.RooBernstein('bern0_' + mesonCat + "_" + tag + "_mm", 'bern0_mm', y, ROOT.RooArgList(bern_mm_c0))
    pdf_bern1_mm = ROOT.RooBernstein('bern1_' + mesonCat + "_" + tag + "_mm", 'bern1_mm', y, ROOT.RooArgList(bern_mm_c0, bern_mm_c1))
    pdf_bern2_mm = ROOT.RooBernstein('bern2_' + mesonCat + "_" + tag + "_mm", 'bern2_mm', y, ROOT.RooArgList(bern_mm_c0, bern_mm_c1, bern_mm_c2))
    pdf_bern3_mm = ROOT.RooBernstein('bern3_' + mesonCat + "_" + tag + "_mm", 'bern3_mm', y, ROOT.RooArgList(bern_mm_c0, bern_mm_c1, bern_mm_c2, bern_mm_c3))
    pdf_bern4_mm = ROOT.RooBernstein('bern4_' + mesonCat + "_" + tag + "_mm", 'bern4_mm', y, ROOT.RooArgList(bern_mm_c0, bern_mm_c1, bern_mm_c2, bern_mm_c3, bern_mm_c4))
    pdf_bern5_mm = ROOT.RooBernstein('bern5_' + mesonCat + "_" + tag + "_mm", 'bern5_mm', y, ROOT.RooArgList(bern_mm_c0, bern_mm_c1, bern_mm_c2, bern_mm_c3, bern_mm_c4, bern_mm_c5))

    #CHEBYCHEV law (Meson mass) ------------------------------------------------------------------------
    chebychev_mm_c0 = ROOT.RooRealVar('chebychev_mm_c0_' + mesonCat + "_" + tag, 'chebychev_mm_c0', fitInitVals[mesonCat]["cheb_mm"][0][0], fitInitVals[mesonCat]["cheb_mm"][0][1], fitInitVals[mesonCat]["cheb_mm"][0][2])
    chebychev_mm_c1 = ROOT.RooRealVar('chebychev_mm_c1_' + mesonCat + "_" + tag, 'chebychev_mm_c1', fitInitVals[mesonCat]["cheb_mm"][1][0], fitInitVals[mesonCat]["cheb_mm"][1][1], fitInitVals[mesonCat]["cheb_mm"][1][2])
    chebychev_mm_c2 = ROOT.RooRealVar('chebychev_mm_c2_' + mesonCat + "_" + tag, 'chebychev_mm_c2', fitInitVals[mesonCat]["cheb_mm"][2][0], fitInitVals[mesonCat]["cheb_mm"][2][1], fitInitVals[mesonCat]["cheb_mm"][2][2])
    chebychev_mm_c3 = ROOT.RooRealVar('chebychev_mm_c3_' + mesonCat + "_" + tag, 'chebychev_mm_c3', fitInitVals[mesonCat]["cheb_mm"][3][0], fitInitVals[mesonCat]["cheb_mm"][3][1], fitInitVals[mesonCat]["cheb_mm"][3][2])
    chebychev_mm_c4 = ROOT.RooRealVar('chebychev_mm_c4_' + mesonCat + "_" + tag, 'chebychev_mm_c4', fitInitVals[mesonCat]["cheb_mm"][4][0], fitInitVals[mesonCat]["cheb_mm"][4][1], fitInitVals[mesonCat]["cheb_mm"][4][2])
    chebychev_mm_c5 = ROOT.RooRealVar('chebychev_mm_c5_' + mesonCat + "_" + tag, 'chebychev_mm_c5', fitInitVals[mesonCat]["cheb_mm"][5][0], fitInitVals[mesonCat]["cheb_mm"][5][1], fitInitVals[mesonCat]["cheb_mm"][5][2])

    pdf_chebychev1_mm = ROOT.RooChebychev("chebychev1_" + mesonCat + "_" + tag + "_mm", "chebychev1_mm", y, ROOT.RooArgList(chebychev_mm_c0, chebychev_mm_c1))
    pdf_chebychev2_mm = ROOT.RooChebychev("chebychev2_" + mesonCat + "_" + tag + "_mm", "chebychev2_mm", y, ROOT.RooArgList(chebychev_mm_c0, chebychev_mm_c1, chebychev_mm_c2))
    pdf_chebychev3_mm = ROOT.RooChebychev("chebychev3_" + mesonCat + "_" + tag + "_mm", "chebychev3_mm", y, ROOT.RooArgList(chebychev_mm_c0, chebychev_mm_c1, chebychev_mm_c2, chebychev_mm_c3))
    pdf_chebychev4_mm = ROOT.RooChebychev("chebychev4_" + mesonCat + "_" + tag + "_mm", "chebychev4_mm", y, ROOT.RooArgList(chebychev_mm_c0, chebychev_mm_c1, chebychev_mm_c2, chebychev_mm_c3, chebychev_mm_c4))

    storedPdfs = ROOT.RooArgList("store_" + mesonCat + "_" + tag)

    

    if mesonCat in ["Phi3Cat", "OmegaCat"]:
        pdf_bern_mh = pdf_bern4_mh
        pdf_bern_mm = pdf_bern4_mm
        pdf_cheb_mh = pdf_chebychev4_mh
        pdf_cheb_mm = pdf_chebychev4_mm
    else:
        pdf_bern_mh = pdf_bern3_mh
        pdf_bern_mm = pdf_bern3_mm
        pdf_cheb_mh = pdf_chebychev3_mh
        pdf_cheb_mm = pdf_chebychev3_mm
    if mesonCat in ["D0StarCat"]:
        gauss_mu = ROOT.RooRealVar('gauss_mu_' + mesonCat + "_" + tag, 'gauss_mu', 1.865, 1.83, 1.90)
        gauss_sigma = ROOT.RooRealVar('gauss_sigma_' + mesonCat + "_" + tag, 'gauss_sigma', 0.03, 0.002, 0.10)
        pdf_gauss = ROOT.RooGaussian('gauss_' + mesonCat + "_" + tag, 'gauss', y , gauss_mu, gauss_sigma)

        fraction_1 = ROOT.RooRealVar("fraction_1", "", 0.95, 0.6, 1.)
        pdf_bern_mm = ROOT.RooAddPdf('bern3_' + mesonCat + "_" + tag + "_mm_mod", 'bern3_mm_mod', ROOT.RooArgList(pdf_bern3_mm, pdf_gauss), ROOT.RooArgList(fraction_1))
        pdf_cheb_mm = ROOT.RooAddPdf('chebychev3_' + mesonCat + "_" + tag + "_mm_mod", 'chebychev3_mm_mod', ROOT.RooArgList(pdf_chebychev3_mm, pdf_gauss), ROOT.RooArgList(fraction_1))

    model2D_bb = ROOT.RooProdPdf("pdf_2d_bkg_bern_bern_" + mesonCat + "_" + tag, "pdf_2d_bkg_bern_bern", ROOT.RooArgList(pdf_bern_mh, pdf_bern_mm))
    model2D_bc = ROOT.RooProdPdf("pdf_2d_bkg_bern_cheb_" + mesonCat + "_" + tag, "pdf_2d_bkg_bern_cheb", ROOT.RooArgList(pdf_bern_mh, pdf_cheb_mm))
    model2D_cb = ROOT.RooProdPdf("pdf_2d_bkg_cheb_bern_" + mesonCat + "_" + tag, "pdf_2d_bkg_cheb_bern", ROOT.RooArgList(pdf_cheb_mh, pdf_bern_mm))
    model2D_cc = ROOT.RooProdPdf("pdf_2d_bkg_cheb_cheb_" + mesonCat + "_" + tag, "pdf_2d_bkg_cheb_cheb", ROOT.RooArgList(pdf_cheb_mh, pdf_cheb_mm))


    fitresults_bb = model2D_bb.fitTo(data, ROOT.RooFit.Minimizer("Minuit2"), ROOT.RooFit.Strategy(2), ROOT.RooFit.Range("full"), ROOT.RooFit.Save(ROOT.kTRUE))
    fitresults_bc = model2D_bc.fitTo(data, ROOT.RooFit.Minimizer("Minuit2"), ROOT.RooFit.Strategy(2), ROOT.RooFit.Range("full"), ROOT.RooFit.Save(ROOT.kTRUE))
    fitresults_cb = model2D_cb.fitTo(data, ROOT.RooFit.Minimizer("Minuit2"), ROOT.RooFit.Strategy(2), ROOT.RooFit.Range("full"), ROOT.RooFit.Save(ROOT.kTRUE))
    fitresults_cc = model2D_cc.fitTo(data, ROOT.RooFit.Minimizer("Minuit2"), ROOT.RooFit.Strategy(2), ROOT.RooFit.Range("full"), ROOT.RooFit.Save(ROOT.kTRUE))
    storedPdfs.add(model2D_bb)
    storedPdfs.add(model2D_bc)
    storedPdfs.add(model2D_cb)
    storedPdfs.add(model2D_cc)

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
    model2D_bb.plotOn(plotFrameWithNormRangeMH, ROOT.RooFit.Components(model2D_bb.GetName()), ROOT.RooFit.Range("full"), ROOT.RooFit.NormRange("full"), ROOT.RooFit.LineColor(ROOT.kRed))
    model2D_cc.plotOn(plotFrameWithNormRangeMH, ROOT.RooFit.Components(model2D_cc.GetName()), ROOT.RooFit.Range("full"), ROOT.RooFit.NormRange("full"), ROOT.RooFit.LineColor(ROOT.kBlue))
    model2D_bb.paramOn(plotFrameWithNormRangeMH, ROOT.RooFit.Layout(0.40, 0.35, 0.5))
    #model2D_cc.paramOn(plotFrameWithNormRangeMH, ROOT.RooFit.Layout(0.65, 0.99, 0.75))
    print(plotFrameWithNormRangeMH.Print("V"))
    name_bb = model2D_bb.GetName() + "_Int[mmeson]_Norm[mh,mmeson]_Comp[" + model2D_bb.GetName() + "]_Range[full]_NormRange[full]"
    name_cc = model2D_cc.GetName() + "_Int[mmeson]_Norm[mh,mmeson]_Comp[" + model2D_cc.GetName() + "]_Range[full]_NormRange[full]"

    hist1 = plotFrameWithNormRangeMH.getCurve(name_bb)
    hist2 = plotFrameWithNormRangeMH.getCurve(name_cc)
    hist1.Print()
    print(type(hist1))
    f = ROOT.TFile("/data/submit/pdmonte/thesisFitRootFiles/{}_MH_curve.root".format(getNameOfHistFileSimple(mesonCat, cat, year, date, extraTitle=extraTitle, regModelName=regModelName)),"RECREATE")
    f.WriteObject(hist1, "curve1")
    f.WriteObject(hist2, "curve2")
    f.Close()
    f = ROOT.TFile("/data/submit/pdmonte/thesisFitRootFiles/{}_hist.root".format(getNameOfHistFileSimple(mesonCat, cat, year, date, extraTitle=extraTitle, regModelName=regModelName)),"RECREATE")
    f.WriteObject(data, "hist")
    f.Close()

    chi2_bb = plotFrameWithNormRangeMH.chiSquare(name_bb, "h_" + data.GetName(), fitresults_bb.floatParsFinal().getSize()) #name1 is name of the model, "h_" + ... is name of the hist
    chi2_cc = plotFrameWithNormRangeMH.chiSquare(name_cc, "h_" + data.GetName(), fitresults_cc.floatParsFinal().getSize()) #name1 is name of the model, "h_" + ... is name of the hist
    
    print('----------------------------------------')
    print(model2D_bb.GetName(), "    chi2/ndof=",round(chi2_bb,2), " ndof", fitresults_bb.floatParsFinal().getSize())
    print(model2D_cc.GetName(), "    chi2/ndof=",round(chi2_cc,2), " ndof", fitresults_cc.floatParsFinal().getSize())
    print('----------------------------------------')
    plotFrameWithNormRangeMH.Draw()
    plotFrameWithNormRangeMH.getAttText().SetTextSize(0.02)
    data_full.GetXaxis().SetRangeUser(xlowRange, xhighRange)

    latexMH = ROOT.TLatex()
    latexMH.SetTextSize(0.03)
    latexMH.SetTextColor(ROOT.kRed)
    latexMH.SetTextAlign(12)
    latexMH.DrawLatexNDC(0.13, 0.865, model2D_bb.GetName())
    latexMH.SetTextAlign(32)
    latexMH.DrawLatexNDC(0.60, 0.865, "#chi^{{2}}/ndof: {}".format(round(chi2_bb, 2)))
    latexMH.SetTextColor(ROOT.kBlue)
    latexMH.SetTextAlign(12)
    latexMH.DrawLatexNDC(0.13, 0.825, model2D_cc.GetName())
    latexMH.SetTextAlign(32)
    latexMH.DrawLatexNDC(0.60, 0.825, "#chi^{{2}}/ndof: {}".format(round(chi2_cc, 2)))
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
    residualsFrame1 = x.frame(ROOT.RooFit.Title("Residuals model 1"))
    hresid1 = plotFrameWithNormRangeMH.residHist("h_" + data.GetName(), name_bb)
    residualsFrame1.addPlotable(hresid1, "P")
    residualsFrame1.Draw()
    
    canvasMH.cd()
    pad3 = ROOT.TPad("Pull pad", "Pull pad", 0, 0, 1.0, 0.20)
    pad3.Draw()
    pad3.cd()
    residualsFrame2 = x.frame(ROOT.RooFit.Title("Residuals model 2"))
    hresid2 = plotFrameWithNormRangeMH.residHist("h_" + data.GetName(), name_cc)
    residualsFrame2.addPlotable(hresid2, "P")
    residualsFrame2.Draw()

    fileName = "~/public_html/fits/{}/{}".format(mesonCat[:-3], mesonCat)
    if regModelName is not None:
        fileName += "_" + regModelName
    if extraTitle is not None:
        fileName += "_" + extraTitle.replace(" ", "_").replace(",", "")
    canvasMH.SaveAs(fileName + "_2Dfit_MH.png")


    # Projection of the HiggsCandMass
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
    model2D_bb.plotOn(plotFrameWithNormRangeMM, ROOT.RooFit.Components(model2D_bb.GetName()), ROOT.RooFit.Range("full"), ROOT.RooFit.NormRange("full"), ROOT.RooFit.LineColor(ROOT.kRed))
    model2D_cc.plotOn(plotFrameWithNormRangeMM, ROOT.RooFit.Components(model2D_cc.GetName()), ROOT.RooFit.Range("full"), ROOT.RooFit.NormRange("full"), ROOT.RooFit.LineColor(ROOT.kBlue))
    model2D_bb.paramOn(plotFrameWithNormRangeMM, ROOT.RooFit.Layout(0.10, 0.40, 0.5))
    print(plotFrameWithNormRangeMM.Print("V"))
    name_bb = model2D_bb.GetName() + "_Int[mh]_Norm[mh,mmeson]_Comp[" + model2D_bb.GetName() + "]_Range[full]_NormRange[full]"
    name_cc = model2D_cc.GetName() + "_Int[mh]_Norm[mh,mmeson]_Comp[" + model2D_cc.GetName() + "]_Range[full]_NormRange[full]"

    hist1 = plotFrameWithNormRangeMM.getCurve(name_bb)
    hist2 = plotFrameWithNormRangeMM.getCurve(name_cc)
    hist1.Print()
    print(type(hist1))
    f = ROOT.TFile("/data/submit/pdmonte/thesisFitRootFiles/{}_MM_curve.root".format(getNameOfHistFileSimple(mesonCat, cat, year, date, extraTitle=extraTitle, regModelName=regModelName)),"RECREATE")
    f.WriteObject(hist1, "curve1")
    f.WriteObject(hist2, "curve2")

    chi2_bb = plotFrameWithNormRangeMM.chiSquare(name_bb, "h_" + data.GetName(), fitresults_bb.floatParsFinal().getSize()) #name1 is name of the model, "h_" + ... is name of the hist
    chi2_cc = plotFrameWithNormRangeMM.chiSquare(name_cc, "h_" + data.GetName(), fitresults_cc.floatParsFinal().getSize()) #name1 is name of the model, "h_" + ... is name of the hist
    
    print('----------------------------------------')
    print(model2D_bb.GetName(), "    chi2/ndof=",round(chi2_bb,2), " ndof", fitresults_bb.floatParsFinal().getSize())
    print(model2D_cc.GetName(), "    chi2/ndof=",round(chi2_cc,2), " ndof", fitresults_cc.floatParsFinal().getSize())
    print('----------------------------------------')
    plotFrameWithNormRangeMM.Draw()
    plotFrameWithNormRangeMM.getAttText().SetTextSize(0.017)
    data_full.GetYaxis().SetRangeUser(ylowRange, yhighRange)

    latexMM = ROOT.TLatex()
    latexMM.SetTextSize(0.03)
    latexMM.SetTextColor(ROOT.kRed)
    latexMM.SetTextAlign(12)
    latexMM.DrawLatexNDC(0.13, 0.865, model2D_bb.GetName())
    latexMM.SetTextAlign(32)
    latexMM.DrawLatexNDC(0.60, 0.865, "#chi^{{2}}/ndof: {}".format(round(chi2_bb, 2)))
    latexMM.SetTextColor(ROOT.kBlue)
    latexMM.SetTextAlign(12)
    latexMM.DrawLatexNDC(0.13, 0.825, model2D_cc.GetName())
    latexMM.SetTextAlign(32)
    latexMM.DrawLatexNDC(0.60, 0.825, "#chi^{{2}}/ndof: {}".format(round(chi2_cc, 2)))
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
    residualsFrame1 = y.frame(ROOT.RooFit.Title("Residuals model 1"))
    hresid1 = plotFrameWithNormRangeMM.residHist("h_" + data.GetName(), name_bb)
    residualsFrame1.addPlotable(hresid1, "P")
    residualsFrame1.Draw()
    
    canvasMM.cd()
    pad3 = ROOT.TPad("Pull pad", "Pull pad", 0, 0, 1.0, 0.20)
    pad3.Draw()
    pad3.cd()
    residualsFrame2 = y.frame(ROOT.RooFit.Title("Residuals model 2"))
    hresid2 = plotFrameWithNormRangeMM.residHist("h_" + data.GetName(), name_cc)
    residualsFrame2.addPlotable(hresid2, "P")
    residualsFrame2.Draw()

    fileName = "~/public_html/fits/{}/{}".format(mesonCat[:-3], mesonCat)
    if regModelName is not None:
        fileName += "_" + regModelName
    if extraTitle is not None:
        fileName += "_" + extraTitle.replace(" ", "_").replace(",", "")
    canvasMM.SaveAs(fileName + "_2Dfit_MM.png")


    # Create workspace
    w = ROOT.RooWorkspace("w", "workspace")
    
    norm_range = data_full.Integral(data_full.GetXaxis().FindBin(xlowRange), data_full.GetXaxis().FindBin(xhighRange), data_full.GetYaxis().FindBin(ylowRange), data_full.GetYaxis().FindBin(yhighRange))
    BKG_norm = ROOT.RooRealVar("multipdf_"+mesonCat+"_"+tag+"_bkg"+"_norm", model2D_bb.GetName()+"_norm", norm_range, 0.5*norm_range, 2*norm_range)

    pdf_cat = ROOT.RooCategory("pdfindex_"+mesonCat+"_"+tag,"pdfindex"+"_"+mesonCat+"_"+tag)
    pdf_bkg = ROOT.RooMultiPdf("multipdf_"+mesonCat+"_"+tag+"_bkg","multipdf",pdf_cat,storedPdfs)
    getattr(w,'import')(pdf_bkg)

    # Import model_norm
    getattr(w,'import')(BKG_norm)
    print("integral BKG", BKG_norm.Print())

    # Import data into the workspace
    getattr(w,'import')(data)
    
    # Print workspace contents
    w.Print()

    # -----------------------------------------------------------------------------
    # Save workspace in file, create folder if it does not exist
    if not os.path.exists(workspaceName):
        os.mkdir(workspaceName)

    workspaceFileName = "Bkg_" + mesonCat[:-3] + "_" + tag + "_" + str(year)
    if regModelName is not None:
        workspaceFileName += "_" + regModelName

    w.writeToFile(workspaceName + "/" + workspaceFileName + "_2D_workspace.root")
    print('\033[1;31m' + "[fitBkg2D] Fit done, workspace created!" + '\033[0m')











if __name__ == "__main__":

    cat = "GFcat"
    year = 2018
    date = "NOV05"


    #BACKGROUND D0Star-----------------------------------------------------------------------------

    #BACKGROUND Phi3-------------------------------------------------------------------------------
    df = False
    mesonCat = "Phi3Cat"
    #mesonCat = "OmegaCat"
    #mesonCat = "D0StarCat"
    #for mesonCat in ["Phi3Cat", "OmegaCat", "D0StarCat", "D0StarRhoCat"]:
    for mesonCat in ["D0StarCat"]:
        with open('models_{}.txt'.format(mesonCat[:-3]), 'r') as file:
            for line in file:
                regModelName = line.strip()
                if regModelName[0] != "#":
                    #fitBkg(cat, mesonCat, year, date, regModelName=regModelName)
                    fitBkg2D(cat, mesonCat, year, date, regModelName=regModelName)
    #fitBkg(cat, mesonCat, year, date)
