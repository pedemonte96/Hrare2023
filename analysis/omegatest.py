import ROOT

ROOT.ROOT.EnableImplicitMT()

chain = ROOT.TChain("events");
chain.Add("/work/submit/pdmonte/Hrare2023/analysis/MAY08/2018/outname_mc1037_GFcat_OmegaCat_2018.root")

df = ROOT.RDataFrame(chain)

h1=df.Histo1D(("hist", "Omega kinematic mass", 100, 0, 2),"goodMeson_mass")
h2=df.Histo1D(("hist", "Omega isolation", 100, 0, 2),"goodMeson_iso")
h3=df.Filter("goodMeson_Nphotons[0] > 1").Histo1D(("hist", "Omega photons", 10, 0, 10),"goodMeson_Nphotons")

h4=df.Filter("goodMeson_threemass[0] > 0.1 && goodMeson_Nphotons[0] > 1").Histo1D(("hist", "Omega three mass", 100, 0, 2),"goodMeson_threemass")
h5=df.Histo1D(("hist", "Omega DR", 100, 0, 0.1),"goodMeson_DR")
h6=df.Histo1D(("hist", "Omega PT", 100, 0, 100),"goodMeson_pt")



canvas = ROOT.TCanvas("canvas", "canvas", 1700, 1500)
canvas.Divide(2, 3)
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
canvas.SaveAs("~/public_html/OmegaKinMass_2.png")

