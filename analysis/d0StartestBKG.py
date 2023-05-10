import ROOT

ROOT.ROOT.EnableImplicitMT()

chainSGN = ROOT.TChain("events");
chainSGN.Add("/work/submit/pdmonte/Hrare2023/analysis/MAY10/2018/outname_mc1039_GFcat_D0StarCat_2018.root")

chainBKG = ROOT.TChain("events");
chainBKG.Add("/work/submit/pdmonte/Hrare2023/analysis/MAY10/2018/outname_mc10_GFcat_D0StarCat_2018.root")
chainBKG.Add("/work/submit/pdmonte/Hrare2023/analysis/MAY10/2018/outname_mc11_GFcat_D0StarCat_2018.root")
chainBKG.Add("/work/submit/pdmonte/Hrare2023/analysis/MAY10/2018/outname_mc12_GFcat_D0StarCat_2018.root")
chainBKG.Add("/work/submit/pdmonte/Hrare2023/analysis/MAY10/2018/outname_mc13_GFcat_D0StarCat_2018.root")
chainBKG.Add("/work/submit/pdmonte/Hrare2023/analysis/MAY10/2018/outname_mc14_GFcat_D0StarCat_2018.root")

df = ROOT.RDataFrame(chainSGN)
dg = ROOT.RDataFrame(chainBKG)

canvas = ROOT.TCanvas("canvas", "canvas", 2000, 3200)
canvas.Divide(2, 4)

#Kinematic Mass
h1SGN=df.Define("scale", "w*lumiIntegrated").Histo1D(("hist", "D0 kinematic mass", 100, 1, 3),"goodMeson_mass", "scale")
h1BKG=dg.Define("scale", "w*lumiIntegrated").Histo1D(("hist", "D0 kinematic mass", 100, 1, 3),"goodMeson_mass", "scale")
h1SGN.SetFillColor(ROOT.kGreen-9)
h1BKG.SetFillColor(ROOT.kRed-9)

p=canvas.cd(1)
stack1 = ROOT.THStack("stack", "D0 kinematic mass")
stack1.Add(h1BKG.GetValue())
stack1.Add(h1SGN.GetValue())
stack1.Draw("hist")
legend1 = ROOT.TLegend(0.7, 0.7, 0.9, 0.9)
legend1.AddEntry(h1SGN.GetValue(), "Signal", "f")
legend1.AddEntry(h1BKG.GetValue(), "Background", "f")
legend1.Draw()

#Photon from Higgs
h8SGN=df.Define("scale", "w*lumiIntegrated").Histo1D(("hist", "Photon from Higgs PT", 100, 0, 200),"goodPhotons_pt", "scale")
h8BKG=dg.Define("scale", "w*lumiIntegrated").Histo1D(("hist", "Photon from Higgs PT", 100, 0, 200),"goodPhotons_pt", "scale")
h8SGN.SetFillColor(ROOT.kGreen-9)
h8BKG.SetFillColor(ROOT.kRed-9)

p=canvas.cd(4)
stack8 = ROOT.THStack("stack", "Photon from Higgs PT")
stack8.Add(h8BKG.GetValue())
stack8.Add(h8SGN.GetValue())
stack8.Draw("hist")
legend8 = ROOT.TLegend(0.7, 0.7, 0.9, 0.9)
legend8.AddEntry(h8SGN.GetValue(), "Signal", "f")
legend8.AddEntry(h8BKG.GetValue(), "Background", "f")
legend8.Draw()

#Isolation
h2SGN=df.Define("scale", "w*lumiIntegrated").Histo1D(("hist", "D0 isolation", 100, 0, 1.5),"goodMeson_iso", "scale")
h2BKG=dg.Define("scale", "w*lumiIntegrated").Histo1D(("hist", "D0 isolation", 100, 0, 1.5),"goodMeson_iso", "scale")
h2SGN.SetFillColor(ROOT.kGreen-9)
h2BKG.SetFillColor(ROOT.kRed-9)

p=canvas.cd(2)
stack2 = ROOT.THStack("stack", "D0 isolation")
stack2.Add(h2BKG.GetValue())
stack2.Add(h2SGN.GetValue())
stack2.Draw("hist")
legend2 = ROOT.TLegend(0.7, 0.7, 0.9, 0.9)
legend2.AddEntry(h2SGN.GetValue(), "Signal", "f")
legend2.AddEntry(h2BKG.GetValue(), "Background", "f")
legend2.Draw()

#DR Kaon-Pion
h3SGN=df.Define("scale", "w*lumiIntegrated").Histo1D(("hist", "D0 DR Kaon-Pion", 100, 0, 0.2),"goodMeson_DR_D0", "scale")
h3BKG=dg.Define("scale", "w*lumiIntegrated").Histo1D(("hist", "D0 DR Kaon-Pion", 100, 0, 0.2),"goodMeson_DR_D0", "scale")
h3SGN.SetFillColor(ROOT.kGreen-9)
h3BKG.SetFillColor(ROOT.kRed-9)

p=canvas.cd(7)
stack3 = ROOT.THStack("stack", "D0 DR Kaon-Pion")
stack3.Add(h3BKG.GetValue())
stack3.Add(h3SGN.GetValue())
stack3.Draw("hist")
legend3 = ROOT.TLegend(0.7, 0.7, 0.9, 0.9)
legend3.AddEntry(h3SGN.GetValue(), "Signal", "f")
legend3.AddEntry(h3BKG.GetValue(), "Background", "f")
legend3.Draw()

#D0 PT
h4SGN=df.Define("scale", "w*lumiIntegrated").Histo1D(("hist", "D0 PT", 100, 0, 200),"goodMeson_pt", "scale")
h4BKG=dg.Define("scale", "w*lumiIntegrated").Histo1D(("hist", "D0 PT", 100, 0, 200),"goodMeson_pt", "scale")
h4SGN.SetFillColor(ROOT.kGreen-9)
h4BKG.SetFillColor(ROOT.kRed-9)

p=canvas.cd(3)
stack4 = ROOT.THStack("stack", "D0 PT")
stack4.Add(h4BKG.GetValue())
stack4.Add(h4SGN.GetValue())
stack4.Draw("hist")
legend4 = ROOT.TLegend(0.7, 0.7, 0.9, 0.9)
legend4.AddEntry(h4SGN.GetValue(), "Signal", "f")
legend4.AddEntry(h4BKG.GetValue(), "Background", "f")
legend4.Draw()

#Pion PT
h5SGN=df.Define("scale", "w*lumiIntegrated").Histo1D(("hist", "Pion PT", 100, 0, 200),"goodMeson_trk1_pt", "scale")
h5BKG=dg.Define("scale", "w*lumiIntegrated").Histo1D(("hist", "Pion PT", 100, 0, 200),"goodMeson_trk1_pt", "scale")
h5SGN.SetFillColor(ROOT.kGreen-9)
h5BKG.SetFillColor(ROOT.kRed-9)

p=canvas.cd(5)
stack5 = ROOT.THStack("stack", "Pion PT")
stack5.Add(h5BKG.GetValue())
stack5.Add(h5SGN.GetValue())
stack5.Draw("hist")
legend5 = ROOT.TLegend(0.7, 0.7, 0.9, 0.9)
legend5.AddEntry(h5SGN.GetValue(), "Signal", "f")
legend5.AddEntry(h5BKG.GetValue(), "Background", "f")
legend5.Draw()

#Kaon PT
h6SGN=df.Define("scale", "w*lumiIntegrated").Histo1D(("hist", "Kaon PT", 100, 0, 200),"goodMeson_trk2_pt", "scale")
h6BKG=dg.Define("scale", "w*lumiIntegrated").Histo1D(("hist", "Kaon PT", 100, 0, 200),"goodMeson_trk2_pt", "scale")
h6SGN.SetFillColor(ROOT.kGreen-9)
h6BKG.SetFillColor(ROOT.kRed-9)

p=canvas.cd(6)
stack6 = ROOT.THStack("stack", "Kaon PT")
stack6.Add(h6BKG.GetValue())
stack6.Add(h6SGN.GetValue())
stack6.Draw("hist")
legend6 = ROOT.TLegend(0.7, 0.7, 0.9, 0.9)
legend6.AddEntry(h6SGN.GetValue(), "Signal", "f")
legend6.AddEntry(h6BKG.GetValue(), "Background", "f")
legend6.Draw()

#H Cand Mass
h7SGN=df.Define("scale", "w*lumiIntegrated").Histo1D(("hist", "H Cand Mass", 100, 0, 200),"HCandMass", "scale")
h7BKG=dg.Define("scale", "w*lumiIntegrated").Histo1D(("hist", "H Cand Mass", 100, 0, 200),"HCandMass", "scale")
h7SGN.SetFillColor(ROOT.kGreen-9)
h7BKG.SetFillColor(ROOT.kRed-9)

p=canvas.cd(8)
stack7 = ROOT.THStack("stack", "H Cand Mass")
stack7.Add(h7BKG.GetValue())
stack7.Add(h7SGN.GetValue())
stack7.Draw("hist")
legend7 = ROOT.TLegend(0.7, 0.7, 0.9, 0.9)
legend7.AddEntry(h7SGN.GetValue(), "Signal", "f")
legend7.AddEntry(h7BKG.GetValue(), "Background", "f")
legend7.Draw()


'''
h3=df.Define("scale", "w*lumiIntegrated").Histo1D(("hist", "D0Star photons", 10, 0, 10),"goodMeson_Nphotons")
h4=df.Define("scale", "w*lumiIntegrated").Filter("goodMeson_threemass[0] > 0.1").Histo1D(("hist", "D0Star three mass", 100, 1, 3),"goodMeson_threemass")
h6=df.Define("scale", "w*lumiIntegrated").Histo1D(("hist", "D0Star DR D0-photon", 100, 0, 10),"goodMeson_DR_D0Star")
h7=df.Define("scale", "w*lumiIntegrated").Filter("goodMeson_three_pt[0] > 25").Histo1D(("hist", "D0Star three PT", 100, 0, 300),"goodMeson_three_pt")
h9=df.Define("scale", "w*lumiIntegrated").Histo1D(("hist", "D0Star Photon PT", 100, 0, 100),"goodMeson_D0Star_photon_pt")
'''

canvas.SaveAs("~/public_html/D0StarBKG.png")

