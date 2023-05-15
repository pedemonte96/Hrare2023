import ROOT

ROOT.ROOT.EnableImplicitMT()

if "/work/submit/pdmonte/Hrare2023/analysis/func_marti.so" not in ROOT.gSystem.GetLibraries():
	ROOT.gSystem.CompileMacro("/work/submit/pdmonte/Hrare2023/analysis/func_marti.cc","k")

date = "MAY11"

chain = ROOT.TChain("events");
chain.Add("/work/submit/pdmonte/Hrare2023/analysis/{0}/2018/outname_mc1037_GFcat_OmegaCat_2018.root".format(date))

df = ROOT.RDataFrame(chain)

h1=df.Define("OmegaGenPT", "getPTParticleMother(GenPart_pdgId, GenPart_genPartIdxMother, GenPart_pt, 223, 25)").Histo1D(("hist", "Omega Gen PT", 100, 0, 300),"OmegaGenPT")

h3=df.Define("HiggsPhotonGenPT", "getPTParticleMother(GenPart_pdgId, GenPart_genPartIdxMother, GenPart_pt, 22, 25)").Histo1D(("hist", "Photon from Higgs Gen PT", 100, 0, 300),"HiggsPhotonGenPT")

h5=df.Define("Pi0OmegaGenPT", "getPTParticleMother(GenPart_pdgId, GenPart_genPartIdxMother, GenPart_pt, 111, 223)").Define("Pi0OmegaGenPTGood", "Pi0OmegaGenPT[Pi0OmegaGenPT>0]").Histo1D(("hist", "Pi0 from Omega Gen PT", 100, 0, 70),"Pi0OmegaGenPTGood")

h6=df.Define("PiplusOmegaGenPT", "getPTParticleMother(GenPart_pdgId, GenPart_genPartIdxMother, GenPart_pt, 211, 223)").Define("PiplusOmegaGenPTGood", "PiplusOmegaGenPT[PiplusOmegaGenPT>0]").Histo1D(("hist", "Pi+ from Omega Gen PT", 100, 0, 70),"PiplusOmegaGenPTGood")

h7=df.Define("PiminusOmegaGenPT", "getPTParticleMother(GenPart_pdgId, GenPart_genPartIdxMother, GenPart_pt, -211, 223)").Define("PiminusOmegaGenPTGood", "PiminusOmegaGenPT[PiminusOmegaGenPT>0]").Histo1D(("hist", "Pi- from Omega Gen PT", 100, 0, 70),"PiminusOmegaGenPTGood")

h7bis=df.Define("ThreeBodyPTGen", "getThreeBody4Momentum(GenPart_pdgId, GenPart_genPartIdxMother, GenPart_phi, GenPart_eta, GenPart_pt, GenPart_mass, 111, 211, -211, 223, 1)").Histo1D(("hist", "Three Body PT Gen", 200, 0, 300),"ThreeBodyPTGen")
h7bis1=df.Define("ThreeBodyMassGen", "getThreeBody4Momentum(GenPart_pdgId, GenPart_genPartIdxMother, GenPart_phi, GenPart_eta, GenPart_pt, GenPart_mass, 111, 211, -211, 223, 0)").Histo1D(("hist", "Three Body Mass Gen", 200, 0, 1.5),"ThreeBodyMassGen")

h8=df.Define("PionGenDR", "getDRParticleMother(GenPart_pdgId, GenPart_genPartIdxMother, GenPart_phi, GenPart_eta, 111, 223, 223, 25)").Histo1D(("hist", "Pion0-Omega DR Gen", 200, 0, 0.5),"PionGenDR")

#h8=df.Define("KaonPionGenDR", "getDRParticleMother(GenPart_pdgId, GenPart_genPartIdxMother, GenPart_phi, GenPart_eta, 211, 421, -321, 421)").Histo1D(("hist", "Kaon-Pion DR Gen", 100, 0, 0.2),"KaonPionGenDR")

#h9=df.Define("HCandMassGen", "getHCandMass(GenPart_pdgId, GenPart_genPartIdxMother, GenPart_phi, GenPart_eta, GenPart_pt, GenPart_mass, 421, 423, 22, 25)").Histo1D(("hist", "H Cand Mass Gen", 100, 0, 200),"HCandMassGen")

canvas = ROOT.TCanvas("canvas", "canvas", 1800, 3800)
canvas.Divide(2, 6)
canvas.cd(1)
h1.Draw("hist")
canvas.cd(2)
h3.Draw("hist")
p = canvas.cd(3)
#p.SetLogy()
h5.Draw("hist")
canvas.cd(4)
h6.Draw("hist")
canvas.cd(5)
h7.Draw("hist")
canvas.cd(6)
stack = ROOT.THStack("stack", "PT Gen Pions from Omega")
h5.SetFillColor(ROOT.kGreen-9)
h6.SetFillColor(ROOT.kRed-9)
h7.SetFillColor(ROOT.kBlue-9)
stack.Add(h5.GetValue())
stack.Add(h6.GetValue())
stack.Add(h7.GetValue())
stack.Draw()
#stack.GetXaxis().SetRangeUser(0, 20)
legend = ROOT.TLegend(0.7, 0.7, 0.9, 0.9)
legend.AddEntry(h5.GetValue(), "Pi0", "f")
legend.AddEntry(h6.GetValue(), "Pi+", "f")
legend.AddEntry(h7.GetValue(), "Pi-", "f")
legend.Draw()

canvas.cd(7)
h7bis.Draw("hist")
canvas.cd(8)
h7bis1.Draw("hist")
canvas.cd(9)
h8.Draw("hist")

canvas.SaveAs("~/public_html/OmegaGEN.png")

