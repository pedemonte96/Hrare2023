import ROOT

ROOT.ROOT.EnableImplicitMT()

if "/home/submit/pdmonte/CMSSW_10_6_27/src/Hrare2023/analysis/func_marti.so" not in ROOT.gSystem.GetLibraries():
    ROOT.gSystem.CompileMacro("/home/submit/pdmonte/CMSSW_10_6_27/src/Hrare2023/analysis/func_marti.cc","k")

date = "MAY19"

chainSGN = ROOT.TChain("events")
chainSGN.Add("/data/submit/pdmonte/outputs/{0}/2018/outname_mc1040_GFcat_OmegaCat_2018.root".format(date))

df = ROOT.RDataFrame(chainSGN)

canvas = ROOT.TCanvas("canvas", "canvas", 1200, 800)

bins=100

thres=1.4

h1=df.Define("scale", "w*lumiIntegrated")\
    .Define("filt", "abs(goodMeson_charged_eta) < {}".format(thres))\
    .Define("good", "goodMeson_threemass[filt]")\
    .Histo1D(("hist", "#phi three mass", bins, 0.4, 1.6),"good", "scale")

h2=df.Define("scale", "w*lumiIntegrated")\
    .Define("filt", "abs(goodMeson_charged_eta) > {}".format(thres))\
    .Define("good", "goodMeson_threemass[filt]")\
    .Histo1D(("hist", "#phi three mass", bins, 0.4, 1.6),"good", "scale")

h1.SetFillColor(ROOT.kGreen-6)
h1.SetLineColor(ROOT.kBlack)
h2.SetFillColor(ROOT.kGreen+3)
h2.SetLineColor(ROOT.kBlack)

stack = ROOT.THStack("stack", "#phi three mass, reconstruction")
stack.Add(h2.GetValue())
stack.Add(h1.GetValue())
stack.Draw("hist")
stack.GetXaxis().SetTitle("m_{#phi}^{#phi#rightarrow #pi#pi#pi} [GeV]")
stack.GetYaxis().SetTitle("Events")
stack.SetMaximum(1100.)

width = 0.004249
center = 1.019461
n=20
l = ROOT.TLine(center, 0, center, 1100)
l.SetLineWidth(2)
l.SetLineColor(ROOT.kBlack)
l.Draw()
l1 = ROOT.TLine(center-n*width, 0, center-n*width, 1100)
l1.SetLineWidth(2)
l1.SetLineStyle(2)
l1.SetLineColor(ROOT.kBlack)
l1.Draw()
l2 = ROOT.TLine(center+n*width, 0, center+n*width, 1100)
l2.SetLineWidth(2)
l2.SetLineStyle(2)
l2.SetLineColor(ROOT.kBlack)
l2.Draw()

legend = ROOT.TLegend(0.61, 0.70, 0.8999, 0.89)
legend.SetMargin(0.12)
legend.SetBorderSize(0)
legend.SetTextSize(0.04)
legend.AddEntry(h1.GetValue(), "Barrel meson (|#kern[-0.3]{{#eta}}|<{0})".format(thres), "f")
legend.AddEntry(h2.GetValue(), "Endcap meson (|#kern[-0.3]{{#eta}}|>{0})".format(thres), "f")
legend.AddEntry(l, "m_{#phi} = 1020 GeV", "l")
legend.AddEntry(l1, "m_{#phi} #pm 20#Gamma_{#phi}", "l")
legend.Draw()

canvas.SaveAs("~/public_html/plotsMAY24/PhiSGN_phi_three_mass_barrel.png")

