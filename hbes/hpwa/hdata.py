# -*- coding: UTF-8 -*-
# Public package
import re
import copy
import numpy
import random
import scipy.stats
import scipy.linalg
# Private package
import headpy.hfile as hfile


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
        if(not hasattr(self, 'correlation')):
            print('Error: no correlation imported')
            exit(0)
        new_data = {}
        temp_num = 0
        temp_names = []
        for name in self.names:
            if(self.parameters[name].error <= 0.0):
                new_data[name] = scipy.stats.norm.rvs(loc=self.parameters[name].value,
                                                      scale=0,
                                                      size=(num))
            else:
                new_data[name] = scipy.stats.norm.rvs(loc=self.parameters[name].value,
                                                      scale=self.parameters[name].error,
                                                      size=(num))
                temp_num += 1
                temp_names.append(name)
        if(len(self.correlation) != temp_num):
            print('Error: not match parameter numbers of correlation')
            exit(0)
        value_matrix = numpy.array([new_data[temp_names[i]] for i in range(temp_num)])
        eigen_value, eigen_vector = scipy.linalg.eigh(self.correlation)
        correction = numpy.dot(eigen_vector, numpy.diag(numpy.sqrt(eigen_value)))
        value_matrix = numpy.dot(correction, value_matrix)
        for i in range(temp_num):
            new_data[temp_names[i]] = value_matrix[i]
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


def write_option(file_name, dict_option):
    '把dictionary（单值）对象写入文件'
    keys = dict_option.keys()
    keys.sort()
    output = ''
    for key in keys:
        output += '{:<25}'.format(key)
        output += '{:<20}'.format(dict_option[key])
        output += '\n'
    with open(file_name, 'w') as outfile:
        outfile.write(output)


def show_parameter(parameters):
    output = ''
    for name in parameters.names:
        output += '{:<25}'.format(parameters.parameters[name].name)
        output += ' = '
        output += '{:<15}'.format('%.6f' % (parameters.parameters[name].value))
        output += '{:<15}'.format('%.6f' % (parameters.parameters[name].error))
        output += '{:<15}'.format('%.6f' % (parameters.parameters[name].limitl))
        output += '{:<15}'.format('%.6f' % (parameters.parameters[name].limitr))
        output += '\n'
    print(output)


def write_parameter(file_name, parameters):
    output = ''
    for name in parameters.names:
        output += '{:<25}'.format(parameters.parameters[name].name)
        output += ' = '
        output += '{:<15}'.format('%.6f' % (parameters.parameters[name].value))
        output += '{:<15}'.format('%.6f' % (parameters.parameters[name].error))
        output += '{:<15}'.format('%.6f' % (parameters.parameters[name].limitl))
        output += '{:<15}'.format('%.6f' % (parameters.parameters[name].limitr))
        output += '\n'
    with open(file_name, 'w') as outfile:
        outfile.write(output)


def read_parameter(file_name):
    output = PARAMETERS()
    lines = hfile.txt_readlines(file_name)
    for line in lines:
        method = r'(\S*)\s*=\s*(\S*)\s*(\S*)\s*(\S*)\s*(\S*)'
        check = re.match(method, line)
        if(check):
            try:
                parameter = PARAMETER(name=check.group(1),
                                      value=float(check.group(2)),
                                      error=float(check.group(3)),
                                      limitl=float(check.group(4)),
                                      limitr=float(check.group(5)))
                if(re.match(r'(.*)space', parameter.name)):
                    continue
                if(re.match(r'(.*)_phase', parameter.name)):
                    parameter.value = adjust_phase_zero(parameter.value)
                    parameter.limitl = -6.28
                    parameter.limitr = 6.28
                output.add(parameter)
            except:
                pass
    return output


def read_correlation(file_name):
    lines = hfile.txt_readlines(file_name)
    for i in range(len(lines)):
        if(re.match(r'MnUserCovariance Parameter correlations:', lines[i])):
            line_start = i + 2
    for i in range(len(lines)):
        if(i < line_start + 2): continue
        if(len(lines[i]) < 2):
            line_end = i - 1
            break
    file_txt = ''
    for i in range(len(lines)):
        if(i >= line_start and i < line_end):
            file_txt += lines[i]
            file_txt += '\n'
        elif(i == line_end):
            file_txt += lines[i]
    hfile.txt_write('temp.txt', file_txt)
    output = numpy.loadtxt('temp.txt', dtype=numpy.float)
    return output.tolist()


def read_matrix(file_name):
    length = 0
    massages = []
    lines = hfile.txt_readlines(file_name)
    for line in lines:
        method = r'(\S*)\s*(\S*)\s*(\S*)'
        check = re.match(method, line)
        if(check):
            num1 = int(check.group(1))
            num2 = int(check.group(2))
            num3 = float(check.group(3))
            massages.append([num1, num2, num3])
            if(num1 > length): length = num1
            if(num2 > length): length = num2
    output = numpy.zeros([length + 1, length + 1])
    for massage in massages:
        output[massage[0]][massage[1]] = massage[2]
    output = output.tolist()
    return output


def read_likelihood(file_name):
    output = 0
    lines = hfile.txt_readlines(file_name)
    for line in lines:
        method = r'Best Likelihood:(.*)'
        check = re.match(method, line)
        if(check):
            output = float(check.group(1))
    return output


def adjust_phase_zero(value):
    pi = 3.1415926
    output = value
    while(output > pi): output -= 2 * pi
    while(output < 0 - pi): output += 2 * pi
    return output


def adjust_phase_pi(value):
    pi = 3.1415926
    output = value
    while(output > 2 * pi): output -= 2 * pi
    while(output < 0): output += 2 * pi
    return output
