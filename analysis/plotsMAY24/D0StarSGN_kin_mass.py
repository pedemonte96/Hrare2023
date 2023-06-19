import ROOT

ROOT.ROOT.EnableImplicitMT()

if "/home/submit/pdmonte/CMSSW_10_6_27/src/Hrare2023/analysis/func_marti.so" not in ROOT.gSystem.GetLibraries():
    ROOT.gSystem.CompileMacro("/home/submit/pdmonte/CMSSW_10_6_27/src/Hrare2023/analysis/func_marti.cc","k")

date = "MAY22"

chain = ROOT.TChain("events")
chain.Add("/data/submit/pdmonte/outputs/{0}/2018/outname_mc1039_GFcat_D0StarCat_2018.root".format(date))

df = ROOT.RDataFrame(chain)

h = df.Define("scale", "w*lumiIntegrated")\
	.Histo1D(("D^{0} kin mass", "D^{0} kinetic mass, reconstruction", 50, 1.6, 2.1),"goodMeson_mass", "scale")

h.GetXaxis().SetTitle("m_{2trk}^{D^{0}#rightarrow K#pi} [GeV]")
h.GetYaxis().SetTitle("Events")

canvas = ROOT.TCanvas("canvas", "canvas", 1200, 800)

h.SetFillColor(ROOT.kGreen-6)
h.SetLineColor(ROOT.kBlack)
h.Draw("hist")
h.Fit("gaus", "E", "", 1.865 - 2*0.03, 1.865 + 2*0.03)
h.GetFunction("gaus").Draw("same")

canvas.SaveAs("~/public_html/plotsMAY24/D0StarSGN_kin_mass.png")

