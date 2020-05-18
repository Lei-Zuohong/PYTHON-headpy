# -*- coding: UTF-8 -*-
'''
This is a package document.
    
    Environment version:
        
        python2
        请在python2环境下运行程序
    
    Content:

        @root_dict:
            把root文件转换为字典对象
        @root_pkl:
            把root文件转换为pkl文件
        @dump:
            批量转换root文件为pkl文件
        @hist1d:
        @hist2d:
            转换数组为hist对象并保存
        @tree1d:
            转换数组为tree对象并保存

'''
# Public package
import pickle
import os
import re
from array import array
# Private package
import headpy.hscreen.hprint as hprint
import ROOT


def root_dict(rootfile='',
              tree='',
              branchs=[],
              fake=1):
    '''
    rootfile: string, 输入读取的root文件位置\n
    tree: string, 输入读取的tree的名称\n
    branchs: list, 输入要读取的branch的名称\n
    fake: double，输入调整处理长度的系数\n
    作用: 读取对应root文件中的对应tree，作为字典返回\n
    '''
    # 读取root文件
    tfile = ROOT.TFile(rootfile)
    ttree = tfile.Get(tree)
    num = ttree.GetEntries()
    # 初始化输出字典
    out_dict = {}
    for branch in branchs:
        out_dict[branch] = []
    # 输入字典
    nnum = int(num / fake)
    for entry in range(nnum):
        ttree.GetEntry(entry)
        for branch in branchs:
            exec("out_dict['%s'].append(ttree.%s)" % (branch, branch))
    # 输出字典
    return out_dict


def root_pkl(rootfile='',
             tree='',
             branchs=[],
             pklfile='',
             protocol=2,
             fake=1):
    '''
    rootfile: string, 输入读取的root文件位置\n
    tree: string, 输入读取的tree的名称\n
    branchs: list, 输入要读取的branch的名称\n
    pklfile: string, 输入输出的pkl文件位置\n
    fake: double, 输入调整处理长度的系数\n
    作用: 读取对应root文件中的对应tree，作为字典返回\n
    '''
    # 读取root至dict
    out_dict = root_dict(rootfile, tree, branchs, fake=fake)
    # 写入pickle文件
    with open(pklfile, 'wb') as outfile:
        pickle.dump(out_dict, outfile, protocol=protocol)


def dump(location='',
         tree='',
         branchs=[],
         fakelist={}):
    '''
    location: string, 输入批量处理的文件夹\n
    tree: string, 输入读取的tree的名称\n
    branchs: list, 输入要读取的branch的名称\n
    作用: 确定文件夹中所有root文件，读取对应的tree保存至对应名称pkl文件\n
    '''
    files = os.listdir(location)
    for i1 in files:
        if(re.match(r'(.*).root', i1)):
            energy = float(i1.replace('.root', ''))
            hprint.pline('Extracting %1.4f' % (energy))
            if(energy in fakelist):
                fakeparameter = fakelist[energy]
                root_pkl('%s/%s' % (location, i1),
                         tree,
                         branchs,
                         '%s/%s' % (location,
                                    i1.replace('.root',
                                               '_%s.pkl' % (tree))),
                         fake=fakeparameter)
            else:
                root_pkl('%s/%s' % (location, i1),
                         tree,
                         branchs,
                         '%s/%s' % (location,
                                    i1.replace('.root',
                                               '_%s.pkl' % (tree))))


def hist1d(name_tfile='',
           name_hist='',
           inter=100,
           left=0,
           right=1,
           data=[],
           weight=[]):
    '''
    name_tfile: string, root文件名\n
    name_hist: string, hist名\n
    inter, left, right: double, hist选项\n
    data: list, hist数据\n
    weight: list, weight数据\n
    '''
    tfile = ROOT.TFile(name_tfile, 'RECREATE')
    hist = ROOT.TH1D(name_hist, '',
                     inter,
                     left,
                     right)
    num = len(data)
    if(num == len(weight)):
        for i in range(num):
            hist.Fill(data[i], weight[i])
    else:
        for i in range(num):
            hist.Fill(data[i])
    tfile.Write()
    tfile.Close()
    return (name_tfile, name_hist)


def hist2d(name_tfile='',
           name_hist='',
           inter1=100,
           left1=0,
           right1=1,
           inter2=100,
           left2=0,
           right2=1,
           data1=[],
           data2=[],
           weight=[]):
    '''
    name_tfile: string, root文件名\n
    name_hist: string, hist名\n
    inter, left, right: double, hist选项\n
    data: list, hist数据\n
    weight: list, weight数据\n
    '''
    tfile = ROOT.TFile(name_tfile, 'RECREATE')
    hist = ROOT.TH2D(name_hist, '',
                     inter1,
                     left1,
                     right1,
                     inter2,
                     left2,
                     right2)
    num = len(data1)
    if(num == len(weight)):
        for i in range(num):
            hist.Fill(data1[i], data2[i], weight[i])
    else:
        for i in range(num):
            hist.Fill(data1[i], data2[i])
    tfile.Write()
    tfile.Close()
    return (name_tfile, name_hist)


def tree1d(name_tfile='',
           name_ttree='',
           name_branch='',
           data=[]):
    '''
    name_tfile: string, root文件名\n
    name_ttree: string, tree名\n
    name_branch: string, branch名\n
    data: list, branch数据\ns
    '''
    tfile = ROOT.TFile(name_tfile, 'RECREATE')
    ttree = ROOT.TTree(name_ttree, '')
    n = array('f', [0])
    ttree.Branch(name_branch, n, '%s/F' % (name_branch))
    for i in data:
        n[0] = i
        ttree.Fill()
    tfile.Write()
    tfile.Close()
    return (name_tfile, name_ttree)
