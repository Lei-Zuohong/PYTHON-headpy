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
