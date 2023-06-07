import ROOT

ROOT.ROOT.EnableImplicitMT()

if "/home/submit/pdmonte/CMSSW_10_6_27/src/Hrare2023/analysis/func_marti.so" not in ROOT.gSystem.GetLibraries():
    ROOT.gSystem.CompileMacro("/home/submit/pdmonte/CMSSW_10_6_27/src/Hrare2023/analysis/func_marti.cc","k")

date = "MAY23"

chainSGN = ROOT.TChain("events")
chainSGN.Add("/home/submit/pdmonte/CMSSW_10_6_27/src/Hrare2023/analysis/outputs/{0}/2018/outname_mc1040_GFcat_OmegaCat_2018.root".format(date))

df = ROOT.RDataFrame(chainSGN)

canvas = ROOT.TCanvas("canvas", "canvas", 1200, 800)

bins=100

h0=df.Define("scale", "w*lumiIntegrated")\
    .Define("filt", "(goodMeson_Nphotons < 1)")\
    .Define("good", "goodMeson_charged_pt[filt]")\
    .Histo1D(("hist", "#phi kinematic mass", bins, 0.0, 200),"good")

h1=df.Define("scale", "w*lumiIntegrated")\
    .Define("filt", "(goodMeson_Nphotons < 2 && goodMeson_Nphotons > 0)")\
    .Define("good", "goodMeson_charged_pt[filt]")\
    .Histo1D(("hist", "#phi kinematic mass", bins, 0.0, 200),"good")

h2=df.Define("scale", "w*lumiIntegrated")\
    .Define("filt", "(goodMeson_Nphotons > 1)")\
    .Define("good", "goodMeson_charged_pt[filt]")\
    .Histo1D(("hist", "#phi kinematic mass", bins, 0.0, 200),"good")

h0.SetFillColorAlpha(ROOT.kRed, 0.5)
h0.SetLineColor(ROOT.kBlack)
h1.SetFillColorAlpha(ROOT.kGreen, 0.5)
h1.SetLineColor(ROOT.kBlack)
h2.SetFillColorAlpha(ROOT.kBlue, 0.5)
h2.SetLineColor(ROOT.kBlack)

h0.Scale(1/h0.GetEntries())
h1.Scale(1/h1.GetEntries())
h2.Scale(1/h2.GetEntries())

print(h0.GetMean())
print(h1.GetMean())
print(h2.GetMean())

stack = ROOT.THStack("stack", "#phi kinetic PT, reconstruction")
stack.Add(h0.GetValue())
stack.Add(h1.GetValue())
stack.Add(h2.GetValue())
stack.Draw("hist nostack")
stack.GetXaxis().SetTitle("p_{T}_{2trk}^{#phi#rightarrow #pi#pi} [GeV]")
stack.GetYaxis().SetTitle("Frequency")

legend = ROOT.TLegend(0.60, 0.65, 0.8999, 0.89)
legend.SetMargin(0.17)
legend.SetBorderSize(0)
legend.SetTextSize(0.04)
legend.AddEntry(h0.GetValue(), "0 #gamma (mean: {:.1f} GeV)".format(round(h0.GetMean(), 3)), "f")
legend.AddEntry(h1.GetValue(), "1 #gamma (mean: {:.1f} GeV)".format(round(h1.GetMean(), 3)), "f")
legend.AddEntry(h2.GetValue(), ">2 #gamma (mean: {:.1f} GeV)".format(round(h2.GetMean(), 3)), "f")
legend.Draw()

canvas.SaveAs("~/public_html/plotsMAY24/PhiSGN_kin_pt_Nphotons.png")

