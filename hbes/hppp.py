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
    #
    output['chisq'] = hnew.SELECTER(center=25,
                                    width=25,
                                    center_show=50,
                                    width_show=50,
                                    inter=50,
                                    title=r'#chi^{2}')
    output['chisq_1g'] = hnew.SELECTER(center=5,
                                       width=5,
                                       center_show=50,
                                       width_show=50,
                                       inter=50,
                                       title=r'#chi^{2}_{#gamma}',
                                       reverse=1)
    output['chisq_3g'] = hnew.SELECTER(center=5,
                                       width=5,
                                       center_show=50,
                                       width_show=50,
                                       inter=50,
                                       title=r'#chi^{2}_{#gamma#gamma#gamma}',
                                       reverse=1)
    output['chisq_4g'] = hnew.SELECTER(center=5,
                                       width=5,
                                       center_show=50,
                                       width_show=50,
                                       inter=50,
                                       title=r'#chi^{2}_{#gamma#gamma#gamma#gamma}',
                                       reverse=1)
    output['chisq_m'] = hnew.SELECTER(center=5,
                                      width=5,
                                      center_show=50,
                                      width_show=50,
                                      inter=50,
                                      title=r'#chi^{2}_{#mu#mu}',
                                      reverse=1)
    output['chisq_e'] = hnew.SELECTER(center=5,
                                      width=5,
                                      center_show=50,
                                      width_show=50,
                                      inter=50,
                                      title=r'#chi^{2}_{ee}',
                                      reverse=1)
    output['chisq_k'] = hnew.SELECTER(center=5,
                                      width=5,
                                      center_show=50,
                                      width_show=50,
                                      inter=50,
                                      title=r'#chi^{2}_{KK}',
                                      reverse=1)
    #
    output['a_pippim'] = hnew.SELECTER(center=0,
                                       width=1,
                                       center_show=-0.99,
                                       width_show=0.01,
                                       inter=20,
                                       title=r'Cos<#pi^{+},#pi^{-}>')
    output['a_pippim'].set_by_edge(-0.99, 1)
    output['pip_ep'] = hnew.SELECTER(center=0.4,
                                     width=0.4,
                                     center_show=0.6,
                                     width_show=0.6,
                                     inter=60,
                                     title=r'E/P ratio of #pi^{+-}')
    output['pim_ep'] = hnew.SELECTER(center=0.4,
                                     width=0.4,
                                     center_show=0.6,
                                     width_show=0.6,
                                     inter=60,
                                     title=r'E/P ratio of #pi^{+-}')
    output['pip_ep'].set_by_edge(0, 0.85)
    output['pim_ep'].set_by_edge(0, 0.85)
    output['gamma1_heli'] = hnew.SELECTER(center=0,
                                          width=0.8,
                                          center_show=0,
                                          width_show=1.,
                                          inter=40,
                                          title=r'Helicity angle of #pi^{0}')
    output['gamma2_heli'] = hnew.SELECTER(center=0,
                                          width=0.8,
                                          center_show=0,
                                          width_show=1.,
                                          inter=40,
                                          title=r'Helicity angle of #pi^{0}')
    #
    output['pip_m'] = hnew.SELECTER(center=hconst.pdg()['m_pipm'],
                                    width=0.045,
                                    center_show=hconst.pdg()['m_pipm'],
                                    width_show=0.045,
                                    inter=90,
                                    title=r'M_{#pi^{+}}',
                                    unit=r'(GeV/c^{2})')
    output['pim_m'] = hnew.SELECTER(center=hconst.pdg()['m_pipm'],
                                    width=0.045,
                                    center_show=hconst.pdg()['m_pipm'],
                                    width_show=0.045,
                                    inter=90,
                                    title=r'M_{#pi^{-}}',
                                    unit=r'(GeV/c^{2})')
    output['piz_m'] = hnew.SELECTER(center=hconst.pdg()['m_pi0'],
                                    width=0.045,
                                    center_show=hconst.pdg()['m_pi0'],
                                    width_show=0.045,
                                    inter=90,
                                    title=r'M_{#gamma#gamma}',
                                    unit=r'(GeV/c^{2})')
    output['pipm_m'] = hnew.SELECTER(center=1.5,
                                     width=1.5,
                                     center_show=1.5,
                                     width_show=1.5,
                                     inter=120,
                                     title=r'M_{#pi^{+}#pi^{-}}',
                                     unit=r'(GeV/c^{2})')
    output['pipz_m'] = hnew.SELECTER(center=1.5,
                                     width=1.5,
                                     center_show=1.5,
                                     width_show=1.5,
                                     inter=120,
                                     title=r'M_{#pi^{+}#pi^{0}}',
                                     unit=r'(GeV/c^{2})')
    output['pimz_m'] = hnew.SELECTER(center=1.5,
                                     width=1.5,
                                     center_show=1.5,
                                     width_show=1.5,
                                     inter=120,
                                     title=r'M_{#pi^{-}#pi^{0}}',
                                     unit=r'(GeV/c^{2})')
    #
    output['pip_p'] = hnew.SELECTER(inter=50,
                                    title=r'p_{#pi^{+}}/p_{beam}')
    output['pim_p'] = hnew.SELECTER(inter=50,
                                    title=r'p_{#pi^{+}}/p_{beam}')
    output['gamma1_p'] = hnew.SELECTER(inter=50,
                                       title=r'p_{#gamma}/p_{beam}')
    output['gamma2_p'] = hnew.SELECTER(inter=50,
                                       title=r'p_{#gamma}/p_{beam}')
    output['piz_p'] = hnew.SELECTER(inter=50,
                                    title=r'p_{#gamma#gamma}/p_{beam}')
    output['pipm_p'] = hnew.SELECTER(inter=50,
                                     title=r'p_{#pi^{+}#pi^{-}}/p_{beam}')
    output['pipz_p'] = hnew.SELECTER(inter=50,
                                     title=r'p_{#pi^{+}#gamma#gamma}/p_{beam}')
    output['pimc_p'] = hnew.SELECTER(inter=50,
                                     title=r'p_{#pi^{-}#gamma#gamma}/p_{beam}')
    #
    output['pip_a'] = hnew.SELECTER(center_show=0,
                                    width_show=1.,
                                    inter=40,
                                    title=r'Cos#theta_{#pi^{+}}')
    output['pim_a'] = hnew.SELECTER(center_show=0,
                                    width_show=1.,
                                    inter=40,
                                    title=r'Cos#theta_{#pi^{-}}')
    output['gamma1_a'] = hnew.SELECTER(center_show=0,
                                       width_show=1.,
                                       inter=40,
                                       title=r'Cos#theta_{#gamma}')
    output['gamma2_a'] = hnew.SELECTER(center_show=0,
                                       width_show=1.,
                                       inter=40,
                                       title=r'Cos#theta_{#gamma}')
    output['piz_a'] = hnew.SELECTER(center_show=0,
                                    width_show=1.,
                                    inter=40,
                                    title=r'Cos#theta_{#gamma#gamma}')
    output['pipm_a'] = hnew.SELECTER(center_show=0,
                                     width_show=1.,
                                     inter=40,
                                     title=r'Cos#theta_{#pi^{+}#pi^{-}}')
    output['pipz_a'] = hnew.SELECTER(center_show=0,
                                     width_show=1.,
                                     inter=40,
                                     title=r'Cos#theta_{#pi^{+}#gamma#gamma}')
    output['pimz_a'] = hnew.SELECTER(center_show=0,
                                     width_show=1.,
                                     inter=40,
                                     title=r'Cos#theta_{#pi^{-}#gamma#gamma}')
    #
    output['dalitz_pm'] = hnew.SELECTER(center_show=2,
                                        width_show=2,
                                        inter=50,
                                        title=r'M^{2}_{#pi^{+}#pi^{-}}',
                                        unit=r'(GeV^{2}/c^{4})')
    output['dalitz_pz'] = hnew.SELECTER(center_show=2,
                                        width_show=2,
                                        inter=50,
                                        title=r'M^{2}_{#pi^{+}#pi^{0}}',
                                        unit=r'(GeV^{2}/c^{4})')
    output['dalitz_mz'] = hnew.SELECTER(center_show=2,
                                        width_show=2,
                                        inter=50,
                                        title=r'M^{2}_{#pi^{-}#pi^{0}}',
                                        unit=r'(GeV^{2}/c^{4})')
    return output
