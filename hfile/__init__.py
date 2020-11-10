# -*- coding: UTF-8 -*-
# Public package
# Private package
import os
import shutil
import pickle

################################################################################
# 文件操作类
################################################################################


def mv(path_source, path_target):
    '用法同shell语言'
    shutil.move(path_source, path_target)


def add_folder(name, path):
    '查看某绝对路径下是否存在某名字的文件夹，没有则创建'
    filelist = os.listdir(path)
    if(name not in filelist):
        os.mkdir('%s/%s' % (path, name))


def copy_file(source_path='',
              source_name='',
              path='',
              name=''):
    '''
    复制文件为source_path/source_name\n
    目标文件为path/name\n
    '''
    if(name in os.listdir(path)):
        os.remove('%s/%s' % (path, name))
    shutil.copy('%s/%s' % (source_path, source_name),
                '%s' % (path))
    if(source_name != name):
        shutil.move('%s/%s' % (path, source_name),
                    '%s/%s' % (path, name))


def copy_folder(source_path='',
                source_name='',
                path='',
                name=''):
    '''
    复制文件夹为source_path/source_name\n
    目标文件夹为path/name\n
    '''
    if(name in os.listdir(path)):
        shutil.rmtree('%s/%s' % (path, name))
    shutil.copytree('%s/%s' % (source_path, source_name),
                    '%s/%s' % (path, name))

################################################################################
# pickle 相关类
################################################################################


def pkl_read(filename):
    with open(filename, 'rb') as infile:
        output = pickle.load(infile)
    return output


def pkl_dump(filename, target, protocol=2):
    with open(filename, 'wb') as outfile:
        pickle.dump(target, outfile, protocol=protocol)

################################################################################
# txt 相关类
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
