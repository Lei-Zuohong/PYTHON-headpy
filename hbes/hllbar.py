# -*- coding: UTF-8 -*-
import headpy.hbes.hconst as hconst
import headpy.hbes.hnew as hnew


def algroot():
    '''
    作用: 返回进行opp分析的分析程序调用所需要的三个字符串\n
    '''
    return ['PPPMPZALGROOT', 'jobOptions_Pppmpz.txt', 'Pppmpz']


def energy_list():
    '''
    作用: 返回能够进行opp相空间分析的19个能量点\n
    '''
    out_list = {}
    out_list[3.097] = [9947, 10878, 1, 'unknown']
    return out_list
