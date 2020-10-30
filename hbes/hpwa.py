# -*- coding: UTF-8 -*-
# Public package
import os
import re
# Private package
import headpy.hfile.hstring as hstring
import headpy.hfile.hoperate as hoperate


def copy_list(empty_list, input_list):
    for i in input_list:
        empty_list.append(i)


def copy_dict(empty_dict, input_dict):
    for i in input_dict:
        empty_dict[i] = input_dict[i]


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


def write_parameter(file_name, dict_option):
    '把dictionary（参数）对象写入文件'
    keys = dict_option.keys()
    keys.sort()
    output = ''
    for key in keys:
        output += '{:<25}'.format(key)
        output += ' = '
        output += '{:<15}'.format(dict_option[key]['value'])
        output += '{:<15}'.format(dict_option[key]['error'])
        output += '{:<15}'.format(dict_option[key]['limitl'])
        output += '{:<15}'.format(dict_option[key]['limitr'])
        output += '\n'
    with open(file_name, 'w') as outfile:
        outfile.write(output)


def read_parameter(file_name):
    output = {}
    lines = hstring.readlines(file_name)
    for line in lines:
        method = r'(.*)=(.*) (.*) (.*) (.*)'
        check = re.match(method, line)
        if(check):
            name = check.group(1)
            value = float(check.group(2))
            error = float(check.group(3))
            limitl = float(check.group(4))
            limitr = float(check.group(5))
            output[name] = {}
            output[name]['value'] = value
            output[name]['error'] = error
            output[name]['limitl'] = limitl
            output[name]['limitr'] = limitr
    return output


def read_likelyhood(file_name):
    output = 0
    lines = hstring.readlines(file_name)
    for line in lines:
        method = r'Best Likelihood:(.*)'
        check = re.match(method, line)
        if(check):
            output = float(check.group(1))
    return output


class MYDATA():
    def __init__(self):
        self.option_value = {}
        self.option_string = {}

        self.input_parameter = {}
        self.input_constant = {}
        self.output_parameter = {}
        self.output_constant = {}

        self.least_likelyhood = 0


def dopwa(project_source_path='',
          project_source_name='',
          project_path='',
          project_name='',
          root_path='',
          root_name_data='',
          root_name_mc='',
          input_option_string={},
          input_option_value={},
          input_constant={},
          input_parameter={},
          file_execute=''):
    '进行一次拟合操作，返回结果类'
    mydata = MYDATA()
    # 拷贝资料文件
    hoperate.copy_folder(source_path=project_source_path,
                         source_name=project_source_name,
                         path=project_path,
                         name=project_name)
    # 拷贝root文件
    hoperate.copy_file(source_path=root_path,
                       source_name=root_name_data,
                       path='%s/%s/%s' % (project_path, project_name, 'data'),
                       name='data.root')
    hoperate.copy_file(source_path=root_path,
                       source_name=root_name_mc,
                       path='%s/%s/%s' % (project_path, project_name, 'data'),
                       name='mc.root')
    # 变更执行地址
    os.chdir('%s/%s' % (project_path, project_name))
    # 写入初值文件
    write_option(file_name='input_option_string.txt', dict_option=input_option_string)
    write_option(file_name='input_option_value.txt', dict_option=input_option_value)
    write_parameter(file_name='input_constant.txt', dict_option=input_constant)
    write_parameter(file_name='input_parameter.txt', dict_option=input_parameter)
    copy_dict(mydata.option_string, input_option_string)
    copy_dict(mydata.option_value, input_option_value)
    copy_dict(mydata.input_constant, input_constant)
    copy_dict(mydata.input_parameter, input_parameter)
    # 开始执行
    os.system('./%s | tee log.txt' % (file_execute))
    # 读取末值文件
    copy_dict(mydata.output_constant, read_parameter('output_constant.txt'))
    copy_dict(mydata.output_parameter, read_parameter('output_parameter.txt'))
    mydata.least_likelyhood = read_likelyhood('output_fitresult.txt')
    # 返回
    return mydata


class MYPWA():

    self.path = ''
    self.root_input = ''
    self.root_output = ''
    self.program_source = ''
    self.program_execute = ''
    self.energy = 0
    self.path_data = ''
    self.path_mc = ''

    def __init__(self, energy):
        # 输入folder
        self.path = os.getcwd()
        self.root_input = '%s/root_input' % (self.path)
        self.root_output = '%s/root_output' % (self.path)
        self.program_source = '%s/program_source' % (self.path)
        self.program_execute = '%s/program_execute' % (self.path)
        # 输入root file
        if('%1.4f_data.root' % (energy) in os.listdir(self.root_input) and
           '%1.4f_mc.root' % (energy) in os.listdir(self.root_input)):
            self.path_data = '%s/%1.4f_data.root' % (self.root_input, energy)
            self.path_mc = '%s/%1.4f_mc.root' % (self.root_input, energy)
        else:
            print('Error: Missing root input file!')
