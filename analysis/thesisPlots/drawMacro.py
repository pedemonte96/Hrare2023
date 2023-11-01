import ROOT

colors = {"RECO": "\033[1;36m", "GEN": "\033[1;34m", "BKG": "\033[1;31m", "NC": "\033[0m", "YELLOW": "\033[1;33m"}

defaultHistColors = [ROOT.kRed + 1, ROOT.kBlue, ROOT.kGreen + 2, ROOT.kYellow + 1, ROOT.kOrange + 8]

def savePlot(histograms, imageName, options=None):
    text = " Starting... ".center(70, "~")
    print(colors["YELLOW"] + "[savePlot]~~~{}".format(text) + colors["NC"])

    imagePath = "/home/submit/pdmonte/public_html/thesisPlots"
    cs = ROOT.TCanvas("canvas", "canvas", 900, 900)

    stack4 = ROOT.THStack()
    legend4 = ROOT.TLegend(0.70, 0.70, 0.899, 0.899)

    usedColors = options["colors"] if "colors" in options else defaultHistColors

    markers = []
    maxHeight = 0
    for i, h in enumerate(histograms):
        maxHeight = max(maxHeight, h[1].GetMaximum())
        if "style" in options:
            if options["style"][i] == "l":
                stack4.Add(h[1])
                legend4.AddEntry(h[1], h[0], "l")
                h[1].SetLineWidth(3)
                h[1].SetLineColor(usedColors[i])
            elif options["style"][i] == "f":
                legend4.AddEntry(h[1], h[0], "f")
                stack4.Add(h[1])
                h[1].SetLineWidth(0)
                h[1].SetFillColor(usedColors[i])
            elif options["style"][i] == "p":
                legend4.AddEntry(h[1], h[0], "lep")
                markers.append((h[1], usedColors[i]))
        else:
            stack4.Add(h[1])
            legend4.AddEntry(h[1], h[0], "l")
            h[1].SetLineWidth(3)
            h[1].SetLineColor(usedColors[i])

    stack4.SetMaximum(1.2*maxHeight)

    if "HCandMass" in options:
        stack4.Draw("hist")
        line1 = ROOT.TLine(115., 0., 115., maxHeight*100)
        line1.SetLineColor(11)
        line1.Draw()
        line2 = ROOT.TLine(135., 0., 135., maxHeight*100)
        line2.SetLineColor(11)
        line2.Draw()
    else:
        stack4.Draw("hist nostack")

    for h, col in markers:
        h.SetMarkerStyle(20)
        h.SetMarkerSize(1.3)
        h.SetLineWidth(3)
        h.SetMarkerColor(col)
        h.SetLineColor(col)
        h.Draw("EP SAME")

    if "labelXAxis" in options:
        stack4.GetXaxis().SetTitle(options["labelXAxis"])
    if "labelYAxis" in options:
        stack4.GetYaxis().SetTitle(options["labelYAxis"])
    if "xRange" in options:
        stack4.GetXaxis().SetRangeUser(options["xRange"][0], options["xRange"][1])
    if "logScale" in options:
        if options["logScale"]:
            stack4.SetMaximum(10*maxHeight)
            stack4.SetMinimum(1)
            cs.SetLogy(1)
    
    legend4.SetTextFont(42)
    legend4.SetFillStyle(0)
    legend4.SetBorderSize(0)
    legend4.SetTextSize(0.04)
    legend4.SetTextAlign(32)
    legend4.Draw("same")

    text = ROOT.TLatex()
    text.SetNDC()
    text.SetTextFont(72)
    text.SetTextSize(0.045)
    text.DrawLatex(0.105, 0.913, "CMS")
    text.SetTextFont(42)
    text.DrawLatex(0.105 + 0.12, 0.913, "Internal" if options["data"] else "Simulation")
    text.SetTextSize(0.035)
    text.DrawLatex(0.59, 0.913, "#sqrt{s} = 13 TeV, %0.2f fb#kern[-0.1]{^{-1}}"% (39.54))
    
    cs.SaveAs("{}/{}".format(imagePath, imageName))

    text = " Done! ".center(70, "~")
    print(colors["YELLOW"] + "[savePlot]~~~{}".format(text) + colors["NC"] + "\n")