# -*- coding: UTF-8 -*-
# Public package
import numpy
import os
import re
from array import array
# Private package
import ROOT
import headpy.hfile.hpickle as hpickle
import headpy.hscreen.hprint as hprint

# 类型定义


class SELECTER:

    def __init__(self,
                 center=0.5,
                 width=0.5,
                 text='',
                 show=0,
                 inter=100,
                 title=''):
        '初始化'
        # 判断类变量
        self.left = center - width
        self.right = center + width
        self.center = center
        self.width = width
        self.text = text
        # 信息类变量
        self.show = show
        self.inter = inter
        self.title = title

    # 方法：判断
    def judge(self, input):
        if(type(input) == type('')):
            output = input == self.text
        else:
            a = input >= self.left
            b = input <= self.right
            output = a * b
        return output

    # 方法：改变变量
    def set_by_edge(self, left, right):
        self.left = left
        self.right = right
        self.center = 0.5 * (left + right)
        self.width = 0.5 * (right - left)

    def set_by_center(self, center, width):
        self.center = center
        self.width = width
        self.left = center - width
        self.right = center + width

    def set_text(self, text):
        self.text = text

    def set_inter(self, inter):
        self.inter = inter

    def set_show(self, show):
        self.show = show

    def set_title(self, title):
        self.title = title

    # 方法：操作
    def shift(self, value):
        self.left = self.left + value
        self.right = self.right + value
        self.center = self.center + value

    # 方法：获取信息
    def get_range(self):
        return self.left, self.right

    # 方法：输出信息
    def get_massage(self):
        print('|{:^44}|'.format('Now print selection'))
        print('|{:^20}|=>|{:^20}|'.format('left', self.left))
        print('|{:^20}|=>|{:^20}|'.format('right', self.right))
        print('|{:^20}|=>|{:^20}|'.format('center', self.center))
        print('|{:^20}|=>|{:^20}|'.format('width', self.width))
        print('|{:^20}|=>|{:^20}|'.format('text', self.text))
        output = {}
        output['left'] = self.left
        output['right'] = self.right
        output['center'] = self.center
        output['width'] = self.width
        output['text'] = self.text
        return output

# root读取类


def root_dict(file_root='',
              tree='',
              branchs=[]):
    '''
    file_root: root文件名\n
    tree: tree名\n
    branchs: branch名列表\n
    \n
    1: 将root文件中对应tree的branchs，转化为numpy数组，放入列表\n
    '''
    # 读取root文件
    tfile = ROOT.TFile(file_root)
    ttree = tfile.Get(tree)
    num = ttree.GetEntries()
    # 初始化输出字典
    output = {}
    for branch in branchs:
        output[branch] = numpy.array([])
    # 输入字典
    for entry in range(num):
        ttree.GetEntry(entry)
        for branch in branchs:
            exec("numpy.append(output['%s'],ttree.%s)" % (branch, branch))
    # 输出字典
    return output


def root_pkl(file_root='',
             tree='',
             branchs=[],
             file_pkl=''):
    '''
    file_root: root文件名\n
    tree: tree名\n
    branchs: branch名列表\n
    file_pkl: pkl文件名\n
    \n
    1: 将root文件中对应tree的branchs，转化为numpy数组，放入列表\n
    2. 将列表存入pkl\n
    '''
    # 读取root至dict
    output = root_dict(file_root=file_root, tree=tree, branchs=branchs)
    # 写入pickle文件
    hpickle.pkl_dump(file_pkl, output)


def dump(folder_root='',
         tree='',
         branchs=[]):
    '''
    folder_root: 存放root文件的文件夹\n
    tree: tree名\n
    branchs: branch名列表\n
    \n
    1: 将root文件中对应tree的branchs，转化为numpy数组，放入列表\n
    2. 将列表存入pkl\n
    '''
    hprint.pstar()
    files = os.listdir(folder_root)
    for file in files:
        match = re.match(r'(.*).root', file)
        if(match):
            name = match.group(1)
            energy = float(name)
            hprint.pline('Extracting %1.4f' % (energy))
            root_pkl('%s/%s' % (folder_root, file),
                     tree,
                     branchs,
                     '%s/%s.pkl' % (folder_root, name))
    hprint.pstar()

# root写入类


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
    \n
    1: 将列表作为直方图存入root文件\n
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
    return name_tfile, name_hist


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
    \n
    1: 将列表作为直方图存入root文件\n
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
    return name_tfile, name_hist


def tree1d(name_tfile='',
           name_ttree='',
           name_branch='',
           data=[]):
    '''
    name_tfile: string, root文件名\n
    name_ttree: string, tree名\n
    name_branch: string, branch名\n
    data: list, branch数据\n
    \n
    1: 将列表作为tree放入root文件
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
    return name_tfile, name_ttree
