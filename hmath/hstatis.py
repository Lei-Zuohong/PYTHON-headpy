# -*- coding: UTF-8 -*-
# Public package
import numpy
import scipy
# Private package


class PARAMETER():
    def __init__(self,
                 name='',
                 value=0.0,
                 error=1.0,
                 limitl=-1.0,
                 limitr=1.0):
        self.name = name
        self.value = value
        self.error = error
        self.limitl = limitl
        self.limitr = limitr


class PARAMETERS():
    def __init__(self):
        self.parameters = []

    def add(self, parameter):
        self.parameters.append(parameter)

    def add_correlation(self, correlation):
        if(len(correlation) != len(correlation[0]) or len(correlation) != len(self.parameters)):
            print('Wrong correlation length')
        self.correlation = correlation



