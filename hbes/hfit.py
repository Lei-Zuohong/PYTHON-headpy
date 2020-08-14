# -*- coding: UTF-8 -*-
'''
This is a package document.

    Environment version:

        python2

    Content:

'''
# Public pack
import pickle
import random
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
             read=[],
             selecters={},
             datar='real',
             datam='omeganpw',
             branch='momega',
             docuts=[],
             doweight='yes'):
    '''
    energy: 能量点\n
    tree: tree的名字\n
    read: 输入要读取名字列表\n
    datar: 在read中，对应真实数据的名字\n
    datam: 在read中，对应真实数据的名字\n
    selecters: 变量参数数组\n
    branch: 横坐标变量\n
    docuts: 输入要进行cut的变量\n
    doweight：蒙卡是否加权
    作用：\n
    将对应能量点的数据，经过cut后，输出到temp文件夹，并返回查询信息\n
    格式为{'r':[file,name],'m':[file,name]}\n
    '''
    massages = hnew.massage_read()
    trees = hnew.trees_read(energy=energy,
                            tree=tree,
                            read=read)
    alldata = hnew.ALLDATA(trees=trees,
                           selecters=selecters,
                           massages=massages)
    '''
    alldata.get_weight(data='omeganpw',
                       energy=energy,
                       name_weight='momegapi02_mpi02pi03',
                       name_branch='wpi02_pi02pi03',
                       dimension=2)
    '''
    alldata.get_weight(data='pppmpz',
                       energy=energy,
                       name_weight='pipm_m_pipz_m',
                       name_branch='pipmpipz',
                       dimension=2)
    histr1, histr2 = alldata.tree(data=datar,
                                  branch=branch,
                                  docuts=docuts,
                                  name='fit_real')
    '''
    histm1, histm2 = alldata.hist(data=datam,
                                  branchs=[branch],
                                  docuts=docuts,
                                  name='fit_mc',
                                  doweight=['wpi02_pi02pi03'])
    '''
    histm1, histm2 = alldata.hist(data=datam,
                                  branchs=[branch],
                                  docuts=docuts,
                                  name='fit_mc',
                                  doweight=['pipmpipz'])
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
                  result='',
                  toy_option='',
                  toy_data=0):
    '''
    histpkl         输入存储数据的文件信息，格式为{'r':[file,name],'m':[file,name]}\n
    optionpkl       输入存储初始参数的信息\n
    datasetpkl      输入横坐标的信息，格式为{'name':,'mass':,'cut':}\n
    backfunciont    输入本底函数形式[d1polynomial,d2polynomial,d3polynomial]\n
    signfunction    输入信号函数形式[None,evolution]\n
    outputpkl       不为空，则输入，输出数据信息的文件位置\n
    picture         不为空，则输入，输出图片的文件位置\n
    result          
    toy_option      取'toy_option'，则使用toy_data拟合\n
    toy_data        替换data sample进行拟合
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
    if(toy_option != 'toy_fit'):
        realpdf = ROOT.RooDataSet('datar', 'datar',
                                  datar,
                                  ROOT.RooArgSet(ROOT.RooArgList(mass)))
        fitresult = allpdf.fitTo(realpdf, ROOT.RooFit.Save())
    # sp.是否toymc拟合
    if(toy_option == 'toy_fit'):
        realpdf = replace_roodataset
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
        massframe.GetXaxis().SetTitle(r'm(#pi^{+}#pi^{-}#pi^{0})')
        massframe.GetXaxis().SetTitleSize(0.05)
        massframe.GetXaxis().SetTitleOffset(0.9)
        massframe.GetXaxis().CenterTitle()
        massframe.GetXaxis().SetNdivisions(505)
        massframe.GetYaxis().SetTitle(r'M_{#pi^{+}#pi^{-}#pi^{0}}(GeV/c^{2})')
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
    if(toy_option == 'toy_return'):
        output = allpdf.generate(ROOT.RooArgSet(ROOT.RooArgList(mass)),
                                 (parameter['npdf1'].getVal() + parameter['npdf2'].getVal()))
    return output


def dofit_sample(energy=0,
                 tree='',
                 read=[],
                 selecters={},
                 datar='real',
                 datam='omeganpw',
                 branch='momega',
                 docuts=[],
                 doweight='yes',
                 tempfolder='',
                 projectname='',
                 scriptname='',
                 option_list={},
                 backfunction='',
                 signfunction='',
                 num=100):
    # 1.1 得到缓存文件地址
    histpkl = '%s/%s/temphist.pkl' % (tempfolder, projectname)
    optionpkl = '%s/%s/tempoption.pkl' % (tempfolder, projectname)
    datasetpkl = '%s/%s/tempdataset.pkl' % (tempfolder, projectname)
    # 1.2 输入数据缓存文件
    hist = fit_dump(energy=energy,
                    tree=tree,
                    read=read,
                    selecters=selecters,
                    datar=datar,
                    datam=datam,
                    branch=branch,
                    docuts=docuts,
                    doweight=doweight)
    hpickle.pkl_dump(histpkl, hist)
    # 1.3 输入坐标轴缓存文件
    dataset = {}
    dataset['name'] = branch
    dataset['mass'] = selecters[branch].center
    dataset['cut'] = selecters[branch].width
    hpickle.pkl_dump(datasetpkl, dataset)
    # 2. 开始进行多次拟合
    check = 0
    result = {}
    for count in range(100 * num):
        if(check > num - 1):
            continue
        # 1. 输入初始值缓存文件
        option = {}
        for i in option_list:
            option[i] = [random.random()
                         * (option_list[i][1] - option_list[i][0])
                         + option_list[i][0],
                         option_list[i][2],
                         option_list[i][3]]
        hpickle.pkl_dump(optionpkl, option)
        # 2.1. 开始运行拟合，并提取log文件
        command1 = 'python2'
        command2 = scriptname
        argv1 = '%s/%s' % (tempfolder, projectname)
        argv2 = backfunction
        argv3 = signfunction
        argv4 = '%1.4f' % (energy)
        tee1 = 'tee'
        tee2 = '%s/%s/tempfit.log' % (tempfolder, projectname)
        os.system('%s %s %s %s %s %s| %s %s' % (command1,
                                                command2,
                                                argv1,
                                                argv2,
                                                argv3,
                                                argv4,
                                                tee1,
                                                tee2))
        checkok = fit_checkok(tee2)
        if(checkok == 1):
            # 判断一次拟合成功
            hprint.pstar()
            hprint.ppoint('%1.4f Fit' % (energy), 'run %d times' % (count + 1))
            hprint.ppoint('%1.4f Fit' % (energy), 'success %d times' % (check))
            hprint.pstar()
            # 转移log文件
            os.system('mv %s/%s/tempfit.log %s/%s/%1.4f_%d.log' % (tempfolder, projectname,
                                                                   tempfolder, projectname,
                                                                   energy,
                                                                   check))
            # 将option写入result
            result[check] = {}
            result[check]['option'] = option
            outputcheck = dofit_method1(energy,
                                        histpkl,
                                        optionpkl,
                                        datasetpkl,
                                        backfunction,
                                        signfunction,
                                        result='yes')
            result[check]['result'] = outputcheck
            check += 1
        else:
            # 判断一次拟合不成功
            hprint.pstar()
            hprint.ppoint('%1.4f not Fit' % (energy), 'run %d times' % (count + 1))
            hprint.ppoint('%1.4f not Fit' % (energy), 'success %d times' % (check))
            hprint.pstar()
    return result
