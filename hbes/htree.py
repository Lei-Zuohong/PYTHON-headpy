# -*- coding: UTF-8 -*-
'''
This is a package document.

    Environment version:

        python2
        python3
        能够在python2,3下使用的通用程序，请不要引入numpy ROOT

    Content:

        @pkl_read:
            读取pkl对象
        @massage_read:
            读取massage.txt文件内的列表信息
        @tree_read:
            读取massage,获取real, mc, pwa-mc, topology的python_tree并返回
        @tree_range:
            输入python_tree,ranges列表
            返回ranges后的python_tree
        @tree_cut:
            输入python_tree，cuts列表，需要cut的branch
            返回cuts后的python_tree
        @bin_search:
            输入单个数据，最标轴信息，返回分bin位置
        @tree_addweight2d:
            对于2Dweight，输入原tree，weight信息列表，返回加入weight数组的新tree
        @tree_addweight1d
            对于1Dweight，输入原tree，weight信息列表，返回加入weight数组的新tree
        @branch_title:
            输入branch，对应的横坐标，返回[xtitle, ytitle]
'''
# Public package
import re
import pickle
import math
# Private package
import headpy.hscreen.hprint as hprint
import headpy.hfile.hpickle as hpickle


def massage_read(file_read='massage.txt',
                 print_text=''):
    '获取目录下文件内容,默认为"massage.txt",输出列表'
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


def tree_read(energy=0,
              tree='',
              read=[]):
    '读取对应的tree文件并返回trees{}'
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


def bin_search(data, l, r, i, d):
    '输入单个数据，最标轴信息，返回分bin位置，超越范围返回empty'
    output = int((data - l) / d)
    if(output > i - 1 or output < 0):
        output = 'empty'
    return output


def tree_addweight2d(in_tree={},
                     weight={},
                     name_branch='',
                     name_ratio=''):
    '对于2Dweight，输入原tree，weight信息列表，返回加入weight数组的新tree'
    # 新tree初始化
    out_tree = in_tree
    num = 0
    for i in in_tree:
        num = len(in_tree[i])
    out_tree[name_branch] = []
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
            out_tree[name_branch].append(weight[name_ratio][bx][by])
        else:
            out_tree[name_branch].append(0)
    return out_tree


def tree_addweight1d(in_tree={},
                     weight={},
                     name_branch='',
                     name_ratio=''):
    '对于1Dweight，输入原tree，weight信息列表，返回加入weight数组的新tree'
    # 新tree初始化
    out_tree = in_tree
    num = 0
    for i in in_tree:
        num = len(in_tree[i])
    out_tree[name_branch] = []
    # 填入weight
    for i in range(num):
        bx = bin_search(in_tree[weight['branchx']][i],
                        weight['xl'],
                        weight['xr'],
                        weight['xi'],
                        weight['dx'])
        if(bx != 'empty'):
            out_tree[name_branch].append(weight[name_ratio][bx])
        else:
            out_tree[name_branch].append(0)
    return out_tree


def branch_title(cuts, branch):
    '输入branch，对应的横坐标，返回[xtitle, ytitle]'
    if('string' in cuts[branch]):
        xtitle = cuts[branch]['string']
    else:
        xtitle = branch
    bwr = float(cuts[branch]['range'])
    bwi = float(cuts[branch]['inter'])
    ytitle = 'Events/%s(GeV/c^{2})' % (str(2 * bwr / bwi))
    output = {}
    output['xtitle'] = xtitle
    output['ytitle'] = ytitle
    return output


class HEPVECTOR:
    '四动量类型'

    def __init__(self, px, py, pz, e):
        self.__px__ = px
        self.__py__ = py
        self.__pz__ = pz
        self.__e__ = e

    def __add__(self, other):
        return HEPVECTOR(self.__px__ + other.__px__,
                         self.__py__ + other.__py__,
                         self.__pz__ + other.__pz__,
                         self.__e__ + other.__e__)

    def __sub__(self, other):
        return HEPVECTOR(self.__px__ - other.__px__,
                         self.__py__ - other.__py__,
                         self.__pz__ - other.__pz__,
                         self.__e__ - other.__e__)

    def m(self):
        px2 = pow(self.__px__, 2)
        py2 = pow(self.__py__, 2)
        pz2 = pow(self.__pz__, 2)
        e2 = pow(self.__e__, 2)
        mass = pow(px2 + py2 + pz2 + e2, 0.5)
        return mass

    def px(self):
        return self.__px__

    def py(self):
        return self.__py__

    def pz(self):
        return self.__pz__

    def e(self):
        return self.__e__

    def costheta(self):
        r = (self.__px__**2 + self.__py__**2 + self.__pz__**2)**0.5
        return self.__pz__ / r

    def theta(self):
        return math.acos(self.costheta())


def tree_range(in_tree={},
               ranges={}):
    '''
    in_tree为输入tree\n
    ranges为字典，key值为需要cut的branch名，value值为二维数组，为数值的下界与上界\n
    '''
    out_tree = {}
    num = 0
    for branch in in_tree:
        out_tree[branch] = []
        num = len(in_tree[branch])
    for entry in range(num):
        check = 1
        for i in ranges:
            if(in_tree[i][entry] < ranges[i][0] or in_tree[i][entry] > ranges[i][1]):
                check = 0
        if(check == 1):
            for branch in in_tree:
                out_tree[branch].append(in_tree[branch][entry])
    return out_tree


def tree_cut(in_tree={},
             cuts={},
             branchs=[],
             print_text=''):
    '''
    in_tree为输入tree\n
    cuts为字典，key值为branch名，value值为字典\n
    branchs为列表，值为需要cut的branch名\n
    '''
    # 输出信息
    if(print_text != ''):
        hprint.pline('Cutting tree')
        for i in branchs:
            hprint.ppoint(i, '%1.4f +- %1.4f' % (cuts[i]['mass'] + cuts[i]['shift'],
                                                 cuts[i]['cut']))
    # 得到ranges
    ranges = {}
    for i in branchs:
        ranges[i] = [cuts[i]['mass'] + cuts[i]['shift'] - cuts[i]['cut'],
                     cuts[i]['mass'] + cuts[i]['shift'] + cuts[i]['cut']]
    # 处理tree
    out_tree = tree_range(in_tree, ranges)
    return out_tree


class TREE:
    'tree 类型'

    def __init__(self, tree):
        self.tree = tree

    def range(self,
              ranges={}):
        '''
        in_tree为输入tree\n
        ranges为字典，key值为需要cut的branch名，value值为二维数组，为数值的下界与上界\n
        '''
        self.tree = tree_range(self.tree, ranges=ranges)
        return 0

    def cut(self,
            cuts={},
            branchs=[],
            print_text=''):
        '''
        in_tree为输入tree\n
        cuts为字典，key值为branch名，value值为字典\n
        branchs为列表，值为需要cut的branch名\n
        '''
        self.tree = tree_cut(self.tree, cuts, branchs)
        return 0

    def add_branch(self,
                   branch_name='',
                   branch_list=[]):
        '添加一个branch'
        self.tree[branch_name] = branch_list
        return 0

    def get_len(self):
        '返回tree的长度'
        num = 0
        for i in self.tree:
            num = len(self.tree[i])
        return num

    def get_branch(self, branch):
        '返回一个branch'
        return self.tree[branch]

    def get_tree(self):
        '返回自己的tree'
        return self.tree

    def add_branch_expression(self,
                              branch_name='',
                              value_list=[],
                              value_expression=''):
        num = self.get_len()
        new_branch = []
        for i1 in range(num):
            for i2 in value_list:
                output = 0
                exec("%s = 0" % (i2))
                exec("%s = self.tree[\'%s\'][i1]" % (i2, i2))
            exec("output=%s" % (value_expression))
            new_branch.append(output)
        self.add_branch(branch_name=branch_name,
                        branch_list=new_branch)
