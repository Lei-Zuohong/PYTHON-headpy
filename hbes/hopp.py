# -*- coding: UTF-8 -*-
import headpy.hbes.hconst as hconst
import headpy.hbes.hnew as hnew


def algroot():
    '''
    作用: 返回进行opp分析的分析程序调用所需要的三个字符串\n
    '''
    return ['OMEGAALGROOT', 'jobOptions_Omega.txt', 'Omega']


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
               2.6444,
               2.6464,
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


def energy_list_pw():
    '''
    作用: 返回能够进行opp分波分析的12个能量点\n
    '''
    in_list = hconst.energy_list()
    se_list = [2.0000,
               2.1000,
               2.1250,
               2.1750,
               2.2000,
               2.2324,
               2.3094,
               2.3864,
               2.3960,
               2.6444,
               2.6464,
               2.9000]
    out_list = {}
    for i1 in se_list:
        out_list[i1] = in_list[i1]
    return out_list


def selecters():
    l1 = 0.009609 * 3
    l2 = 0.009231 * 3
    l3 = 0.007509 * 3
    r1 = 0.008620 * 3
    r2 = 0.010711 * 3
    r3 = 0.009896 * 3
    output = {}
    output['chisq'] = hnew.SELECTER(center=50,
                                    width=50,
                                    show=50,
                                    inter=100,
                                    title=r'#chi_{#pi^{+}#pi^{-}6#gamma}^{2}')
    # 不变质量部分
    output['momega'] = hnew.SELECTER(center=hconst.pdg()['m_omega'],
                                     width=hconst.pdg()['m_omega'],
                                     show=0.15,
                                     inter=60,
                                     title=r'M_{#pi^{+}#pi^{-}#pi^{0}}',
                                     unit=r'(GeV/c^{2})')
    output['mpip'] = hnew.SELECTER(center=hconst.pdg()['m_pipm'],
                                   width=hconst.pdg()['m_pipm'],
                                   show=0.045,
                                   inter=90,
                                   title=r'M_{#pi^{+}}',
                                   unit=r'(GeV/c^{2})')
    output['mpim'] = hnew.SELECTER(center=hconst.pdg()['m_pipm'],
                                   width=hconst.pdg()['m_pipm'],
                                   show=0.045,
                                   inter=90,
                                   title=r'M_{#pi^{-}}',
                                   unit=r'(GeV/c^{2})')
    output['mpi01'] = hnew.SELECTER(show=0.045,
                                    inter=90,
                                    title=r'M_{#pi_{1}^{0}}',
                                    unit=r'(GeV/c^{2})')
    output['mpi02'] = hnew.SELECTER(show=0.045,
                                    inter=90,
                                    title=r'M_{#pi_{2}^{0}}',
                                    unit=r'(GeV/c^{2})')
    output['mpi03'] = hnew.SELECTER(show=0.045,
                                    inter=90,
                                    title=r'M_{#pi_{3}^{0}}',
                                    unit=r'(GeV/c^{2})')
    output['mpi01'].set_by_edge(hconst.pdg()['m_pi0'] - l1, hconst.pdg()['m_pi0'] + r1)
    output['mpi02'].set_by_edge(hconst.pdg()['m_pi0'] - l2, hconst.pdg()['m_pi0'] + r2)
    output['mpi03'].set_by_edge(hconst.pdg()['m_pi0'] - l3, hconst.pdg()['m_pi0'] + r3)
    output['mpi02pi03'] = hnew.SELECTER(center=0.8,
                                        width=0.8,
                                        show=0.8,
                                        inter=50,
                                        title=r'M_{#pi_{2}^{0}#pi_{3}^{0}}',
                                        unit=r'(GeV/c^{2})')
    output['momegapi02'] = hnew.SELECTER(center=1.5,
                                         width=1.5,
                                         show=1.5,
                                         inter=160,
                                         title=r'M_{#omega#pi_{2}^{0}}',
                                         unit=r'(GeV/c^{2})')
    output['momegapi03'] = hnew.SELECTER(center=1.5,
                                         width=1.5,
                                         show=1.5,
                                         inter=160,
                                         title=r'M_{#omega#pi_{3}^{0}}',
                                         unit=r'(GeV/c^{2})')
    # 角分布部分
    output['aomega'] = hnew.SELECTER(center=0,
                                     show=1,
                                     inter=50,
                                     title=r'#theta_{#pi^{+}#pi^{-}#pi^{0}}')
    output['apip'] = hnew.SELECTER(center=0,
                                   show=1,
                                   inter=50,
                                   title=r'#theta_{#pi^{+}}')
    output['apim'] = hnew.SELECTER(center=0,
                                   show=1,
                                   inter=50,
                                   title=r'#theta_{#pi^{-}}')
    output['api01'] = hnew.SELECTER(center=0,
                                    show=1,
                                    inter=50,
                                    title=r'#theta_{#pi_{1}^{0}}')
    output['api02'] = hnew.SELECTER(center=0,
                                    show=1,
                                    inter=50,
                                    title=r'#theta_{#pi_{2}^{0}}')
    output['api03'] = hnew.SELECTER(center=0,
                                    show=1,
                                    inter=50,
                                    title=r'#theta_{#pi_{3}^{0}}')
    # 动量部分
    output['pomega'] = hnew.SELECTER(center=1,
                                     show=1,
                                     inter=50,
                                     title=r'p_{#pi^{+}#pi^{-}#pi^{0}}',
                                     unit=r'(GeV/c)')
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
    output['ppi01'] = hnew.SELECTER(center=1,
                                    show=1,
                                    inter=50,
                                    title=r'p_{#pi_{1}^{0}}',
                                    unit=r'(GeV/c)')
    output['ppi02'] = hnew.SELECTER(center=1,
                                    show=1,
                                    inter=50,
                                    title=r'p_{#pi_{2}^{0}}',
                                    unit=r'(GeV/c)')
    output['ppi03'] = hnew.SELECTER(center=1,
                                    show=1,
                                    inter=50,
                                    title=r'p_{#pi_{3}^{0}}',
                                    unit=r'(GeV/c)')
    # 能量部分
    output['epi01'] = hnew.SELECTER(center=0.5,
                                    show=0.5,
                                    title=r'Epi01',
                                    unit=r'(GeV)')
    return output
