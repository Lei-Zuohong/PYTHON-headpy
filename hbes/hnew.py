# -*- coding: UTF-8 -*-
# Public package
import numpy
import os
import re
import copy
from array import array
# Private package
try:
    import ROOT
except:
    root_exit = 0
else:
    root_exit = 1
import headpy.hfile as hfile
import headpy.hscreen.hprint as hprint

# 类型定义


class SELECTER:

    def __init__(self,
                 center=0.5,
                 width=0.5,
                 center_show=0.5,
                 width_show=0.5,
                 inter=100,
                 title='',
                 unit='',
                 reverse=0):
        '初始化'
        # 判断类变量
        self.left = center - width
        self.right = center + width
        self.center = center
        self.width = width
        # 信息类变量
        self.left_show = center_show - width_show
        self.right_show = center_show + width_show
        self.center_show = center_show
        self.width_show = width_show

        self.inter = inter
        self.title = title
        self.unit = unit
        # 反向判断变量
        self.reverse = reverse

    # 方法：判断
    def judge(self, input):
        a = input >= self.left
        b = input <= self.right
        output = a * b
        if(self.reverse != 0):
            output = bool(1) ^ output
        return output

    # 方法：改变选择变量
    def set_by_center(self, center, width):
        self.center = center
        self.width = width
        self.left = center - width
        self.right = center + width

    def set_by_edge(self, left, right):
        self.left = left
        self.right = right
        self.center = 0.5 * (left + right)
        self.width = 0.5 * (right - left)

    def set_width(self, value):
        self.width = value
        self.left = self.center - self.width
        self.right = self.center + self.width

    def set_scale(self, value):
        self.width = self.width * value
        self.left = self.center - self.width
        self.right = self.center + self.width

    # 方法：改变显示范围
    def set_by_center_show(self, center_show, width_show):
        self.center_show = center_show
        self.width_show = width_show
        self.left_show = center_show - width_show
        self.right_show = center_show + width_show

    def set_by_edge_show(self, left_show, right_show):
        self.left_show = left_show
        self.right_show = right_show
        self.center_show = 0.5 * (left_show + right_show)
        self.width_show = 0.5 * (right_show - left_show)

    def set_width_show(self, value_show):
        self.width_show = value_show
        self.left_show = self.center_show - self.width_show
        self.right_show = self.center_show + self.width_show

    def set_scale_show(self, value_show):
        self.width_show = self.width_show * value_show
        self.left_show = self.center_show - self.width_show
        self.right_show = self.center_show + self.width_show

    # 方法：操作
    def shift(self, value):
        '整体平移坐标'
        self.left = self.left + value
        self.right = self.right + value
        self.center = self.center + value

    def reverse(self):
        '进行反向选择'
        self.reverse = 1 - self.reverse

    # 方法：获取信息

    def get_range(self):
        '返回cut边界'
        return self.left, self.right

    def get_range_show(self):
        '返回show边界'
        return self.left_show, self.right_show

    def get_title(self):
        '返回坐标轴标题'
        value = 2 * self.width_show / self.inter
        xtitle = self.title
        ytitle = r'Events/%s' % (str(value))
        xtitle += self.unit
        ytitle += self.unit
        return xtitle, ytitle

    # 方法：输出信息
    def get_massage(self):
        print('|{:^44}|'.format('Now print selection'))
        print('|{:^20}|=>|{:^20}|'.format('left', self.left))
        print('|{:^20}|=>|{:^20}|'.format('right', self.right))
        print('|{:^20}|=>|{:^20}|'.format('center', self.center))
        print('|{:^20}|=>|{:^20}|'.format('width', self.width))
        print('|{:^20}|=>|{:^20}|'.format('text', self.text))


class SELECTER_value:
    '''
    对value判断的selecter
    '''

    def __init__(self,
                 values=[],
                 reverse=0):
        self.values = values
        self.reverse = reverse

    def judge(self, value):
        output = bool(0)
        for i in self.values:
            check = (value >= i) * (value <= i)
            output += check
        if(self.reverse != 0):
            output = bool(1) ^ output
        return output


def significance_no_root(value=10, num_parameter=1):
    execute_path = os.getenv("SIGNIFICANCE")
    execute_path = '%s/significance' % (execute_path)
    os.system('%s %f %d | tee significance.txt' % (execute_path, value, num_parameter))
    text = hfile.txt_read('significance.txt')
    output = float(text)
    os.system('rm significance.txt')
    return output


if(root_exit == 1):
    # 计算函数

    def significance(value=[],
                     num_parameter=1,
                     method='likelyhood'):
        # method
        if(method == 'chisq'):
            factor = 1
        elif(method == 'likelyhood'):
            factor = 2.
        else:
            print('Error: Wrong significance method!')
        # value
        if(len(value) == 1):
            delta = value[0]
        elif(len(value) == 2):
            delta = abs(value[1] - value[0])
        else:
            print('Error: Wrong significance value input!')
        # calculate
        probability = ROOT.TMath.Prob(factor * delta, num_parameter)
        significance = ROOT.RooStats.PValueToSignificance(0.5 * probability)
        # return
        return significance

    # root 读取类 - need to modified

    def root_dict(**kwargs):
        '''
        file_root: root文件名\n
        tree: tree名\n
        branchs: branch名列表\n
        \n
        1: 将root文件中对应tree的branchs，转化为numpy数组，放入列表\n
        '''
        # 读取root文件
        tfile = ROOT.TFile(kwargs['file_root'])
        ttree = tfile.Get(kwargs['tree'])
        num = ttree.GetEntries()
        # 初始化输出字典
        output = {}
        for branch in kwargs['branchs']:
            output[branch] = numpy.zeros(num)
        # 输入字典
        for entry in range(num):
            ttree.GetEntry(entry)
            for branch in kwargs['branchs']:
                exec("output[branch][entry] = ttree.%s" % (branch))
        # 输出字典
        return output

    def root_pkl(func,
                 file_root='',
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
        output = func(file_root=file_root,
                      tree=tree,
                      branchs=branchs)
        # 写入pickle文件
        hfile.pkl_dump(file_pkl, output)

    def dump(func,
             folder_root='',
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
                root_pkl(func,
                         file_root='%s/%s' % (folder_root, file),
                         tree=tree,
                         branchs=branchs,
                         file_pkl='%s/%s_%s.pkl' % (folder_root, name, tree))
        hprint.pstar()

    # root 写入类

    def hist1d(name_tfile='',
               name_hist='',
               inter=100, left=0, right=1,
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
        hist = ROOT.TH1D(name_hist, '', inter, left, right)
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
               inter1=100, left1=0, right1=1,
               inter2=100, left2=0, right2=1,
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
                         inter1, left1, right1,
                         inter2, left2, right2)
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

    def treend(name_tfile='',
               name_ttree='',
               branchs=[]):
        '''
        name_tfile: string, root文件名\n
        name_ttree: string, tree名\n
        branchs: dict, tree的python实体\n
        \n
        1: 将某一个tree的python实体放入root文件
        '''
        tfile = ROOT.TFile(name_tfile, 'RECREATE')
        ttree = ROOT.TTree(name_ttree, '')
        num = 0
        for branch in branchs:
            num = len(branchs[branch])
        tarray = {}
        for branch in branchs:
            tarray[branch] = array('f', [0])
            ttree.Branch(branch, tarray[branch], '%s/F' % (branch))
        for i in range(num):
            for branch in branchs:
                tarray[branch][0] = branchs[branch][i]
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

    def tree_len(dict_tree):
        output = 0
        for i in dict_tree:
            output = len(dict_tree[i])
        return output

    def get_index(data, l, r, i):
        '''
        返回bin的位置
        '''
        output = int(i * (data - l) / (r - l))
        if(output > i - 1 or output < 0):
            output = 'empty'
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
            output[method] = hfile.pkl_read(filename)
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
            self.trees = copy.deepcopy(trees)
            self.selecters = copy.deepcopy(selecters)
            self.massages = copy.deepcopy(massages)

        def get_weight_2d(self,
                          data='',
                          energy=0,
                          name_weight='',
                          name_branch=''):
            '内部调用函数'
            # 读取weight信息
            weight_file = '%s/%s_%1.4f.pkl' % (self.massages['weight'],
                                               name_weight,
                                               energy)
            weight = hfile.pkl_read(weight_file)
            # 更改cut
            self.selecters[weight['branchx']].set_by_edge_show(weight['xl'], weight['xr'])
            self.selecters[weight['branchx']].inter = weight['xi']
            self.selecters[weight['branchy']].set_by_edge_show(weight['yl'], weight['yr'])
            self.selecters[weight['branchy']].inter = weight['yi']
            # 添加新的branch
            new_branch = []
            for i in range(tree_len(self.trees[data])):
                xindex = get_index(self.trees[data][weight['branchx']][i],
                                   weight['xl'],
                                   weight['xr'],
                                   weight['xi'])
                yindex = get_index(self.trees[data][weight['branchy']][i],
                                   weight['yl'],
                                   weight['yr'],
                                   weight['yi'])
                if(xindex != 'empty' and yindex != 'empty'):
                    new_branch.append(weight['ratio'][xindex][yindex])
                else:
                    new_branch.append(0)
            new_branch = numpy.array(new_branch)
            self.trees[data][name_branch] = new_branch

        def get_weight_1d(self,
                          data='',
                          energy=0,
                          name_weight='',
                          name_branch=''):
            '内部调用函数'
            # 读取weight信息
            weight_file = '%s/%s_%1.4f.pkl' % (self.massages['weight'],
                                               name_weight,
                                               energy)
            weight = hfile.pkl_read(weight_file)
            # 更改cut
            self.selecters[weight['branchx']].set_by_edge_show(weight['xl'], weight['xr'])
            self.selecters[weight['branchx']].inter = weight['xi']
            # 添加新的branch
            new_branch = []
            for i in range(tree_len(self.trees[data])):
                xindex = get_index(self.trees[data][weight['branchx']][i],
                                   weight['xl'],
                                   weight['xr'],
                                   weight['xi'])
                if(xindex != 'empty'):
                    new_branch.append(weight['ratio'][xindex])
                else:
                    new_branch.append(0)
            new_branch = numpy.array(new_branch)
            self.trees[data][name_branch] = new_branch

        def get_weight(self,
                       data='',
                       energy=0,
                       name_weight='',
                       name_branch='',
                       dimension=0):
            if(dimension == 2):
                self.get_weight_2d(data=data,
                                   energy=energy,
                                   name_weight=name_weight,
                                   name_branch=name_branch)
            elif(dimension == 1):
                self.get_weight_1d(data=data,
                                   energy=energy,
                                   name_weight=name_weight,
                                   name_branch=name_branch)
            else:
                print('Error dimension!!!!')

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
            tfilename = '%s/%s_%s_%s.root' % (os.getenv("TEMPROOT"), data, branch, name)
            histname = '%s_%s' % (data, branch)
            inter = self.selecters[branch].inter
            left, right = self.selecters[branch].get_range_show()
            num = len(ntree[branch])
            hprint.ppoint('Entires', num)
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
            tfilename = '%s/%s_%s_%s_%s.root' % (os.getenv("TEMPROOT"),
                                                 data,
                                                 branch1,
                                                 branch2,
                                                 name)
            histname = '%s_%s_%s' % (data,
                                     branch1,
                                     branch2)
            inter1 = self.selecters[branch1].inter
            left1, right1 = self.selecters[branch1].get_range_show()
            inter2 = self.selecters[branch2].inter
            left2, right2 = self.selecters[branch2].get_range_show()
            data1 = ntree[branch1]
            data2 = ntree[branch2]
            num = len(data1)
            hprint.ppoint('Entires', num)
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
            1：返回tfile的名字，thist的名字\n
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

        def tree(self,
                 data='',
                 branch='',
                 change_name='',
                 docuts=[],
                 name=''):
            '''
            data: 数据来源的tree\n
            branch: 提取的数据的branch名\n
            docuts: 进行筛选的branch名\n
            name: 提供文件名保证名称不重复\n
            \n
            1：返回tfile的名字，ttree的名字\n
            '''
            # 输出信息
            hprint.pline('Building TTree')
            hprint.ppoint('Source', data)
            hprint.ppoint('Branch', branch)
            hprint.pstar()
            # 得到cut后的tree
            ntree = tree_cut(self.trees[data], self.selecters, docuts)
            # 新建root文件,tree对象
            tfilename = '%s/%s_%s_%s.root' % (os.getenv("TEMPROOT"), data, branch, name)
            ttreename = '%s_%s' % (data, branch)
            if(change_name != ''):
                tfilename, ttreename = tree1d(name_tfile=tfilename,
                                              name_ttree=ttreename,
                                              name_branch=change_name,
                                              data=ntree[branch])
            else:
                tfilename, ttreename = tree1d(name_tfile=tfilename,
                                              name_ttree=ttreename,
                                              name_branch=branch,
                                              data=ntree[branch])
            return tfilename, ttreename

        def statis(self,
                   data='',
                   docuts=[],
                   doweight=''):
            '''
            data: 进行统计的tree名\n
            docuts: 进行cut的branch名\n
            doweight: weight列表\n
            \n
            1：返回一个tree后的加权总数\n
            '''
            # 输出信息
            hprint.pline('Getting entries of a tree')
            hprint.ppoint('Source', data)
            # 得到cut后的tree
            ntree = tree_cut(self.trees[data], self.selecters, docuts)
            # 初始化统计
            output = 0
            num = tree_len(ntree)
            # 开始填入直方图
            if (len(doweight) == 0):
                hprint.ppoint('Weight', 'NO')
            else:
                hprint.ppoint('Weight', 'YES')
            for i in range(num):
                # 填入非weight数量
                if (len(doweight) == 0):
                    output += 1
                # 填入weight数量
                else:
                    factor = 1
                    for name in doweight:
                        factor = factor * ntree[name][i]
                    output += factor
            hprint.pstar()
            return float(output)
