# -*- coding: UTF-8 -*-
'''
This is a package document.

    Environment version:

        etc

    Content:
    
        @pkl_read()
        @pkl_dump()
        @addfolder()
'''
# Public package
import os
import pickle


def pkl_read(filename):
    with open(filename, 'rb') as infile:
        output = pickle.load(infile)
    return output


def pkl_dump(filename, target, protocol=2):
    with open(filename, 'wb') as outfile:
        pickle.dump(target, outfile, protocol=protocol)


def addfolder(name, path):
    '''
    name: string, 输入新建的文件夹的名字
    path: string, 输入目标位置的绝对路径

    function: 查看某绝对路径下是否存在某名字的文件夹，没有则创建
    '''
    filelist = os.listdir(path)
    if(name not in filelist):
        os.system('mkdir %s/%s' % (path, name))
