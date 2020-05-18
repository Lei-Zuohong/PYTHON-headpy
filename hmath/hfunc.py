# -*- coding: UTF-8 -*-
'''
This is a package document.

    Environment version:

        etc

    Content:
    
        @etc:
            etc
'''

'''
parameter1: type, usage
functon1:
'''
# Public package
import math

def bar_bw(e, mr, wr):
    i = 1j
    part1 = mr * wr
    part2 = mr**2 - e**2 - i * e * wr
    output = part1 / part2
    return output


def bar_none(e, a, b):
    output = a / (e**2 - b**2)
    return output


def bar_module(e, mr, wr, sigma, phi, a, b):
    i = 1j
    part1 = sigma**0.5 * bar_bw(e, mr, wr)
    part2 = math.cos(phi) + math.sin(phi) * i
    part2 = part2 * bar_none(e, a, b)
    output = abs(part1 + part2)
    output = output**2
    return output


def bar_function(e, mr, wr, sigma, phi, a, b):
    output = bar_module(e, mr, wr, sigma, phi, a, b)
    #output = output / e**2
    return output

