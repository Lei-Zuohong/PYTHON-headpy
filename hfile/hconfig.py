# -*- coding: UTF-8 -*-
# Public package

# Private package


import configparser

conf = configparser.ConfigParser()
conf.read('test.txt')
sections = conf.sections()  # 获取配置文件中所有sections，sections是列表
print(sections)
option = conf.options(conf.sections()[0])  # 获取某个section下的所有选项或value，等价于 option = conf.options('logoninfo')
print(option)
value = conf.get('222', 'option21')  # 根据section和value获取key值,等价于value = conf.get(conf.sections()[0], conf.options(conf.sections()[0])[0])
print(value)
item = conf.items('333')
print(item)
