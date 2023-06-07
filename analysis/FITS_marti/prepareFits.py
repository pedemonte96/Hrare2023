import ROOT
ROOT.ROOT.EnableImplicitMT()


def getHisto(nbin, xlow, xhigh, num, cat, mesonCat, year):

   date = "JUN07"

   chain = ROOT.TChain("events")
   chain.Add("/home/submit/pdmonte/CMSSW_10_6_27/src/Hrare2023/analysis/outputs/{}/{}/outname_mc{}_{}_{}_{}.root".format(date, year, num, cat, mesonCat, year))

   df = ROOT.RDataFrame(chain)

   h=df.Define("scale", "w*lumiIntegrated").Histo1D(("m_{H}", "Higgs candidate invariant mass, reconstruction", nbin, xlow, xhigh),"HCandMass", "scale")

   h.GetXaxis().SetTitle("m_{#gamma meson}^{H} [GeV]")
   h.GetYaxis().SetTitle("Events")

   h.SetFillColor(ROOT.kGreen-6)
   h.SetLineColor(ROOT.kBlack)
   return h
