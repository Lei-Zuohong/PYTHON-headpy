# -*- coding: UTF-8 -*-
# Public package
import copy
import numpy
import random
import scipy.stats
import scipy.linalg
# Private package


class PARAMETER():
    def __init__(self,
                 name='',
                 value=0.0,
                 error=1.0,
                 limitl=-1.0,
                 limitr=1.0):
        self.name = name
        self.value = value
        self.error = error
        self.limitl = limitl
        self.limitr = limitr

    def set_value(self, value, error, limitl, limitr):
        self.value = value
        self.error = error
        self.limitl = limitl
        self.limitr = limitr

    def __getitem__(self, key):
        output = 0
        exec('output=self.%s' % (key))
        return output

    def __setitem__(self, key, value):
        exec('self.%s = value' % (key))


class PARAMETERS():
    def __init__(self):
        self.names = []
        self.parameters = {}

    def add(self, parameter):
        self.names.append(parameter.name)
        self.parameters[parameter.name] = parameter

    def add_parameters(self, parameters):
        for name in parameters.names:
            if(name not in self.names):
                self.add(parameters.parameters[name])

    def add_correlation(self, correlation):
        self.correlation = correlation

    def add_covariance(self, covariance):
        self.covariance = covariance

    def generate_random(self, num):
        new_data = {}
        for name in self.names:
            if(self.parameters[name].error <= 0.0):
                new_data[name] = scipy.stats.norm.rvs(loc=self.parameters[name].value,
                                                      scale=0,
                                                      size=(num))
            else:
                new_data[name] = scipy.stats.norm.rvs(loc=self.parameters[name].value,
                                                      scale=self.parameters[name].error,
                                                      size=(num))
        output = []
        for i in range(num):
            temp_parameters = copy.deepcopy(self)
            for name in temp_parameters.names:
                temp_parameters.parameters[name].value = new_data[name][i]
                temp_parameters.parameters[name].error = -1.0
            output.append(temp_parameters)
        return output

    def generate_random_correlation(self, num):
        # 检查是否存在关联矩阵
        if(not hasattr(self, 'correlation') and not hasattr(self, 'covariance')):
            print('Error: no correlation or covariance imported')
            exit(0)
        # 生成新的随机数组，其中关联部分中心值暂定为0.0
        new_data = {}
        temp_num = 0
        temp_names = []
        for name in self.names:
            if(self.parameters[name].error <= 0.0):
                new_data[name] = scipy.stats.norm.rvs(loc=self.parameters[name].value,
                                                      scale=0,
                                                      size=(num))
            else:
                new_data[name] = scipy.stats.norm.rvs(loc=0.0,
                                                      scale=1.0,
                                                      size=(num))
                temp_num += 1
                temp_names.append(name)
        # 检查关联参数数量与矩阵是否一致
        if(len(self.correlation) != temp_num):
            print('Error: not match parameter numbers of correlation')
            exit(0)
        # 转换correlation and covariance
        if(hasattr(self, 'correlation')):
            covariance = copy.deepcopy(self.correlation)
            for i1 in range(temp_num):
                for i2 in range(temp_num):
                    covariance[i1][i2] *= self.parameters[temp_names[i1]].error * self.parameters[temp_names[i2]].error
        else:
            covariance = copy.deepcopy(self.covariance)
        # 转换变量，并放回参数
        value_matrix = numpy.array([new_data[temp_names[i]] for i in range(temp_num)])
        eigen_value, eigen_vector = scipy.linalg.eigh(covariance)
        correction = numpy.dot(eigen_vector, numpy.diag(numpy.sqrt(eigen_value)))
        value_matrix = numpy.dot(correction, value_matrix)
        for i in range(temp_num):
            new_data[temp_names[i]] = value_matrix[i] + self.parameters[temp_names[i]].value
        # 输出参数
        output = []
        for i in range(num):
            temp_parameters = copy.deepcopy(self)
            for name in temp_parameters.names:
                temp_parameters.parameters[name].value = new_data[name][i]
                temp_parameters.parameters[name].error = -1.0
            output.append(temp_parameters)
        return output

    def generate_random_spread(self, num):
        new_data = {}
        for name in self.names:
            if(self.parameters[name].error <= 0.0):
                new_data[name] = scipy.stats.norm.rvs(loc=self.parameters[name].value,
                                                      scale=0,
                                                      size=(num))
            else:
                new_data[name] = [random.uniform(self.parameters[name].limitl, self.parameters[name].limitr) for i in range(num)]
        output = []
        for i in range(num):
            temp_parameters = copy.deepcopy(self)
            for name in temp_parameters.names:
                temp_parameters.parameters[name].value = new_data[name][i]
            output.append(temp_parameters)
        return output

    def __getitem__(self, key):
        return self.parameters[key]

    def __setitem__(self, key, value):
        self.parameters[key] = value
