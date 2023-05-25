import ROOT

ROOT.ROOT.EnableImplicitMT()

if "/home/submit/pdmonte/Hrare2023/analysis/func_marti.so" not in ROOT.gSystem.GetLibraries():
    ROOT.gSystem.CompileMacro("/home/submit/pdmonte/Hrare2023/analysis/func_marti.cc","k")

date = "MAY19"

chainSGN = ROOT.TChain("events")
chainSGN.Add("/home/submit/pdmonte/Hrare2023/analysis/outputs/{0}/2018/outname_mc1040_GFcat_OmegaCat_2018.root".format(date))

chainBKG = ROOT.TChain("events")
chainBKG.Add("/home/submit/pdmonte/Hrare2023/analysis/outputs/{0}/2018/outname_mc10_GFcat_OmegaCat_2018.root".format(date))
chainBKG.Add("/home/submit/pdmonte/Hrare2023/analysis/outputs/{0}/2018/outname_mc11_GFcat_OmegaCat_2018.root".format(date))
chainBKG.Add("/home/submit/pdmonte/Hrare2023/analysis/outputs/{0}/2018/outname_mc12_GFcat_OmegaCat_2018.root".format(date))
chainBKG.Add("/home/submit/pdmonte/Hrare2023/analysis/outputs/{0}/2018/outname_mc13_GFcat_OmegaCat_2018.root".format(date))
chainBKG.Add("/home/submit/pdmonte/Hrare2023/analysis/outputs/{0}/2018/outname_mc14_GFcat_OmegaCat_2018.root".format(date))

df = ROOT.RDataFrame(chainSGN)
dg = ROOT.RDataFrame(chainBKG)

canvas = ROOT.TCanvas("canvas", "canvas", 1200, 800)

bins=100

hSGN = df.Define("scale", "w*lumiIntegrated").Histo1D(("hist", "#phi three mass, reconstruction", bins, 0.4, 1.6),"goodMeson_threemass", "scale")
hBKG = dg.Define("scale", "w*lumiIntegrated").Histo1D(("hist", "#phi three mass, reconstruction", bins, 0.4, 1.6),"goodMeson_threemass", "scale")


hSGN.SetFillColor(ROOT.kGreen-6)
hSGN.SetLineColor(ROOT.kBlack)
hBKG.SetFillColor(ROOT.kRed-6)
hBKG.SetLineColor(ROOT.kBlack)

stack = ROOT.THStack("stack", "#phi three mass, reconstruction")
stack.Add(hBKG.GetValue())
stack.Add(hSGN.GetValue())
stack.Draw("hist")
stack.GetXaxis().SetTitle("m_{#phi}^{#phi#rightarrow #pi#pi#pi} [GeV]")
stack.GetYaxis().SetTitle("Events")
stack.SetMaximum(2250.)

width = 0.004249
center = 1.019461
n=20
l = ROOT.TLine(center, 0, center, 2250)
l.SetLineWidth(2)
l.SetLineColor(ROOT.kBlack)
l.Draw()
l1 = ROOT.TLine(center-n*width, 0, center-n*width, 2250)
l1.SetLineWidth(2)
l1.SetLineStyle(2)
l1.SetLineColor(ROOT.kBlack)
l1.Draw()
l2 = ROOT.TLine(center+n*width, 0, center+n*width, 2250)
l2.SetLineWidth(2)
l2.SetLineStyle(2)
l2.SetLineColor(ROOT.kBlack)
l2.Draw()

legend = ROOT.TLegend(0.7, 0.65, 0.8999, 0.89)
legend.SetMargin(0.25)
legend.SetBorderSize(0)
legend.AddEntry(hSGN.GetValue(), "Signal", "f")
legend.AddEntry(hBKG.GetValue(), "Background", "f")
legend.AddEntry(l, "m_{#phi} = 1020 GeV", "l")
legend.AddEntry(l1, "m_{#phi} #pm 20#Gamma_{#phi}", "l")
legend.Draw()

canvas.SaveAs("~/public_html/plotsMAY24/PhiBKG_three_mass.png")
