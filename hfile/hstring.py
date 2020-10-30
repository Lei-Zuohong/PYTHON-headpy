# -*- coding: UTF-8 -*-


def txt_write(out_string, txt_name):
    '输出字符串到txt文件'
    with open(txt_name, 'w') as outfile:
        outfile.write(out_string)


def txt_writelines(out_strings, txt_name):
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


