# -*- coding: UTF-8 -*-
# Public package
import os
import re
import copy
import numpy
# Private package
import hdata as hdata
import headpy.hfile as hfile


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
    project_source_path = argv['project_source_path']
    project_source_name = argv['project_source_name']
    project_path = argv['project_path']
    project_name = argv['project_name']
    root_path_data = argv['root_path_data']
    root_name_data = argv['root_name_data']
    root_path_mc = argv['root_path_mc']
    root_name_mc = argv['root_name_mc']
    input_option_string = copy.deepcopy(argv['input_option_string'])
    input_option_value = copy.deepcopy(argv['input_option_value'])
    input_constant = copy.deepcopy(argv['input_constant'])
    input_parameter = copy.deepcopy(argv['input_parameter'])
    file_execute = argv['file_execute']
    # 1. 初始化拟合
    origin_path = os.getcwd()
    mydata = MYDATA()
    # 2. 拷贝资料文件
    hfile.copy_folder(source_path=project_source_path,
                      source_name=project_source_name,
                      path=project_path,
                      name=project_name)
    # 2. 拷贝root文件
    hfile.copy_file(source_path=root_path_data,
                    source_name=root_name_data,
                    path='%s/%s/%s' % (project_path, project_name, 'data'),
                    name='data.root')
    hfile.copy_file(source_path=root_path_mc,
                    source_name=root_name_mc,
                    path='%s/%s/%s' % (project_path, project_name, 'data'),
                    name='mc.root')
    # 2. 变更执行地址
    os.chdir('%s/%s' % (project_path, project_name))
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
        print('Info from hpwa.dopwa: Missing output file.')
    try:
        mydata.output_parameter = copy.deepcopy(hdata.read_parameter('output_parameter.txt'))
    except:
        print('Info from hpwa.dopwa: Missing output file.')
    try:
        mydata.least_likelihood = copy.deepcopy(hdata.read_likelihood('output_fitresult.txt'))
    except:
        print('Info from hpwa.dopwa: Missing output file.')
    try:
        mydata.fraction = copy.deepcopy(hdata.read_matrix('output_fraction.txt'))
    except:
        print('Info from hpwa.dopwa: Missing output file.')
    try:
        mydata.correlation = copy.deepcopy(hdata.read_correlation('minimum_covariance.txt'))
        mydata.output_parameter.add_correlation(mydata.correlation)
    except:
        print('Info from hpwa.dopwa: Missing output file.')
    # 4. 删除大体积文件
    os.system('rm %s' % (file_execute))
    os.system('rm -r data')
    # 4. 结束
    os.chdir(origin_path)
    return mydata


def dopwa_amplitude(**argv):
    '拟合时，返回data.root的振幅'
    # 读取 argv
    project_source_path = argv['project_source_path']
    project_source_name = argv['project_source_name']
    project_path = argv['project_path']
    project_name = argv['project_name']
    root_path_data = argv['root_path_data']
    root_name_data = argv['root_name_data']
    root_path_mc = argv['root_path_mc']
    root_name_mc = argv['root_name_mc']
    input_option_string = copy.deepcopy(argv['input_option_string'])
    input_option_value = copy.deepcopy(argv['input_option_value'])
    input_constant = copy.deepcopy(argv['input_constant'])
    input_parameter = copy.deepcopy(argv['input_parameter'])
    file_execute = argv['file_execute']
    # 1. 初始化拟合
    origin_path = os.getcwd()
    # 2. 拷贝资料文件
    hfile.copy_folder(source_path=project_source_path,
                      source_name=project_source_name,
                      path=project_path,
                      name=project_name)
    # 2. 拷贝root文件
    hfile.copy_file(source_path=root_path_data,
                    source_name=root_name_data,
                    path='%s/%s/%s' % (project_path, project_name, 'data'),
                    name='data.root')
    hfile.copy_file(source_path=root_path_mc,
                    source_name=root_name_mc,
                    path='%s/%s/%s' % (project_path, project_name, 'data'),
                    name='mc.root')
    # 2. 变更执行地址
    os.chdir('%s/%s' % (project_path, project_name))
    # 2. 写入初值文件
    hdata.write_option('input_option_string.txt', input_option_string)
    hdata.write_option('input_option_value.txt', input_option_value)
    hdata.write_parameter('input_constant.txt', input_constant)
    hdata.write_parameter('input_parameter.txt', input_parameter)
    # 3. 开始执行拟合
    os.system('./%s | tee log.txt' % (file_execute))
    # 4. 读取振幅文件
    output = hfile.txt_readlines('output_amplitude_data.txt')
    new_output = []
    for i in range(input_option_value['number_data']):
        new_output.append(float(re.match(r'(.*)\n', output[i]).group(1)))
    output = new_output
    ######################################## 读取振幅文件 ########################################
    # 4. 删除大体积文件
    os.system('rm %s' % (file_execute))
    os.system('rm -r data')
    # 4. 结束
    os.chdir(origin_path)
    return output


def dopwa_plot(target_folder, target_file, **argv):
    '在拟合时，转移图片文件'
    # 读取 argv
    project_source_path = argv['project_source_path']
    project_source_name = argv['project_source_name']
    project_path = argv['project_path']
    project_name = argv['project_name']
    root_path_data = argv['root_path_data']
    root_name_data = argv['root_name_data']
    root_path_mc = argv['root_path_mc']
    root_name_mc = argv['root_name_mc']
    input_option_string = copy.deepcopy(argv['input_option_string'])
    input_option_value = copy.deepcopy(argv['input_option_value'])
    input_constant = copy.deepcopy(argv['input_constant'])
    input_parameter = copy.deepcopy(argv['input_parameter'])
    file_execute = argv['file_execute']
    # 1. 初始化拟合
    origin_path = os.getcwd()
    # 2. 拷贝资料文件
    hfile.copy_folder(source_path=project_source_path,
                      source_name=project_source_name,
                      path=project_path,
                      name=project_name)
    # 2. 拷贝root文件
    hfile.copy_file(source_path=root_path_data,
                    source_name=root_name_data,
                    path='%s/%s/%s' % (project_path, project_name, 'data'),
                    name='data.root')
    hfile.copy_file(source_path=root_path_mc,
                    source_name=root_name_mc,
                    path='%s/%s/%s' % (project_path, project_name, 'data'),
                    name='mc.root')
    # 2. 变更执行地址
    os.chdir('%s/%s' % (project_path, project_name))
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
    hfile.copy_file(source_path='.',
                    source_name='output.root',
                    path=target_folder,
                    name=target_file)
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
