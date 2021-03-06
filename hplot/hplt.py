# -*- coding: UTF-8 -*-
# Public package
import matplotlib.pyplot as plt
# Private package


def plt_scatter_errorbar(plt,
                         x=0, y=0, xl=0, xr=0, yl=0, yr=0,
                         color='',
                         marker='',
                         markersize=10,
                         linestyle='',
                         label=''):
    '绘制一个带有横纵误差棒的数据点'
    output = {}
    output['v'], = plt.plot([x, x], [y - yr, y + yr], color, linestyle=linestyle, label=label)
    output['h'], = plt.plot([x - xl, x + xr], [y, y], color, linestyle=linestyle, label=label)
    output['p'] = plt.scatter(x, y, c=color, s=markersize, marker=marker, label=label)
    return output
