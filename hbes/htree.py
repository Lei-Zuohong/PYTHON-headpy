# -*- coding: UTF-8 -*-
'''
This is a package document.

    Environment version:

        python2
        python3

    Content:

        @pkl_read:
        @massage_read:
        @tree_read:
        @tree_range:
        @tree_cut:
        @bin_search:
        @tree_addweight2d:
        @tree_addweight1d
        @branch_title:
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
    '''
    file_read 为读取文件名\n
    print_text 如果不为空，则输出读取内容\n
    作用：读取txt内信息，返回字典\n
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


def tree_read(energy=0,
              tree='',
              read=[]):
    '''
    energy 为文件名中的能量点\n
    tree 为文件名中的tree名\n
    read 为读取的method名组成的列表\n
    作用：读取pkl文件内的tree，地址为massage中的指定文件夹，返回字典\n
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


def bin_search(data, l, r, i, d):
    '''
    data 为数值\n
    l, r 为左边界和右边界\n
    i 为总bin数\n
    d 为分bin间隔\n
    作用：数组数值，输入坐标轴信息，返回所在bin\n
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
    in_tree 为tree\n
    weight 为weight信息字典\n
    name_branch 为tree中存放权重的branch名\n
    name_ratio 为weight中存放权重矩阵的key名\n
    作用：输入weight信息字典，给tree添加权重的branch\n
    '''
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
    '''
    in_tree 为tree\n
    weight 为weight信息字典\n
    name_branch 为tree中存放权重的branch名\n
    name_ratio 为weight中存放权重矩阵的key名\n
    作用：输入weight信息字典，给tree添加权重的branch\n
    '''
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
    '''
    cuts 为branch信息字典\n
    branch 为branch名\n
    作用：返回字典，分别对应xtitle,ytitle字符串\n
    '''
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
    in_tree 为输入tree\n
    ranges 为字典，key值为需要cut的branch名，value值为二维数组，为数值的下界与上界\n
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
    in_tree 为输入tree\n
    cuts 为字典，key为branch名\n
    branchs 为需要cut的branch名的列表\n
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
        in_tree 为输入tree\n
        ranges 为字典，key值为需要cut的branch名，value值为二维数组，为数值的下界与上界\n
        '''
        self.tree = tree_range(self.tree, ranges=ranges)
        return 0

    def cut(self,
            cuts={},
            branchs=[],
            print_text=''):
        '''
        in_tree 为输入tree\n
        cuts 为字典，key为branch名\n
        branchs 为需要cut的branch名的列表\n
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
        '''
        branch_name 为新添加的branch\n
        作用：添加一个branch，value分别为需要调用的其它branch和其组成新branch的表达式\n
        '''
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
