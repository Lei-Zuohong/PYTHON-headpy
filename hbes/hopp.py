# -*- coding: UTF-8 -*-
# Public package

# Private package
import headpy.hbes.hnew as hnew
import headpy.hbes.hconst as hconst


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


def energy_sort():
    in_energy_list = energy_list()
    out_energy_list = in_energy_list.keys()
    out_energy_list.sort()
    return out_energy_list


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
                                    center_show=100,
                                    width_show=100,
                                    inter=100,
                                    title=r'#chi_{#pi^{+}#pi^{-}6#gamma}^{2}')
    # 不变质量部分
    output['pip_m'] = hnew.SELECTER(center=hconst.pdg()['m_pipm'],
                                    width=hconst.pdg()['m_pipm'],
                                    center_show=hconst.pdg()['m_pipm'],
                                    width_show=0.045,
                                    inter=90,
                                    title=r'M_{#pi^{+}}',
                                    unit=r'(GeV/c^{2})')
    output['pim_m'] = hnew.SELECTER(center=hconst.pdg()['m_pipm'],
                                    width=hconst.pdg()['m_pipm'],
                                    center_show=hconst.pdg()['m_pipm'],
                                    width_show=0.045,
                                    inter=90,
                                    title=r'M_{#pi^{-}}',
                                    unit=r'(GeV/c^{2})')
    output['pi01_m'] = hnew.SELECTER(center_show=hconst.pdg()['m_pi0'],
                                     width_show=0.05,
                                     inter=100,
                                     title=r'M_{#pi_{1}^{0}}',
                                     unit=r'(GeV/c^{2})')
    output['pi02_m'] = hnew.SELECTER(center_show=hconst.pdg()['m_pi0'],
                                     width_show=0.05,
                                     inter=100,
                                     title=r'M_{#pi_{2}^{0}}',
                                     unit=r'(GeV/c^{2})')
    output['pi03_m'] = hnew.SELECTER(center_show=hconst.pdg()['m_pi0'],
                                     width_show=0.05,
                                     inter=100,
                                     title=r'M_{#pi_{3}^{0}}',
                                     unit=r'(GeV/c^{2})')
    output['pi01_m'].set_by_edge(hconst.pdg()['m_pi0'] - l1, hconst.pdg()['m_pi0'] + r1)
    output['pi02_m'].set_by_edge(hconst.pdg()['m_pi0'] - l2, hconst.pdg()['m_pi0'] + r2)
    output['pi03_m'].set_by_edge(hconst.pdg()['m_pi0'] - l3, hconst.pdg()['m_pi0'] + r3)
    output['omega_m'] = hnew.SELECTER(center=hconst.pdg()['m_omega'],
                                      width=hconst.pdg()['m_omega'],
                                      center_show=hconst.pdg()['m_omega'],
                                      width_show=0.15,
                                      inter=60,
                                      title=r'M_{#pi^{+}#pi^{-}#pi^{0}_{1}}',
                                      unit=r'(GeV/c^{2})')
    output['pi02pi03_m'] = hnew.SELECTER(center_show=0.8,
                                         width_show=0.8,
                                         inter=100,
                                         title=r'M_{#pi_{2}^{0}#pi_{3}^{0}}',
                                         unit=r'(GeV/c^{2})')
    output['omegapi02_m'] = hnew.SELECTER(center_show=1.5,
                                          width_show=1.5,
                                          inter=100,
                                          title=r'M_{#omega#pi_{2}^{0}}',
                                          unit=r'(GeV/c^{2})')
    output['omegapi03_m'] = hnew.SELECTER(center_show=1.5,
                                          width_show=1.5,
                                          inter=100,
                                          title=r'M_{#omega#pi_{3}^{0}}',
                                          unit=r'(GeV/c^{2})')
    # 角分布部分
    output['pip_a'] = hnew.SELECTER(center_show=0,
                                    width_show=1.,
                                    inter=50,
                                    title=r'cos#theta_{#pi^{+}}')
    output['pim_a'] = hnew.SELECTER(center_show=0,
                                    width_show=1.,
                                    inter=50,
                                    title=r'cos#theta_{#pi^{-}}')
    output['pi01_a'] = hnew.SELECTER(center_show=0,
                                     width_show=1.,
                                     inter=50,
                                     title=r'cos#theta_{#pi_{1}^{0}}')
    output['pi02_a'] = hnew.SELECTER(center_show=0,
                                     width_show=1.,
                                     inter=50,
                                     title=r'cos#theta_{#pi_{2}^{0}}')
    output['pi03_a'] = hnew.SELECTER(center_show=0,
                                     width_show=1.,
                                     inter=50,
                                     title=r'cos#theta_{#pi_{3}^{0}}')
    output['omega_a'] = hnew.SELECTER(center_show=0,
                                      width_show=1.,
                                      inter=50,
                                      title=r'cos#theta_{#pi^{+}#pi^{-}#pi^{0}}')
    # 动量部分
    output['pip_p'] = hnew.SELECTER(center_show=0.5,
                                    width_show=0.5,
                                    inter=50,
                                    title=r'p_{#pi^{+}}/p_{beam}',
                                    unit=r'(GeV/c)')
    output['pim_p'] = hnew.SELECTER(center_show=0.5,
                                    width_show=0.5,
                                    inter=50,
                                    title=r'p_{#pi^{-}}/p_{beam}',
                                    unit=r'(GeV/c)')
    output['pi01_p'] = hnew.SELECTER(center_show=0.5,
                                     width_show=0.5,
                                     inter=50,
                                     title=r'p_{#pi_{1}^{0}}/p_{beam}',
                                     unit=r'(GeV/c)')
    output['pi02_p'] = hnew.SELECTER(center_show=0.5,
                                     width_show=0.5,
                                     inter=50,
                                     title=r'p_{#pi_{2}^{0}}/p_{beam}',
                                     unit=r'(GeV/c)')
    output['pi03_p'] = hnew.SELECTER(center_show=0.5,
                                     width_show=0.5,
                                     inter=50,
                                     title=r'p_{#pi_{3}^{0}}/p_{beam}',
                                     unit=r'(GeV/c)')
    output['omega_p'] = hnew.SELECTER(center_show=0.5,
                                      width_show=0.5,
                                      inter=50,
                                      title=r'p_{#pi^{+}#pi^{-}#pi^{0}}/p_{beam}',
                                      unit=r'(GeV/c)')
    # 其它
    output['dalitz_s'] = hnew.SELECTER(center=2,
                                       width=2,
                                       center_show=0.3,
                                       width_show=0.3,
                                       inter=100,
                                       title=r'M^{2}_{#pi^{+}#pi^{-}}',
                                       unit=r'(GeV^{2}/c^{4})')
    output['dalitz_t'] = hnew.SELECTER(center=2,
                                       width=2,
                                       center_show=0.3,
                                       width_show=0.3,
                                       inter=100,
                                       title=r'M^{2}_{#pi^{-}#pi^{0}}',
                                       unit=r'(GeV^{2}/c^{4})')
    output['dalitz_u'] = hnew.SELECTER(center=2,
                                       width=2,
                                       center_show=0.3,
                                       width_show=0.3,
                                       inter=100,
                                       title=r'M^{2}_{#pi^{+}#pi^{0}}',
                                       unit=r'(GeV^{2}/c^{4})')
    output['dalitz_x1'] = hnew.SELECTER(center=0,
                                        width=1,
                                        center_show=0,
                                        width_show=1,
                                        inter=40,
                                        title='X')
    output['dalitz_y1'] = hnew.SELECTER(center=0,
                                        width=1,
                                        center_show=0.1,
                                        width_show=1.1,
                                        inter=40,
                                        title='Y')
    output['dalitz_x2'] = output['dalitz_x1']
    output['dalitz_y2'] = output['dalitz_y1']
    return output
