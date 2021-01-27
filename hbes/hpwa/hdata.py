# -*- coding: UTF-8 -*-
# Public package
import re
import copy
import numpy
# Private package
import headpy.hfile as hfile
import headpy.hmath.hstatis as hstatis


def write_option(file_name, dict_option):
    '把dictionary（单值）对象写入文件'
    keys = sorted(dict_option)
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
    output = hstatis.PARAMETERS()
    lines = hfile.txt_readlines(file_name)
    for line in lines:
        method = r'(\S*)\s*=\s*(\S*)\s*(\S*)\s*(\S*)\s*(\S*)'
        check = re.match(method, line)
        if(check):
            try:
                parameter = hstatis.PARAMETER(name=check.group(1),
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


def read_amplitude(file_name, num):
    output = hfile.txt_readlines(file_name)
    new_output = []
    for i in range(num):
        new_output.append(float(re.match(r'(.*)\n', output[i]).group(1)))
    return new_output


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
