import ROOT

ROOT.ROOT.EnableImplicitMT()

if "/home/submit/pdmonte/CMSSW_10_6_27/src/Hrare2023/analysis/func_marti.so" not in ROOT.gSystem.GetLibraries():
    ROOT.gSystem.CompileMacro("/home/submit/pdmonte/CMSSW_10_6_27/src/Hrare2023/analysis/func_marti.cc","k")

#date = "MAY30"
date = "JUN13"

chainSGN = ROOT.TChain("events");
chainSGN.Add("/home/submit/pdmonte/CMSSW_10_6_27/src/Hrare2023/analysis/outputs/{0}/2018/outname_mc1041_GFcat_D0StarCat_2018.root".format(date))

date = "MAY22"

chainBKG = ROOT.TChain("events");
chainBKG.Add("/home/submit/pdmonte/CMSSW_10_6_27/src/Hrare2023/analysis/outputs/{0}/2018/outname_mc10_GFcat_D0StarCat_2018.root".format(date))
chainBKG.Add("/home/submit/pdmonte/CMSSW_10_6_27/src/Hrare2023/analysis/outputs/{0}/2018/outname_mc11_GFcat_D0StarCat_2018.root".format(date))
chainBKG.Add("/home/submit/pdmonte/CMSSW_10_6_27/src/Hrare2023/analysis/outputs/{0}/2018/outname_mc12_GFcat_D0StarCat_2018.root".format(date))
chainBKG.Add("/home/submit/pdmonte/CMSSW_10_6_27/src/Hrare2023/analysis/outputs/{0}/2018/outname_mc13_GFcat_D0StarCat_2018.root".format(date))
chainBKG.Add("/home/submit/pdmonte/CMSSW_10_6_27/src/Hrare2023/analysis/outputs/{0}/2018/outname_mc14_GFcat_D0StarCat_2018.root".format(date))

df = ROOT.RDataFrame(chainSGN)
dg = ROOT.RDataFrame(chainBKG)

canvas = ROOT.TCanvas("canvas", "canvas", 3000, 5100)
canvas.Divide(3, 12)
ROOT.gStyle.SetOptFit(1)

#Kinematic Mass
h1SGN=df.Define("scale", "w*lumiIntegrated").Histo1D(("hist", "D0 kinematic mass", 50, 1.6, 2.1),"goodMeson_mass", "scale")
h1BKG=dg.Define("scale", "w*lumiIntegrated").Histo1D(("hist", "D0 kinematic mass", 50, 1.6, 2.1),"goodMeson_mass", "scale")
h1SGN.SetFillColor(ROOT.kGreen-9)
h1BKG.SetFillColor(ROOT.kRed-9)

p=canvas.cd(1)
h1SGN.Draw("hist")
h1SGN.Fit("gaus", "E", "", 1.805, 1.925)
h1SGN.Draw("func same")

p=canvas.cd(2)
h1BKG.Draw("hist")
p=canvas.cd(3)
stack1 = ROOT.THStack("stack", "D0 kinematic mass")
stack1.Add(h1BKG.GetValue())
stack1.Add(h1SGN.GetValue())
stack1.Draw("hist")
legend1 = ROOT.TLegend(0.7, 0.7, 0.9, 0.9)
legend1.AddEntry(h1SGN.GetValue(), "Signal", "f")
legend1.AddEntry(h1BKG.GetValue(), "Background", "f")
legend1.Draw()

#Isolation
h2SGN=df.Define("scale", "w*lumiIntegrated").Histo1D(("hist", "D0 isolation", 100, 0.8, 1.2),"goodMeson_iso", "scale")
h2BKG=dg.Define("scale", "w*lumiIntegrated").Histo1D(("hist", "D0 isolation", 100, 0.8, 1.2),"goodMeson_iso", "scale")
h2SGN.SetFillColor(ROOT.kGreen-9)
h2BKG.SetFillColor(ROOT.kRed-9)

p=canvas.cd(4)
h2SGN.Draw("hist")
p=canvas.cd(5)
h2BKG.Draw("hist")
p=canvas.cd(6)
stack2 = ROOT.THStack("stack", "D0 isolation")
stack2.Add(h2BKG.GetValue())
stack2.Add(h2SGN.GetValue())
stack2.Draw("hist")
legend2 = ROOT.TLegend(0.7, 0.7, 0.9, 0.9)
legend2.AddEntry(h2SGN.GetValue(), "Signal", "f")
legend2.AddEntry(h2BKG.GetValue(), "Background", "f")
legend2.Draw()

#D0 PT
h4SGN=df.Define("scale", "w*lumiIntegrated").Histo1D(("hist", "D0 PT", 100, 0, 200),"goodMeson_pt", "scale")
h4BKG=dg.Define("scale", "w*lumiIntegrated").Histo1D(("hist", "D0 PT", 100, 0, 200),"goodMeson_pt", "scale")
h4SGN.SetFillColor(ROOT.kGreen-9)
h4BKG.SetFillColor(ROOT.kRed-9)

p=canvas.cd(7)
h4SGN.Draw("hist")
p=canvas.cd(8)
h4BKG.Draw("hist")
p=canvas.cd(9)
stack4 = ROOT.THStack("stack", "D0 PT")
stack4.Add(h4BKG.GetValue())
stack4.Add(h4SGN.GetValue())
stack4.Draw("hist")
legend4 = ROOT.TLegend(0.7, 0.7, 0.9, 0.9)
legend4.AddEntry(h4SGN.GetValue(), "Signal", "f")
legend4.AddEntry(h4BKG.GetValue(), "Background", "f")
legend4.Draw()

#Photon from Higgs
h8SGN=df.Define("scale", "w*lumiIntegrated").Histo1D(("hist", "Photon from Higgs PT", 100, 0, 200),"goodPhotons_pt", "scale")
h8BKG=dg.Define("scale", "w*lumiIntegrated").Histo1D(("hist", "Photon from Higgs PT", 100, 0, 200),"goodPhotons_pt", "scale")
h8SGN.SetFillColor(ROOT.kGreen-9)
h8BKG.SetFillColor(ROOT.kRed-9)

p=canvas.cd(10)
h8SGN.Draw("hist")
p=canvas.cd(11)
h8BKG.Draw("hist")
p=canvas.cd(12)
stack8 = ROOT.THStack("stack", "Photon from Higgs PT")
stack8.Add(h8BKG.GetValue())
stack8.Add(h8SGN.GetValue())
stack8.Draw("hist")
legend8 = ROOT.TLegend(0.7, 0.7, 0.9, 0.9)
legend8.AddEntry(h8SGN.GetValue(), "Signal", "f")
legend8.AddEntry(h8BKG.GetValue(), "Background", "f")
legend8.Draw()

#Pion PT
h5SGN=df.Define("scale", "w*lumiIntegrated").Histo1D(("hist", "Pion PT", 100, 0, 100),"goodMeson_trk1_pt", "scale")
h5BKG=dg.Define("scale", "w*lumiIntegrated").Histo1D(("hist", "Pion PT", 100, 0, 100),"goodMeson_trk1_pt", "scale")
h5SGN.SetFillColor(ROOT.kGreen-9)
h5BKG.SetFillColor(ROOT.kRed-9)

p=canvas.cd(13)
h5SGN.Draw("hist")
p=canvas.cd(14)
h5BKG.Draw("hist")
p=canvas.cd(15)
stack5 = ROOT.THStack("stack", "Pion PT")
stack5.Add(h5BKG.GetValue())
stack5.Add(h5SGN.GetValue())
stack5.Draw("hist")
legend5 = ROOT.TLegend(0.7, 0.7, 0.9, 0.9)
legend5.AddEntry(h5SGN.GetValue(), "Signal", "f")
legend5.AddEntry(h5BKG.GetValue(), "Background", "f")
legend5.Draw()

#Kaon PT
h6SGN=df.Define("scale", "w*lumiIntegrated").Histo1D(("hist", "Kaon PT", 100, 0, 100),"goodMeson_trk2_pt", "scale")
h6BKG=dg.Define("scale", "w*lumiIntegrated").Histo1D(("hist", "Kaon PT", 100, 0, 100),"goodMeson_trk2_pt", "scale")
h6SGN.SetFillColor(ROOT.kGreen-9)
h6BKG.SetFillColor(ROOT.kRed-9)

p=canvas.cd(16)
h6SGN.Draw("hist")
p=canvas.cd(17)
h6BKG.Draw("hist")
p=canvas.cd(18)
stack6 = ROOT.THStack("stack", "Kaon PT")
stack6.Add(h6BKG.GetValue())
stack6.Add(h6SGN.GetValue())
stack6.Draw("hist")
legend6 = ROOT.TLegend(0.7, 0.7, 0.9, 0.9)
legend6.AddEntry(h6SGN.GetValue(), "Signal", "f")
legend6.AddEntry(h6BKG.GetValue(), "Background", "f")
legend6.Draw()

#DR Kaon-Pion
h3SGN=df.Define("scale", "w*lumiIntegrated").Histo1D(("hist", "D0 DR Kaon-Pion", 100, 0, 0.2),"goodMeson_DR", "scale")
h3BKG=dg.Define("scale", "w*lumiIntegrated").Histo1D(("hist", "D0 DR Kaon-Pion", 100, 0, 0.2),"goodMeson_DR", "scale")
h3SGN.SetFillColor(ROOT.kGreen-9)
h3BKG.SetFillColor(ROOT.kRed-9)

p=canvas.cd(19)
h3SGN.Draw("hist")
p=canvas.cd(20)
h3BKG.Draw("hist")
p=canvas.cd(21)
stack3 = ROOT.THStack("stack", "D0 DR Kaon-Pion")
stack3.Add(h3BKG.GetValue())
stack3.Add(h3SGN.GetValue())
stack3.Draw("hist")
legend3 = ROOT.TLegend(0.7, 0.7, 0.9, 0.9)
legend3.AddEntry(h3SGN.GetValue(), "Signal", "f")
legend3.AddEntry(h3BKG.GetValue(), "Background", "f")
legend3.Draw()

#H Cand Mass
h7SGN=df.Define("scale", "w*lumiIntegrated").Histo1D(("hist", "H Cand Mass", 100, 0, 200),"HCandMass", "scale")
h7BKG=dg.Define("scale", "w*lumiIntegrated").Histo1D(("hist", "H Cand Mass", 100, 0, 200),"HCandMass", "scale")
h7SGN.SetFillColor(ROOT.kGreen-9)
h7BKG.SetFillColor(ROOT.kRed-9)

p=canvas.cd(22)
h7SGN.Draw("hist")
p=canvas.cd(23)
h7BKG.Draw("hist")
p=canvas.cd(24)
stack7 = ROOT.THStack("stack", "H Cand Mass")
stack7.Add(h7BKG.GetValue())
stack7.Add(h7SGN.GetValue())
stack7.Draw("hist")
legend7 = ROOT.TLegend(0.7, 0.7, 0.9, 0.9)
legend7.AddEntry(h7SGN.GetValue(), "Signal", "f")
legend7.AddEntry(h7BKG.GetValue(), "Background", "f")
legend7.Draw()

#Track1 PT
h9SGN=df.Define("scale", "w*lumiIntegrated").Define("leading", "getMaximum(goodMeson_trk1_pt, goodMeson_trk2_pt)").Histo1D(("hist", "Leading track from D0 PT", 100, 0, 100),"leading", "scale")
h9BKG=dg.Define("scale", "w*lumiIntegrated").Define("leading", "getMaximum(goodMeson_trk1_pt, goodMeson_trk2_pt)").Histo1D(("hist", "Leading track from D0 PT", 100, 0, 100),"leading", "scale")
h9SGN.SetFillColor(ROOT.kGreen-9)
h9BKG.SetFillColor(ROOT.kRed-9)

p=canvas.cd(25)
h9SGN.Draw("hist")
p=canvas.cd(26)
h9BKG.Draw("hist")
p=canvas.cd(27)
stack9 = ROOT.THStack("stack", "Leading track from D0 PT")
stack9.Add(h9BKG.GetValue())
stack9.Add(h9SGN.GetValue())
stack9.Draw("hist")
legend9 = ROOT.TLegend(0.7, 0.7, 0.9, 0.9)
legend9.AddEntry(h9SGN.GetValue(), "Signal", "f")
legend9.AddEntry(h9BKG.GetValue(), "Background", "f")
legend9.Draw()

#Track2 PT
h10SGN=df.Define("scale", "w*lumiIntegrated").Define("sub", "getMinimum(goodMeson_trk1_pt, goodMeson_trk2_pt)").Histo1D(("hist", "Subleading track from D0 PT", 100, 0, 100),"sub", "scale")
h10BKG=dg.Define("scale", "w*lumiIntegrated").Define("sub", "getMinimum(goodMeson_trk1_pt, goodMeson_trk2_pt)").Histo1D(("hist", "Subleading track from D0 PT", 100, 0, 100),"sub", "scale")
h10SGN.SetFillColor(ROOT.kGreen-9)
h10BKG.SetFillColor(ROOT.kRed-9)

p=canvas.cd(28)
h10SGN.Draw("hist")
p=canvas.cd(29)
h10BKG.Draw("hist")
p=canvas.cd(30)
stack10 = ROOT.THStack("stack", "Subleading track from D0 PT")
stack10.Add(h10BKG.GetValue())
stack10.Add(h10SGN.GetValue())
stack10.Draw("hist")
legend10 = ROOT.TLegend(0.7, 0.7, 0.9, 0.9)
legend10.AddEntry(h10SGN.GetValue(), "Signal", "f")
legend10.AddEntry(h10BKG.GetValue(), "Background", "f")
legend10.Draw()

#3mass
h11SGN=df.Define("scale", "w*lumiIntegrated").Histo1D(("hist", "D0* three mass", 100, 1.6, 2.6),"goodMeson_threemass", "scale")
h11BKG=dg.Define("scale", "w*lumiIntegrated").Histo1D(("hist", "D0* three mass", 100, 1.6, 2.6),"goodMeson_threemass", "scale")
h11SGN.SetFillColor(ROOT.kGreen-9)
h11BKG.SetFillColor(ROOT.kRed-9)

p=canvas.cd(31)
h11SGN.Draw("hist")
p=canvas.cd(32)
h11BKG.Draw("hist")
p=canvas.cd(33)
stack11 = ROOT.THStack("stack", "D0* three mass")
stack11.Add(h11BKG.GetValue())
stack11.Add(h11SGN.GetValue())
stack11.Draw("hist")
legend11 = ROOT.TLegend(0.7, 0.7, 0.9, 0.9)
legend11.AddEntry(h11SGN.GetValue(), "Signal", "f")
legend11.AddEntry(h11BKG.GetValue(), "Background", "f")
legend11.Draw()

#3pt
h12SGN=df.Define("scale", "w*lumiIntegrated").Define("good", "goodMeson_three_pt[goodMeson_Nphotons>0]").Histo1D(("hist", "D0* three PT", 100, 0, 200),"good", "scale")
h12BKG=dg.Define("scale", "w*lumiIntegrated").Define("good", "goodMeson_three_pt[goodMeson_Nphotons>0]").Histo1D(("hist", "D0* three PT", 100, 0, 200),"good", "scale")
h12SGN.SetFillColor(ROOT.kGreen-9)
h12BKG.SetFillColor(ROOT.kRed-9)

p=canvas.cd(34)
h12SGN.Draw("hist")
p=canvas.cd(35)
h12BKG.Draw("hist")
p=canvas.cd(36)
stack12 = ROOT.THStack("stack", "D0* three PT")
stack12.Add(h12BKG.GetValue())
stack12.Add(h12SGN.GetValue())
stack12.Draw("hist")
legend12 = ROOT.TLegend(0.7, 0.7, 0.9, 0.9)
legend12.AddEntry(h12SGN.GetValue(), "Signal", "f")
legend12.AddEntry(h12BKG.GetValue(), "Background", "f")
legend12.Draw()

canvas.SaveAs("~/public_html/D0StarBKG_new.png")

