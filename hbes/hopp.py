# -*- coding: UTF-8 -*-
'''
This is a package document.

    Environment version:

        python2
        python3

    Content:
    
        @algroot
        @energy_list
        @energy_list_pw
        @cut
'''
# Public package
# Private package
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
    l1 = 0.009274 * 2
    l2 = 0.008766 * 2
    l3 = 0.007139 * 2
    r1 = 0.007873 * 2
    r2 = 0.010412 * 2
    r3 = 0.009957 * 2
    output = {}
    output['momega'] = hnew.SELECTER(center=hconst.pdg()['m_omega'],
                                     width=hconst.pdg()['m_omega'],
                                     show=0.15,
                                     inter=60,
                                     title=r'M_{#pi^{+}#pi^{-}#pi^{0}}(GeV/c^{2})')
    output['mpip'] = hnew.SELECTER(center=hconst.pdg()['m_pipm'],
                                   width=hconst.pdg()['m_pipm'],
                                   show=0.045,
                                   inter=90,
                                   title=r'M_{#pi^{+}}(GeV/c^{2})')
    output['mpim'] = hnew.SELECTER(center=hconst.pdg()['m_pipm'],
                                   width=hconst.pdg()['m_pipm'],
                                   show=0.045,
                                   inter=90,
                                   title=r'M_{#pi^{-}}(GeV/c^{2})')
    output['mpi01'] = hnew.SELECTER(show=0.045,
                                    inter=90,
                                    title=r'M_{#pi_{1}^{0}}(GeV/c^{2})')
    output['mpi02'] = hnew.SELECTER(show=0.045,
                                    inter=90,
                                    title=r'M_{#pi_{2}^{0}}(GeV/c^{2})')
    output['mpi03'] = hnew.SELECTER(show=0.045,
                                    inter=90,
                                    title=r'M_{#pi_{3}^{0}}(GeV/c^{2})')
    output['mpi01'].set_by_edge(hconst.pdg()['m_pi0'] - l1, hconst.pdg()['m_pi0'] + r1)
    output['mpi02'].set_by_edge(hconst.pdg()['m_pi0'] - l2, hconst.pdg()['m_pi0'] + r2)
    output['mpi03'].set_by_edge(hconst.pdg()['m_pi0'] - l3, hconst.pdg()['m_pi0'] + r3)
    output['mpip'] = hnew.SELECTER(center=hconst.pdg()['m_pipm'],
                                   show=0.005,
                                   inter=100,
                                   title=r'M_{#pi^{+}}(GeV/c^{2})')
    output['mpim'] = hnew.SELECTER(center=hconst.pdg()['m_pipm'],
                                   show=0.005,
                                   inter=100,
                                   title=r'M_{#pi^{-}}(GeV/c^{2})')
    output['chisq'] = hnew.SELECTER(center=50,
                                    width=50,
                                    show=50,
                                    inter=100,
                                    title=r'#chi_{#pi^{+}#pi^{-}6#gamma}^{2}')
    output['mpi02pi03'] = hnew.SELECTER(center=0.8,
                                        width=0.8,
                                        show=0.8,
                                        inter=50,
                                        title=r'M_{#pi_{2}^{0}#pi_{3}^{0}}(GeV/c^{2})')
    output['momegapi02'] = hnew.SELECTER(center=1.5,
                                         width=1.5,
                                         show=1.5,
                                         inter=160,
                                         title=r'M_{#omega#pi_{2}^{0}}(GeV/c^{2})')
    output['momegapi03'] = hnew.SELECTER(center=1.5,
                                         width=1.5,
                                         show=1.5,
                                         inter=160,
                                         title=r'M_{#omega#pi_{3}^{0}}(GeV/c^{2})')
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
    output['apip'] = hnew.SELECTER(center=0,
                                   show=1,
                                   inter=50,
                                   title=r'#theta_{#pi^{+}}')
    output['apim'] = hnew.SELECTER(center=0,
                                   show=1,
                                   inter=50,
                                   title=r'#theta_{#pi^{-}}')
    # 动量部分
    output['pomega'] = hnew.SELECTER(center=1,
                                     show=1,
                                     inter=50,
                                     title=r'p_{#pi^{+}#pi^{-}#pi^{0}}(GeV/c^{2})')
    output['ppip'] = hnew.SELECTER(center=1,
                                   show=1,
                                   inter=50,
                                   title=r'p_{#pi^{+}}(GeV/c^{2})')
    output['ppim'] = hnew.SELECTER(center=1,
                                   show=1,
                                   inter=50,
                                   title=r'p_{#pi^{-}}(GeV/c^{2})')
    output['ppi01'] = hnew.SELECTER(center=1,
                                    show=1,
                                    inter=50,
                                    title=r'p_{#pi_{1}^{0}}(GeV/c^{2})')
    output['ppi02'] = hnew.SELECTER(center=1,
                                    show=1,
                                    inter=50,
                                    title=r'p_{#pi_{2}^{0}}(GeV/c^{2})')
    output['ppi03'] = hnew.SELECTER(center=1,
                                    show=1,
                                    inter=50,
                                    title=r'p_{#pi_{3}^{0}}(GeV/c^{2})')
    output['ppip'] = hnew.SELECTER(center=1,
                                   show=1,
                                   inter=50,
                                   title=r'p_{#pi^{+}}(GeV/c^{2})')
    output['ppim'] = hnew.SELECTER(center=1,
                                   show=1,
                                   inter=50,
                                   title=r'p_{#pi^{-}}(GeV/c^{2})')
    return output


def cut():
    '''
    作用: 返回进行opp分析的绘图选项\n
    '''
    output = {}
    l1 = 0.009274 * 2
    l2 = 0.008766 * 2
    l3 = 0.007139 * 2
    r1 = 0.007873 * 2
    r2 = 0.010412 * 2
    r3 = 0.009957 * 2
    m0 = hconst.pdg()['m_pi0']
    # 质量部分
    output['momega'] = {'mass': hconst.pdg()['m_omega'],
                        'cut': hconst.pdg()['m_omega'],
                        'range': 0.15,
                        'inter': 60,
                        'string': r'M_{#pi^{+}#pi^{-}#pi^{0}}(GeV/c^{2})',
                        'shift': 0}
    output['mpip'] = {'mass': 0.139,
                      'range': 0.045,
                      'inter': 90,
                      'string': r'M_{#pi^{+}}(GeV/c^{2})'}
    output['mpim'] = {'mass': 0.139,
                      'range': 0.045,
                      'inter': 90,
                      'string': r'M_{#pi^{-}}(GeV/c^{2})'}
    output['mpi01'] = {'mass': m0 + 0.5 * r1 - 0.5 * l1,
                       'cut': 0.5 * (r1 + l1),
                       'range': 0.045,
                       'inter': 90,
                       'string': r'M_{#pi_{1}^{0}}(GeV/c^{2})',
                       'shift': 0}
    output['mpi02'] = {'mass': m0 + 0.5 * r2 - 0.5 * l2,
                       'cut': 0.5 * (r2 + l2),
                       'range': 0.045,
                       'inter': 90,
                       'string': r'M_{#pi_{2}^{0}}(GeV/c^{2})',
                       'shift': 0}
    output['mpi03'] = {'mass': m0 + 0.5 * r3 - 0.5 * l3,
                       'cut': 0.5 * (r3 + l3),
                       'range': 0.045,
                       'inter': 90,
                       'string': r'M_{#pi_{3}^{0}}(GeV/c^{2})',
                       'shift': 0}
    output['chisq'] = {'mass': 50,
                       'cut': 50,
                       'range': 50,
                       'inter': 100,
                       'string': r'#chi_{#pi^{+}#pi^{-}6#gamma}^{2}',
                       'shift': 0}
    output['mpi02pi03'] = {'mass': 0.800,
                           'cut': 0.800,
                           'range': 0.800,
                           'inter': 50,
                           'string': r'M_{#pi_{2}^{0}#pi_{3}^{0}}(GeV/c^{2})',
                           'shift': 0}
    output['momegapi02'] = {'mass': 1.5,
                            'cut': 1.5,
                            'range': 0.8,
                            'inter': 160,
                            'string': r'M_{#omega#pi_{2}^{0}}(GeV/c^{2})',
                            'shift': 0}
    output['momegapi03'] = {'mass': 1.5,
                            'cut': 1.5,
                            'range': 0.8,
                            'inter': 160,
                            'string': r'M_{#omega#pi_{3}^{0}}(GeV/c^{2})',
                            'shift': 0}
    # 角分布部分
    output['aomega'] = {'mass': 0,
                        'range': 1,
                        'inter': 50,
                        'string': r'#theta_{#pi^{+}#pi^{-}#pi^{0}}(GeV/c^{2})'}
    output['apip'] = {'mass': 0,
                      'range': 1,
                      'inter': 50,
                      'string': r'#theta_{#pi^{+}}(GeV/c^{2})'}
    output['apim'] = {'mass': 0,
                      'range': 1,
                      'inter': 50,
                      'string': r'#theta_{#pi^{-}}(GeV/c^{2})'}
    output['api01'] = {'mass': 0,
                       'range': 1,
                       'inter': 50,
                       'string': r'#theta_{#pi_{1}^{0}}(GeV/c^{2})'}
    output['api02'] = {'mass': 0,
                       'range': 1,
                       'inter': 50,
                       'string': r'#theta_{#pi_{2}^{0}}(GeV/c^{2})'}
    output['api03'] = {'mass': 0,
                       'range': 1,
                       'inter': 50,
                       'string': r'#theta_{#pi_{3}^{0}}(GeV/c^{2})'}
    # 动量部分
    output['pomega'] = {'mass': 1,
                        'range': 1,
                        'inter': 50,
                        'string': r'p_{#pi^{+}#pi^{-}#pi^{0}}(GeV/c^{2})'}
    output['ppip'] = {'mass': 1,
                      'range': 1,
                      'inter': 50,
                      'string': r'p_{#pi^{+}}(GeV/c^{2})'}
    output['ppim'] = {'mass': 1,
                      'range': 1,
                      'inter': 50,
                      'string': r'p_{#pi^{-}}(GeV/c^{2})'}
    output['ppi01'] = {'mass': 1,
                       'range': 1,
                       'inter': 50,
                       'string': r'p_{#pi_{1}^{0}}(GeV/c^{2})'}
    output['ppi02'] = {'mass': 1,
                       'range': 1,
                       'inter': 50,
                       'string': r'p_{#pi_{2}^{0}}(GeV/c^{2})'}
    output['ppi03'] = {'mass': 1,
                       'range': 1,
                       'inter': 50,
                       'string': r'p_{#pi_{3}^{0}}(GeV/c^{2})'}
    output['pomegapi02'] = {'mass': 1,
                            'range': 1,
                            'inter': 50,
                            'string': r'p_{#omega#pi_{3}^{0}}(GeV/c^{2})'}
    output['pomegapi03'] = {'mass': 1,
                            'range': 1,
                            'inter': 50,
                            'string': r'p_{#omega#pi_{2}^{0}}(GeV/c^{2})'}
    output['ppi02pi03'] = {'mass': 1,
                           'range': 1,
                           'inter': 50,
                           'string': r'p_{#pi_{2}^{0}#pi_{3}^{0}}(GeV/c^{2})'}
    return output
