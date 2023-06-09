import ROOT

ROOT.ROOT.EnableImplicitMT()

if "/home/submit/pdmonte/CMSSW_10_6_27/src/Hrare2023/analysis/func_marti.so" not in ROOT.gSystem.GetLibraries():
    ROOT.gSystem.CompileMacro("/home/submit/pdmonte/CMSSW_10_6_27/src/Hrare2023/analysis/func_marti.cc","k")

date = "MAY11"

chain = ROOT.TChain("events")
chain.Add("/data/submit/pdmonte/outputs/{0}/2018/outname_mc1040_GFcat_OmegaCat_2018.root".format(date))

df = ROOT.RDataFrame(chain)

h = df.Define("PionGenDR", "getDR(GenPart_eta, GenPart_phi, GenPart_pdgId, GenPart_genPartIdxMother, 111, 333, 25, 333, 25)")\
	.Histo1D(("DR #phi-#pi^{0}", "DR of #phi-#pi^{0}, generation", 50, 0, 0.1),"PionGenDR")

h.GetXaxis().SetTitle("DR [rad]")
h.GetYaxis().SetTitle("Events")

canvas = ROOT.TCanvas("canvas", "canvas", 1200, 800)

#p=canvas.cd(1)
#p.SetLogy()
h.SetFillColor(ROOT.kBlue-6)
h.SetLineColor(ROOT.kBlack)
h.Draw("hist")

canvas.SaveAs("~/public_html/plotsMAY24/PhiGEN_pi0_DR.png")

