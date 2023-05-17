import ROOT

ROOT.ROOT.EnableImplicitMT()

if "/work/submit/pdmonte/Hrare2023/analysis/func_marti.so" not in ROOT.gSystem.GetLibraries():
    ROOT.gSystem.CompileMacro("/work/submit/pdmonte/Hrare2023/analysis/func_marti.cc","k")

date = "MAY16"

chainSGN = ROOT.TChain("events");
chainSGN.Add("/work/submit/pdmonte/Hrare2023/analysis/{0}/2018/outname_mc1039_GFcat_D0StarCat_2018.root".format(date))

chainBKG = ROOT.TChain("events");
chainBKG.Add("/work/submit/pdmonte/Hrare2023/analysis/{0}/2018/outname_mc10_GFcat_D0StarCat_2018.root".format(date))
chainBKG.Add("/work/submit/pdmonte/Hrare2023/analysis/{0}/2018/outname_mc11_GFcat_D0StarCat_2018.root".format(date))
chainBKG.Add("/work/submit/pdmonte/Hrare2023/analysis/{0}/2018/outname_mc12_GFcat_D0StarCat_2018.root".format(date))
chainBKG.Add("/work/submit/pdmonte/Hrare2023/analysis/{0}/2018/outname_mc13_GFcat_D0StarCat_2018.root".format(date))
chainBKG.Add("/work/submit/pdmonte/Hrare2023/analysis/{0}/2018/outname_mc14_GFcat_D0StarCat_2018.root".format(date))

df = ROOT.RDataFrame(chainSGN)
dg = ROOT.RDataFrame(chainBKG)

canvas = ROOT.TCanvas("canvas", "canvas", 1200, 800)

hSGN = df.Define("scale", "w*lumiIntegrated")\
	.Histo1D(("D^{0} kin mass", "D^{0} kinetic mass, reconstruction", 50, 1.6, 2.1),"goodMeson_mass", "scale")
hBKG = dg.Define("scale", "w*lumiIntegrated")\
	.Histo1D(("D^{0} kin mass", "D^{0} kinetic mass, reconstruction", 50, 1.6, 2.1),"goodMeson_mass", "scale")

hSGN.SetFillColor(ROOT.kGreen-6)
hSGN.SetLineColor(ROOT.kBlack)
hBKG.SetFillColor(ROOT.kRed-6)
hBKG.SetLineColor(ROOT.kBlack)

stack = ROOT.THStack("stack", "D^{0} kinetic mass, reconstruction")
stack.Add(hBKG.GetValue())
stack.Add(hSGN.GetValue())
stack.Draw("hist")
stack.GetXaxis().SetTitle("m_{2trk}^{D^{0}#rightarrow K#pi} [GeV]")
stack.GetYaxis().SetTitle("Events")

legend = ROOT.TLegend(0.72, 0.7, 0.8999, 0.89)
legend.SetMargin(0.32)
legend.SetBorderSize(0)
legend.AddEntry(hSGN.GetValue(), "Signal", "f")
legend.AddEntry(hBKG.GetValue(), "Background", "f")
legend.Draw()

canvas.SaveAs("~/public_html/plotsMAY24/D0StarBKG_kin_mass.png")

