import ROOT

ROOT.ROOT.EnableImplicitMT()

if "/work/submit/pdmonte/Hrare2023/analysis/func_marti.so" not in ROOT.gSystem.GetLibraries():
    ROOT.gSystem.CompileMacro("/work/submit/pdmonte/Hrare2023/analysis/func_marti.cc","k")

date = "MAY11"

chain = ROOT.TChain("events");
chain.Add("/work/submit/pdmonte/Hrare2023/analysis/{0}/2018/outname_mc1040_GFcat_OmegaCat_2018.root".format(date))

df = ROOT.RDataFrame(chain)

h = df.Define("PionGenDR", "getDRParticleMother(GenPart_pdgId, GenPart_genPartIdxMother, GenPart_phi, GenPart_eta, 111, 333, 333, 25)")\
	.Histo1D(("DR #phi-#pi^{0}", "DR of #phi-#pi^{0}, generation", 50, 0, 0.2),"PionGenDR")

h.GetXaxis().SetTitle("DR [rad]")
h.GetYaxis().SetTitle("Events")

canvas = ROOT.TCanvas("canvas", "canvas", 1200, 800)

h.SetFillColor(ROOT.kBlue-6)
h.SetLineColor(ROOT.kBlack)
h.Draw("hist")

canvas.SaveAs("~/public_html/plotsMAY24/PhiGEN_pi0_DR.png")

