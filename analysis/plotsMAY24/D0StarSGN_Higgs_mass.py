import ROOT

ROOT.ROOT.EnableImplicitMT()

if "/home/submit/pdmonte/CMSSW_10_6_27/src/Hrare2023/analysis/func_marti.so" not in ROOT.gSystem.GetLibraries():
    ROOT.gSystem.CompileMacro("/home/submit/pdmonte/CMSSW_10_6_27/src/Hrare2023/analysis/func_marti.cc","k")

date = "MAY22"

chainSGN = ROOT.TChain("events")
chainSGN.Add("/data/submit/pdmonte/outputs/{0}/2018/outname_mc1039_GFcat_D0StarCat_2018.root".format(date))

df = ROOT.RDataFrame(chainSGN)

canvas = ROOT.TCanvas("canvas", "canvas", 1200, 800)

h=df.Define("scale", "w*lumiIntegrated").Histo1D(("m_{H}", "Higgs candidate invariant mass, reconstruction", 80, 0, 200),"HCandMass", "scale")


h.GetXaxis().SetTitle("m_{#gamma D*^{0}}^{H} [GeV]")
h.GetYaxis().SetTitle("Events")

#ROOT.gStyle.SetTitleH(0.10)
#ROOT.gStyle.SetTitleW(0.70)

h.SetFillColor(ROOT.kGreen-6)
h.SetLineColor(ROOT.kBlack)
h.Draw("hist")

canvas.SaveAs("~/public_html/plotsMAY24/D0StarSGN_Higgs_mass.png")
