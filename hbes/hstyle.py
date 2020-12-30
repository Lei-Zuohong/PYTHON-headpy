# -*- coding: UTF-8 -*-
import ROOT


def set_style():
    '设定BESIII合作组要求的图例'
    # 无画布边界
    ROOT.gStyle.SetCanvasBorderMode(0)
    ROOT.gStyle.SetCanvasBorderSize(0)
    # 白色画布背景
    ROOT.gStyle.SetCanvasColor(10)
    # 设定坐标轴
    ROOT.gStyle.SetLabelFont(42, "xyz")
    ROOT.gStyle.SetLabelSize(0.06, "xyz")
    ROOT.gStyle.SetLabelOffset(0.01, "xyz")
    ROOT.gStyle.SetNdivisions(510, "xyz")
    ROOT.gStyle.SetTitleFont(42, "xyz")
    ROOT.gStyle.SetTitleColor(1, "xyz")
    ROOT.gStyle.SetTitleSize(0.07, "xyz")
    ROOT.gStyle.SetTitleOffset(1.15, "xyz")
    # 无画板边界
    ROOT.gStyle.SetPadBorderMode(0)
    ROOT.gStyle.SetPadBorderSize(0)
    # 白色画板背景
    ROOT.gStyle.SetPadColor(10)
    # 设置画板边距
    ROOT.gStyle.SetPadLeftMargin(0.17)
    ROOT.gStyle.SetPadBottomMargin(0.19)
    ROOT.gStyle.SetPadRightMargin(0.05)
    # ROOT.gStyle.SetPadRightMargin(0.12)
    ROOT.gStyle.SetPadTopMargin(0.05)
    # 横坐标无误差棒
    ROOT.gStyle.SetErrorX(0)
    # 设置标注
    ROOT.gStyle.SetLegendBorderSize(0)
    ROOT.gStyle.SetOptDate(0)
    ROOT.gStyle.SetOptStat(0)
    ROOT.gStyle.SetOptFit(0)
    ROOT.gStyle.SetOptTitle(0)

#


def get_canvas(x=800, y=600, dx=1, dy=1):
    '''
    x, y 为画布大小\n
    dx, dy 为画布分区\n
    作用1：返回一个TCanvas对象\n
    '''
    canvas = ROOT.TCanvas('canvas', '', x, y)
    canvas.Divide(dx, dy)
    return canvas


def get_legend(legendlist=[],
               l=0.6, r=0.93, d=0.7, u=0.93,
               Fillcolor=0,
               Textfont=42,
               Textsize=0.035,
               header=''):
    '''
    legendlist 为列表，其中元素为[TObject,str,str]\n
    第一个元素为TObject\n
    第二个元素为标注内容\n
    第三个元素为标注标志('F','lp')\n
    l,r,d,u 为注释占画布比例\n
    作用1：返回一个TLegend对象\n
    '''
    legend = ROOT.TLegend(l, d, r, u)
    for i in legendlist:
        legend.AddEntry(i[0], i[1], i[2])
    legend.SetFillColor(Fillcolor)
    legend.SetTextFont(Textfont)
    legend.SetTextSize(Textsize)
    legend.SetHeader(header)
    return legend


def add_arrow(drawlist,
              x0, y0, x1, y1,
              Linecolor=2,
              Linewidth=3):
    '''
    x0,y0,x1,y1 为箭头起始结束位置坐标\n
    作用1：添加一个TArrow对象到drawlist\n
    '''
    in_drawlist = drawlist
    newarrow = ROOT.TArrow(x0, y0, x1, y1, 0.05, '|>')
    newarrow.SetLineColor(Linecolor)
    newarrow.SetLineWidth(Linewidth)
    in_drawlist.append(newarrow)
    return in_drawlist


def add_box(drawlist,
            l, r, d, u,
            Linecolor=2,
            Linewidth=3):
    '''
    l,r,d,u 为方框的边位置\n
    作用1：添加一系列TArrow对象到drawlist，形成方框\n
    '''
    in_drawlist = drawlist
    in_drawlist = add_arrow(in_drawlist, l, d, l, u, Linecolor, Linewidth)
    in_drawlist = add_arrow(in_drawlist, l, u, r, u, Linecolor, Linewidth)
    in_drawlist = add_arrow(in_drawlist, r, u, r, d, Linecolor, Linewidth)
    in_drawlist = add_arrow(in_drawlist, r, d, l, d, Linecolor, Linewidth)
    return in_drawlist

#


def set_axis(hist, xname, yname):
    '''
    作用1：设定BESIII合作组要求的坐标轴样式\n
    '''
    hist.GetXaxis().SetTitle(xname)
    hist.GetYaxis().SetTitle(yname)
    hist.GetXaxis().SetLabelFont(42)
    hist.GetXaxis().SetLabelSize(0.06)
    hist.GetXaxis().SetLabelOffset(0.01)
    hist.GetXaxis().SetNdivisions(505)
    hist.GetXaxis().SetTitleFont(42)
    hist.GetXaxis().SetTitleColor(1)
    hist.GetXaxis().SetTitleSize(0.07)
    hist.GetXaxis().SetTitleOffset(1.15)
    hist.GetXaxis().CenterTitle()

    hist.GetYaxis().SetLabelFont(42)
    hist.GetYaxis().SetLabelSize(0.06)
    hist.GetYaxis().SetLabelOffset(0.01)
    hist.GetYaxis().SetNdivisions(505)
    hist.GetYaxis().SetTitleFont(42)
    hist.GetYaxis().SetTitleColor(1)
    hist.GetYaxis().SetTitleSize(0.07)
    hist.GetYaxis().SetTitleOffset(1.15)
    hist.GetYaxis().CenterTitle()


def set_marker(hist, Markerstyle=20, Markersize=1.2, Linewidth=2):
    '''
    作用1：设定一个误差棒的样式\n
    '''
    hist.SetMarkerStyle(Markerstyle)
    hist.SetMarkerSize(Markersize)
    hist.SetLineWidth(Linewidth)


def set_height(hist, multiple=1.5):
    '''
    作用1：设定一个要绘制的图像的高度为几倍其最大值\n
    '''
    height = hist.GetMaximum()
    hist.GetYaxis().SetRangeUser(0, multiple * height)


def set_background(hist,
                   Fillcolor=4,
                   Linecolor=4,
                   Linewidth=2,
                   Fillstyle=3001):
    '''
    作用1：设定直方图样式
    '''
    hist.SetLineColor(Linecolor)
    hist.SetFillColor(Fillcolor)
    hist.SetLineWidth(Linewidth)
    hist.SetFillStyle(Fillstyle)


def set_xrange(hist):
    # 得到参数
    bins = hist.GetNbinsX()
    width = hist.GetBinWidth(0)
    lowedge = hist.GetBinLowEdge(0)
    bin_left = 0
    bin_left_check = 0
    bin_right = 0
    for bini in range(bins):
        bincontent = hist.GetBinContent(bini)
        if(bincontent == 0 and bin_left_check == 0):
            bin_left = bini
        if(bincontent != 0):
            bin_left_check = 1
            bin_right = bini
    # 调整向外延伸bin
    bin_left_save = 1.25 * bin_left - 0.25 * bin_right
    bin_right_save = 1.25 * bin_right - 0.25 * bin_left

    if(bin_left > bin_left_save): bin_left = bin_left_save
    if(bin_right < bin_right_save): bin_right = bin_right_save

    x_left = lowedge + bin_left * width
    x_right = lowedge + (bin_right + 1) * width
    # 设定range
    hist.GetXaxis().SetRangeUser(x_left, x_right)
