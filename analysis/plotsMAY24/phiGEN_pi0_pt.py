import ROOT

ROOT.ROOT.EnableImplicitMT()

if "/home/submit/pdmonte/Hrare2023/analysis/func_marti.so" not in ROOT.gSystem.GetLibraries():
    ROOT.gSystem.CompileMacro("/home/submit/pdmonte/Hrare2023/analysis/func_marti.cc","k")

date = "MAY11"

chain = ROOT.TChain("events");
chain.Add("/home/submit/pdmonte/Hrare2023/analysis/outputs/{0}/2018/outname_mc1040_GFcat_OmegaCat_2018.root".format(date))

df = ROOT.RDataFrame(chain)

h = df.Define("Pi0PhiGenPT", "getPTParticleMotherGrandMother(GenPart_pdgId, GenPart_genPartIdxMother, GenPart_pt, 111, 333, 25)")\
	.Define("Pi0PhiGenPTGood", "Pi0PhiGenPT[Pi0PhiGenPT>0]")\
	.Histo1D(("#pi^{0} p_{T}", "p_{T} of #pi^{0} from #phi, generation", 35, 0, 70),"Pi0PhiGenPTGood")

h.GetXaxis().SetTitle("p_{T} [GeV]")
h.GetYaxis().SetTitle("Events")

canvas = ROOT.TCanvas("canvas", "canvas", 1200, 800)

h.SetFillColor(ROOT.kBlue-6)
h.SetLineColor(ROOT.kBlack)
h.Draw("hist")

canvas.SaveAs("~/public_html/plotsMAY24/PhiGEN_pi0_pt.png")

