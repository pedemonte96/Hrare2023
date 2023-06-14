import ROOT

ROOT.ROOT.EnableImplicitMT()

if "/home/submit/pdmonte/CMSSW_10_6_27/src/Hrare2023/analysis/func_marti.so" not in ROOT.gSystem.GetLibraries():
    ROOT.gSystem.CompileMacro("/home/submit/pdmonte/CMSSW_10_6_27/src/Hrare2023/analysis/func_marti.cc","k")

date = "MAY09"

chain = ROOT.TChain("events");
chain.Add("/data/submit/pdmonte/outputs/{0}/2018/outname_mc1039_GFcat_D0StarCat_2018.root".format(date))

df = ROOT.RDataFrame(chain)

canvas = ROOT.TCanvas("canvas", "canvas", 1200, 800)

hg = df.Define("PhotonD0StarGenPT", "getPTParticleMotherGrandMother(GenPart_pdgId, GenPart_genPartIdxMother, GenPart_pt, 22, 423, 25)")\
	.Histo1D(("hist", "#gamma from D^{0}* PT GEN", 80, 0, 20),"PhotonD0StarGenPT")

hp = df.Define("Pi0D0StarGenPT", "getPTParticleMotherGrandMother(GenPart_pdgId, GenPart_genPartIdxMother, GenPart_pt, 111, 423, 25)")\
	.Histo1D(("hist", "#pi^{0} from D^{0}* PT GEN", 80, 0, 20),"Pi0D0StarGenPT")


hg.SetFillColor(ROOT.kBlue+2)
hp.SetFillColor(ROOT.kBlue-9)
hg.SetLineColor(ROOT.kBlack)
hp.SetLineColor(ROOT.kBlack)

stack = ROOT.THStack("stack", "p_{T} of #gamma/#pi^{0} from D*^{0} #rightarrow D^{0}+#gamma/#pi^{0}, generation")
stack.Add(hg.GetValue())
stack.Add(hp.GetValue())
stack.Draw()
stack.GetXaxis().SetTitle("p_{T} [GeV]")
stack.GetYaxis().SetTitle("Events")

legend = ROOT.TLegend(0.8, 0.7, 0.8999, 0.89)
legend.SetMargin(0.6)
legend.SetBorderSize(0)
legend.AddEntry(hg.GetValue(), "#gamma", "f")
legend.AddEntry(hp.GetValue(), "#pi^{0}", "f")
legend.Draw()

canvas.SaveAs("~/public_html/plotsMAY24/D0StarGEN_pi0photon_pt.png")

