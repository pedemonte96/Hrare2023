import ROOT

ROOT.ROOT.EnableImplicitMT()

if "/home/submit/pdmonte/Hrare2023/analysis/func_marti.so" not in ROOT.gSystem.GetLibraries():
    ROOT.gSystem.CompileMacro("/home/submit/pdmonte/Hrare2023/analysis/func_marti.cc","k")

date = "MAY30"

chain = ROOT.TChain("events");
chain.Add("/home/submit/pdmonte/Hrare2023/analysis/outputs/{0}/2018/outname_mc1037_GFcat_OmegaCat_2018.root".format(date))

df = ROOT.RDataFrame(chain)



h1=df.Define("PhiGenPT", "getPTParticleMother(GenPart_pdgId, GenPart_genPartIdxMother, GenPart_pt, 223, 25)").Histo1D(("hist", "#omega PT GEN", 200, 0, 200),"PhiGenPT")

h2=df.Define("HiggsPhotonGenPT", "getPTParticleMother(GenPart_pdgId, GenPart_genPartIdxMother, GenPart_pt, 22, 25)").Histo1D(("hist", "#gamma from Higgs PT GEN", 200, 0, 200),"HiggsPhotonGenPT")

h3=df.Define("Pi0PhiGenPT", "getPTParticleMotherGrandMother(GenPart_pdgId, GenPart_genPartIdxMother, GenPart_pt, 111, 223, 25)").Define("Pi0PhiGenPTGood", "Pi0PhiGenPT[Pi0PhiGenPT>0]").Histo1D(("#pi^{0} p_{T}", "p_{T} of #pi^{0} from #omega, generation", 35, 0, 70),"Pi0PhiGenPTGood")
h3.GetXaxis().SetTitle("p_{T} [GeV]")
h3.GetYaxis().SetTitle("Events")



h4=df.Define("PiplusPhiGenPT", "getPTParticleMotherGrandMother(GenPart_pdgId, GenPart_genPartIdxMother, GenPart_pt, 211, 223, 25)").Define("PiplusPhiGenPTGood", "PiplusPhiGenPT[PiplusPhiGenPT>0]").Histo1D(("hist", "#pi^{+} from #omega PT GEN", 70, 0, 70),"PiplusPhiGenPTGood")

h5=df.Define("PiminusPhiGenPT", "getPTParticleMotherGrandMother(GenPart_pdgId, GenPart_genPartIdxMother, GenPart_pt, -211, 223, 25)").Define("PiminusPhiGenPTGood", "PiminusPhiGenPT[PiminusPhiGenPT>0]").Histo1D(("hist", "#pi^{-} from #omega PT GEN", 70, 0, 70),"PiminusPhiGenPTGood")

h4lead=df.Define("PiplusPhiGenPT", "getMaximum(getPTParticleMotherGrandMother(GenPart_pdgId, GenPart_genPartIdxMother, GenPart_pt, 211, 223, 25), getPTParticleMotherGrandMother(GenPart_pdgId, GenPart_genPartIdxMother, GenPart_pt, -211, 223, 25))").Define("PiplusPhiGenPTGood", "PiplusPhiGenPT[PiplusPhiGenPT>0]").Histo1D(("hist", "Leading track from #omega PT GEN", 70, 0, 70),"PiplusPhiGenPTGood")

h5sublead=df.Define("PiplusPhiGenPT", "getMinimum(getPTParticleMotherGrandMother(GenPart_pdgId, GenPart_genPartIdxMother, GenPart_pt, 211, 223, 25), getPTParticleMotherGrandMother(GenPart_pdgId, GenPart_genPartIdxMother, GenPart_pt, -211, 223, 25))").Define("PiplusPhiGenPTGood", "PiplusPhiGenPT[PiplusPhiGenPT>0]").Histo1D(("hist", "Subleading track from #omega PT GEN", 70, 0, 70),"PiplusPhiGenPTGood")

h6pt=df.Define("ThreeBodyPTGen", "getThreeBody4Momentum(GenPart_pdgId, GenPart_genPartIdxMother, GenPart_phi, GenPart_eta, GenPart_pt, GenPart_mass, 111, 211, -211, 223, 1)").Histo1D(("hist", "Three Body #omega PT GEN", 200, 0, 200),"ThreeBodyPTGen")
h6m=df.Define("ThreeBodyMassGen", "getThreeBody4Momentum(GenPart_pdgId, GenPart_genPartIdxMother, GenPart_phi, GenPart_eta, GenPart_pt, GenPart_mass, 111, 211, -211, 223, 0)").Histo1D(("hist", "Three Body #omega Mass GEN", 200, 0, 1.5),"ThreeBodyMassGen")

h8=df.Define("PionGenDR", "getDRParticleMother(GenPart_pdgId, GenPart_genPartIdxMother, GenPart_phi, GenPart_eta, 111, 223, 223, 25)").Histo1D(("DR #omega-#pi^{0}", "DR #omega-#pi^{0}, generation", 50, 0, 0.2),"PionGenDR")

h8.GetXaxis().SetTitle("DR [rad]")
h8.GetYaxis().SetTitle("Events")
#h8=df.Define("KaonPionGenDR", "getDRParticleMother(GenPart_pdgId, GenPart_genPartIdxMother, GenPart_phi, GenPart_eta, 211, 421, -321, 421)").Histo1D(("hist", "Kaon-Pion DR Gen", 100, 0, 0.2),"KaonPionGenDR")

#h9=df.Define("HCandMassGen", "getHCandMass(GenPart_pdgId, GenPart_genPartIdxMother, GenPart_phi, GenPart_eta, GenPart_pt, GenPart_mass, 421, 423, 22, 25)").Histo1D(("hist", "H Cand Mass Gen", 100, 0, 200),"HCandMassGen")

canvas = ROOT.TCanvas("canvas", "canvas", 1800, 3800)
canvas.Divide(2, 6)


canvas.cd(1)
h1.Draw("hist")
canvas.cd(2)
h2.Draw("hist")




canvas.cd(3)
h3.SetFillColor(ROOT.kBlue-6)
h3.SetLineColor(ROOT.kBlack)
h3.Draw("hist")









canvas.cd(4)
h4.SetFillColor(ROOT.kBlue-2)
h4.Draw("hist")
#h4lead.SetFillColor(ROOT.kBlue-2)
#h4lead.Draw("hist")
canvas.cd(5)
h5.SetFillColor(ROOT.kBlue-9)
h5.Draw("hist")
#h5sublead.SetFillColor(ROOT.kBlue-9)
#h5sublead.Draw("hist")
canvas.cd(6)
stack = ROOT.THStack("stack", "Pions from #omega PT GEN")
stack.Add(h3.GetValue())
#stack.Add(h4.GetValue())
#stack.Add(h5.GetValue())
stack.Add(h4lead.GetValue())
stack.Add(h5sublead.GetValue())
stack.Draw()
#stack.GetXaxis().SetRangeUser(0, 20)
legend = ROOT.TLegend(0.7, 0.7, 0.9, 0.9)
legend.AddEntry(h3.GetValue(), "Pi0", "f")
#legend.AddEntry(h4.GetValue(), "Pi+", "f")
#legend.AddEntry(h5.GetValue(), "Pi-", "f")
legend.AddEntry(h4lead.GetValue(), "Leading", "f")
legend.AddEntry(h5sublead.GetValue(), "Subleading", "f")
legend.Draw()

canvas.cd(7)
h6pt.Draw("hist")
canvas.cd(8)
h6m.Draw("hist")
canvas.cd(9)
h8.SetFillColor(ROOT.kBlue-6)
h8.SetLineColor(ROOT.kBlack)
h8.Draw("hist")

canvas.SaveAs("~/public_html/OmegaGEN.png")

