import ROOT

ROOT.ROOT.EnableImplicitMT()

if "/home/submit/pdmonte/CMSSW_10_6_27/src/Hrare2023/analysis/func_marti.so" not in ROOT.gSystem.GetLibraries():
    ROOT.gSystem.CompileMacro("/home/submit/pdmonte/CMSSW_10_6_27/src/Hrare2023/analysis/func_marti.cc","k")

date = "MAY22"

chainSGN = ROOT.TChain("events");
chainSGN.Add("/home/submit/pdmonte/CMSSW_10_6_27/src/Hrare2023/analysis/outputs/{0}/2018/outname_mc1039_GFcat_D0StarCat_2018.root".format(date))

chainBKG = ROOT.TChain("events");
chainBKG.Add("/home/submit/pdmonte/CMSSW_10_6_27/src/Hrare2023/analysis/outputs/{0}/2018/outname_mc10_GFcat_D0StarCat_2018.root".format(date))
chainBKG.Add("/home/submit/pdmonte/CMSSW_10_6_27/src/Hrare2023/analysis/outputs/{0}/2018/outname_mc11_GFcat_D0StarCat_2018.root".format(date))
chainBKG.Add("/home/submit/pdmonte/CMSSW_10_6_27/src/Hrare2023/analysis/outputs/{0}/2018/outname_mc12_GFcat_D0StarCat_2018.root".format(date))
chainBKG.Add("/home/submit/pdmonte/CMSSW_10_6_27/src/Hrare2023/analysis/outputs/{0}/2018/outname_mc13_GFcat_D0StarCat_2018.root".format(date))
chainBKG.Add("/home/submit/pdmonte/CMSSW_10_6_27/src/Hrare2023/analysis/outputs/{0}/2018/outname_mc14_GFcat_D0StarCat_2018.root".format(date))

df = ROOT.RDataFrame(chainSGN)
dg = ROOT.RDataFrame(chainBKG)

canvas = ROOT.TCanvas("canvas", "canvas", 1200, 800)

hSGN = df.Define("scale", "w*lumiIntegrated")\
	.Histo1D(("D^{0} kin mass", "D^{0} kinetic mass, reconstruction", 50, 1.6, 2.1),"goodMeson_mass", "scale")
hBKGD0 = dg.Define("scale", "w*lumiIntegrated")\
    .Define("goodMeson_mass_D0", "getValuesIdParticle(goodMeson_mass, GenPart_pdgId, 421, 1)")\
	.Histo1D(("D^{0} kin mass", "D^{0} kinetic mass, reconstruction", 50, 1.6, 2.1),"goodMeson_mass_D0", "scale")
hBKG = dg.Define("scale", "w*lumiIntegrated")\
    .Define("goodMeson_mass_D0", "getValuesIdParticle(goodMeson_mass, GenPart_pdgId, 421, 0)")\
	.Histo1D(("D^{0} kin mass", "D^{0} kinetic mass, reconstruction", 50, 1.6, 2.1),"goodMeson_mass_D0", "scale")

hSGN.SetFillColor(ROOT.kGreen-6)
hSGN.SetLineColor(ROOT.kBlack)
hBKGD0.SetFillColor(ROOT.kRed-3)
hBKGD0.SetLineColor(ROOT.kBlack)
hBKG.SetFillColor(ROOT.kRed-6)
hBKG.SetLineColor(ROOT.kBlack)

stack = ROOT.THStack("stack", "D^{0} kinetic mass, reconstruction")
stack.Add(hBKG.GetValue())
stack.Add(hBKGD0.GetValue())
stack.Add(hSGN.GetValue())
stack.Draw("hist")
stack.GetXaxis().SetTitle("m_{2trk}^{D^{0}#rightarrow K#pi} [GeV]")
stack.GetYaxis().SetTitle("Events")

legend = ROOT.TLegend(0.7, 0.65, 0.8999, 0.89)
legend.SetMargin(0.27)
legend.SetBorderSize(0)
legend.AddEntry(hSGN.GetValue(), "Signal", "f")
legend.AddEntry(hBKGD0.GetValue(), "Background with D^{0}", "f")
legend.AddEntry(hBKG.GetValue(), "#splitline{Background wrong}{combination}", "f")
legend.Draw()

canvas.SaveAs("~/public_html/plotsMAY24/D0StarBKG_kin_mass.png")

