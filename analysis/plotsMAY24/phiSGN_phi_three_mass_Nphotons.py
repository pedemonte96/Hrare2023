import ROOT

ROOT.ROOT.EnableImplicitMT()

if "/home/submit/pdmonte/CMSSW_10_6_27/src/Hrare2023/analysis/func_marti.so" not in ROOT.gSystem.GetLibraries():
    ROOT.gSystem.CompileMacro("/home/submit/pdmonte/CMSSW_10_6_27/src/Hrare2023/analysis/func_marti.cc","k")

date = "MAY19"

chainSGN = ROOT.TChain("events")
chainSGN.Add("/home/submit/pdmonte/CMSSW_10_6_27/src/Hrare2023/analysis/outputs/{0}/2018/outname_mc1040_GFcat_OmegaCat_2018.root".format(date))

df = ROOT.RDataFrame(chainSGN)

canvas = ROOT.TCanvas("canvas", "canvas", 1200, 800)

bins=100

h0=df.Define("scale", "w*lumiIntegrated")\
    .Define("filt", "(goodMeson_Nphotons < 1)")\
    .Define("good", "goodMeson_threemass[filt]")\
    .Histo1D(("hist", "#phi three mass", bins, 0.4, 1.6),"good", "scale")

h1=df.Define("scale", "w*lumiIntegrated")\
    .Define("filt", "(goodMeson_Nphotons < 2 && goodMeson_Nphotons > 0)")\
    .Define("good", "goodMeson_threemass[filt]")\
    .Histo1D(("hist", "#phi three mass", bins, 0.4, 1.6),"good", "scale")

h2=df.Define("scale", "w*lumiIntegrated")\
    .Define("filt", "(goodMeson_Nphotons > 1)")\
    .Define("good", "goodMeson_threemass[filt]")\
    .Histo1D(("hist", "#phi three mass", bins, 0.4, 1.6),"good", "scale")

hgen=df.Define("scale", "w*lumiIntegrated")\
    .Define("ThreeBodyMassGen", "getThreeBody4Momentum(GenPart_pdgId, GenPart_genPartIdxMother, GenPart_phi, GenPart_eta, GenPart_pt, GenPart_mass, 111, 211, -211, 333, 0)")\
    .Histo1D(("hist", "Three Body #phi Mass GEN", bins, 0.4, 1.6),"ThreeBodyMassGen", "scale")

h0.SetFillColor(ROOT.kRed)
h0.SetLineColor(ROOT.kBlack)
h1.SetFillColor(ROOT.kGreen-6)
h1.SetLineColor(ROOT.kBlack)
h2.SetFillColor(ROOT.kGreen+3)
h2.SetLineColor(ROOT.kBlack)
hgen.SetLineColor(ROOT.kBlue)
hgen.SetLineWidth(2)
hgen.GetXaxis().SetRangeUser(0.8, 1.3)

#h0.Scale(1/h0.GetEntries())
#h1.Scale(1/h1.GetEntries())
#h2.Scale(1/h2.GetEntries())

#print(h0.GetMean())
#h1.Scale(1/h1.GetEntries())
#print(h1.Integral(0,80),h1.GetEntries())
#print(h2.Integral(0,80))
hgen.Scale((h1.Integral(0,bins)+h2.Integral(0,bins))/(hgen.Integral(0,bins)))

#total = (h0.GetEntries()+h1.GetEntries()+h2.GetEntries())/100.

stack = ROOT.THStack("stack", "#phi three mass, reconstruction")
#stack.Add(h0.GetValue())
stack.Add(h2.GetValue())
stack.Add(h1.GetValue())
stack.Draw("hist")
hgen.Draw("hist same")
stack.GetXaxis().SetTitle("m_{#phi}^{#phi#rightarrow #pi#pi#pi} [GeV]")
stack.GetYaxis().SetTitle("Events")
stack.SetMaximum(3100.)

width = 0.004249
center = 1.019461
n=20
l = ROOT.TLine(center, 0, center, 3100)
l.SetLineWidth(2)
l.SetLineColor(ROOT.kBlack)
l.Draw()
l1 = ROOT.TLine(center-n*width, 0, center-n*width, 3100)
l1.SetLineWidth(2)
l1.SetLineStyle(2)
l1.SetLineColor(ROOT.kBlack)
l1.Draw()
l2 = ROOT.TLine(center+n*width, 0, center+n*width, 3100)
l2.SetLineWidth(2)
l2.SetLineStyle(2)
l2.SetLineColor(ROOT.kBlack)
l2.Draw()

legend = ROOT.TLegend(0.70, 0.65, 0.8999, 0.89)
legend.SetMargin(0.16)
legend.SetBorderSize(0)
legend.SetTextSize(0.04)
#legend.AddEntry(h0.GetValue(), "0 #gamma (mean: {:.3f} GeV)".format(round(h0.GetMean(), 3)), "f")
legend.AddEntry(h1.GetValue(), "m_{#phi} for 1 #gamma", "f")
legend.AddEntry(h2.GetValue(), "m_{#phi} for >2 #gamma", "f")
legend.AddEntry(hgen.GetValue(), "m_{#phi} gen level", "l")
legend.AddEntry(l, "m_{#phi} = 1020 GeV", "l")
legend.AddEntry(l1, "m_{#phi} #pm 20#Gamma_{#phi}", "l")
legend.Draw()

canvas.SaveAs("~/public_html/plotsMAY24/PhiSGN_phi_three_mass_Nphotons.png")

