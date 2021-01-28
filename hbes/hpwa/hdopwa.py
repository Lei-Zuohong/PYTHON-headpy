# -*- coding: UTF-8 -*-
# Public package
import os
import re
import copy
import numpy
# Private package
import headpy.hfile as hfile
try:
    import headpy.hbes.hpwa.hdata as hdata
except:
    import hdata as hdata


class MYDATA():
    def __init__(self):
        self.option_value = {}
        self.option_string = {}

        self.input_parameter = {}
        self.input_constant = {}
        self.output_parameter = {}
        self.output_constant = {}

        self.fraction = [[]]
        self.correlation = [[]]

        self.least_likelihood = 0

        self.amplitude = []


def dopwa(**argv):
    '进行一次拟合操作，返回结果类'
    # 读取 argv
    project_source = argv['project_source']
    project_target = argv['project_target']
    root_data = argv['root_data']
    root_mc = argv['root_mc']

    input_option_string = copy.deepcopy(argv['input_option_string'])
    input_option_value = copy.deepcopy(argv['input_option_value'])
    input_constant = copy.deepcopy(argv['input_constant'])
    input_parameter = copy.deepcopy(argv['input_parameter'])

    file_execute = argv['file_execute']
    # 1. 初始化拟合
    origin_path = os.getcwd()
    mydata = MYDATA()
    # 2. 拷贝资料文件
    hfile.copy_folder(source=project_source,
                      target=project_target)
    # 2. 拷贝root文件
    hfile.copy_file(source=root_data,
                    target='%s/%s/data.root' % (project_target, 'data'))
    hfile.copy_file(source=root_mc,
                    target='%s/%s/mc.root' % (project_target, 'data'))
    # 2. 变更执行地址
    os.chdir('%s' % (project_target))
    # 2. 写入初值文件
    hdata.write_option('input_option_string.txt', input_option_string)
    hdata.write_option('input_option_value.txt', input_option_value)
    hdata.write_parameter('input_constant.txt', input_constant)
    hdata.write_parameter('input_parameter.txt', input_parameter)
    mydata.option_string = copy.deepcopy(input_option_string)
    mydata.option_value = copy.deepcopy(input_option_value)
    mydata.input_constant = copy.deepcopy(input_constant)
    mydata.input_parameter = copy.deepcopy(input_parameter)
    # 3. 开始执行拟合
    os.system('./%s | tee log.txt' % (file_execute))
    # 4. 读取末值文件
    try:
        mydata.output_constant = copy.deepcopy(hdata.read_parameter('output_constant.txt'))
    except:
        print('Info from hpwa.dopwa: Missing file output_constant.')
    try:
        mydata.output_parameter = copy.deepcopy(hdata.read_parameter('output_parameter.txt'))
    except:
        print('Info from hpwa.dopwa: Missing file output_parameter.')
    try:
        mydata.least_likelihood = copy.deepcopy(hdata.read_likelihood('output_fitresult.txt'))
    except:
        print('Info from hpwa.dopwa: Missing file output_fitresult')
    try:
        mydata.fraction = copy.deepcopy(hdata.read_matrix('output_fraction.txt'))
    except:
        print('Info from hpwa.dopwa: Missing file output_fraction.')
    try:
        mydata.amplitude = hdata.read_amplitude('output_amplitude_data.txt', input_option_value['number_data'])
    except:
        print('Info from hpwa.dopwa: Missing file output_amplitude_data.txt')
    try:
        mydata.correlation = copy.deepcopy(hdata.read_correlation('minimum_covariance.txt'))
        mydata.output_parameter.add_correlation(mydata.correlation)
    except:
        print('Info from hpwa.dopwa: Missing file minimum_covariance.')
    # 4. 删除大体积文件
    os.system('rm %s' % (file_execute))
    os.system('rm -r data')
    # 4. 结束
    os.chdir(origin_path)
    return mydata


def dopwa_plot(target, **argv):
    '在拟合时，转移图片文件'
    # 读取 argv
    project_source = argv['project_source']
    project_target = argv['project_target']
    root_data = argv['root_data']
    root_mc = argv['root_mc']

    input_option_string = copy.deepcopy(argv['input_option_string'])
    input_option_value = copy.deepcopy(argv['input_option_value'])
    input_constant = copy.deepcopy(argv['input_constant'])
    input_parameter = copy.deepcopy(argv['input_parameter'])

    file_execute = argv['file_execute']
    # 1. 初始化拟合
    origin_path = os.getcwd()
    mydata = MYDATA()
    # 2. 拷贝资料文件
    hfile.copy_folder(source=project_source,
                      target=project_target)
    # 2. 拷贝root文件
    hfile.copy_file(source=root_data,
                    target='%s/%s/data.root' % (project_target, 'data'))
    hfile.copy_file(source=root_mc,
                    target='%s/%s/mc.root' % (project_target, 'data'))
    # 2. 变更执行地址
    os.chdir('%s' % (project_target))
    # 2. 写入初值文件
    hdata.write_option('input_option_string.txt', input_option_string)
    hdata.write_option('input_option_value.txt', input_option_value)
    hdata.write_parameter('input_constant.txt', input_constant)
    hdata.write_parameter('input_parameter.txt', input_parameter)
    # 3. 开始执行拟合
    os.system('./%s | tee log.txt' % (file_execute))
    # 4. 删除大体积文件
    os.system('rm %s' % (file_execute))
    os.system('rm -r data')
    # 4. 转移文件
    hfile.copy_file(source='./output.root',
                    target=target)
    # 4. 结束
    os.chdir(origin_path)
    return 1


def dopwa_spread(nrandom, **argv):
    # 产生随机初始参数放入列表
    input_parameter = argv['input_parameter']
    multi_input_parameter = input_parameter.generate_random_spread(nrandom)
    # 多次拟合得到最佳结果
    best_likelihood = 0
    best_input_parameter = 0
    for use_input_parameter in multi_input_parameter:
        argv['input_parameter'] = use_input_parameter
        result = dopwa(**argv)
        if(result.least_likelihood < best_likelihood):
            best_likelihood = result.least_likelihood
            best_input_parameter = copy.deepcopy(use_input_parameter)
        del result
    # 进行一次最优拟合结果
    argv['input_parameter'] = best_input_parameter
    output = dopwa(**argv)
    return output
