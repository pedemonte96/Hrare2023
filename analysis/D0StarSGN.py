import ROOT

ROOT.ROOT.EnableImplicitMT()

date = "MAY09"

chain = ROOT.TChain("events");
chain.Add("/home/submit/pdmonte/Hrare2023/analysis/outputs/{0}/2018/outname_mc1039_GFcat_D0StarCat_2018.root".format(date))

df = ROOT.RDataFrame(chain)

h1=df.Histo1D(("hist", "D0 kinematic mass", 100, 1, 3),"goodMeson_mass")
h2=df.Histo1D(("hist", "D0 isolation", 100, 0, 2),"goodMeson_iso")
h3=df.Histo1D(("hist", "D0Star photons", 10, 0, 10),"goodMeson_Nphotons")

h4=df.Filter("goodMeson_threemass[0] > 0.1").Histo1D(("hist", "D0Star three mass", 100, 1, 3),"goodMeson_threemass")
h5=df.Histo1D(("hist", "D0 DR kaon-pion", 100, 0, 0.2),"goodMeson_DR_D0")
h6=df.Histo1D(("hist", "D0Star DR D0-photon", 100, 0, 10),"goodMeson_DR_D0Star")
h7=df.Filter("goodMeson_three_pt[0] > 25").Histo1D(("hist", "D0Star three PT", 100, 0, 300),"goodMeson_three_pt")
h8=df.Filter("goodMeson_pt[0] > 25").Histo1D(("hist", "D0 PT", 100, 0, 300),"goodMeson_pt")
h9=df.Histo1D(("hist", "D0Star Photon PT", 100, 0, 100),"goodMeson_D0Star_photon_pt")
h10=df.Histo1D(("hist", "Pion PT", 60, 0, 300),"goodMeson_trk1_pt")
h11=df.Histo1D(("hist", "Kaon PT", 60, 0, 300),"goodMeson_trk2_pt")



canvas = ROOT.TCanvas("canvas", "canvas", 1800, 3800)
canvas.Divide(2, 6)
canvas.cd(1)
h1.Draw("hist")
canvas.cd(2)
h2.Draw("hist")
pad = canvas.cd(3)
pad.SetLogy()
h3.Draw("hist")
pad = canvas.cd(4)
#pad.SetLogy()
h4.Draw("hist")
canvas.cd(5)
h5.Draw("hist")
canvas.cd(6)
h6.Draw("hist")
canvas.cd(7)
h7.Draw("hist")
pad=canvas.cd(8)
#pad.SetLogy()
h8.Draw("hist")
pad=canvas.cd(9)
pad.SetLogy()
h9.Draw("hist")
pad=canvas.cd(10)
h10.Draw("hist")
pad=canvas.cd(11)
h11.Draw("hist")
canvas.SaveAs("~/public_html/D0StarSGN.png")

