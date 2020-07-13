# -*- coding: UTF-8 -*-
'''
This is a package document.

    Environment version:

        python2
        请在python2环境下运行程序

    Content:
    
        @get_canvas():
	    @get_legend()：
        @add_arrow():
        @add_box():
        @set_style():
        @set_axis():
        @set_marker():
        @set_height():
        @set_background():
'''
# Public package
# Private package
import ROOT


def get_canvas(x=800, y=600, dx=1, dy=1):
    '''
    x为浮点，输入画布横向长度\n
    y为浮点，输入画布纵向长度\n
    dx为分区，输入画布横向分区\n
    dy为分区，输入画布纵向分区\n
    作用1：返回一个TCanvas对象\n
    '''
    canvas = ROOT.TCanvas('canvas', '', x, y)
    canvas.Divide(dx, dy)
    return canvas


def get_legend(legendlist=[],
               l=0.6, r=0.93, d=0.7, u=0.93,
               fillcolor=0,
               textfont=42,
               textsize=0.035,
               header=''):
    '''
    legendlist为列表，其中元素为[TObject,str,str]\n
    第一个元素为标注目标\n
    第二个元素为标注字符\n
    第三个元素为标注选项\n
    l,r,d,u为浮点，输入标注占画布比例\n
    作用1：返回一个TLegend对象\n
    '''
    legend = ROOT.TLegend(l, d, u, r)
    for i in legendlist:
        legend.AddEntry(i[0], i[1], i[2])
    legend.SetFillColor(fillcolor)
    legend.SetTextFont(textfont)
    legend.SetTextSize(textsize)
    legend.SetHeader(header)
    return legend


def add_arrow(drawlist,
              x0, y0, x1, y1,
              colornumber=2,
              width=3):
    '''
    drawlist为列表，输入初始列表\n
    x0,y0,x1,y1为浮点，输入箭头的开始和初始位置\n
    colornumber为整形，输入箭头的颜色\n
    width为整形，输入箭头的粗细\n
    作用1：添加一个TArrow对象到drawlist\n
    '''
    in_drawlist = drawlist
    newarrow = ROOT.TArrow(x0, y0, x1, y1, 0.05, '|>')
    newarrow.SetLineColor(colornumber)
    newarrow.SetLineWidth(width)
    in_drawlist.append(newarrow)
    return in_drawlist


def add_box(drawlist,
            l, r, d, u,
            colornumber=2,
            width=3):
    '''
    drawlist为列表，输入初始列表\n
    l,r,d,u为浮点，输入方框的边位置\n
    colornumber为整形，输入方框的颜色\n
    width为整形，输入方框的粗细\n
    作用1：添加一系列TArrow对象到drawlist，形成方框\n
    '''
    in_drawlist = drawlist
    in_drawlist = add_arrow(in_drawlist, l, d, l, u, colornumber, width)
    in_drawlist = add_arrow(in_drawlist, l, u, r, u, colornumber, width)
    in_drawlist = add_arrow(in_drawlist, r, u, r, d, colornumber, width)
    in_drawlist = add_arrow(in_drawlist, r, d, l, d, colornumber, width)
    return in_drawlist


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


def set_axis(hist, xname, yname):
    '''
    hist为TH1，输入要改变坐标的TObject\n
    xname为字符，输入横坐标字符\n
    yname为字符，输入纵坐标字符\n
    作用1：设定BESIII合作组要求的坐标轴样式\n
    '''
    hist.GetXaxis().SetTitle(xname)
    hist.GetYaxis().SetTitle(yname)
    hist.GetXaxis().SetLabelFont(42)
    hist.GetXaxis().SetLabelSize(0.06)
    hist.GetXaxis().SetLabelOffset(0.01)
    hist.GetXaxis().SetNdivisions(510)
    hist.GetXaxis().SetTitleFont(42)
    hist.GetXaxis().SetTitleColor(1)
    hist.GetXaxis().SetTitleSize(0.07)
    hist.GetXaxis().SetTitleOffset(1.15)
    hist.GetXaxis().CenterTitle()
    hist.GetYaxis().SetLabelFont(42)
    hist.GetYaxis().SetLabelSize(0.06)
    hist.GetYaxis().SetLabelOffset(0.01)
    hist.GetYaxis().SetNdivisions(510)
    hist.GetYaxis().SetTitleFont(42)
    hist.GetYaxis().SetTitleColor(1)
    hist.GetYaxis().SetTitleSize(0.07)
    hist.GetYaxis().SetTitleOffset(1.15)
    hist.GetYaxis().CenterTitle()


def set_marker(hist):
    '设定一个要绘制误差棒的图像的样式'
    hist.SetMarkerStyle(20)
    hist.SetMarkerSize(1.2)
    hist.SetLineWidth(2)


def set_height(hist, multiple=1.5):
    '设定一个要绘制的图像的高度为几倍其最大值'
    height = hist.GetMaximum()
    hist.GetYaxis().SetRangeUser(0, multiple * height)


def set_background(hist):
    'Set hist of a background'
    hist.SetLineColor(4)
    hist.SetFillColor(4)
    hist.SetLineWidth(2)
    hist.SetFillStyle(3001)


def set_background_alter(hist):
    'Set hist of another background'
    hist.SetLineColor(2)
    hist.SetFillColor(2)
    hist.SetLineWidth(2)
    hist.SetFillStyle(3001)


def set_background_stack(hist, Fillcolor=2, Linecolor=2, Linewidth=0, Fillstyle=3001):
    'Set hist of a sideband'
    hist.SetLineColor(Linecolor)
    hist.SetFillColor(Fillcolor)
    hist.SetLineWidth(Linewidth)
    hist.SetFillStyle(Fillstyle)
