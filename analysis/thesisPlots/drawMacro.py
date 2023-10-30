import ROOT

colors = {"RECO": "\033[1;36m", "GEN": "\033[1;34m", "BKG": "\033[1;31m", "NC": "\033[0m", "YELLOW": "\033[1;33m"}

defaultHistColors = [ROOT.kRed, ROOT.kBlue, ROOT.kGreen + 2, ROOT.kYellow + 1, ROOT.kOrange + 8]

def savePlot(histograms, imageName, options=None):
    text = " Starting... ".center(70, "~")
    print(colors["YELLOW"] + "[savePlot]~~~{}".format(text) + colors["NC"])

    imagePath = "/home/submit/pdmonte/public_html/thesisPlots"
    cs = ROOT.TCanvas("canvas", "canvas", 800, 800)

    stack4 = ROOT.THStack("stack", options["title"] if "title" in options else "Stack")
    legend4 = ROOT.TLegend(0.70, 0.70, 0.899, 0.899)

    usedColors = options["colors"] if "colors" in options else defaultHistColors

    for i, h in enumerate(histograms):
        stack4.Add(h[1])
        if "style" in options:
            if options["style"][i] == "l":
                legend4.AddEntry(h[1], h[0], "l")
                h[1].SetLineWidth(2)
                h[1].SetLineColor(usedColors[i])
            else:
                legend4.AddEntry(h[1], h[0], "f")
                h[1].SetLineWidth(0)
                h[1].SetFillColor(usedColors[i])
        else:
            legend4.AddEntry(h[1], h[0], "l")
            h[1].SetLineWidth(2)
            h[1].SetLineColor(usedColors[i])
    
    stack4.Draw("hist nostack")
    if "labelXAxis" in options:
        stack4.GetXaxis().SetTitle(options["labelXAxis"])
    if "labelYAxis" in options:
        stack4.GetYaxis().SetTitle(options["labelYAxis"])
    if "xRange" in options:
        stack4.GetXaxis().SetRangeUser(options["xRange"][0], options["xRange"][1])
    
    #legend4.SetMargin(0.17)
    legend4.SetBorderSize(0)
    legend4.SetTextSize(0.035)
    legend4.Draw()

    #cs.SetGrid()
    
    cs.SaveAs("{}/{}".format(imagePath, imageName))

    text = " Done! ".center(70, "~")
    print(colors["YELLOW"] + "[savePlot]~~~{}".format(text) + colors["NC"] + "\n")