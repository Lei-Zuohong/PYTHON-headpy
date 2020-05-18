# -*- coding: UTF-8 -*-
'''
This is a package document.

    Environment version:

        python2
        python3
        提供程序使用的物理学常数

    Content:
    
        @pdg:
        @energy_list:
'''
# Public package
# Private package


def pdg():
    '''
    作用: 提供PDG网页上的各种参数\n
    '''
    output = {}
    output['m_omega'] = 0.78265
    output['m_pi0'] = 0.13498
    output['m_pipm'] = 0.13957
    output['br_omega'] = 0.893
    output['br_pi0'] = 0.98823
    return output


def energy_list():
    '''
    作用: 提供tQCD合作做所使用的能量点信息\n
    格式为:\n
        {energy:[runnumber_lower,\n
                runnumber_upper,\n
                luminosity,\n
                luminosity string for latex]}\n
    '''
    out_list = {2.0000: [41729, 41909, 10.077, '10.1$\pm$0.1'],
                2.0500: [41911, 41958, 3.351, '3.34$\pm$0.03'],
                2.1000: [41588, 41727, 12.167, '12.2$\pm$0.1'],
                2.1250: [42004, 43253, 108.49, '108$\pm$1'],
                2.1500: [41533, 41570, 2.849, '2.84$\pm$0.02'],
                2.1750: [41416, 41532, 10.641, '10.6$\pm$0.1'],
                2.2000: [40989, 41121, 13.670, '13.7$\pm$0.1'],
                2.2324: [41122, 41239, 11.858, '11.9$\pm$0.1'],
                2.3094: [41240, 41411, 21.080, '21.1$\pm$0.1'],
                2.3864: [40806, 40951, 22.588, '22.5$\pm$0.2'],
                2.3960: [40459, 40769, 66.893, '66.9$\pm$0.5'],
                2.5000: [40771, 40776, 1.099, '1.10$\pm$0.01'],
                2.6444: [40128, 40296, 33.650, '33.7$\pm$0.2'],
                2.6464: [40300, 40435, 34.064, '34.0$\pm$0.3'],
                2.7000: [40436, 40439, 1.035, '1.03$\pm$0.01'],
                2.8000: [40440, 40443, 1.008, '1.01$\pm$0.01'],
                2.9000: [39775, 40069, 105.53, '105$\pm$1'],
                2.9500: [39619, 39650, 15.960, '15.9$\pm$0.1'],
                2.9810: [39651, 39679, 16.046, '16.1$\pm$0.1'],
                3.0000: [39680, 39710, 15.849, '15.9$\pm$0.1'],
                3.0200: [39711, 39738, 17.315, '17.3$\pm$0.1'],
                3.0800: [39355, 39618, 126.21, '126$\pm$1']
                }
    return out_list
