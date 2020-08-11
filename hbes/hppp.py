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
    in_list = hconst.energy_list()
    se_list = [2.0000,
               2.0500,
               2.1000,
               2.1250,
               2.1500,
               2.1750,
               2.2000,
               2.2324,
               2.3094,
               2.3864,
               2.3960,
               2.5000,
               2.6444,
               2.6464,
               2.7000,
               2.8000,
               2.9000,
               2.9500,
               2.9810,
               3.0000,
               3.0200,
               3.0800]
    out_list = {}
    for i1 in se_list:
        out_list[i1] = in_list[i1]
    return out_list


def selecters():
    output = {}
    # Other
    output['flag1'] = hnew.SELECTER_value(values=[0])
    output['flag2'] = hnew.SELECTER_value(values=[0])
    output['flag3'] = hnew.SELECTER_value(values=[0])
    output['pid'] = hnew.SELECTER_value(values=[1])
    # dimiu
    output['bhabhae'] = hnew.SELECTER(center=0.2,
                                      width=0.1,
                                      show=0.5,
                                      inter=50,
                                      reverse=1,
                                      title='Energy deposited')
    output['bhabhaa'] = hnew.SELECTER(center=5,
                                      width=5,
                                      show=90,
                                      inter=90,
                                      reverse=1,
                                      title='#theta')
    # helicity
    output['hgamma1'] = hnew.SELECTER(center=0,
                                      width=0.8,
                                      show=1,
                                      inter=50,
                                      title='Helicity angle',
                                      unit='',
                                      reverse=0)
    output['hgamma2'] = hnew.SELECTER(center=0,
                                      width=0.8,
                                      show=1,
                                      inter=50,
                                      title='',
                                      unit='',
                                      reverse=0)
    output['agamma'] = hnew.SELECTER(center=0,
                                     width=1,
                                     show=1,
                                     inter=50,
                                     title='',
                                     reverse=0)
    # kinematic fit
    output['chisq'] = hnew.SELECTER(center=40,
                                    width=40,
                                    show=40,
                                    inter=80,
                                    title=r'#chi^{2}')
    if(1 == 0):
        output['chisq'] = hnew.SELECTER(center=100,
                                        width=100,
                                        show=100,
                                        inter=100,
                                        title=r'#chi^{2}')
    output['chisq_4g'] = hnew.SELECTER(center=10,
                                       width=10,
                                       show=100,
                                       reverse=1,
                                       title=r'#chi_{4#gamma}^{2}')
    if(1 == 0):
        output['chisq_4g'] = hnew.SELECTER(center=100,
                                           width=100,
                                           show=100,
                                           reverse=0,
                                           title=r'#chi_{4#gamma}^{2}')
    output['chisq_3g'] = hnew.SELECTER(center=100,
                                       width=100,
                                       show=100,
                                       reverse=0,
                                       title=r'#chi_{3#gamma}^{2}')
    output['chisq_1g'] = hnew.SELECTER(center=10,
                                       width=10,
                                       show=200,
                                       reverse=1,
                                       title=r'#chi_{1#gamma}^{2}')
    if(1 == 0):
        output['chisq_1g'] = hnew.SELECTER(center=100,
                                           width=100,
                                           show=100,
                                           reverse=1,
                                           title=r'#chi_{1#gamma}^{2}')
    output['chisq_0g'] = hnew.SELECTER(center=0.0001,
                                       width=0.0001,
                                       show=0.0001,
                                       reverse=1,
                                       title=r'#chi_{0#gamma}^{2}')
    # 不变质量
    output['mpip'] = hnew.SELECTER(center=hconst.pdg()['m_pipm'],
                                   width=hconst.pdg()['m_pipm'],
                                   show=0.0005,
                                   inter=50,
                                   title=r'M_{#pi^{+}}',
                                   unit=r'(GeV/c^{2})')
    output['mpim'] = hnew.SELECTER(center=hconst.pdg()['m_pipm'],
                                   width=hconst.pdg()['m_pipm'],
                                   show=0.0005,
                                   inter=50,
                                   title=r'M_{#pi^{-}}',
                                   unit=r'(GeV/c^{2})')
    output['mpiz'] = hnew.SELECTER(center=hconst.pdg()['m_pi0'],
                                   width=0.045,
                                   show=0.045,
                                   inter=90,
                                   title=r'M_{#pi^{0}}',
                                   unit=r'(GeV/c^{2})')
    if(1 == 0):
        output['mpiz'] = hnew.SELECTER(center=0.8,
                                       width=0.8,
                                       show=0.8,
                                       inter=160,
                                       title=r'M_{#pi^{0}}',
                                       unit=r'(GeV/c^{2})')
    output['mpipm'] = hnew.SELECTER(center=1.5,
                                    show=1.5,
                                    inter=100,
                                    title=r'M_{#pi^{+}#pi^{-}}',
                                    unit=r'(GeV/c^{2})')
    output['mpipz'] = hnew.SELECTER(center=1.5,
                                    show=1.5,
                                    inter=100,
                                    title=r'M_{#pi^{+}#pi^{0}}',
                                    unit=r'(GeV/c^{2})')
    output['mpimz'] = hnew.SELECTER(center=1.5,
                                    show=1.5,
                                    inter=100,
                                    title=r'M_{#pi^{-}#pi^{0}}',
                                    unit=r'(GeV/c^{2})')
    # 动量
    output['ppip'] = hnew.SELECTER(center=1,
                                   show=1,
                                   inter=50,
                                   title=r'p_{#pi^{+}}',
                                   unit=r'(GeV/c)')
    output['ppim'] = hnew.SELECTER(center=1,
                                   show=1,
                                   inter=50,
                                   title=r'p_{#pi^{-}}',
                                   unit=r'(GeV/c)')
    # 角分布

    return output
