# -*- coding: UTF-8 -*-
# Public pack
import os
import re
import sys
# Private pack
import ROOT
import headpy.hscreen.hprint as hprint
import headpy.hfile.hpickle as hpickle
import headpy.hbes.hnew as hnew


def fit_checkok(filename, do_print='yes'):
    '''
    输入log文件，返回是否OK
    '''
    output = 0
    with open(filename, 'r') as infile:
        log = infile.read()
        # 寻找所有状态字符
        checklist = re.compile(r'STATUS=(.*) ').findall(log)
        checkok = 0
        # 输出所有状态字符
        if(do_print != ''):
            hprint.pstar()
            for i in checklist:
                hprint.pline(i)
            hprint.pstar()
        # 最后一个状态OK则返回
        for status in checklist:
            checkok = 0
            if(re.search(r'OK', status)):
                checkok = 1
    output = checkok
    return output


def fit_dump(energy=0,
             tree='',
             selecters={},
             datar='',
             datam='',
             branch='',
             docuts=[],
             doweight=''):
    '''
    作用：\n
    将对应能量点的数据，经过cut后，输出到temp文件夹，并返回查询信息\n
    格式为{'r':[file,name],'m':[file,name]}\n
    '''
    massages = hnew.massage_read()
    trees = hnew.trees_read(energy=energy,
                            tree=tree,
                            read=[datar, datam])
    alldata = hnew.ALLDATA(trees=trees,
                           selecters=selecters,
                           massages=massages)
    if(doweight != ''):
        alldata.get_weight(data='omeganpw',
                           energy=energy,
                           name_weight=doweight,
                           name_branch='fit_weight',
                           dimension=2)
    histr1, histr2 = alldata.tree(data=datar,
                                  branch=branch,
                                  docuts=docuts,
                                  name='fit_real')
    histm1, histm2 = alldata.hist(data=datam,
                                  branchs=[branch],
                                  docuts=docuts,
                                  name='fit_mc',
                                  doweight=['fit_weight'])
    hist = {}
    hist['r'] = [histr1, histr2]
    hist['m'] = [histm1, histm2]
    return hist


def dofit_method1(energy=0,
                  histpkl='',
                  optionpkl='',
                  datasetpkl='',
                  backfunction='',
                  signfunction='',
                  pictures=[],
                  picture_stop='',
                  picture_xtitle='',
                  picture_ytitle=''):
    '''
    histpkl         输入存储数据的文件信息，格式为{'r':[file,name],'m':[file,name]}\n
    optionpkl       输入存储初始参数的信息\n
    datasetpkl      输入横坐标的信息，格式为{'name':,'mass':,'cut':}\n
    backfunciont    输入本底函数形式[d1polynomial,d2polynomial,d3polynomial]\n
    signfunction    输入信号函数形式[None,evolution]\n
    picture         不为空，则输入，输出图片的文件位置\n
    \n
    作用1：         根据输入参数进行一次拟合\n
    作用2：         输出拟合的数值结果\n
    作用3：         输出拟合的图片文件\n
    '''
    # 1.输入数据hist
    hist = hpickle.pkl_read(histpkl)
    tfilem = ROOT.TFile(hist['m'][0])
    tfiler = ROOT.TFile(hist['r'][0])
    datam = tfilem.Get(hist['m'][1])
    datar = tfiler.Get(hist['r'][1])
    # 1.输入数据option
    option = hpickle.pkl_read(optionpkl)
    # 1.输入数据dataset
    dataset = hpickle.pkl_read(datasetpkl)
    # 2.构建横坐标参数
    mass = ROOT.RooRealVar(dataset['name'],
                           dataset['name'],
                           dataset['mass'] - dataset['cut'],
                           dataset['mass'] + dataset['cut'])
    # 2.构建拟合参数
    parameter = {}
    for i in option:
        parameter[i] = ROOT.RooRealVar(i, i,
                                       option[i][0],
                                       option[i][1],
                                       option[i][2])
    # 2.构建本底函数
    if(backfunction == 'd1polynomial'):
        backpdf = ROOT.RooPolynomial('backpdf', 'backpdf',
                                     mass,
                                     ROOT.RooArgList(parameter['p0']))
    elif(backfunction == 'd2polynomial'):
        backpdf = ROOT.RooPolynomial('backpdf', 'backpdf',
                                     mass,
                                     ROOT.RooArgList(parameter['p0'],
                                                     parameter['p1']))
    elif(backfunction == 'd3polynomial'):
        backpdf = ROOT.RooPolynomial('backpdf', 'backpdf',
                                     mass,
                                     ROOT.RooArgList(parameter['p0'],
                                                     parameter['p1'],
                                                     parameter['p2']))
    else:
        print('输入了错误的本底函数形式')
    # 3.构建信号函数
    histm = ROOT.RooDataHist('histm', 'histm',
                             ROOT.RooArgList(mass),
                             datam)
    if(signfunction == 'None'):
        signpdf = ROOT.RooHistPdf('signpdf', 'signpdf',
                                  ROOT.RooArgSet(mass),
                                  histm,
                                  1)
    if(signfunction == 'evolution'):
        mcpdf = ROOT.RooHistPdf('signpdf', 'signpdf',
                                ROOT.RooArgSet(mass),
                                histm,
                                1)
        gauss = ROOT.RooGaussian('gauss', 'gauss',
                                 mass,
                                 parameter['gmean'],
                                 parameter['gsigm'])
        signpdf = ROOT.RooFFTConvPdf('signpdf', 'signpdf',
                                     mass,
                                     mcpdf,
                                     gauss)
    # 3.构建总函数
    allpdf = ROOT.RooAddPdf('allpdf', 'allpdf',
                            ROOT.RooArgList(signpdf, backpdf),
                            ROOT.RooArgList(parameter['npdf1'],
                                            parameter['npdf2']))
    # 3.输入真实数据
    # 4.拟合
    realpdf = ROOT.RooDataSet('datar', 'datar',
                              datar,
                              ROOT.RooArgSet(ROOT.RooArgList(mass)))
    fitresult = allpdf.fitTo(realpdf, ROOT.RooFit.Save())
    # 5.输出数据
    output = {}
    output['nevent'] = parameter['npdf1'].getVal()
    output['enevent'] = parameter['npdf1'].getError()
    # 5.输出图片
    if(len(pictures) != 0):
        massframe = mass.frame()
        realpdf.plotOn(massframe)
        allpdf.plotOn(massframe)
        allpdf.plotOn(massframe, ROOT.RooFit.Components('backpdf'),
                      ROOT.RooFit.LineStyle(ROOT.kDashed),
                      ROOT.RooFit.LineColor(ROOT.kRed))
        cvs = ROOT.TCanvas('canvas', '', 1200, 900)
        cvs.SetFillColor(10)
        cvs.SetFrameLineWidth(2)
        cvs.SetTickx()
        cvs.SetTicky()
        massframe.SetTitle('')
        massframe.GetXaxis().SetTitle(picture_xtitle)
        massframe.GetXaxis().SetTitleSize(0.05)
        massframe.GetXaxis().SetTitleOffset(0.9)
        massframe.GetXaxis().CenterTitle()
        massframe.GetXaxis().SetNdivisions(505)
        massframe.GetYaxis().SetTitle(picture_ytitle)
        massframe.GetYaxis().SetTitleSize(0.05)
        massframe.GetYaxis().SetTitleOffset(0.9)
        massframe.GetYaxis().CenterTitle()
        massframe.Draw()
        pt = ROOT.TPaveText(0.60, 0.60, 0.85, 0.85, 'BRNDC')
        pt.SetBorderSize(0)
        pt.SetTextAlign(12)
        pt.SetTextColor(1)
        pt.SetTextSize(0.05)
        pt.AddText('Energy: %1.4f GeV' % (energy))
        pt.AddText('Sig: ' + str(round(parameter['npdf1'].getVal(), 1)) +
                   '#pm' + str(round(parameter['npdf1'].getError(), 1)))
        pt.AddText('Bkg:  ' + str(round(parameter['npdf2'].getVal(), 1)) +
                   '#pm' + str(round(parameter['npdf2'].getError(), 1)))
        pt.Draw()
        if(picture_stop != ''):
            input()
        for i in pictures:
            cvs.Print(i)
    del tfilem
    del tfiler
    del datar
    del datam
    return output


def dofit_method2(energy=0,
                  histpkl='',
                  optionpkl='',
                  datasetpkl='',
                  backfunction='',
                  signfunction='',
                  pictures=[],
                  picture_stop='',
                  picture_xtitle='',
                  picture_ytitle=''):
    '''
    histpkl         输入存储数据的文件信息，格式为{'r':[file,name],'m':[file,name]}\n
    optionpkl       输入存储初始参数的信息\n
    datasetpkl      输入横坐标的信息，格式为{'name':,'mass':,'cut':}\n
    backfunciont    输入本底函数形式[d1polynomial,d2polynomial,d3polynomial]\n
    signfunction    输入信号函数形式[None,evolution]\n
    picture         不为空，则输入，输出图片的文件位置\n
    \n
    作用1：         根据输入参数进行一次拟合\n
    作用2：         输出拟合的数值结果\n
    作用3：         输出拟合的图片文件\n
    '''
    # 1.输入数据hist
    hist = hpickle.pkl_read(histpkl)
    tfilem = ROOT.TFile(hist['m'][0])
    tfiler = ROOT.TFile(hist['r'][0])
    tfileb = ROOT.TFile(hist['b'][0])
    datam = tfilem.Get(hist['m'][1])
    datar = tfiler.Get(hist['r'][1])
    datab = tfileb.Get(hist['b'][1])
    # 1.输入数据option
    option = hpickle.pkl_read(optionpkl)
    # 1.输入数据dataset
    dataset = hpickle.pkl_read(datasetpkl)
    # 2.构建横坐标参数
    mass = ROOT.RooRealVar(dataset['name'],
                           dataset['name'],
                           dataset['mass'] - dataset['cut'],
                           dataset['mass'] + dataset['cut'])
    # 2.构建拟合参数
    parameter = {}
    for i in option:
        parameter[i] = ROOT.RooRealVar(i, i,
                                       option[i][0],
                                       option[i][1],
                                       option[i][2])
    # 2.构建本底函数
    if(backfunction == 'd1polynomial'):
        backpdf = ROOT.RooPolynomial('backpdf', 'backpdf',
                                     mass,
                                     ROOT.RooArgList(parameter['p0']))
    elif(backfunction == 'd2polynomial'):
        backpdf = ROOT.RooPolynomial('backpdf', 'backpdf',
                                     mass,
                                     ROOT.RooArgList(parameter['p0'],
                                                     parameter['p1']))
    elif(backfunction == 'd3polynomial'):
        backpdf = ROOT.RooPolynomial('backpdf', 'backpdf',
                                     mass,
                                     ROOT.RooArgList(parameter['p0'],
                                                     parameter['p1'],
                                                     parameter['p2']))
    else:
        print('输入了错误的本底函数形式')
    # 3.构建信号函数
    histm = ROOT.RooDataHist('histm', 'histm',
                             ROOT.RooArgList(mass),
                             datam)
    if(signfunction == 'None'):
        signpdf = ROOT.RooHistPdf('signpdf', 'signpdf',
                                  ROOT.RooArgSet(mass),
                                  histm,
                                  1)
    if(signfunction == 'evolution'):
        mcpdf = ROOT.RooHistPdf('signpdf', 'signpdf',
                                ROOT.RooArgSet(mass),
                                histm,
                                1)
        gauss = ROOT.RooGaussian('gauss', 'gauss',
                                 mass,
                                 parameter['gmean'],
                                 parameter['gsigm'])
        signpdf = ROOT.RooFFTConvPdf('signpdf', 'signpdf',
                                     mass,
                                     mcpdf,
                                     gauss)
    # 3.构建总函数
    allpdf = ROOT.RooAddPdf('allpdf', 'allpdf',
                            ROOT.RooArgList(signpdf, backpdf),
                            ROOT.RooArgList(parameter['npdf1'],
                                            parameter['npdf2']))
    # 3.输入真实数据
    # 4.拟合
    realpdf = ROOT.RooDataSet('datar', 'datar',
                              datar,
                              ROOT.RooArgSet(ROOT.RooArgList(mass)))
    fitresult = allpdf.fitTo(realpdf, ROOT.RooFit.Save())
    # 5.输出数据
    output = {}
    output['nevent'] = parameter['npdf1'].getVal()
    output['enevent'] = parameter['npdf1'].getError()
    # 5.输出图片
    if(len(pictures) != 0):
        massframe = mass.frame()
        realpdf.plotOn(massframe)
        allpdf.plotOn(massframe)
        allpdf.plotOn(massframe, ROOT.RooFit.Components('backpdf'),
                      ROOT.RooFit.LineStyle(ROOT.kDashed),
                      ROOT.RooFit.LineColor(ROOT.kRed))
        cvs = ROOT.TCanvas('canvas', '', 1200, 900)
        cvs.SetFillColor(10)
        cvs.SetFrameLineWidth(2)
        cvs.SetTickx()
        cvs.SetTicky()
        massframe.SetTitle('')
        massframe.GetXaxis().SetTitle(picture_xtitle)
        massframe.GetXaxis().SetTitleSize(0.05)
        massframe.GetXaxis().SetTitleOffset(0.9)
        massframe.GetXaxis().CenterTitle()
        massframe.GetXaxis().SetNdivisions(505)
        massframe.GetYaxis().SetTitle(picture_ytitle)
        massframe.GetYaxis().SetTitleSize(0.05)
        massframe.GetYaxis().SetTitleOffset(0.9)
        massframe.GetYaxis().CenterTitle()
        massframe.Draw()
        pt = ROOT.TPaveText(0.60, 0.60, 0.85, 0.85, 'BRNDC')
        pt.SetBorderSize(0)
        pt.SetTextAlign(12)
        pt.SetTextColor(1)
        pt.SetTextSize(0.05)
        pt.AddText('Energy: %1.4f GeV' % (energy))
        pt.AddText('Sig: ' + str(round(parameter['npdf1'].getVal(), 1)) +
                   '#pm' + str(round(parameter['npdf1'].getError(), 1)))
        pt.AddText('Bkg:  ' + str(round(parameter['npdf2'].getVal(), 1)) +
                   '#pm' + str(round(parameter['npdf2'].getError(), 1)))
        pt.Draw()
        if(picture_stop != ''):
            input()
        for i in pictures:
            cvs.Print(i)
    del tfilem
    del tfiler
    del datar
    del datam
    return output
