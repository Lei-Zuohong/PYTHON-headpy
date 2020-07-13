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
                 title='',
                 reverse=0):
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
        self.reverse = reverse

    # 方法：判断
    def judge(self, input):
        if(type(input) == type('')):
            output = input == self.text
        else:
            a = input >= self.left
            b = input <= self.right
            output = a * b
        if(self.reverse != 0):
            output = 1 - output
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

    def reverse(self):
        self.reverse = 1 - self.reverse

    # 方法：获取信息
    def get_range(self):
        return self.left, self.right

    def get_title(self):
        value = 2 * self.show / self.inter
        xtitle = self.title
        ytitle = 'Events/%s(GeV/c^{2})' % (str(value))
        return xtitle, ytitle

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

    # 特殊方法
    def set_series(self, series):
        self.series = series

    def judge_by_series(self, input):
        output = False
        if(input in self.series()):
            output = True
        if(self.reverse != 0):
            output = 1 - output
        return output


# root 读取类


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
        output[branch] = numpy.zeros(num)
    # 输入字典
    for entry in range(num):
        ttree.GetEntry(entry)
        for branch in branchs:
            exec("output[branch][entry] = ttree.%s" % (branch))
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
                     '%s/%s_%s.pkl' % (folder_root, name, tree))
    hprint.pstar()

# root 写入类


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

# tree_numpy 处理类


def tree_cut(dict_tree,
             dict_selecter,
             branchs=[]):
    '''
    dict_tree: tree型字典\n
    dict_selecter: selecter型字典\n
    branchs: 进行选择的branch\n
    \n
    1: 对tree型字典进行cut\n
    '''
    num = 0
    for i in dict_tree:
        num = len(dict_tree[i])
    list_bool = numpy.ones(num, dtype=bool)
    for i in branchs:
        list_bool = list_bool * dict_selecter[i].judge(dict_tree[i])
    dict_tree_new = {}
    for i in dict_tree:
        dict_tree_new[i] = dict_tree[i][list_bool]
    return dict_tree_new


def bin_search(data, l, r, i, d):
    '''
    data: 数值\n
    l, r: 左边界和右边界\n
    i: 总bin数\n
    d: 分bin间隔\n
    \n
    1：数组数值，输入坐标轴信息，返回所在bin\n
    '''
    output = int((data - l) / d)
    if(output > i - 1 or output < 0):
        output = 'empty'
    return output


def tree_addweight2d(in_tree={},
                     weight={},
                     name_branch='',
                     name_ratio=''):
    '''
    in_tree: tree\n
    weight: weight信息字典\n
    name_branch: tree中存放权重的branch名\n
    name_ratio: weight中存放权重矩阵的key名\n
    \n
    作用：输入weight信息字典，给tree添加权重的branch\n
    '''
    # 新tree初始化
    out_tree = in_tree
    num = 0
    for i in in_tree:
        num = len(in_tree[i])
    out_tree[name_branch] = numpy.array([])
    # 填入weight
    for i in range(num):
        bx = bin_search(in_tree[weight['branchx']][i],
                        weight['xl'],
                        weight['xr'],
                        weight['xi'],
                        weight['dx'])
        by = bin_search(in_tree[weight['branchy']][i],
                        weight['yl'],
                        weight['yr'],
                        weight['yi'],
                        weight['dy'])
        if(bx != 'empty' and by != 'empty'):
            out_tree[name_branch] = numpy.append(out_tree[name_branch], weight[name_ratio][bx][by])
        else:
            out_tree[name_branch] = numpy.append(out_tree[name_branch], 0)
    return out_tree


def tree_addweight1d(in_tree={},
                     weight={},
                     name_branch='',
                     name_ratio=''):
    '''
    in_tree: tree\n
    weight: weight信息字典\n
    name_branch: tree中存放权重的branch名\n
    name_ratio: weight中存放权重矩阵的key名\n
    \n
    作用：输入weight信息字典，给tree添加权重的branch\n
    '''
    # 新tree初始化
    out_tree = in_tree
    num = 0
    for i in in_tree:
        num = len(in_tree[i])
    out_tree[name_branch] = numpy.array([])
    # 填入weight
    for i in range(num):
        bx = bin_search(in_tree[weight['branchx']][i],
                        weight['xl'],
                        weight['xr'],
                        weight['xi'],
                        weight['dx'])
        if(bx != 'empty'):
            out_tree[name_branch] = numpy.append(out_tree[name_branch], weight[name_ratio][bx])
        else:
            out_tree[name_branch] = numpy.append(out_tree[name_branch], 0)
    return out_tree


def tree_len(dict_tree):
    output = 0
    for i in dict_tree:
        output = len(dict_tree[i])
    return output

# 系统信息处理类


def massage_read(file_read='massage.txt',
                 print_text=''):
    '''
    file_read: 读取文件名\n
    print_text: 如果不为空，则输出读取内容\n
    \n
    1：读取txt内信息，返回字典\n
    '''
    # 读取文件
    with open(file_read, 'r') as infile:
        lines = infile.readlines()
    # 匹配字符
    massage = {}
    method = r'(.*):(.*) (endl|version)'
    for line in lines:
        check = re.match(method, line)
        if(check):
            if(check.group(3) == 'endl'):
                massage[check.group(1)] = check.group(2)
            if(check.group(3) == 'version'):
                massage[check.group(1)] = check.group(2) + massage['version']
    # 输出信息
    if(print_text != ''):
        hprint.pstar()
        hprint.pline("Reading %s ......" % (file_read))
        hprint.ppointbox(massage)
    return massage


def trees_read(energy=0,
               tree='',
               read=[]):
    '''
    energy: 文件名中的能量点\n
    tree: 文件名中的tree名\n
    read: 读取的method名组成的列表\n
    \n
    1：读取pkl文件内的tree，地址为massage中的指定文件夹，返回字典\n
    '''
    # 读取文件
    massage = massage_read(print_text='yes')
    # 建立项目名字
    name = '%1.4f_%s.pkl' % (energy, tree)
    # 建立文件路径
    output = {}
    hprint.pline('Reading tree objects from file ......')
    for method in read:
        hprint.pline('Reading tree object for %1.4f - %s - %s' % (energy,
                                                                  tree,
                                                                  method))
        filename = '%s/%s' % (massage[method],
                              name)
        output[method] = hpickle.pkl_read(filename)
    hprint.pstar()
    return output


class ALLDATA:
    '''
    数据处理整合类
    '''

    def __init__(self,
                 trees={},
                 selecters={},
                 massages={}):
        '''
        数据集合类初始化\n
        trees: 入对应method的tree\n
        selecters: 对应branch的各项参数\n
        massages: 对应key的信息\n
        '''
        self.trees = trees
        self.selecters = selecters
        self.massages = massages

    def get_weight_2d(self,
                      data='',
                      energy=0,
                      name_weight='',
                      name_branch='',
                      name_ratio=''):
        '内部调用函数'
        # 读取weight信息
        weight_file = '%s/%s_%1.4f.pkl' % (self.massages['weight'],
                                           name_weight,
                                           energy)
        weight = hpickle.pkl_read(weight_file)
        # 更改cut
        self.selections[weight['branchx']].set_by_edge(weight['xl'], weight['xr'])
        self.selections[weight['branchx']].set_inter(weight['xi'])
        self.selections[weight['branchy']].set_by_edge(weight['yl'], weight['yr'])
        self.selections[weight['branchy']].set_inter(weight['yi'])
        # 添加tree[weight_name]的weight数组branch
        self.weights.append(name_branch)
        self.trees[data] = tree_addweight2d(self.trees[data],
                                            weight,
                                            name_branch=name_branch,
                                            name_ratio=name_ratio)

    def get_weight_1d(self,
                      data='',
                      energy=0,
                      name_weight='',
                      name_branch='',
                      name_ratio=''):
        '内部调用函数'
        # 读取weight信息
        weight_file = '%s/%s_%1.4f.pkl' % (self.massages['weight'],
                                           name_weight,
                                           energy)
        weight = hpickle.pkl_read(weight_file)
        # 更改cut
        self.selections[weight['branchx']].set_by_edge(weight['xl'], weight['xr'])
        self.selections[weight['branchx']].set_inter(weight['xi'])
        # 添加tree[name]的weight数组branch
        self.weights.append(name_branch)
        self.trees[data] = tree_addweight1d(self.trees[data],
                                            weight,
                                            name_branch=name_branch,
                                            name_ratio=name_ratio)

    def get_weight(self,
                   data='',
                   energy=0,
                   name_weight='',
                   name_branch='',
                   name_ratio='',
                   dimension=2):
        '''
        data: 进行weighting的tree的name\n
        energy: 进行weighting的能量点\n
        name_weight: 进行weighting的method的名字\n
        name_branch: 添加的branch的名字\n
        name_ratio: weighting阵列的key\n
        dimension: 进行weighting的维度\n
        \n
        1：给tree添加name_branch的branch，数值为权重\n
        \n
        Note: weight信息请放置在 massage['weight']/name_energy.pkl 的文件中\n
        '''
        if(dimension == 2):
            self.get_weight_2d(data=data,
                               energy=energy,
                               name_weight=name_weight,
                               name_branch=name_branch,
                               name_ratio=name_ratio)
        elif(dimension == 1):
            self.get_weight_1d(data=data,
                               energy=energy,
                               name_weight=name_weight,
                               name_branch=name_branch,
                               name_ratio=name_ratio)
        else:
            print('error：维度输入错误')

    def hist1d(self,
               data='',
               branch='',
               docuts=[],
               doweight=[],
               name=''):
        '内部调用函数'
        # 输出信息
        hprint.pline('Building TH1D')
        hprint.ppoint('Source', data)
        hprint.ppoint('Branch', branch)
        # 得到cut后的tree
        ntree = tree_cut(self.trees[data], self.selecters, docuts)
        # 新建root文件,hist对象
        tfilename = 'ftemp/root/%s_%s_%s.root' % (data, branch, name)
        histname = '%s_%s' % (data, branch)
        inter = self.selecters[branch].inter
        left, right = self.selecters[branch].get_range()
        num = len(ntree[branch])
        # 开始填入直方图
        if (len(doweight) == 0):
            hprint.ppoint('Weight', 'NO')
            tfilename, histname = hist1d(name_tfile=tfilename,
                                         name_hist=histname,
                                         inter=inter,
                                         left=left,
                                         right=right,
                                         data=ntree[branch])
        else:
            hprint.ppoint('Weight', 'YES')
            weight = []
            for i in range(num):
                factor = 1
                for name in doweight:
                    factor = factor * ntree[name][i]
                weight.append(factor)
            tfilename, histname = hist1d(name_tfile=tfilename,
                                         name_hist=histname,
                                         inter=inter,
                                         left=left,
                                         right=right,
                                         data=ntree[branch],
                                         weight=weight)
        hprint.pstar()
        return tfilename, histname

    def hist2d(self,
               data='',
               branch1='',
               branch2='',
               docuts=[],
               doweight=[],
               name=''):
        '内部调用函数'
        # 输出信息
        hprint.pline('Building TH1D')
        hprint.ppoint('Source', data)
        hprint.ppoint('Branch1', branch1)
        hprint.ppoint('Branch2', branch2)
        # 得到cut后的tree
        ntree = tree_cut(self.trees[data], self.selecters, docuts)
        # 新建root文件,hist对象
        tfilename = 'ftemp/root/%s_%s_%s_%s.root' % (data,
                                                     branch1,
                                                     branch2,
                                                     name)
        histname = '%s_%s_%s' % (data,
                                 branch1,
                                 branch2)
        inter1 = self.selecters[branch1].inter
        left1, right1 = self.selecters[branch1].get_range()
        inter2 = self.selecters[branch2].inter
        left2, right2 = self.selecters[branch2].get_range()
        data1 = ntree[branch1]
        data2 = ntree[branch2]
        num = len(data1)
        # 开始填入直方图
        if (len(doweight) == 0):
            hprint.ppoint('Weight', 'NO')
            tfilename, histname = hist2d(name_tfile=tfilename,
                                               name_hist=histname,
                                               inter1=inter1,
                                               left1=left1,
                                               right1=right1,
                                               inter2=inter2,
                                               left2=left2,
                                               right2=right2,
                                               data1=data1,
                                               data2=data2)
        else:
            hprint.ppoint('Weight', 'YES')
            weight = []
            for i in range(num):
                factor = 1
                for name in self.weights:
                    factor = factor * ntree[name][i]
                weight.append(factor)
            tfilename, histname = hist2d(name_tfile=tfilename,
                                               name_hist=histname,
                                               inter1=inter1,
                                               left1=left1,
                                               right1=right1,
                                               inter2=inter2,
                                               left2=left2,
                                               right2=right2,
                                               data1=data1,
                                               data2=data2,
                                               weight=weight)
        hprint.pstar()
        return tfilename, histname

    def hist(self,
             data='',
             branchs=[],
             docuts=[],
             doweight=[],
             name=''):
        '''
        data: 数据来源的tree\n
        branchs: 提取的数据的branch名\n
        docuts: 进行筛选的branch名\n
        doweight: 按列表进行weighting\n
        name为字符，提供文件名保证名称不重复\n
        \n
        1：返回tfile的名字，thist的名字]\n
        \n
        Note: 请在目录ftemp文件夹下建立root文件夹
        '''
        if(len(branchs) == 1):
            tfilename, histname = self.hist1d(data,
                                              branchs[0],
                                              docuts,
                                              doweight,
                                              name)
        if(len(branchs) == 2):
            tfilename, histname = self.hist2d(data,
                                              branchs[0],
                                              branchs[1],
                                              docuts,
                                              doweight,
                                              name)
        return tfilename, histname
