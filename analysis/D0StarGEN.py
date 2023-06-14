import ROOT

ROOT.ROOT.EnableImplicitMT()

if "/home/submit/pdmonte/CMSSW_10_6_27/src/Hrare2023/analysis/func_marti.so" not in ROOT.gSystem.GetLibraries():
	ROOT.gSystem.CompileMacro("/home/submit/pdmonte/CMSSW_10_6_27/src/Hrare2023/analysis/func_marti.cc","k")

date = "MAY09"

chain = ROOT.TChain("events")
chain.Add("/data/submit/pdmonte/outputs/{0}/2018/outname_mc1039_GFcat_D0StarCat_2018.root".format(date))

df = ROOT.RDataFrame(chain)

h0=df.Define("D0StarGenPT", "getPTParticleMother(GenPart_pdgId, GenPart_genPartIdxMother, GenPart_pt, 423, 25)").Histo1D(("hist", "D^{0}* PT GEN", 200, 0, 200),"D0StarGenPT")

h1=df.Define("D0GenPT", "getPTParticleMotherGrandMother(GenPart_pdgId, GenPart_genPartIdxMother, GenPart_pt, 421, 423, 25)").Define("D0GenPTgood","D0GenPT[D0GenPT>0]").Histo1D(("hist", "D^{0} PT GEN", 200, 0, 200),"D0GenPTgood")

h2=df.Define("HiggsPhotonGenPT", "getPTParticleMother(GenPart_pdgId, GenPart_genPartIdxMother, GenPart_pt, 22, 25)").Histo1D(("hist", "#gamma from Higgs PT GEN", 200, 0, 200),"HiggsPhotonGenPT")

h3g=df.Define("PhotonD0StarGenPT", "getPTParticleMotherGrandMother(GenPart_pdgId, GenPart_genPartIdxMother, GenPart_pt, 22, 423, 25)").Define("PhotonD0StarGenPTGood", "PhotonD0StarGenPT[PhotonD0StarGenPT>0]").Histo1D(("hist", "#gamma from D^{0}* PT GEN", 150, 0, 30),"PhotonD0StarGenPTGood")

h3p=df.Define("Pi0D0StarGenPT", "getPTParticleMotherGrandMother(GenPart_pdgId, GenPart_genPartIdxMother, GenPart_pt, 111, 423, 25)").Define("Pi0D0StarGenPTGood", "Pi0D0StarGenPT[Pi0D0StarGenPT>0]").Histo1D(("hist", "#pi^{0} from D^{0}* PT GEN", 150, 0, 30),"Pi0D0StarGenPTGood")

h4=df.Define("PiplusD0GenPT", "getPTParticleMotherGrandMother(GenPart_pdgId, GenPart_genPartIdxMother, GenPart_pt, 211, 421, 423)").Define("PiplusD0GenPTGood", "PiplusD0GenPT[PiplusD0GenPT>0]").Histo1D(("hist", "#pi^{+} from D^{0} PT GEN", 70, 0, 70),"PiplusD0GenPTGood")

h5=df.Define("KaonD0GenPT", "getPTParticleMotherGrandMother(GenPart_pdgId, GenPart_genPartIdxMother, GenPart_pt, -321, 421, 423)").Define("KaonD0GenPTGood", "KaonD0GenPT[KaonD0GenPT>0]").Histo1D(("hist", "K^{-} from D^{0} PT GEN", 70, 0, 70),"KaonD0GenPTGood")

h6pt=df.Define("TwoBodyPTGen", "getTwoBody4MomentumGrandMother(GenPart_pdgId, GenPart_genPartIdxMother, GenPart_phi, GenPart_eta, GenPart_pt, GenPart_mass, -321, 211, 421, 423, 1)").Histo1D(("hist", "Two Body D^{0} PT GEN", 200, 0, 200),"TwoBodyPTGen")
h6m=df.Define("TwoBodyMassGen", "getTwoBody4MomentumGrandMother(GenPart_pdgId, GenPart_genPartIdxMother, GenPart_phi, GenPart_eta, GenPart_pt, GenPart_mass, -321, 211, 421, 423, 0)").Histo1D(("hist", "Two Body D^{0} Mass GEN", 200, 0, 3.0),"TwoBodyMassGen")

h8=df.Define("KaonPionGenDR", "getDRParticleMother(GenPart_pdgId, GenPart_genPartIdxMother, GenPart_phi, GenPart_eta, 211, 421, -321, 421)").Histo1D(("hist", "Kaon-Pion DR Gen", 100, 0, 0.2),"KaonPionGenDR")

h8p=df.Define("Pi0D0GenDR", "getDRParticleMother(GenPart_pdgId, GenPart_genPartIdxMother, GenPart_phi, GenPart_eta, 111, 423, 421, 423)").Histo1D(("hist", "Pion0-D0 DR Gen", 100, 0, 0.2),"Pi0D0GenDR")
h8g=df.Define("PhotonD0GenDR", "getDRParticleMother(GenPart_pdgId, GenPart_genPartIdxMother, GenPart_phi, GenPart_eta, 22, 423, 421, 423)").Histo1D(("hist", "Photon-D0 DR Gen", 100, 0, 0.2),"PhotonD0GenDR")

#h9=df.Define("HCandMassGen", "getHCandMass(GenPart_pdgId, GenPart_genPartIdxMother, GenPart_phi, GenPart_eta, GenPart_pt, GenPart_mass, 421, 423, 22, 25)").Histo1D(("hist", "H Cand Mass Gen", 100, 0, 200),"HCandMassGen")



canvas = ROOT.TCanvas("canvas", "canvas", 1800, 3800)
canvas.Divide(2, 6)
canvas.cd(10)
h0.Draw("hist")
canvas.cd(1)
h1.Draw("hist")
canvas.cd(2)
h2.Draw("hist")
#canvas.cd(3)
#h4.Draw("hist")
#canvas.cd(5)
#h5.Draw("hist")
canvas.cd(3)
stack3 = ROOT.THStack("stack", "#gamma/#pi^{0} from D^{0}* #rightarrow D^{0}+#gamma/#pi^{0} PT GEN")
h3g.SetFillColor(ROOT.kGreen-9)
h3p.SetFillColor(ROOT.kRed-9)
stack3.Add(h3g.GetValue())
stack3.Add(h3p.GetValue())
stack3.Draw()
stack3.GetXaxis().SetRangeUser(0, 20)
legend3 = ROOT.TLegend(0.7, 0.7, 0.9, 0.9)
legend3.AddEntry(h3g.GetValue(), "Photon", "f")
legend3.AddEntry(h3p.GetValue(), "Pion", "f")
legend3.Draw()
canvas.cd(4)
h4.SetFillColor(ROOT.kBlue-2)
h4.Draw("hist")
canvas.cd(5)
h5.SetFillColor(ROOT.kBlue-9)
h5.Draw("hist")
canvas.cd(6)
stack = ROOT.THStack("stack", "Two tracks from D^{0} PT GEN")
stack.Add(h4.GetValue())
stack.Add(h5.GetValue())
stack.Draw()
#stack.GetXaxis().SetRangeUser(0, 20)
legend = ROOT.TLegend(0.7, 0.7, 0.9, 0.9)
legend.AddEntry(h4.GetValue(), "Pi+", "f")
legend.AddEntry(h5.GetValue(), "K-", "f")
legend.Draw()



canvas.cd(7)
h6pt.Draw("hist")
canvas.cd(8)
h6m.Draw("hist")
canvas.cd(9)
h8.Draw("hist")
canvas.cd(11)
h8g.Draw("hist")
canvas.cd(12)
h8p.Draw("hist")

canvas.SaveAs("~/public_html/D0StarGEN.png")

