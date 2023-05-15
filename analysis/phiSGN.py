import ROOT

ROOT.ROOT.EnableImplicitMT()

if "/work/submit/pdmonte/Hrare2023/analysis/func_marti.so" not in ROOT.gSystem.GetLibraries():
    ROOT.gSystem.CompileMacro("/work/submit/pdmonte/Hrare2023/analysis/func_marti.cc","k")

date = "MAY11"

chain = ROOT.TChain("events");
chain.Add("/work/submit/pdmonte/Hrare2023/analysis/{0}/2018/outname_mc1040_GFcat_OmegaCat_2018.root".format(date))

df = ROOT.RDataFrame(chain)



h1=df.Define("scale", "w*lumiIntegrated").Histo1D(("hist", "#phi PT", 200, 0, 200),"goodMeson_pt", "scale")

h2=df.Define("scale", "w*lumiIntegrated").Histo1D(("hist", "#gamma from Higgs PT", 200, 0, 200),"goodPhotons_pt", "scale")

#h3=df.Define("Pi0PhiGenPT", "getPTParticleMotherGrandMother(GenPart_pdgId, GenPart_genPartIdxMother, GenPart_pt, 111, 333, 25)").Define("Pi0PhiGenPTGood", "Pi0PhiGenPT[Pi0PhiGenPT>0]").Histo1D(("hist", "#pi^{0} from #phi PT GEN", 70, 0, 70),"Pi0PhiGenPTGood")



h4=df.Define("scale", "w*lumiIntegrated").Histo1D(("hist", "Track 1 from #phi PT", 70, 0, 70),"goodMeson_trk1_pt", "scale")

h5=df.Define("scale", "w*lumiIntegrated").Histo1D(("hist", "Track 2 from #phi PT", 70, 0, 70),"goodMeson_trk2_pt", "scale")

h4lead=df.Define("scale", "w*lumiIntegrated").Define("leading", "getMaximum(goodMeson_trk1_pt, goodMeson_trk2_pt)").Histo1D(("hist", "Leading track from #phi PT", 70, 0, 70),"leading", "scale")

h5sublead=df.Define("scale", "w*lumiIntegrated").Define("subleading", "getMinimum(goodMeson_trk1_pt, goodMeson_trk2_pt)").Histo1D(("hist", "Subleading track from #phi PT", 70, 0, 70),"subleading", "scale")

h6pt=df.Define("ThreeBodyPTGen", "getThreeBody4Momentum(GenPart_pdgId, GenPart_genPartIdxMother, GenPart_phi, GenPart_eta, GenPart_pt, GenPart_mass, 111, 211, -211, 333, 1)").Histo1D(("hist", "Three Body #phi PT GEN", 200, 0, 200),"ThreeBodyPTGen")
h6m=df.Define("ThreeBodyMassGen", "getThreeBody4Momentum(GenPart_pdgId, GenPart_genPartIdxMother, GenPart_phi, GenPart_eta, GenPart_pt, GenPart_mass, 111, 211, -211, 333, 0)").Histo1D(("hist", "Three Body #phi Mass GEN", 200, 0, 1.5),"ThreeBodyMassGen")

#h8=df.Define("PionGenDR", "getDRParticleMother(GenPart_pdgId, GenPart_genPartIdxMother, GenPart_phi, GenPart_eta, 111, 333, 333, 25)").Histo1D(("hist", "Pion0-Phi DR Gen", 200, 0, 0.5),"PionGenDR")

#h8=df.Define("KaonPionGenDR", "getDRParticleMother(GenPart_pdgId, GenPart_genPartIdxMother, GenPart_phi, GenPart_eta, 211, 421, -321, 421)").Histo1D(("hist", "Kaon-Pion DR Gen", 100, 0, 0.2),"KaonPionGenDR")

#h9=df.Define("HCandMassGen", "getHCandMass(GenPart_pdgId, GenPart_genPartIdxMother, GenPart_phi, GenPart_eta, GenPart_pt, GenPart_mass, 421, 423, 22, 25)").Histo1D(("hist", "H Cand Mass Gen", 100, 0, 200),"HCandMassGen")

canvas = ROOT.TCanvas("canvas", "canvas", 1800, 3800)
canvas.Divide(2, 6)


canvas.cd(1)
h1.Draw("hist")
canvas.cd(2)
h2.Draw("hist")




#canvas.cd(3)
#h3.SetFillColor(ROOT.kRed-9)
#h3.Draw("hist")









canvas.cd(4)
#h4.SetFillColor(ROOT.kBlue-2)
#h4.Draw("hist")
h4lead.SetFillColor(ROOT.kBlue-2)
h4lead.Draw("hist")
canvas.cd(5)
#h5.SetFillColor(ROOT.kBlue-9)
#h5.Draw("hist")
h5sublead.SetFillColor(ROOT.kBlue-9)
h5sublead.Draw("hist")
canvas.cd(6)
stack = ROOT.THStack("stack", "Pions from #phi PT GEN")
#stack.Add(h3.GetValue())
#stack.Add(h4.GetValue())
#stack.Add(h5.GetValue())
stack.Add(h4lead.GetValue())
stack.Add(h5sublead.GetValue())
stack.Draw("hist")
#stack.GetXaxis().SetRangeUser(0, 20)
legend = ROOT.TLegend(0.7, 0.7, 0.9, 0.9)
#legend.AddEntry(h3.GetValue(), "Pi0", "f")
#legend.AddEntry(h4.GetValue(), "Pi+", "f")
#legend.AddEntry(h5.GetValue(), "Pi-", "f")
legend.AddEntry(h4lead.GetValue(), "Leading", "f")
legend.AddEntry(h5sublead.GetValue(), "Subleading", "f")
legend.Draw()

#canvas.cd(7)
#h6pt.Draw("hist")
#canvas.cd(8)
#h6m.Draw("hist")

canvas.SaveAs("~/public_html/PhiSGN.png")

