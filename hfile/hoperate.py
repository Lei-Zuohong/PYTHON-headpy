# -*- coding: UTF-8 -*-
import os
import shutil


def add_folder(name, path):
    '查看某绝对路径下是否存在某名字的文件夹，没有则创建'
    filelist = os.listdir(path)
    if(name not in filelist):
        os.mkdir('%s/%s' % (path, name))


def mv(path_source, path_target):
    '移动文件或者文件夹'
    shutil.move(path_source, path_target)


def copy_file(source_path='',
              source_name='',
              path='',
              name=''):
    '智能复制文件'
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
    '智能复制文件夹'
    if(name in os.listdir(path)):
        shutil.rmtree('%s/%s' % (path, name))
    shutil.copytree('%s/%s' % (source_path, source_name),
                    '%s/%s' % (path, name))


# 不常用


def shutil_copy(path_source, path_target):
    '复制文件到路径'
    shutil.copy(path_source, path_target)


def shutil_copytree(path_source, path_target):
    '复制文件夹内所有文件到目标文件夹'
    shutil.copytree(path_source, path_target)
