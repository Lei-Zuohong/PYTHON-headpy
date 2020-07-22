# -*- coding: UTF-8 -*-
'''
'''
# Public package
# Private package
import numpy


def get_index(data, l, r, i):
    index = int(i * (data - l) / (r - l))
    return index


def weight2d(data, xl, xr, xi, yl, yr, yi, backlist=[]):
    '''
    计算概率分布二维数组
    '''
    # 初始化数组
    numall = 0
    numsec = numpy.zeros(shape=(xi, yi))
    for point in data:
        xindex = get_index(point[0], xl, xr, xi)
        yindex = get_index(point[1], yl, yr, yi)
        numsec[xindex, yindex] += 1
        numall += 1
    # 扣除backlist
    for method in backlist:
        for point in method:
            xindex = get_index(point[0], xl, xr, xi)
            yindex = get_index(point[1], yl, yr, yi)
            numsec[xindex, yindex] -= 1.0 / len(backlist)
            numall -= 1.0 / len(backlist)
    numsec = numsec / numall
    return numsec, numall


def weight1d(data, xl, xr, xi, backlist=[]):
    '''
    计算概率分布二维数组
    '''
    # 设定初始参数
    dx = (xr - xl) / xi
    # 初始化数组
    numall = 0
    numsec = numpy.zeros(xi)
    for point in data:
        index = get_index(point, xl, xr, xi)
        numsec[index] += 1
        numall += 1
    for method in backlist:
        for point in method:
            index = get_index(point, xl, xr, xi)
            numsec[index] -= 1.0 / len(backlist)
            numall -= 1.0 / len(backlist)
    numsec = numsec / numall
    return numsec


def weight2d_ratio(data1, data2, xl, xr, xi, yl, yr, yi, backlist=[]):
    '''
    计算概率分布数组比值,其中分母为data2
    '''
    numsec1, numall1 = weight2d(data1, xl, xr, xi, yl, yr, yi, backlist=backlist)
    numsec2, numall2 = weight2d(data2, xl, xr, xi, yl, yr, yi)
    for i1 in range(xi):
        for i2 in range(yi):
            if(numsec2[i1][i2] == 0):
                numsec2[i1][i2] = 10000
    ratio = numsec1 / numsec2
    return ratio


def weight1d_ratio(data1, data2, xl, xr, xi, backlist=[]):
    '''
    计算概率分布数组比值,其中分母为data2
    '''
    numsec1 = weight1d(data1, xl, xr, xi, backlist=backlist)
    numsec2 = weight1d(data2, xl, xr, xi)
    for i1 in range(xi):
        if(numsec2[i1] == 0):
            numsec2[i1] = 10000
    ratio = numsec1 / numsec2
    return ratio
