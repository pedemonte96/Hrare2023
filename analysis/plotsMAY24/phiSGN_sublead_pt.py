import ROOT

ROOT.ROOT.EnableImplicitMT()

if "/home/submit/pdmonte/CMSSW_10_6_27/src/Hrare2023/analysis/func_marti.so" not in ROOT.gSystem.GetLibraries():
    ROOT.gSystem.CompileMacro("/home/submit/pdmonte/CMSSW_10_6_27/src/Hrare2023/analysis/func_marti.cc","k")

date = "MAY19"

chain = ROOT.TChain("events");
chain.Add("/data/submit/pdmonte/outputs/{0}/2018/outname_mc1040_GFcat_OmegaCat_2018.root".format(date))

df = ROOT.RDataFrame(chain)

canvas = ROOT.TCanvas("canvas", "canvas", 1200, 800)

h=df.Define("scale", "w*lumiIntegrated").Define("sub", "getMinimum(goodMeson_trk1_pt, goodMeson_trk2_pt)").Histo1D(("hist", "Subleading track from #phi PT, reconstruction", 70, 0, 70),"sub", "scale")


h.GetXaxis().SetTitle("p_{T}^{subleadtrk} [GeV]")
h.GetYaxis().SetTitle("Events")

h.SetFillColor(ROOT.kGreen-6)
h.SetLineColor(ROOT.kBlack)
h.Draw("hist")

canvas.SaveAs("~/public_html/plotsMAY24/PhiSGN_sublead_pt.png")

