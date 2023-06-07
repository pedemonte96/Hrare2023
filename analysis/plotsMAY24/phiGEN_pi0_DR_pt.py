import ROOT
ROOT.ROOT.EnableImplicitMT()

if "/home/submit/pdmonte/CMSSW_10_6_27/src/Hrare2023/analysis/func_marti.so" not in ROOT.gSystem.GetLibraries():
    ROOT.gSystem.CompileMacro("/home/submit/pdmonte/CMSSW_10_6_27/src/Hrare2023/analysis/func_marti.cc","k")


date = "MAY11"

chain = ROOT.TChain("events")
chain.Add("/home/submit/pdmonte/CMSSW_10_6_27/src/Hrare2023/analysis/outputs/{0}/2018/outname_mc1040_GFcat_OmegaCat_2018.root".format(date))

df = ROOT.RDataFrame(chain)

canvas = ROOT.TCanvas("canvas", "canvas", 1200, 1000)
#canvas = ROOT.TCanvas()

h = df.Define("Pi0PhiGenPT", "getPTParticleMotherGrandMother(GenPart_pdgId, GenPart_genPartIdxMother, GenPart_pt, 111, 333, 25)")\
    .Define("PionGenDR", "getDRParticleMotherOneGrandMother(GenPart_pdgId, GenPart_genPartIdxMother, GenPart_phi, GenPart_eta, 111, 333, 25, 333, 25)")\
    .Histo2D(("#pi^{0} p_{T}", "DR vs p_{T} of #pi^{0} from #phi, generation", 70, 0, 70, 50, 0, 0.1),"Pi0PhiGenPT", "PionGenDR")

h.GetXaxis().SetTitle("p_{T} [GeV]")
h.GetYaxis().SetTitle("DR [rad]")
h.GetZaxis().SetTitle("Events")

h.SetContour(100)
h.Draw("colz")
h.SetStats(0)
canvas.SetRightMargin(0.13)

canvas.SaveAs("~/public_html/plotsMAY24/PhiGEN_pi0_DR_pt.png")
