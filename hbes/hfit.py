# -*- coding: UTF-8 -*-
'''
This is a package document.

    Environment version:

        python2

    Content:

        @dodump:
        @dofit:
        @fit:
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
import headpy.hbes.htree as htree
import headpy.hbes.hsci as hsci
import headpy.hfile.hpickle as hpickle


def getchose(result):
    nevent = []
    for i in range(9):
        nevent.append(result[i]['nevent'])
    average = 0
    for i in range(9):
        average += nevent[i]
    average = average / 9
    chi = 1000
    chosei = 1000
    for i in range(9):
        thischi = abs(average - nevent[i])
        if(thischi < chi):
            chi = thischi
            chosei = i
    return chosei


def dodump(energy=0,
           tree='',
           read=[],
           cuts=[],
           datar='real',
           datam='omeganpw',
           branch='momega',
           docuts=[]):
    '''
    energy: double, 输入能量点\n
    tree: string, 输入tree的名字\n
    read: list, 输入要读取的文件的名字\n
    cuts: dict, 输入变量的参数cut\n
    datar: string, 在read中，对应真实数据的名字\n
    datam: string, 在read中，对应真实数据的名字\n
    branch: string, 目标变量的名字\n
    docuts: list, 输入要进行cut的变量\n
    作用：\n
    将对应能量点的数据，经过cut后，输出到temp文件夹，并返回查询信息\n
    格式为{'r':[file,name],'m':[file,name]}\n
    '''
    trees = htree.tree_read(energy=energy,
                            tree=tree,
                            read=read)
    massages = htree.massage_read()
    alldata = hsci.ALLDATA(trees, cuts, massages)
    histr = alldata.tree1d(data=datar,
                           branch=branch,
                           docuts=docuts,
                           name='real')
    histm = alldata.hist1d(data=datam,
                           branch=branch,
                           docuts=docuts,
                           name='mc')
    hist = {}
    hist['r'] = histr
    hist['m'] = histm
    return hist


def dofit(energy=0,
          histpkl='',
          optionpkl='',
          datasetpkl='',
          backfunction='',
          signfunction='',
          picture=''):
    '''
    histpkl为字符，输入存储数据的文件信息，格式为{'r':[file,name],'m':[file,name]}\n
    optionpkl为字符，输入存储初始参数的信息\n
    datasetpkl为字符，输入横坐标的信息，格式为{'name':,'mass':,'cut':}\n
    backfunciont为字符，输入本底函数形式[d1polynomial,d2polynomial,d3polynomial]\n
    signfunction为字符，输入信号函数形式[None,evolution]\n
    outputpkl为字符，如果不为空，则输入输出数据信息的文件位置\n
    picture为字符，如果不为空，则输入输出图片的文件位置\n
    作用1：根据输入参数进行一次拟合\n
    作用2：输出拟合的数值结果\n
    作用3：输出拟合的图片文件\n
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
    mass = ROOT.RooRealVar(dataset['name'], dataset['name'],
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
    realpdf = ROOT.RooDataSet('datar', 'datar',
                              datar,
                              ROOT.RooArgSet(ROOT.RooArgList(mass)))
    # 4.拟合
    allpdf.fitTo(realpdf)
    output = {}
    output['nevent'] = parameter['npdf1'].getVal()
    output['enevent'] = parameter['npdf1'].getError()
    # 5.输出图片
    if(picture != ''):
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
        cvs.Print(picture)
    del tfilem
    del tfiler
    del datar
    del datam
    return output


def fit(energy=0,
        tree='',
        read=[],
        cuts=[],
        datar='',
        datam='',
        branch='',
        docuts=[],
        tempfolder='',
        projectname='',
        option_list='',
        backfunction='',
        signfunction='',
        picture=''):
    '''
    '''
    # 写入前两个缓存文件
    hist = dodump(energy,
                  tree,
                  read,
                  cuts,
                  datar,
                  datam,
                  branch,
                  docuts)
    histpkl = '%s/%s/temphist.pkl' % (tempfolder, projectname)
    optionpkl = '%s/%s/tempoption.pkl' % (tempfolder, projectname)
    datasetpkl = '%s/%s/tempdataset.pkl' % (tempfolder, projectname)
    with open(histpkl, 'wb') as outfile:
        pickle.dump(hist, outfile)
    dataset = {}
    dataset['name'] = branch
    dataset['mass'] = cuts[branch]['mass']
    dataset['cut'] = cuts[branch]['cut']
    with open(datasetpkl, 'wb') as outfile:
        pickle.dump(dataset, outfile)
    # 开始进行多次拟合
    check = 0
    result = {}
    for count in range(1000):
        if(check > 8):
            continue
        # 写入最后一个缓存文件
        option = {}
        for i in option_list:
            option[i] = [random.random()
                         * (option_list[i][1] - option_list[i][0])
                         + option_list[i][0],
                         option_list[i][2],
                         option_list[i][3]]
        with open(optionpkl, 'wb') as outfile:
            pickle.dump(option, outfile)
        # 开始运行拟合，并提取log文件
        os.system('python2 /afs/ihep.ac.cn/users/l/leizh/myscript/dofit.py %s/%s %s %s %s| tee %s/%s/tempfit.log' % (tempfolder, projectname,
                                                                                                                     backfunction,
                                                                                                                     signfunction,
                                                                                                                     '%1.4f' % (energy),
                                                                                                                     tempfolder, projectname))
        with open('%s/%s/tempfit.log' % (tempfolder, projectname), 'r') as infile:
            log = infile.read()
            checklist = re.compile(r'STATUS=(.*) ').findall(log)
            checkok = 0
            print(checklist)
            for status in checklist:
                checkok = 0
                if(re.search(r'OK', status)):
                    checkok = 1
        if(checkok == 1):
            # 判断一次拟合成功
            hprint.pstar()
            hprint.ppoint('%1.4f Fit' % (energy), 'run %d times' % (count))
            hprint.ppoint('%1.4f Fit' % (energy), 'success %d times' % (check + 1))
            hprint.pstar()
            # 转移log文件
            os.system('mv %s/%s/tempfit.log %s/%s/%1.4f_%d.log' % (tempfolder, projectname,
                                                                   tempfolder, projectname,
                                                                   energy,
                                                                   check))
            # 将option写入result
            result[check] = {}
            result[check]['option'] = option
            outputcheck = dofit(energy,
                                histpkl,
                                optionpkl,
                                datasetpkl,
                                backfunction,
                                signfunction)
            result[check]['nevent'] = outputcheck['nevent']
            check += 1
        else:
            # 判断一次拟合不成功
            hprint.pstar()
            hprint.ppoint('%1.4f not Fit' % (energy), 'run %d times' % (count))
            hprint.ppoint('%1.4f not Fit' % (energy), 'success %d times' % (check + 1))
            hprint.pstar()
    # 得到最优结果的编号
    chosei = getchose(result)
    # 保存最优结果log
    os.system('mv %s/%s/%1.4f_%d.log %s/%s/%1.4f.log' % (tempfolder, projectname,
                                                         energy,
                                                         check,
                                                         tempfolder, projectname,
                                                         energy))
    os.system('rm %s/%s/*_*.log' % (tempfolder, projectname))
    option = result[chosei]['option']
    # 绘图最优结果
    with open(optionpkl, 'wb') as outfile:
        pickle.dump(option, outfile)
    output = dofit(energy,
                   histpkl,
                   optionpkl,
                   datasetpkl,
                   backfunction,
                   signfunction,
                   picture=picture)
    return output
