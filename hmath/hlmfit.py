# -*- coding: UTF-8 -*-
# Public package
import lmfit
# Private package
import hstatis as hstatis


def trans_parameters_lmfit(parameters):
    output = lmfit.Parameters()
    for name in parameters.names:
        output.add(name,
                   value=parameters.parameters[name].value,
                   min=parameters.parameters[name].limitl,
                   max=parameters.parameters[name].limitr)
    return output


def trans_parameters_hstatis(parameters):
    output = hstatis.PARAMETERS()
    # output.add(hstatis.PARAMETER())
    return output
