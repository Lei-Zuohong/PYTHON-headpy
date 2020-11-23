# -*- coding: UTF-8 -*-
# Public package
import os
import re
import sys
import copy
import numpy
# Private package
import headpy.hfile as hfile


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
    '读取: parameter = value error limitl limitr 类txt信息'
    output = {}
    lines = hfile.txt_readlines(file_name)
    for line in lines:
        method = r'(\S*)\s*=\s*(\S*)\s*(\S*)\s*(\S*)\s*(\S*)'
        check = re.match(method, line)
        if(check):
            try:
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
            except:
                pass
    return output


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


def read_likelyhood(file_name):
    '读取：Best likelihood: value 类txt信息'
    output = 0
    lines = hfile.txt_readlines(file_name)
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

        self.fraction = [[]]

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
    origin_path = os.getcwd()
    mydata = MYDATA()
    # 拷贝资料文件
    hfile.copy_folder(source_path=project_source_path,
                      source_name=project_source_name,
                      path=project_path,
                      name=project_name)
    # 拷贝root文件
    hfile.copy_file(source_path=root_path,
                    source_name=root_name_data,
                    path='%s/%s/%s' % (project_path, project_name, 'data'),
                    name='data.root')
    hfile.copy_file(source_path=root_path,
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
    mydata.option_string = copy.deepcopy(input_option_string)
    mydata.option_value = copy.deepcopy(input_option_value)
    mydata.input_constant = copy.deepcopy(input_constant)
    mydata.input_parameter = copy.deepcopy(input_parameter)
    # 开始执行
    os.system('./%s | tee log.txt' % (file_execute))
    # 读取末值文件
    mydata.output_constant = copy.deepcopy(read_parameter('output_constant.txt'))
    mydata.output_parameter = copy.deepcopy(read_parameter('output_parameter.txt'))
    mydata.least_likelyhood = copy.deepcopy(read_likelyhood('output_fitresult.txt'))
    mydata.fraction = copy.deepcopy(read_matrix('output_fraction.txt'))
    # 结束
    os.chdir(origin_path)
    return mydata


class MYWAVE():
    def __init__(self, wave_possible=[], wave_consider=[], wave_nomial=[], wave_save=[]):
        self.wave_possible = copy.deepcopy(wave_possible)
        self.wave_consider = copy.deepcopy(wave_consider)
        self.wave_nomial = copy.deepcopy(wave_nomial)
        self.wave_save = copy.deepcopy(wave_save)

    def get_nomial_option(self, input_option_value):
        '''
        字典形式输出一个wave是否被添加
        '''
        output = copy.deepcopy(input_option_value)
        for wave in self.wave_possible:
            if(wave in self.wave_nomial):
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
            if(wave in self.wave_nomial):
                output['add_%s' % (wave)] = 1
            else:
                output['add_%s' % (wave)] = 0
        if(wave_check in self.wave_possible):
            output['add_%s' % (wave_check)] = 1 - output['add_%s' % (wave_check)]
        return output

    def give_fraction_name(self, input_list):
        '''
        将一个fraction矩阵转化为波名字作为索引的字典
        '''
        output_dict = {}
        output_wave = []
        # 按顺序整合wave
        for wave in self.wave_possible:
            if(wave in self.wave_nomial):
                output_wave.append(wave)
        # 检测矩阵长度是否一致
        length = len(input_list)
        if(length != len(self.wave_nomial)):
            print("Error: Fraction matrix with wrong length!")
            exit()
        for i in range(length):
            output_dict[output_wave[i]] = {}
            for j in range(length):
                output_dict[output_wave[i]][output_wave[j]] = input_list[i][j]
        return output_dict


class MYPWA():

    def __init__(self, project):
        # 输入folder
        self.path = os.getcwd()
        self.path_program_source = self.path + '/program_source'
        self.path_program_execute = self.path + '/program_execute'
        self.path_root_input = self.path + '/root_input'
        self.path_root_output = self.path + '/root_output'
        self.path_txt_input = self.path + '/txt_input'
        self.path_txt_output = self.path + '/txt_output'
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

    def set_waves(self, wave_possible=[], wave_consider=[], wave_nomial=[], wave_save=[]):
        self.mywave = MYWAVE(wave_possible=wave_possible,
                             wave_consider=wave_consider,
                             wave_nomial=wave_nomial,
                             wave_save=wave_save)

    def set_output_step(self, file_name):
        self.output_step = '%s/%s' % (self.path, file_name)
        with open(self.output_step, 'w') as outfile:
            outfile.write('Fitting start:\n\n')

    # Fitting
    def get_fit_nomial(self):
        output = dopwa(project_source_path=self.path_program_source,
                       project_source_name=self.project,
                       project_path=self.path_program_execute,
                       project_name='%1.4f_nomial' % (self.energy),
                       root_path=self.path_root_input,
                       root_name_data=self.root_data,
                       root_name_mc=self.root_mc,
                       input_option_string=self.input_option_string,
                       input_option_value=self.mywave.get_nomial_option(self.input_option_value),
                       input_constant=self.input_constant,
                       input_parameter=self.input_parameter,
                       file_execute=self.project)
        output.fraction = copy.deepcopy(self.mywave.give_fraction_name(output.fraction))
        return output

    def get_test_significance(self):
        data_nomial = self.get_fit_nomial()
        self.significance = {}
        for wave in self.mywave.wave_consider:
            data_check = dopwa(project_source_path=self.path_program_source,
                               project_source_name=self.project,
                               project_path=self.path_program_execute,
                               project_name='%1.4f_%s' % (self.energy, wave),
                               root_path=self.path_root_input,
                               root_name_data=self.root_data,
                               root_name_mc=self.root_mc,
                               input_option_string=self.input_option_string,
                               input_option_value=self.mywave.get_check_option(self.input_option_value, wave),
                               input_constant=self.input_constant,
                               input_parameter=self.input_parameter,
                               file_execute=self.project)
            self.significance[wave] = data_nomial.least_likelyhood - data_check.least_likelyhood
        if(hasattr(self, 'output_step')):
            with open(self.output_step, 'a') as outfile:
                outfile.write('Check significance:\n')
                for wave in self.significance:
                    outfile.write('{:<25} {:<15}\n'.format(wave, self.significance[wave]))
                outfile.write('\n')

    def get_scan(self,
                 parameter='',
                 limitl=0,
                 limitr=1,
                 inter=100):
        outputx = []
        outputy = []
        unit = (limitr - limitl) / inter
        use_parameter = copy.deepcopy(self.input_parameter)
        for i in range(inter):
            use_value = limitl + i * unit
            use_parameter[parameter]['value'] = use_value
            use_parameter[parameter]['error'] = -1
            data = dopwa(project_source_path=self.path_program_source,
                         project_source_name=self.project,
                         project_path=self.path_program_execute,
                         project_name='%1.4f_scan' % (self.energy),
                         root_path=self.path_root_input,
                         root_name_data=self.root_data,
                         root_name_mc=self.root_mc,
                         input_option_string=self.input_option_string,
                         input_option_value=self.mywave.get_nomial_option(self.input_option_value),
                         input_constant=self.input_constant,
                         input_parameter=use_parameter,
                         file_execute=self.project)
            outputx.append(use_value)
            outputy.append(data.least_likelyhood)
        return [outputx, outputy]

    # Processing

    def check_significance(self):
        '检查significance是否满足5sigma，返回bool'
        check_minus = 1
        check_plus = 1
        for wave in self.significance:
            if(wave in self.mywave.wave_save): continue
            if(wave in self.mywave.wave_nomial and self.significance[wave] < 0 and self.significance[wave] > -14.372):
                check_minus = 0
            if(wave not in self.mywave.wave_nomial and self.significance[wave] > 14.372):
                check_plus = 0
        check = check_minus * check_plus
        return check

    def adjust_significance(self):
        '根据significance调整mywave的wave_nomial列表'
        # 得到检测结果
        check_minus = 1
        check_plus = 1
        for wave in self.significance:
            if(wave in self.mywave.wave_save): continue
            if(wave in self.mywave.wave_nomial and self.significance[wave] < 0 and self.significance[wave] > -14.372):
                check_minus = 0
            if(wave not in self.mywave.wave_nomial and self.significance[wave] > 14.372):
                check_plus = 0
        # 先考虑减去波
        if(check_minus == 0):
            save_key = ''
            save_value = -9999
            for wave in self.significance:
                if(wave in self.mywave.wave_save): continue
                if(wave not in self.mywave.wave_nomial): continue
                if(self.significance[wave] > 0): continue
                if (self.significance[wave] > save_value):
                    save_key = wave
                    save_value = self.significance[wave]
            new_nomial = []
            for wave in self.mywave.wave_nomial:
                if(wave != save_key):
                    new_nomial.append(wave)
            self.mywave.wave_nomial = new_nomial
        # 再考虑加上波
        elif(check_plus == 0):
            save_key = ''
            save_value = 0
            for wave in self.significance:
                if(wave in self.mywave.wave_save): continue
                if(wave in self.mywave.wave_nomial): continue
                if(self.significance[wave] < 0): continue
                if (self.significance[wave] > save_value):
                    save_key = wave
                    save_value = self.significance[wave]
            self.mywave.wave_nomial.append(save_key)
        if(hasattr(self, 'output_step')):
            with open(self.output_step, 'a') as outfile:
                outfile.write('Adjust nomial waves:\n')
                for wave in self.mywave.wave_nomial:
                    outfile.write('{:<25}\n'.format(wave))
                outfile.write('\n')

    def dump_significance(self, filename):
        hfile.pkl_dump(filename, self.significance)
