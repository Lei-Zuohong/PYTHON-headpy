# -*- coding: UTF-8 -*-
# Public package
# Private package
import os
import re
import sys
import copy
import shutil
import pickle


################################################################################
# Python 命令行指令操作类
################################################################################

def argv(argv=sys.argv):
    '返回命令行输入的列表和字典'
    option_list = []
    option_dict = {}
    option = copy.deepcopy(argv)
    for i in range(len(option)):
        check1 = re.match(r'-(.*)', option[i])
        check2 = re.match(r'--(.*)', option[i])
        if(check2):
            if(i + 1 >= len(option)):
                print('Info from hfile.argv: Error with input option!')
                exit(0)
            option_dict[check2.group(1)] = option[i + 1]
        elif(check1):
            option_list.append(check1.group(1))
    return option_list, option_dict


################################################################################
# 文件操作类
################################################################################


def divide_path(in_string):
    if(re.match(r'(.*)/([^/]*)', in_string)):
        check = re.match(r'(.*)/([^/]*)', in_string)
        path = check.group(1)
        name = check.group(2)
    else:
        path = ''
        name = in_string
    return path, name


def mv(path_source, path_target):
    '用法同shell语言'
    shutil.move(path_source, path_target)


def add_folder(path='', name=''):
    '查看某绝对路径下是否存在某名字的文件夹，没有则创建'
    filelist = os.listdir(path)
    if(name not in filelist):
        os.mkdir('%s/%s' % (path, name))


def copy_file(source='', target=''):
    source_path, source_name = divide_path(source)
    target_path, target_name = divide_path(target)
    if(target_name in os.listdir(target_path)):
        os.remove('%s/%s' % (target_path, target_name))
    shutil.copy('%s/%s' % (source_path, source_name),
                '%s' % (target_path))
    if(source_name != target_name):
        shutil.move('%s/%s' % (target_path, source_name),
                    '%s/%s' % (target_path, target_name))


def copy_folder(source='', target=''):
    source_path, source_name = divide_path(source)
    target_path, target_name = divide_path(target)
    if(target_name in os.listdir(target_path)):
        shutil.rmtree('%s/%s' % (target_path, target_name))
    shutil.copytree('%s/%s' % (source_path, source_name),
                    '%s/%s' % (target_path, target_name))


def rm_file(filename):
    os.remove(filename)


def rm_folder(filename):
    shutil.rmtree(filename)


################################################################################
# 文件列表类
################################################################################


def get_tree(source_path):
    '''
    遍历本地目录返回字典树
    '''
    output = {}
    if(os.path.isfile(source_path)):
        return 'file'
    else:
        files = os.listdir(source_path)
        for file in files:
            if(re.match(r'\.(.*)', file)): continue
            output[file] = get_tree(os.path.join(source_path, file))
        return output


################################################################################
# .pickle 相关类
################################################################################


def pkl_read(filename):
    with open(filename, 'rb') as infile:
        output = pickle.load(infile)
    return output


def pkl_dump(filename, target, protocol=2):
    with open(filename, 'wb') as outfile:
        pickle.dump(target, outfile, protocol=protocol)

################################################################################
# .txt 相关类
################################################################################


def txt_write(txt_name, out_string):
    '输出字符串到txt文件'
    with open(txt_name, 'w') as outfile:
        outfile.write(out_string)


def txt_writelines(txt_name, out_strings):
    '输出字符串列表到txt文件'
    output = ''
    for out_string in out_strings:
        output += out_string
        output += '\n'
    txt_write(output, txt_name)


def txt_read(txt_name):
    '读取文件为string'
    with open(txt_name, 'r') as infile:
        output = infile.read()
    return output


def txt_readlines(txt_name):
    '读取文件为string列表'
    with open(txt_name, 'r') as infile:
        output = infile.readlines()
    return output


def txt_add(txt_name, out_string):
    output = txt_read(txt_name)
    output += out_string
    txt_write(txt_name, output)
