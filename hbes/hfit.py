# -*- coding: UTF-8 -*-
# Public pack
import os
import re
import copy
import random
# Private pack
import ROOT
import headpy.hfile as hfile
import headpy.hbes.hnew as hnew
import headpy.hscreen.hprint as hprint


def fit_checkok(filename, do_print=''):
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


def dofit(**argv):
    # region 打开root
    namef = argv['namef']
    nameh = argv['nameh']
    tfile = {}
    thist = {}
    for i in namef:
        tfile[i] = ROOT.TFile(namef[i])
        thist[i] = tfile[i].Get(nameh[i])
    # endregion
    # region 打开参数
    parameters = argv['parameters']
    selecters = argv['selecters']
    branch = argv['branch']
    backfunction = argv['backfunction']
    signfunction = argv['signfunction']
    pictures = argv['pictures']
    # endregion
    # region 构建变量参数
    used_parameter = []
    mass = ROOT.RooRealVar(branch, branch,
                           selecters[branch].left_show,
                           selecters[branch].right_show)
    # endregion
    # region 构建拟合参数
    parameter = {}
    for i in parameters:
        parameter[i] = ROOT.RooRealVar(i, i,
                                       parameters[i]['init'],
                                       parameters[i]['left'],
                                       parameters[i]['right'])
    # endregion
    # region 构建本底函数
    if(backfunction == 'd1polynomial'):
        backpdf = ROOT.RooPolynomial('backpdf', 'backpdf',
                                     mass,
                                     ROOT.RooArgList(parameter['p0']))
        used_parameter.append('p0')
    elif(backfunction == 'd2polynomial'):
        backpdf = ROOT.RooPolynomial('backpdf', 'backpdf',
                                     mass,
                                     ROOT.RooArgList(parameter['p0'],
                                                     parameter['p1']))
        used_parameter.append('p0')
        used_parameter.append('p1')
    elif(backfunction == 'd3polynomial'):
        backpdf = ROOT.RooPolynomial('backpdf', 'backpdf',
                                     mass,
                                     ROOT.RooArgList(parameter['p0'],
                                                     parameter['p1'],
                                                     parameter['p2']))
        used_parameter.append('p0')
        used_parameter.append('p1')
        used_parameter.append('p2')
    else:
        print('输入了错误的本底函数形式')
    # endregion
    # region 构建信号函数
    histm = ROOT.RooDataHist('histm', 'histm',
                             ROOT.RooArgList(mass),
                             thist['m'])
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
        used_parameter.append('gmean')
        used_parameter.append('gsigm')
    # endregion
    # region 构建总函数
    allpdf = ROOT.RooAddPdf('allpdf', 'allpdf',
                            ROOT.RooArgList(signpdf, backpdf),
                            ROOT.RooArgList(parameter['npdf1'],
                                            parameter['npdf2']))
    used_parameter.append('npdf1')
    used_parameter.append('npdf2')
    # endregion
    # region 拟合
    realpdf = ROOT.RooDataSet('datar', 'datar',
                              thist['r'],
                              ROOT.RooArgSet(ROOT.RooArgList(mass)))
    fitresult = allpdf.fitTo(realpdf, ROOT.RooFit.Save())
    output = {}
    output['nevent'] = parameter['npdf1'].getVal()
    output['enevent'] = parameter['npdf1'].getError()
    for i in used_parameter:
        output[i] = parameter[i].getVal()
        output[i + 'e'] = parameter[i].getError()
    # endregion
    # region 作图
    if(len(pictures) != 0):
        picture_xtitle = argv['picture_xtitle']
        picture_ytitle = argv['picture_ytitle']
        picture_energy = argv['energy']
        picture_stop = argv['picture_stop']
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
        pt.SetFillColor(10)
        pt.SetBorderSize(0)
        pt.SetTextAlign(12)
        pt.SetTextColor(1)
        pt.SetTextSize(0.04)
        pt.AddText('Energy: %1.4f GeV' % (picture_energy))
        pt.AddText('Sig: %.1f #pm %.1f' % (parameter['npdf1'].getVal(), parameter['npdf1'].getError()))
        pt.AddText('Bkg: %.1f #pm %.1f' % (parameter['npdf2'].getVal(), parameter['npdf2'].getError()))
        pt.Draw()
        if(picture_stop != ''):
            input()
        for i in pictures:
            cvs.Print(i)
    # endregion
    del thist
    del tfile
    if('output_pkl' in argv):
        hfile.pkl_dump(argv['output_pkl'], output)
    return output


class MYFIT():
    def __init__(self):
        self.path_temp = ''

        self.namef = []
        self.nameh = []

        self.script = ''

    def set_parameters(self, parameters):
        self.parameters = copy.deepcopy(parameters)

    def set_best_parameters(self, best_parameters):
        self.best_parameters = copy.deepcopy(best_parameters)

    def do_dump(self, func_dump, **argv):
        self.namef, self.nameh = func_dump(**argv)

    def do_fit_spread(self, **argv):
        # 设定ROOT文件
        argv['namef'] = self.namef
        argv['nameh'] = self.nameh
        # 设定spread序列
        record_nevent = []
        record_parameters = []
        record_output = []
        # 循环拟合
        count1 = 0
        count2 = 0
        while(count1 < argv['spread_times']):
            hprint.pstar()
            hprint.ppoint('Fitting success: ', '%d' % (count1))
            hprint.ppoint('Fitting times:   ', '%d' % (count2))
            hprint.ppoint('Fitting target:  ', '%d' % (argv['spread_times']))
            hprint.pstar()
            parameters_spread = copy.deepcopy(self.parameters)
            for i in self.parameters:
                parameters_spread[i]['init'] = random.uniform(parameters_spread[i]['left_init'], parameters_spread[i]['right_init'])
            argv['parameters'] = parameters_spread
            argv['output_pkl'] = '%s/%s.pkl' % (self.path_temp, 'temp_output')
            hfile.pkl_dump('%s/%s.pkl' % (self.path_temp, 'temp_argv'), argv)
            os.system('python2 %s %s | tee %s' % (self.script,
                                                  '%s/%s.pkl' % (self.path_temp, 'temp_argv'),
                                                  '%s/%s.txt' % (self.path_temp, 'temp_log')))
            checkok = fit_checkok('%s/%s.txt' % (self.path_temp, 'temp_log'))
            if(checkok):
                fit_data = hfile.pkl_read('%s/%s.pkl' % (self.path_temp, 'temp_output'))
                record_nevent.append(fit_data['nevent'])
                record_parameters.append(parameters_spread)
                record_output.append(fit_data)
                count1 += 1
            count2 += 1
        # 统计spread序列
        sum = 0
        for i in range(argv['spread_times']):
            sum += record_nevent[i]
        sum = sum / argv['spread_times']
        # 选择spread序列
        use_i = -1
        use_dif = 99999
        for i in range(argv['spread_times']):
            if(abs(sum - record_nevent[i]) < use_dif):
                use_i = i
                use_dif = abs(sum - record_nevent[i])
        # 储存拟合结果
        self.best_parameters = record_parameters[use_i]
        self.best_output = record_output[use_i]
        # 返回拟合结果
        return record_output[use_i]

    def do_fit_plot(self, **argv):
        if(hasattr(self, 'best_parameters')):
            print('')
        else:
            print('Info from hfit.MYFIT.do_fit_plot: Have not done fit_spread yet!!!')
            exit(0)
        # 设定ROOT文件
        argv['parameters'] = self.best_parameters
        argv['namef'] = self.namef
        argv['nameh'] = self.nameh
        output = argv['func_fit'](**argv)
        return output
