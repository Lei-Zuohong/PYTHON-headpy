# -*- coding: UTF-8 -*-
# Public package
import os
import re
import sys
import copy
import numpy
import random
# Private package
import hdata as hdata
import headpy.hfile as hfile


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
    '不进行拟合，直接返回data.root的振幅'
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
    origin_path = os.getcwd()
    mydata = MYDATA()
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
    '不进行拟合，直接进行作图'
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
    return mydata


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


class MYWAVE():
    def __init__(self, wave_possible=[], wave_consider=[], wave_nominal=[], wave_save=[]):
        self.wave_possible = copy.deepcopy(wave_possible)
        self.wave_consider = copy.deepcopy(wave_consider)
        self.wave_nominal = copy.deepcopy(wave_nominal)
        self.wave_save = copy.deepcopy(wave_save)

    def get_nominal_option(self, input_option_value):
        '''
        字典形式输出一个wave是否被添加
        '''
        output = copy.deepcopy(input_option_value)
        for wave in self.wave_possible:
            if(wave in self.wave_nominal):
                output['add_%s' % (wave)] = 1
            else:
                output['add_%s' % (wave)] = 0
        return output

    def get_check_option(self, input_option_value, wave_check):
        '''
        字典形式输出一个wave是否被添加，对于指定的wave，变更其结果
        '''
        output = copy.deepcopy(input_option_value)
        for wave in self.wave_possible:
            if(wave in self.wave_nominal):
                output['add_%s' % (wave)] = 1
            else:
                output['add_%s' % (wave)] = 0
        if(wave_check in self.wave_possible):
            output['add_%s' % (wave_check)] = 1 - output['add_%s' % (wave_check)]
        return output

    def give_fraction_name(self, input_list):
        '将一个fraction矩阵转化为波名字作为索引的字典'
        output_dict = {}
        output_wave = []
        # 按顺序整合wave
        for wave in self.wave_possible:
            if(wave in self.wave_nominal):
                output_wave.append(wave)
        # 检测矩阵长度是否一致
        length = len(input_list)
        if(length != len(self.wave_nominal)):
            print("Error: Fraction matrix with wrong length!")
            exit()
        for i in range(length):
            output_dict[output_wave[i]] = {}
            for j in range(length):
                output_dict[output_wave[i]][output_wave[j]] = input_list[i][j]
        return output_dict


class MYSCANER():
    def __init__(self,
                 l1=0., r1=0., inter1=10,
                 l2=0., r2=0., inter2=10):
        self.l1 = float(l1)
        self.r1 = float(r1)
        self.inter1 = int(inter1)
        self.l2 = float(l2)
        self.r2 = float(r2)
        self.inter2 = int(inter2)
        # 计算输入参数
        self.d1 = (self.r1 - self.l1) / self.inter1
        self.d2 = (self.r2 - self.l2) / self.inter2
        # 一维坐标序列
        self.plot1dx = numpy.zeros(self.inter1)
        self.plot1dy = numpy.zeros(self.inter2)
        for i1 in range(self.inter1):
            self.plot1dx[i1] = self.l1 + self.d1 * i1
        for i2 in range(self.inter2):
            self.plot1dy[i2] = self.l2 + self.d2 * i2
        # 二维坐标序列
        self.plot2dx = numpy.zeros([self.inter1, self.inter2])
        self.plot2dy = numpy.zeros([self.inter1, self.inter2])
        self.plot2dz = numpy.zeros([self.inter1, self.inter2])
        for i1 in range(self.inter1):
            for i2 in range(self.inter2):
                self.plot2dx[i1][i2] = self.l1 + self.d1 * i1
                self.plot2dy[i1][i2] = self.l2 + self.d2 * i2

    def get_xy(self):
        outputx = copy.deepcopy(self.plot1dx)
        outputy = copy.deepcopy(self.plot1dy)
        return outputx, outputy

    def set_z(self, data):
        for i1 in range(self.inter1):
            for i2 in range(self.inter2):
                self.plot2dz[i1][i2] = data[i1][i2]

    def get_optimize_x(self):
        outputz = numpy.zeros(self.inter1)
        for i1 in range(self.inter1):
            temp = 0
            for i2 in range(self.inter2):
                if(self.plot2dz[i1][i2] < temp):
                    temp = self.plot2dz[i1][i2]
            outputz[i1] = temp
        return outputz

    def get_optimize_y(self):
        outputz = numpy.zeros(self.inter1)
        for i2 in range(self.inter2):
            temp = 0
            for i1 in range(self.inter1):
                if(self.plot2dz[i1][i2] < temp):
                    temp = self.plot2dz[i1][i2]
            outputz[i2] = temp
        return outputz


class MYPWA():

    def __init__(self, project):
        # 输入folder
        self.path = os.getcwd()
        self.path_program_source = self.path + '/program_source'
        self.path_program_execute = self.path + '/program_execute'
        self.path_root_input = self.path + '/root_input'
        self.path_root_output = self.path + '/root_output'
        self.project = project

    # Setting
    def set_energy_root(self, energy):
        # 根据energy设定root文件
        self.energy = energy
        if('%1.4f_data.root' % (energy) in os.listdir(self.path_root_input) and
           '%1.4f_mc.root' % (energy) in os.listdir(self.path_root_input)):
            self.root_data = '%1.4f_data.root' % (energy)
            self.root_mc = '%1.4f_mc.root' % (energy)
        else:
            print('Error: Missing root input file!')
            sys.exit()

    def set_option_value(self, input_option_value):
        self.input_option_value = copy.deepcopy(input_option_value)

    def set_option_string(self, input_option_string):
        self.input_option_string = copy.deepcopy(input_option_string)

    def set_parameter(self, input_parameter):
        self.input_parameter = copy.deepcopy(input_parameter)

    def set_constant(self, input_constant):
        self.input_constant = copy.deepcopy(input_constant)

    def set_waves(self, wave_possible=[], wave_consider=[], wave_nominal=[], wave_save=[]):
        self.mywave = MYWAVE(wave_possible=wave_possible,
                             wave_consider=wave_consider,
                             wave_nominal=wave_nominal,
                             wave_save=wave_save)

    def set_output_step(self, file_name):
        self.output_step = '%s/%s' % (self.path, file_name)
        with open(self.output_step, 'w') as outfile:
            outfile.write('Fitting start:\n\n')

    # Fitting

    def get_fit_nominal(self):  # 进行一次正常拟合
        output = dopwa(project_source_path=self.path_program_source,
                       project_source_name=self.project,
                       project_path=self.path_program_execute,
                       project_name='%1.4f_nominal' % (self.energy),
                       root_path_data=self.path_root_input,
                       root_name_data=self.root_data,
                       root_path_mc=self.path_root_input,
                       root_name_mc=self.root_mc,
                       input_option_string=self.input_option_string,
                       input_option_value=self.mywave.get_nominal_option(self.input_option_value),
                       input_constant=self.input_constant,
                       input_parameter=self.input_parameter,
                       file_execute=self.project)
        output.fraction = copy.deepcopy(self.mywave.give_fraction_name(output.fraction))
        return output

    def get_fit_nominal_spread(self):  # 进行一次撒点拟合
        output = dopwa_spread(50,
                              project_source_path=self.path_program_source,
                              project_source_name=self.project,
                              project_path=self.path_program_execute,
                              project_name='%1.4f_nominal' % (self.energy),
                              root_path_data=self.path_root_input,
                              root_name_data=self.root_data,
                              root_path_mc=self.path_root_input,
                              root_name_mc=self.root_mc,
                              input_option_string=self.input_option_string,
                              input_option_value=self.mywave.get_nominal_option(self.input_option_value),
                              input_constant=self.input_constant,
                              input_parameter=self.input_parameter,
                              file_execute=self.project)
        output.fraction = copy.deepcopy(self.mywave.give_fraction_name(output.fraction))
        return output

    def get_fit_amplitude(self, target_folder='root_fit4c'):  # 读取指定文件夹中的root，返回amplitude列表
        new_input_option_value = copy.deepcopy(self.mywave.get_nominal_option(self.input_option_value))
        new_input_parameter = copy.deepcopy(self.input_parameter)
        nums = hfile.pkl_read('%s/%1.4f_entries.pkl' % (target_folder, self.energy))
        new_input_option_value['number_data'] = nums['signal']
        new_input_option_value['do_fit_minuit'] = 0
        new_input_option_value['do_output_amplitude'] = 1
        for parameter in new_input_parameter:
            new_input_parameter[parameter]['error'] = -1

        output = dopwa_amplitude(project_source_path=self.path_program_source,
                                 project_source_name=self.project,
                                 project_path=self.path_program_execute,
                                 project_name='%1.4f_amplitude' % (self.energy),
                                 root_path_data='%s' % (target_folder),
                                 root_name_data='%1.4f_mc.root' % (self.energy),
                                 root_path_mc=self.path_root_input,
                                 root_name_mc=self.root_mc,
                                 input_option_string=self.input_option_string,
                                 input_option_value=new_input_option_value,
                                 input_constant=self.input_constant,
                                 input_parameter=new_input_parameter,
                                 file_execute=self.project)
        if(len(output) != nums['signal']):
            print("Input  entries: %d" % (nums['signal']))
            print("Output entries: %d" % (len(output)))
        return output

    def get_fit_plot(self, target_folder='root_plot'):  # 绘制拟合图片，返回指定文件夹
        new_input_option_value = copy.deepcopy(self.mywave.get_nominal_option(self.input_option_value))
        new_input_option_value['do_output_root'] = 1
        new_input_option_value['do_fit_minuit'] = 0
        output = dopwa_plot(target_folder, '%1.4f.root' % (self.energy),
                            project_source_path=self.path_program_source,
                            project_source_name=self.project,
                            project_path=self.path_program_execute,
                            project_name='%1.4f_plot' % (self.energy),
                            root_path_data=self.path_root_input,
                            root_name_data=self.root_data,
                            root_path_mc=self.path_root_input,
                            root_name_mc=self.root_mc,
                            input_option_string=self.input_option_string,
                            input_option_value=new_input_option_value,
                            input_constant=self.input_constant,
                            input_parameter=self.input_parameter,
                            file_execute=self.project)

    def get_test_significance(self):  # 计算significance
        data_nominal = self.get_fit_nominal()
        self.significance = {}
        for wave in self.mywave.wave_consider:
            print('Checking wave name: %s' % (wave))
            data_check = dopwa(project_source_path=self.path_program_source,
                               project_source_name=self.project,
                               project_path=self.path_program_execute,
                               project_name='%1.4f_%s' % (self.energy, wave),
                               root_path_data=self.path_root_input,
                               root_name_data=self.root_data,
                               root_path_mc=self.path_root_input,
                               root_name_mc=self.root_mc,
                               input_option_string=self.input_option_string,
                               input_option_value=self.mywave.get_check_option(self.input_option_value, wave),
                               input_constant=self.input_constant,
                               input_parameter=self.input_parameter,
                               file_execute=self.project)
            self.significance[wave] = data_nominal.least_likelihood - data_check.least_likelihood
        if(hasattr(self, 'output_step')):
            with open(self.output_step, 'a') as outfile:
                outfile.write('Check significance:\n')
                for wave in self.significance:
                    outfile.write('{:<25} {:<15}\n'.format(wave, self.significance[wave]))
                outfile.write('\n')

    def get_scan(self,
                 parameter='', limitl=0, limitr=1, inter=100):
        outputx = []
        outputy = []
        unit = (limitr - limitl) / inter
        # 重新更改一些参数
        use_parameter = copy.deepcopy(self.input_parameter)
        use_option_value = copy.deepcopy(self.mywave.get_nominal_option(self.input_option_value))
        use_option_value['multifit_times'] = 20
        use_option_value['strategy_level'] = 0
        use_option_value['strategy_times'] = 5000
        nrandom = 10
        for i in range(inter):
            use_value = limitl + i * unit
            use_parameter.parameters[parameter].value = use_value
            use_parameter.parameters[parameter].error = -1
            data = dopwa_spread(project_source_path=self.path_program_source,
                                project_source_name=self.project,
                                project_path=self.path_program_execute,
                                project_name='%1.4f_scan' % (self.energy),
                                root_path_data=self.path_root_input,
                                root_name_data=self.root_data,
                                root_path_mc=self.path_root_input,
                                root_name_mc=self.root_mc,
                                input_option_string=self.input_option_string,
                                input_option_value=use_option_value,
                                input_constant=self.input_constant,
                                input_parameter=use_parameter,
                                file_execute=self.project,
                                nrandom=nrandom)
            outputx.append(use_value)
            outputy.append(data.least_likelihood)
        return [outputx, outputy]

    def get_scan_resonance(self,
                           wave='',
                           parameter1='', limitl1=0, limitr1=1, inter1=100,
                           parameter2='', limitl2=0, limitr2=1, inter2=100):
        myscaner = MYSCANER(l1=limitl1, r1=limitr1, inter1=inter1,
                            l2=limitl2, r2=limitr2, inter2=inter2)
        listx, listy = myscaner.get_xy()
        # 重新更改一些参数
        use_parameter = copy.deepcopy(self.input_parameter)
        use_constant = copy.deepcopy(self.input_constant)
        use_option_value = copy.deepcopy(self.mywave.get_check_option(self.input_option_value, wave))
        use_option_value['multifit_times'] = 20  # 20
        use_option_value['strategy_level'] = 0  # 0
        use_option_value['strategy_times'] = 5000  # 5000
        nrandom = 10  # 10
        # 进行拟合
        outputz = numpy.zeros([int(inter1), int(inter2)])
        for i1, value1 in enumerate(listx):
            for i2, value2 in enumerate(listy):
                print('Iteration: %.4f %.4f' % (value1, value2))
                use_constant.parameters[parameter1].value = value1
                use_constant.parameters[parameter1].error = -1
                use_constant.parameters[parameter2].value = value2
                use_constant.parameters[parameter2].error = -1
                data = dopwa_spread(project_source_path=self.path_program_source,
                                    project_source_name=self.project,
                                    project_path=self.path_program_execute,
                                    project_name='%1.4f_scan' % (self.energy),
                                    root_path_data=self.path_root_input,
                                    root_name_data=self.root_data,
                                    root_path_mc=self.path_root_input,
                                    root_name_mc=self.root_mc,
                                    input_option_string=self.input_option_string,
                                    input_option_value=use_option_value,
                                    input_constant=use_constant,
                                    input_parameter=use_parameter,
                                    file_execute=self.project,
                                    nrandom=nrandom)
                outputz[i1][i2] = data.least_likelihood
        myscaner.set_z(outputz)
        return myscaner

    # Processing

    def check_significance(self):  # 判断significance
        '检查significance是否满足5sigma，返回bool'
        check_minus = 1
        check_plus = 1
        for wave in self.significance:
            if(wave in self.mywave.wave_save): continue
            if(wave in self.mywave.wave_nominal and self.significance[wave] < 0 and self.significance[wave] > -14.372):
                check_minus = 0
            if(wave not in self.mywave.wave_nominal and self.significance[wave] > 14.372):
                check_plus = 0
        check = check_minus * check_plus
        return check

    def adjust_significance(self):  # 调整significance
        '根据significance调整mywave的wave_nominal列表'
        # 得到检测结果
        check_minus = 1
        check_plus = 1
        for wave in self.significance:
            if(wave in self.mywave.wave_save): continue
            if(wave in self.mywave.wave_nominal and self.significance[wave] < 0 and self.significance[wave] > -14.372):
                check_minus = 0
            if(wave not in self.mywave.wave_nominal and self.significance[wave] > 14.372):
                check_plus = 0
        # 先考虑减去波
        if(check_minus == 0):
            save_key = ''
            save_value = -9999
            for wave in self.significance:
                if(wave in self.mywave.wave_save): continue
                if(wave not in self.mywave.wave_nominal): continue
                if(self.significance[wave] > 0): continue
                if (self.significance[wave] > save_value):
                    save_key = wave
                    save_value = self.significance[wave]
            new_nominal = []
            for wave in self.mywave.wave_nominal:
                if(wave != save_key):
                    new_nominal.append(wave)
            self.mywave.wave_nominal = new_nominal
        # 再考虑加上波
        elif(check_plus == 0):
            save_key = ''
            save_value = 0
            for wave in self.significance:
                if(wave in self.mywave.wave_save): continue
                if(wave in self.mywave.wave_nominal): continue
                if(self.significance[wave] < 0): continue
                if (self.significance[wave] > save_value):
                    save_key = wave
                    save_value = self.significance[wave]
            self.mywave.wave_nominal.append(save_key)
        if(hasattr(self, 'output_step')):
            with open(self.output_step, 'a') as outfile:
                outfile.write('Adjust nominal waves:\n')
                for wave in self.mywave.wave_nominal:
                    outfile.write('{:<25}\n'.format(wave))
                outfile.write('\n')

    def dump_significance(self, filename):  # 储存significance
        hfile.pkl_dump(filename, self.significance)

    # Special analysis

    def analysis_bump(self,  # 得到关于一个关于参数扫描的细致图片
                      parameter_name='rho1450pi_phase',
                      parameter_left=0.0,
                      parameter_right=1.0,
                      parameter_inter=100,
                      target_folder=''):
        new_input_option_value = copy.deepcopy(self.mywave.get_nominal_option(self.input_option_value))
        new_input_option_value['do_output_root'] = 1
        new_input_option_value['do_fit_minuit'] = 0
        new_input_parameter = copy.deepcopy(self.input_parameter)
        for i in range(parameter_inter):
            temp_value = parameter_left + float(i) / parameter_inter * (parameter_right - parameter_left)
            new_input_parameter[parameter_name]['value'] = temp_value
            output = dopwa_plot(target_folder, '%1.4f_%03d.root' % (self.energy, i),
                                project_source_path=self.path_program_source,
                                project_source_name=self.project,
                                project_path=self.path_program_execute,
                                project_name='%1.4f_plot' % (self.energy),
                                root_path_data=self.path_root_input,
                                root_name_data=self.root_data,
                                root_path_mc=self.path_root_input,
                                root_name_mc=self.root_mc,
                                input_option_string=self.input_option_string,
                                input_option_value=new_input_option_value,
                                input_constant=self.input_constant,
                                input_parameter=new_input_parameter,
                                file_execute=self.project)