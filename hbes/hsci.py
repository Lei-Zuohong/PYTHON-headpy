# -*- coding: UTF-8 -*-
'''
This is a package document.

    Environment version:

        python2

    Content:

        CLASS ALLDATA
        @get_weight_2d:
        @get_weight_1d:
        @get_weight:
        @hist1d:
        @hsit2d:
        @hist:
        @statis:
        @tree1d:
        @title:
'''
# Public package
import re
import os
import pickle
from array import array
# Private package
import ROOT
import headpy.hscreen.hprint as hprint
import headpy.hbes.htree as htree
import headpy.hbes.hroot as hroot


class ALLDATA:
    '数据集合类'

    def __init__(self,
                 trees={},
                 cuts={},
                 massages={}):
        '''
        数据集合类初始化\n
        trees为字典，输入对应method的tree\n
        cuts为字典，输入对应branch的各项参数\n
        massages为字典，为对应key的信息\n
        '''
        self.trees = trees
        self.cuts = cuts
        self.massages = massages
        self.weights = []

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
        with open(weight_file, 'rb') as infile:
            weight = pickle.load(infile)
        # 更改cut
        self.cuts[weight['branchx']]['mass'] = 0.5 * (weight['xr'] + weight['xl'])
        self.cuts[weight['branchx']]['range'] = 0.5 * (weight['xr'] - weight['xl'])
        self.cuts[weight['branchx']]['inter'] = weight['xi']
        self.cuts[weight['branchy']]['mass'] = 0.5 * (weight['yr'] + weight['yl'])
        self.cuts[weight['branchy']]['range'] = 0.5 * (weight['yr'] - weight['yl'])
        self.cuts[weight['branchy']]['inter'] = weight['yi']
        # 添加tree[weight_name]的weight数组branch
        self.weights.append(name_branch)
        self.trees[data] = htree.tree_addweight2d(self.trees[data],
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
        with open(weight_file, 'rb') as infile:
            weight = pickle.load(infile)
        # 更改cut
        self.cuts[weight['branchx']]['mass'] = 0.5 * (weight['xr'] + weight['xl'])
        self.cuts[weight['branchx']]['range'] = 0.5 * (weight['xr'] - weight['xl'])
        self.cuts[weight['branchx']]['inter'] = weight['xi']
        # 添加tree[name]的weight数组branch
        self.weights.append(name_branch)
        self.trees[data] = htree.tree_addweight1d(self.trees[data],
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
        data为字符，输入要进行weighting的tree的name\n
        energy为浮点，输入要进行的weighting的能量点\n
        name为字符，输入要进行weighting的method的名字\n
        dimension为整形，输入要进行weighting的维度\n
        ratio_name为字符，输入weighting数据中心代表要使用的阵列的key\n
        作用1：给tree添加name的branch，数值为权重\n
        作用2：将name添加进内部变量weights\n
        Note:\n
        weight信息请放置在massage['weight']/name_energy.pkl多的文件中\n
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
               doweight='',
               name='',
               select_branchs=[],
               select_values=[],
               reject_branchs=[],
               reject_values=[]):
        '内部调用函数'
        # 输出信息
        hprint.pline('Building TH1D')
        hprint.ppoint('Source', data)
        hprint.ppoint('Branch', branch)
        # 得到cut后的tree
        ntree = htree.tree_cut(self.trees[data], self.cuts, docuts)
        for selecti in range(len(select_branchs)):
            ntree = htree.tree_select(ntree,
                                      select_branchs[selecti],
                                      select_values[selecti])
        for rejecti in range(len(reject_branchs)):
            ntree = htree.tree_reject(ntree,
                                      reject_branchs[rejecti],
                                      reject_values[rejecti])
        # 新建root文件,hist对象
        tfilename = 'ftemp/root/%s_%s_%s.root' % (data, branch, name)
        histname = '%s_%s' % (data, branch)
        inter = self.cuts[branch]['inter']
        left = self.cuts[branch]['mass'] - self.cuts[branch]['range']
        right = self.cuts[branch]['mass'] + self.cuts[branch]['range']
        num = len(ntree[branch])
        # 开始填入直方图
        if (doweight == ''):
            hprint.ppoint('Weight', 'NO')
            hroot.hist1d(name_tfile=tfilename,
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
                for name in self.weights:
                    factor = factor * ntree[name][i]
                weight.append(factor)
            hroot.hist1d(name_tfile=tfilename,
                         name_hist=histname,
                         inter=inter,
                         left=left,
                         right=right,
                         data=ntree[branch],
                         weight=weight)
        hprint.pstar()
        return (tfilename, histname)

    def hist2d(self,
               data='',
               branch1='',
               branch2='',
               docuts=[],
               doweight='',
               name='',
               select_branchs=[],
               select_values=[],
               reject_branchs=[],
               reject_values=[]):
        '内部调用函数'
        # 输出信息
        hprint.pline('Building TH1D')
        hprint.ppoint('Source', data)
        hprint.ppoint('Branch1', branch1)
        hprint.ppoint('Branch2', branch2)
        # 得到cut后的tree
        ntree = htree.tree_cut(self.trees[data], self.cuts, docuts)
        for selecti in range(len(select_branchs)):
            ntree = htree.tree_select(ntree,
                                      select_branchs[selecti],
                                      select_values[selecti])
        for rejecti in range(len(reject_branchs)):
            ntree = htree.tree_reject(ntree,
                                      reject_branchs[rejecti],
                                      reject_values[rejecti])
        # 新建root文件,hist对象
        tfilename = 'ftemp/root/%s_%s_%s_%s.root' % (data,
                                                     branch1,
                                                     branch2,
                                                     name)
        histname = '%s_%s_%s' % (data,
                                 branch1,
                                 branch2)
        inter1 = self.cuts[branch1]['inter']
        left1 = self.cuts[branch1]['mass'] - self.cuts[branch1]['range']
        right1 = self.cuts[branch1]['mass'] + self.cuts[branch1]['range']
        inter2 = self.cuts[branch2]['inter']
        left2 = self.cuts[branch2]['mass'] - self.cuts[branch2]['range']
        right2 = self.cuts[branch2]['mass'] + self.cuts[branch2]['range']
        data1 = ntree[branch1]
        data2 = ntree[branch2]
        num = len(data1)
        weight = []
        for i in range(num):
            factor = 1
            for name in self.weights:
                factor = factor * ntree[name][i]
            weight.append(factor)
        # 开始填入直方图
        if (doweight == ''):
            hprint.ppoint('Weight', 'NO')
            output = hroot.hist2d(name_tfile=tfilename,
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
            output = hroot.hist2d(name_tfile=tfilename,
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
        return output

    def tree1d(self,
               data='',
               branch='',
               docuts=[],
               name=''):
        '''
        data为字符，输入数据来源的tree\n
        branch为字符，输入提取的数据的branch名\n
        docuts为列表，输入进行筛选的branch名\n
        name为字符，提供文件名保证名称不重复\n
        作用1：返回列表，[tfile的名字，ttree的名字]\n
        Note：\n
        请在目录ftemp文件夹下建立root文件夹\n
        '''
        # 输出信息
        hprint.pline('Building TTree')
        hprint.ppoint('Source', data)
        hprint.ppoint('Branch', branch)
        # 得到cut后的tree
        ntree = htree.tree_cut(self.trees[data], self.cuts, docuts)
        # 新建root文件,tree对象
        tfilename = 'ftemp/root/%s_%s_%s.root' % (data, branch, name)
        ttreename = '%s_%s' % (data, branch)
        output = hroot.tree1d(name_tfile=tfilename,
                              name_ttree=ttreename,
                              name_branch=branch,
                              data=ntree[branch])
        return output

    def hist(self,
             data='',
             branchs=[],
             docuts=[],
             doweight='',
             name='',
             select_branchs=[],
             select_values=[],
             reject_branchs=[],
             reject_values=[]):
        '''
        data为字符，输入数据来源的tree\n
        branchs为列表，输入提取的数据的branch名\n
        docuts为列表，输入进行筛选的branch名\n
        doweight为字符，如果不为空，则进行weighting\n
        name为字符，提供文件名保证名称不重复\n
        作用1：返回列表，[tfile的名字，thist的名字]\n
        Note：\n
        请在目录ftemp文件夹下建立root文件夹
        '''
        if(len(branchs) == 1):
            output = self.hist1d(data,
                                 branchs[0],
                                 docuts,
                                 doweight,
                                 name,
                                 select_branchs=select_branchs,
                                 select_values=select_values,
                                 reject_branchs=reject_branchs,
                                 reject_values=reject_values)
        if(len(branchs) == 2):
            output = self.hist2d(data,
                                 branchs[0],
                                 branchs[1],
                                 docuts,
                                 doweight,
                                 name,
                                 select_branchs=select_branchs,
                                 select_values=select_values,
                                 reject_branchs=reject_branchs,
                                 reject_values=reject_values)
        return output

    def statis(self,
               data='',
               docuts=[],
               doweight=''):
        '''
        data为字符，输入要进行统计的tree名\n
        docuts为列表，输入要进行cut的branch名\n
        doweight为字符，如不为空，则进行weighting\n
        作用1：返回数值，为统计一个tree筛选后的加权总数\n
        '''
        # 输出信息
        hprint.pline('Getting entries of a tree')
        hprint.ppoint('Source', data)
        # 得到cut后的tree
        ntree = htree.tree_cut(self.trees[data], self.cuts, docuts)
        # 初始化统计
        output = 0
        for i in ntree:
            num = len(ntree[i])
        # 开始填入直方图
        if (doweight == ''):
            hprint.ppoint('Weight', 'NO')
        else:
            hprint.ppoint('Weight', 'YES')
        for i in range(num):
            # 填入非weight数量
            if (doweight == ''):
                output += 1
            # 填入weight数量
            else:
                factor = 1
                for name in self.weights:
                    factor = factor * ntree[name][i]
                output += factor
        hprint.pstar()
        return float(output)

    def title(self,
              branch=''):
        '''
        branch为字符，输入要提取坐标轴的数据\n
        作用1：返回字典，['xtitle':横坐标字符串，'ytitle':纵坐标字符串]\n
        '''
        output = htree.branch_title(self.cuts, branch)
        return output

    def get_tree(self, name):
        return self.trees[name]
