import ROOT

ROOT.ROOT.EnableImplicitMT()

if "/home/submit/pdmonte/Hrare2023/analysis/func_marti.so" not in ROOT.gSystem.GetLibraries():
    ROOT.gSystem.CompileMacro("/home/submit/pdmonte/Hrare2023/analysis/func_marti.cc","k")

date = "MAY19"

chain = ROOT.TChain("events");
chain.Add("/home/submit/pdmonte/Hrare2023/analysis/outputs/{0}/2018/outname_mc1040_GFcat_OmegaCat_2018.root".format(date))

df = ROOT.RDataFrame(chain)

canvas = ROOT.TCanvas("canvas", "canvas", 1200, 800)

h=df.Define("scale", "w*lumiIntegrated").Histo1D(("hist", "#phi kinetic mass, reconstruction", 80, 0, 2),"goodMeson_charged_mass", "scale")

h.GetXaxis().SetTitle("m_{2trk}^{#phi#rightarrow #pi#pi} [GeV]")
h.GetYaxis().SetTitle("Events")

h.SetFillColor(ROOT.kGreen-6)
h.SetLineColor(ROOT.kBlack)
h.Draw("hist")
h.Fit("gaus", "E", "", 0.4, 0.8)
h.GetFunction("gaus").Draw("same")

canvas.SaveAs("~/public_html/plotsMAY24/PhiSGN_kin_mass.png")

