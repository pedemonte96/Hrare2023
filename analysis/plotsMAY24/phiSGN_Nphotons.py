import ROOT

ROOT.ROOT.EnableImplicitMT()

if "/home/submit/pdmonte/Hrare2023/analysis/func_marti.so" not in ROOT.gSystem.GetLibraries():
    ROOT.gSystem.CompileMacro("/home/submit/pdmonte/Hrare2023/analysis/func_marti.cc","k")

date = "MAY23"

chain = ROOT.TChain("events");
chain.Add("/home/submit/pdmonte/Hrare2023/analysis/outputs/{0}/2018/outname_mc1040_GFcat_OmegaCat_2018.root".format(date))

df = ROOT.RDataFrame(chain)

h = df.Histo1D(("# #gamma", "Number of photons, reconstruction", 10, 0, 10),"goodMeson_Nphotons")

h.GetXaxis().SetTitle("Number of photons")
h.GetYaxis().SetTitle("Events")

canvas = ROOT.TCanvas("canvas", "canvas", 1200, 800)

h.SetFillColor(ROOT.kGreen-6)
h.SetLineColor(ROOT.kBlack)
h.Draw("hist")

canvas.SaveAs("~/public_html/plotsMAY24/PhiSGN_Nphotons.png")

