# -*- coding: UTF-8 -*-
'''
This is a package document.

    Environment version:
        python2
        screen.hprint
    
    MyDataset:
        @__init__():
        @cuttree():
        @hist1d():
        @hist2d():
        @hist2d2():
        @xtitle():
        @ytitle():
        @histtopo():

    Content:
        @getmassage():
	    @getroot():
        @gettopo():
'''
# Public pack
import re
import os
import pickle
# Private pack
import ROOT
import headpy.besiii.homega as ana
import headpy.screen.hprint as hprint


#########################################
#                                       #
#       section 1: set class option     #
#                                       #
#########################################


class MyDataset:
    '请使用 hist["r"]["m"]["p"]["b"], topotlogy="" 来初始化该类'
    momega = {'m': 0.782,
              'c': 0.782,
              'r': 0.15,
              'i': 60,
              's': r'M_{#pi^{+}#pi^{-}#pi^{0}}(GeV/c^{2})'}
    mpi01 = {'m': 0.135,
             'c': 0.015,
             'r': 0.045,
             'i': 90,
             's': r'M_{#pi_{1}^{0}}(GeV/c^{2})',
             'shift': 0}
    mpi02 = {'m': 0.135,
             'c': 0.015,
             'r': 0.045,
             'i': 90,
             's': r'M_{#pi_{2}^{0}}(GeV/c^{2})',
             'shift': 0}
    mpi03 = {'m': 0.135,
             'c': 0.015,
             'r': 0.045,
             'i': 90,
             's': r'M_{#pi_{3}^{0}}(GeV/c^{2})',
             'shift': 0}
    chisq = {'m': 100,
             'c': 100,
             'r': 100,
             'i': 100,
             's': r'#chi_{#pi^{+}#pi^{-}6#gamma}^{2}'}
    mpi02pi03 = {'m': 0.800,
                 'c': 0.800,
                 'r': 0.800,
                 'i': 160,
                 's': r'M_{#pi_{2}^{0}#pi_{3}^{0}}(GeV/c^{2})'}
    momegapi02 = {'m': 1.5,
                  'c': 1.5,
                  'r': 0.8,
                  'i': 160,
                  's': r'M_{#omega#pi_{2}^{0}}(GeV/c^{2})'}
    momegapi03 = {'m': 1.5,
                  'c': 1.5,
                  'r': 0.8,
                  'i': 160,
                  's': r'M_{#omega#pi_{3}^{0}}(GeV/c^{2})'}
    momega['dc'] = 0
    mpi01['dc'] = 1
    mpi02['dc'] = 1
    mpi03['dc'] = 1
    chisq['dc'] = 1

    def __init__(self, rootlist, topology='none'):
        '初始化数据列'
        self.rootlist = rootlist
        self.topology = topology

    def cuttree(self, data, tree):
        '获得Cut以后的tree'
        if(1 == 1):  # 是否输出信息
            hprint.pline('Extracting New Tree ......')
            hprint.ppoint('Data source', data)
            hprint.ppoint('Tree name', tree)
            if(self.chisq['dc'] == 1):
                hprint.ppoint('Cut range for chisq', self.chisq['c'])
            else:
                hprint.ppoint('Cut range for chisq', 'No cut')
            if(self.mpi01['dc'] == 1):
                hprint.ppoint('Cut range for mpi01', self.mpi01['c'])
            else:
                hprint.ppoint('Cut range for mpi01', 'No cut')
            if(self.mpi02['dc'] == 1):
                hprint.ppoint('Cut range for mpi02', self.mpi02['c'])
            else:
                hprint.ppoint('Cut range for mpi02', 'No cut')
            if(self.mpi03['dc'] == 1):
                hprint.ppoint('Cut range for mpi03', self.mpi03['c'])
            else:
                hprint.ppoint('Cut range for mpi03', 'No cut')
            if(self.momega['dc'] == 1):
                hprint.ppoint('Cut range for momega', self.momega['c'])
            else:
                hprint.ppoint('Cut range for momega', 'No cut')
            hprint.pstar()
        # get tree
        ttree = self.rootlist[data].Get(tree)
        ntree = ttree.CloneTree(0)
        num = ttree.GetEntries()
        # fill hist
        for i in range(num):
            ttree.GetEntry(i)
            if(self.chisq['dc']*ttree.chisq < self.chisq['c'] and
               self.momega['dc']*abs(ttree.momega-self.momega['m']) < self.momega['c'] and
               self.mpi01['dc']*abs(ttree.mpi01-(self.mpi01['m'] + self.mpi01['shift'])) < self.mpi01['c'] and
               self.mpi02['dc']*abs(ttree.mpi02-(self.mpi02['m'] + self.mpi02['shift'])) < self.mpi02['c'] and
               self.mpi03['dc']*abs(ttree.mpi03-(self.mpi03['m'] + self.mpi03['shift'])) < self.mpi03['c']):
                ntree.Fill()
        return ntree

    def hist1d(self, data, tree, name, branch):
        '获得TH1D histogram'
        if(1 == 1):  # 是否输出信息
            hprint.pline('Extracting TH1D ......')
            hprint.ppoint('Data source', data)
            hprint.ppoint('Tree name', tree)
            hprint.ppoint('Branch name', branch)
            if(self.chisq['dc'] == 1):
                hprint.ppoint('Cut range for chisq', self.chisq['c'])
            else:
                hprint.ppoint('Cut range for chisq', 'No cut')
            if(self.mpi01['dc'] == 1):
                hprint.ppoint('Cut range for mpi01', self.mpi01['c'])
            else:
                hprint.ppoint('Cut range for mpi01', 'No cut')
            if(self.mpi02['dc'] == 1):
                hprint.ppoint('Cut range for mpi02', self.mpi02['c'])
            else:
                hprint.ppoint('Cut range for mpi02', 'No cut')
            if(self.mpi03['dc'] == 1):
                hprint.ppoint('Cut range for mpi03', self.mpi03['c'])
            else:
                hprint.ppoint('Cut range for mpi03', 'No cut')
            if(self.momega['dc'] == 1):
                hprint.ppoint('Cut range for momega', self.momega['c'])
            else:
                hprint.ppoint('Cut range for momega', 'No cut')
        # get tree
        ttree = self.rootlist[data].Get(tree)
        num = ttree.GetEntries()
        # get hist
        inter = 0
        left = 0
        right = 0
        exec("inter = self.%s['i']" % (branch))
        exec("left = self.%s['m'] - self.%s['r']" % (branch, branch))
        exec("right = self.%s['m'] + self.%s['r']" % (branch, branch))
        histout = ROOT.TH1D('%s_%s_%s_%s' %
                            (name, data, tree, branch), '', inter, left, right)
        # fill hist
        for i in range(num):
            ttree.GetEntry(i)
            if(self.chisq['dc']*ttree.chisq < self.chisq['c'] and
               self.momega['dc']*abs(ttree.momega-self.momega['m']) < self.momega['c'] and
               self.mpi01['dc']*abs(ttree.mpi01-(self.mpi01['m'] + self.mpi01['shift'])) < self.mpi01['c'] and
               self.mpi02['dc']*abs(ttree.mpi02-(self.mpi02['m'] + self.mpi02['shift'])) < self.mpi02['c'] and
               self.mpi03['dc']*abs(ttree.mpi03-(self.mpi03['m'] + self.mpi03['shift'])) < self.mpi03['c']):
                exec("histout.Fill(ttree.%s)" % (branch))
        hprint.ppoint('Number', histout.GetEntries())
        hprint.pstar()
        return histout

    def hist2d(self, data, tree, name, branch1, branch2):
        '获得TH2D histogram'
        if(1 == 1):  # 是否输出信息
            hprint.pline('Extracting TH2D ......')
            hprint.ppoint('Data source', data)
            hprint.ppoint('Tree', tree)
            hprint.ppoint('Branch 1', branch1)
            hprint.ppoint('Branch 2', branch2)
            if(self.chisq['dc'] == 1):
                hprint.ppoint('Cut range for chisq', self.chisq['c'])
            else:
                hprint.ppoint('Cut range for chisq', 'No cut')
            if(self.mpi01['dc'] == 1):
                hprint.ppoint('Cut range for mpi01', self.mpi01['c'])
            else:
                hprint.ppoint('Cut range for mpi01', 'No cut')
            if(self.mpi02['dc'] == 1):
                hprint.ppoint('Cut range for mpi02', self.mpi02['c'])
            else:
                hprint.ppoint('Cut range for mpi02', 'No cut')
            if(self.mpi03['dc'] == 1):
                hprint.ppoint('Cut range for mpi03', self.mpi03['c'])
            else:
                hprint.ppoint('Cut range for mpi03', 'No cut')
            if(self.momega['dc'] == 1):
                hprint.ppoint('Cut range for momega', self.momega['c'])
            else:
                hprint.ppoint('Cut range for momega', 'No cut')
        # get tree
        ttree = self.rootlist[data].Get(tree)
        num = ttree.GetEntries()
        # get hist
        inter1 = 0
        left1 = 0
        right1 = 0
        exec("inter1 = self.%s['i']" % (branch1))
        exec("left1 = self.%s['m'] - self.%s['r']" % (branch1, branch1))
        exec("right1 = self.%s['m'] + self.%s['r']" % (branch1, branch1))
        inter2 = 0
        left2 = 0
        right2 = 0
        exec("inter2 = self.%s['i']" % (branch2))
        exec("left2 = self.%s['m'] - self.%s['r']" % (branch2, branch2))
        exec("right2 = self.%s['m'] + self.%s['r']" % (branch2, branch2))
        histout = ROOT.TH2D(name+'_'+data+'_'+tree+'_'+branch1+'_'+branch2, '',
                            inter1, left1, right1,
                            inter2, left2, right2)
        # fill hist
        for i in range(num):
            ttree.GetEntry(i)
            if(self.chisq['dc']*ttree.chisq < self.chisq['c'] and
               self.momega['dc']*abs(ttree.momega-self.momega['m']) < self.momega['c'] and
               self.mpi01['dc']*abs(ttree.mpi01-(self.mpi01['m'] + self.mpi01['shift'])) < self.mpi01['c'] and
               self.mpi02['dc']*abs(ttree.mpi02-(self.mpi02['m'] + self.mpi02['shift'])) < self.mpi02['c'] and
               self.mpi03['dc']*abs(ttree.mpi03-(self.mpi03['m'] + self.mpi03['shift'])) < self.mpi03['c']):
                exec('histout.Fill(ttree.%s,ttree.%s)' % (branch1, branch2))
        hprint.ppoint('Nummber', histout.GetEntries())
        hprint.pstar()
        return histout

    def hist2d2(self, data, tree, name, branch1, branch2):
        '获得TH1D+TH1D histogram'

        if(1 == 1):  # 是否输出信息
            hprint.pline('Extracting TH1D + TH1D ......')
            hprint.ppoint('Data source', data)
            hprint.ppoint('Tree', tree)
            hprint.ppoint('Branch 1', branch1)
            hprint.ppoint('Branch 2', branch2)
            if(self.chisq['dc'] == 1):
                hprint.ppoint('Cut range for chisq', self.chisq['c'])
            else:
                hprint.ppoint('Cut range for chisq', 'No cut')
            if(self.mpi01['dc'] == 1):
                hprint.ppoint('Cut range for mpi01', self.mpi01['c'])
            else:
                hprint.ppoint('Cut range for mpi01', 'No cut')
            if(self.mpi02['dc'] == 1):
                hprint.ppoint('Cut range for mpi02', self.mpi02['c'])
            else:
                hprint.ppoint('Cut range for mpi02', 'No cut')
            if(self.mpi03['dc'] == 1):
                hprint.ppoint('Cut range for mpi03', self.mpi03['c'])
            else:
                hprint.ppoint('Cut range for mpi03', 'No cut')
            if(self.momega['dc'] == 1):
                hprint.ppoint('Cut range for momega', self.momega['c'])
            else:
                hprint.ppoint('Cut range for momega', 'No cut')
            hprint.pstar()
        # get tree
        ttree = self.rootlist[data].Get(tree)
        num = ttree.GetEntries()
        # get hist
        inter1 = 0
        left1 = 0
        right1 = 0
        exec("inter1 = self.%s['i']" % (branch1))
        exec("left1 = self.%s['m'] - self.%s['r']" % (branch1, branch1))
        exec("right1 = self.%s['m'] + self.%s['r']" % (branch1, branch1))
        inter2 = 0
        left2 = 0
        right2 = 0
        exec("inter2 = self.%s['i']" % (branch2))
        exec("left2 = self.%s['m'] - self.%s['r']" % (branch2, branch2))
        exec("right2 = self.%s['m'] + self.%s['r']" % (branch2, branch2))
        histout = ROOT.TH2D(name+'_'+data+'_'+tree+'_'+branch1+'_'+branch2, '',
                            inter1, left1, right1,
                            inter2, left2, right2)
        # fill hist
        for i in range(num):
            ttree.GetEntry(i)
            if(self.chisq['dc']*ttree.chisq < self.chisq['c'] and
               self.momega['dc']*abs(ttree.momega-self.momega['m']) < self.momega['c'] and
               self.mpi01['dc']*abs(ttree.mpi01-(self.mpi01['m'] + self.mpi01['shift'])) < self.mpi01['c'] and
               self.mpi02['dc']*abs(ttree.mpi02-(self.mpi02['m'] + self.mpi02['shift'])) < self.mpi02['c'] and
               self.mpi03['dc']*abs(ttree.mpi03-(self.mpi03['m'] + self.mpi03['shift'])) < self.mpi03['c']):
                exec('histout.Fill(pow(ttree.%s,2),pow(ttree.%s,2))' %
                     (branch1, branch2))
        return histout

    def xtitle(self, branch):
        '得到branch的latex表达式'
        xt = ''
        exec("xt = xt + self.%s['s']" % (branch))
        return xt

    def ytitle(self, branch):
        '得到根据分bin的bin宽字符'
        bwr = 0
        bwi = 0
        exec("bwr = self.%s['r']" % (branch))
        exec("bwi = self.%s['i']" % (branch))
        bw = 'Events/%s(GeV/c^{2})' % (str(2*bwr/bwi))
        return bw

    def histtopo(self, tree, name, branch):
        '获得TH1D histograms for topology'
        # 输出信息
        if(1 == 1):
            hprint.pline('Extracting TH1D list for topology ......')
            hprint.ppoint('Data source', 'b')
            hprint.ppoint('Tree', tree)
            hprint.ppoint('Branch', branch)
            if(self.chisq['dc'] == 1):
                hprint.ppoint('Cut range for chisq', self.chisq['c'])
            else:
                hprint.ppoint('Cut range for chisq', 'No cut')
            if(self.mpi01['dc'] == 1):
                hprint.ppoint('Cut range for mpi01', self.mpi01['c'])
            else:
                hprint.ppoint('Cut range for mpi01', 'No cut')
            if(self.mpi02['dc'] == 1):
                hprint.ppoint('Cut range for mpi02', self.mpi02['c'])
            else:
                hprint.ppoint('Cut range for mpi02', 'No cut')
            if(self.mpi03['dc'] == 1):
                hprint.ppoint('Cut range for mpi03', self.mpi03['c'])
            else:
                hprint.ppoint('Cut range for mpi03', 'No cut')
            if(self.momega['dc'] == 1):
                hprint.ppoint('Cut range for momega', self.momega['c'])
            else:
                hprint.ppoint('Cut range for momega', 'No cut')
            hprint.pstar()
        # get tree
        ttree = self.rootlist['b'].Get(tree)
        num = ttree.GetEntries()
        # build output
        dataout_signal = []
        dataout_backa = []
        dataout_back = []
        dataout_backi = {}
        for i in self.topology['background']:
            dataout_backi[i] = []
        # read file
        for i1 in range(num):
            ttree.GetEntry(i1)
            if(self.chisq['dc']*ttree.chisq < self.chisq['c'] and
               self.momega['dc']*abs(ttree.momega-self.momega['m']) < self.momega['c'] and
               self.mpi01['dc']*abs(ttree.mpi01-(self.mpi01['m'] + self.mpi01['shift'])) < self.mpi01['c'] and
               self.mpi02['dc']*abs(ttree.mpi02-(self.mpi02['m'] + self.mpi02['shift'])) < self.mpi02['c'] and
               self.mpi03['dc']*abs(ttree.mpi03-(self.mpi03['m'] + self.mpi03['shift'])) < self.mpi03['c']):
                if(ttree.itopo in self.topology['signal']):
                    exec("dataout_signal.append(ttree.%s)" % (branch))
                elif(ttree.itopo in self.topology['background']):
                    for i in self.topology['background']:
                        if(ttree.itopo == i):
                            exec("dataout_back.append(ttree.%s)" % (branch))
                            exec(
                                "dataout_backi[i].append(ttree.%s)" % (branch))
                else:
                    exec("dataout_backa.append(ttree.%s)" % (branch))
                    exec("dataout_back.append(ttree.%s)" % (branch))
        # build TH1D
        inter = 0
        left = 0
        right = 0
        exec("inter = self.%s['i']" % (branch))
        exec("left = self.%s['m'] - self.%s['r']" % (branch, branch))
        exec("right = self.%s['m'] + self.%s['r']" % (branch, branch))
        histout_signal = ROOT.TH1D(
            name+'_'+tree+'_'+branch+'_'+'signal', '', inter, left, right)
        histout_backa = ROOT.TH1D(
            name+'_'+tree+'_'+branch+'_'+'backa', '', inter, left, right)
        histout_back = ROOT.TH1D(
            name+'_'+tree+'_'+branch+'_'+'back', '', inter, left, right)
        for i in dataout_signal:
            histout_signal.Fill(i)
        for i in dataout_backa:
            histout_backa.Fill(i)
        for i in dataout_back:
            histout_back.Fill(i)
        histout_backi = {}
        for i1 in dataout_backi:
            histout_backi[i1] = ROOT.TH1D(
                name+'_'+tree+'_'+branch+'_'+'%s' % (i1), '', inter, left, right)
            for i in dataout_backi[i1]:
                histout_backi[i1].Fill(i)
        histout = {'signal': histout_signal,
                   'backa': histout_backa,
                   'backi': histout_backi,
                   'back': histout_back}
        return histout


#########################################
#                                       #
#       section 2: read file            #
#                                       #
#########################################

def getmassage():
    '获取当前目录下massage.txt文件的内容'
    hprint.pstar()
    hprint.pline("Reading massage.txt ......")
    with open('massage.txt', 'r') as infile:
        lines = infile.readlines()
    massage = {}
    method = r'(.*):(.*)\r'
    for line in lines:
        check = re.match(method, line)
        if(check):
            massage[check.group(1)] = check.group(2)
    hprint.ppointbox(massage)
    return massage


def getroot(inenergy, intree, readr, readm, readp, readb):
    '获取real, mc, pwmc, back的TFile'
    # read location.txt
    massage = getmassage()
    hprint.pline('Reading TFile ......')
    # build root file name
    energy = inenergy
    filename_project_topo = '%1.4f_%s' % (energy, intree)
    filename_project = '%1.4f.root' % (energy)
    # build root file path
    filename_rootb = '%s/%s/topo.root' % (massage['b'],
                                          filename_project_topo)
    filename_rootr = '%s/%s' % (massage['r'],
                                filename_project)
    filename_rootm = '%s%s/%s' % (massage['m'],
                                  massage['version'],
                                  filename_project)
    filename_rootp = '%s%s/%s' % (massage['p'],
                                  massage['version'],
                                  filename_project)
    # build tree parameter
    output = {}
    if (readr == 1):
        rootr = ROOT.TFile(filename_rootr)
        output['r'] = rootr
        hprint.pline('Reading TFile for real')
    if (readm == 1):
        rootm = ROOT.TFile(filename_rootm)
        output['m'] = rootm
        hprint.pline('Reading TFile for mc')
    if (readp == 1):
        rootm = ROOT.TFile(filename_rootp)
        output['p'] = rootm
        hprint.pline('Reading TFile for pwmc')
    if (readb == 1):
        rootb = ROOT.TFile(filename_rootb)
        output['b'] = rootb
        hprint.pline('Reading TFile for background')
    hprint.pstar()
    return output


def gettopo(inenergy, intree, num):
    '获取Topology文件信息'
    # read location.txt
    massage = getmassage()
    # build root file name
    energy = inenergy
    filename_project_topo = '%1.4f_%s' % (energy, intree)
    # build tex file path
    tex_topology = '%s/%s/notice.tex' % (massage['b'],
                                         filename_project_topo)
    # read tex file
    with open(tex_topology, 'r') as infile:
        tex_content = infile.readlines()
    process_signal1 = r'$e^{+} e^{-} \rightarrow \omega f_{0}(980) ,\ \omega  \rightarrow \pi^{-} \pi^{0} \pi^{+} ,\ f_{0}(980)  \rightarrow \pi^{0} \pi^{0} \ $'
    process_signal2 = r'$e^{+} e^{-} \rightarrow \gamma_{ISR} \gamma^{\star},\ \gamma^{\star} \rightarrow \omega f_{0}(980) ,\ \omega  \rightarrow \pi^{-} \pi^{0} \pi^{+} ,\ f_{0}(980)  \rightarrow \pi^{0} \pi^{0} \ $'
    process_signal3 = r'$e^{+} e^{-} \rightarrow \gamma_{ISR} \gamma^{\star},\ \gamma^{\star} \rightarrow \pi^{0} b_{1}^{0} ,\ b_{1}^{0}  \rightarrow \pi^{0} \omega ,\ \omega  \rightarrow \pi^{-} \pi^{0} \pi^{+} \ $'
    process_signal4 = r'$e^{+} e^{-} \rightarrow \gamma_{ISR} \gamma^{\star},\ \gamma^{\star} \rightarrow \pi^{0} \pi^{0} \omega ,\ \omega  \rightarrow \pi^{-} \pi^{0} \pi^{+} \ $'
    # itopo = {itopo : process text}
    itopo_signal = {}
    itopo_background = {}
    method = r'([0-9]*)& (.*) & (.*) & (.*) & (.*) & (.*) \\'
    for line in tex_content:
        if(re.match(method, line)):
            if(re.match(method, line).group(2) == process_signal1):
                itopo_signal[int(re.match(method, line).group(
                    4))] = re.match(method, line).group(2)
            elif(re.match(method, line).group(2) == process_signal2):
                itopo_signal[int(re.match(method, line).group(
                    4))] = re.match(method, line).group(2)
            elif(re.match(method, line).group(2) == process_signal3):
                itopo_signal[int(re.match(method, line).group(
                    4))] = re.match(method, line).group(2)
            elif(re.match(method, line).group(2) == process_signal4):
                itopo_signal[int(re.match(method, line).group(
                    4))] = re.match(method, line).group(2)
            elif(int(re.match(method, line).group(1)) < num):
                itopo_background[int(re.match(method, line).group(
                    4))] = re.match(method, line).group(2).replace('\\', '#').replace('#star', '*').replace('# ', '').replace('$', '')
    topology = {}
    topology['signal'] = itopo_signal
    topology['background'] = itopo_background
    return topology
