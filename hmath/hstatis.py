# -*- coding: UTF-8 -*-
'''
This is a package document.

    Environment version:

        python3
        请在python3环境下运行程序

    Content:
    
        @weight2d:
            输入二维数组，输入双坐标参数，返回概率数组
        @weight1d:
            输入一维数组，输入双参数坐标，返回概率数组
        @weight2d_ratio:
            输入二维数组，输入双坐标参数，返回概率数组之比
        @weight1d_ratio:
            输入一维数组，输入双坐标参数，返回概率数组之比
'''
# Public package
# Private package
import numpy as np


def weight2d(data, xl, xr, xi, yl, yr, yi, backlist=[]):
    '''
    data: list, 二维坐标组成的数组
    xl,xr,xi: double, x轴边界与分割数
    yl,yr,yi: double, y轴边界与分割数
    backlist: list, 由data相同类型的对象组成的数组，用来对原数据进行相减操作
    
    function: 返回众多二维坐标的概率分布数组
    '''
    # 设定初始参数
    dx = (xr - xl) / xi
    dy = (yr - yl) / yi
    # 初始化数组
    numall = 0
    numsec = np.zeros(shape=(xi, yi))
    # 统计数组
    for point in data:
        pointx = point[0]
        pointy = point[1]
        pointsx = int((pointx - xl) / dx)
        pointsy = int((pointy - yl) / dy)
        numsec[pointsx][pointsy] += 1
        numall += 1
    for method in backlist:
        for point in method:
            pointx = point[0]
            pointy = point[1]
            pointsx = int((pointx - xl) / dx)
            pointsy = int((pointy - yl) / dy)
            numsec[pointsx][pointsy] -= 1 / len(backlist)
            numall -= 1 / len(backlist)
    numsec = numsec / numall
    return numsec


def weight1d(data, xl, xr, xi, backlist=[]):
    '''
    data: list, 一维坐标组成的数组
    xl,xr,xi: double, x轴边界与分割数
    backlist: list, 由data相同类型的对象组成的数组，用来对原数据进行相减操作
    
    function: 返回众多一维坐标的概率分布数组
    '''
    # 设定初始参数
    dx = (xr - xl) / xi
    # 初始化数组
    numall = 0
    numsec = np.zeros(xi)
    for point in data:
        points = int((point - xl) / dx)
        numsec[points] += 1
        numall += 1
    for method in backlist:
        for point in method:
            points = int((point - xl) / dx)
            numsec[points] -= 1 / len(backlist)
            numall -= 1 / len(backlist)
    numsec = numsec / numall
    return numsec


def weight2d_ratio(data1, data2, xl, xr, xi, yl, yr, yi, backlist=[]):
    '''
    data: list, 二维坐标组成的数组
    xl,xr,xi: double, x轴边界与分割数
    yl,yr,yi: double, y轴边界与分割数
    backlist: list, 由data相同类型的对象组成的数组，用来对原数据进行相减操作
    
    function: 返回众多二维坐标的概率分布数组的比值
    '''
    numsec1 = weight2d(data1, xl, xr, xi, yl, yr, yi, backlist=backlist)
    numsec2 = weight2d(data2, xl, xr, xi, yl, yr, yi)
    for i1 in range(xi):
        for i2 in range(yi):
            if(numsec2[i1][i2] == 0):
                numsec2[i1][i2] = 100
    ratio = numsec1 / numsec2
    return ratio


def weight1d_ratio(data1, data2, xl, xr, xi, backlist=[]):
    '''
    data: list, 一维坐标组成的数组
    xl,xr,xi: double, x轴边界与分割数
    backlist: list, 由data相同类型的对象组成的数组，用来对原数据进行相减操作
    
    function: 返回众多一维坐标的概率分布数组的比值
    '''
    numsec1 = weight1d(data1, xl, xr, xi, backlist=backlist)
    numsec2 = weight1d(data2, xl, xr, xi)
    for i1 in range(xi):
        if(numsec2[i1] == 0):
            numsec2[i1] = 100
    ratio = numsec1 / numsec2
    return ratio
