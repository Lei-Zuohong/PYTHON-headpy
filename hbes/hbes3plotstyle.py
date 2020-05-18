# -*- coding: UTF-8 -*-
import ROOT


# Format for data points
def FormatAxis(axis):
    axis.SetLabelFont(42)
    axis.SetLabelSize(0.06)
    axis.SetLabelOffset(0.01)
    axis.SetNdivisions(510)
    axis.SetTitleFont(42)
    axis.SetTitleColor(1)
    axis.SetTitleSize(0.07)
    axis.SetTitleOffset(1.15)
    axis.CenterTitle()


def FormatData(datahist):
    datahist.SetMarkerStyle(20)
    datahist.SetMarkerSize(1.2)
    datahist.SetLineWidth(2)
    FormatAxis(datahist.GetXaxis())
    FormatAxis(datahist.GetYaxis())


def NameAxes(datahist, xname, yname):
    datahist.GetXaxis().SetTitle(xname)
    datahist.GetYaxis().SetTitle(yname)

# Format for main MC (red line)


def FormatMC1(mc1hist):
    mc1hist.SetLineColor(2)
    mc1hist.SetLineWidth(2)

# Format for second MC or background
# (Blue shaded area)


def FormatMC2_hist(mc2hist):
    mc2hist.SetLineColor(4)
    mc2hist.SetFillColor(4)
    mc2hist.SetLineWidth(2)
    mc2hist.SetFillStyle(3001)


def FormatMC2_graph(mc2hist):
    mc2hist.SetLineColor(4)
    mc2hist.SetLineWidth(2)

# Format for thired MC or background


def FormatMC3(mc3hist):
    mc3hist.SetLineColor(6)
    mc3hist.SetLineWidth(2)

# Write "BESIII" in the upper right corner


def WriteBes3():
    bes3 = ROOT.TLatex(0.94, 0.94, "BESIII")
    bes3.SetNDC()
    bes3.SetTextFont(72)
    bes3.SetTextSize(0.1)
    bes3.SetTextAlign(33)
    bes3.Draw()


# Write "Preliminary" below BESIII to be used together with WriteBes3()
def WritePreliminary():
    prelim = ROOT.TLatex(0.94, 0.86, "Preliminary")
    prelim.SetNDC()
    prelim.SetTextFont(62)
    prelim.SetTextSize(0.055)
    prelim.SetTextAlign(33)
    prelim.Draw()

# Make a legend
# position will have to change depending on the data shape


def MakeLegend_hist(datahist,   # Histogram with data
                    dataname,   # Description of data
                    mc1hist,    # Histogram with first MC
                    mc1name,    # Description of first MC
                    mc2hist,    # Histogram with 2nd MC/BG
                    mc2name,    # Description of second MC/BG
                    xlow,       # Left edge of legend
                    ylow,       # Bottom edge of legend
                    xhi,        # Right edge of legend
                    yhi):       # Top edge of legend
    leg = ROOT.TLegend(xlow, ylow, xhi, yhi)
    if(datahist and dataname):
        leg.AddEntry(datahist, dataname, 'LEP')
    if(mc1hist and mc1name):
        leg.AddEntry(mc1hist, mc1name, 'L')
    if(mc2hist and mc2name):
        leg.AddEntry(mc2hist, mc2name, 'LF')
    leg.SetFillColor(0)
    leg.SetTextFont(42)
    leg.Draw()


def MakeLegend_graph(datahist,
                     dataname,
                     mc1hist,
                     mc1name,
                     mc2hist,
                     mc2name,
                     mc3hist,
                     mc3name,
                     xlow,
                     ylow,
                     xhi,
                     yhi):
    leg = ROOT.TLegend(xlow, ylow, xhi, yhi)
    if(datahist and dataname):
        leg.AddEntry(datahist, dataname, 'LEP')
    if(mc1hist and mc1name):
        leg.AddEntry(mc1hist, mc1name, 'L')
    if(mc2hist and mc2name):
        leg.AddEntry(mc2hist, mc2name, 'L')
    if(mc3hist and mc3name):
        leg.AddEntry(mc3hist, mc3name, 'L')
    leg.SetFillColor(0)
    leg.SetTextFont(42)
    leg.Draw()

# Make a legend (version for fit functions)
# position will have to change depending on the data shape


def MakeLegend_fit(datahist,
                   dataname,
                   functionnames,   # List of fitting funcitons names
                   xlow,
                   ylow,
                   xhi,
                   yhi):
    leg = ROOT.TLegend(xlow, ylow, xhi, yhi)
    if(datahist and dataname):
        leg.AddEntry(datahist, dataname, 'LEP')
    list = datahist.GetListOfFunctions()
    nfun = list.GetEntries()
    for i in range(nfun):
        f1 = list.At(i)
        leg.AddEntry(f1, functionnames[i], 'L')
    leg.SetFillColor(0)
    leg.SetTextFont(42)
    leg.Draw()

# Set the general style options


def SetStyle():
    # No Canvas Border
    ROOT.gStyle.SetCanvasBorderMode(0)
    ROOT.gStyle.SetCanvasBorderSize(0)
    # White BG
    ROOT.gStyle.SetCanvasColor(10)
    # Format for axes
    ROOT.gStyle.SetLabelFont(42, "xyz")
    ROOT.gStyle.SetLabelSize(0.06, "xyz")
    ROOT.gStyle.SetLabelOffset(0.01, "xyz")
    ROOT.gStyle.SetNdivisions(510, "xyz")
    ROOT.gStyle.SetTitleFont(42, "xyz")
    ROOT.gStyle.SetTitleColor(1, "xyz")
    ROOT.gStyle.SetTitleSize(0.07, "xyz")
    ROOT.gStyle.SetTitleOffset(1.15, "xyz")
    # No pad borders
    ROOT.gStyle.SetPadBorderMode(0)
    ROOT.gStyle.SetPadBorderSize(0)
    # White BG
    ROOT.gStyle.SetPadColor(10)
    # Margins for labels etc.
    ROOT.gStyle.SetPadLeftMargin(0.17)
    ROOT.gStyle.SetPadBottomMargin(0.19)
    ROOT.gStyle.SetPadRightMargin(0.05)
    # ROOT.gStyle.SetPadRightMargin(0.12)
    ROOT.gStyle.SetPadTopMargin(0.05)
    # No error bars in x direction
    ROOT.gStyle.SetErrorX(0)
    # Format legend
    ROOT.gStyle.SetLegendBorderSize(0)

# Style options for "final" plots
# (no stat/fit box)


def SetPrelimStyle():
    ROOT.gStyle.SetOptDate(0)
    ROOT.gStyle.SetOptStat(0)
    ROOT.gStyle.SetOptFit(0)
    ROOT.gStyle.SetOptTitle(0)

# Style options for internal meetings
# (stat/fit box)


def SetMeetingStyle():
    ROOT.gStyle.SetOptDate(0)
    ROOT.gStyle.SetOptTitle(0)
    ROOT.gStyle.SetOptStat(1111)
    ROOT.gStyle.SetStatBorderSize(1)
    ROOT.gStyle.SetStatColor(10)
    ROOT.gStyle.SetStatFont(42)
    ROOT.gStyle.SetStatFontSize(0.03)
    ROOT.gStyle.SetOptFit(1111)
