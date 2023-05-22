import ROOT

ROOT.ROOT.EnableImplicitMT()

if "/home/submit/pdmonte/Hrare2023/analysis/func_marti.so" not in ROOT.gSystem.GetLibraries():
    ROOT.gSystem.CompileMacro("/home/submit/pdmonte/Hrare2023/analysis/func_marti.cc","k")

date = "MAY22"

chainSGN = ROOT.TChain("events")
chainSGN.Add("/home/submit/pdmonte/Hrare2023/analysis/outputs/{0}/2018/outname_mc1039_GFcat_D0StarCat_2018.root".format(date))

chainBKG = ROOT.TChain("events")
chainBKG.Add("/home/submit/pdmonte/Hrare2023/analysis/outputs/{0}/2018/outname_mc10_GFcat_D0StarCat_2018.root".format(date))
chainBKG.Add("/home/submit/pdmonte/Hrare2023/analysis/outputs/{0}/2018/outname_mc11_GFcat_D0StarCat_2018.root".format(date))
chainBKG.Add("/home/submit/pdmonte/Hrare2023/analysis/outputs/{0}/2018/outname_mc12_GFcat_D0StarCat_2018.root".format(date))
chainBKG.Add("/home/submit/pdmonte/Hrare2023/analysis/outputs/{0}/2018/outname_mc13_GFcat_D0StarCat_2018.root".format(date))
chainBKG.Add("/home/submit/pdmonte/Hrare2023/analysis/outputs/{0}/2018/outname_mc14_GFcat_D0StarCat_2018.root".format(date))

df = ROOT.RDataFrame(chainSGN)
dg = ROOT.RDataFrame(chainBKG)

canvas = ROOT.TCanvas("canvas", "canvas", 1200, 800)

hSGN = df.Define("scale", "w*lumiIntegrated").Histo1D(("hist", "Higgs candidate invariant mass, reconstruction", 80, 0, 200),"HCandMass", "scale")
hBKG = dg.Define("scale", "w*lumiIntegrated").Histo1D(("hist", "Higgs candidate invariant mass, reconstruction", 80, 0, 200),"HCandMass", "scale")


hSGN.SetFillColor(ROOT.kGreen-6)
hSGN.SetLineColor(ROOT.kBlack)
hBKG.SetFillColor(ROOT.kRed-6)
hBKG.SetLineColor(ROOT.kBlack)

stack = ROOT.THStack("stack", "Higgs candidate invariant mass, reconstruction")
stack.Add(hBKG.GetValue())
stack.Add(hSGN.GetValue())
stack.Draw("hist")
stack.GetXaxis().SetTitle("m_{#gamma D*^{0}}^{H} [GeV]")
stack.GetYaxis().SetTitle("Events")

legend = ROOT.TLegend(0.7, 0.65, 0.8999, 0.89)
legend.SetMargin(0.27)
legend.SetBorderSize(0)
legend.AddEntry(hSGN.GetValue(), "Signal", "f")
legend.AddEntry(hBKG.GetValue(), "Background", "f")
legend.Draw()

canvas.SaveAs("~/public_html/plotsMAY24/D0StarBKG_Higgs_mass.png")
