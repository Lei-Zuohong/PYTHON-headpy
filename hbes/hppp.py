# -*- coding: UTF-8 -*-
import hnew as hnew
import hconst as hconst


def algroot():
    return ['PPPMPZALGROOT', 'jobOptions_Pppmpz.txt', 'Pppmpz']


def energy_list():
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


def energy_sort():
    in_energy_list = energy_list()
    out_energy_list = sorted(in_energy_list)
    return out_energy_list


def selecters():
    output = {}
    #
    output['pip_ep'] = hnew.SELECTER(center=0.4,
                                     width=0.4,
                                     center_show=0.6,
                                     width_show=0.6,
                                     inter=60,
                                     title=r'E/p(#pi^{+-})')
    output['pim_ep'] = output['pip_ep']
    output['pip_ep'].set_by_edge(0, 0.9)
    output['pim_ep'].set_by_edge(0, 0.9)
    output['pip_pid_pi'] = hnew.SELECTER(center=0.00005,
                                         width=0.00005,
                                         center_show=0.0005,
                                         width_show=0.0005,
                                         inter=10,
                                         title=r'Prob(#pi^{+-})',
                                         reverse=1)
    output['pim_pid_pi'] = output['pip_pid_pi']
    output['pip_pid_mu'] = hnew.SELECTER(center=1,
                                         width=1,
                                         center_show=1,
                                         width_show=1,
                                         inter=100,
                                         title=r'Prob(#mu^{+-})/Prob(#pi^{+-})')
    output['pim_pid_mu'] = output['pip_pid_mu']
    output['pip_pid_e'] = hnew.SELECTER(center=1,
                                        width=1,
                                        center_show=1,
                                        width_show=1,
                                        inter=100,
                                        title=r'Prob(#e^{+-})/Prob(#pi^{+-})')
    output['pim_pid_e'] = output['pip_pid_e']
    #
    output['vertex'] = hnew.SELECTER(center=50,
                                     width=50,
                                     center_show=50,
                                     width_show=50,
                                     inter=50,
                                     title=r'#chi^{2}_{Vertex}')
    #
    output['chisq'] = hnew.SELECTER(center=25,
                                    width=25,
                                    center_show=50,
                                    width_show=50,
                                    inter=50,
                                    title=r'#chi^{2}')
    #
    output['a_pippim'] = hnew.SELECTER(title=r'#theta(Track^{+},Track^{-})')
    output['a_pippim'].set_by_edge(0, 160)
    output['a_pippim'].set_by_edge_show(100, 180)
    output['a_pippim'].inter = 80
    output['b_pippim'] = output['a_pippim']
    output['gamma1_heli'] = hnew.SELECTER(center=0.,
                                          width=0.85,
                                          center_show=0.,
                                          width_show=1.,
                                          inter=40,
                                          title=r'cos(#theta_{helicity})')
    output['gamma2_heli'] = output['gamma1_heli']
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
                                    width=0.060,
                                    center_show=hconst.pdg()['m_pi0'],
                                    width_show=0.060,
                                    inter=120,
                                    title=r'M_{#gamma#gamma}',
                                    unit=r'(GeV/c^{2})')
    output['pipm_m'] = hnew.SELECTER(center=1.5,
                                     width=1.5,
                                     center_show=1.5,
                                     width_show=1.5,
                                     inter=60,
                                     title=r'M_{#pi^{+}#pi^{-}}',
                                     unit=r'(GeV/c^{2})')
    output['pipz_m'] = hnew.SELECTER(center=1.5,
                                     width=1.5,
                                     center_show=1.5,
                                     width_show=1.5,
                                     inter=60,
                                     title=r'M_{#pi^{+}#pi^{0}}',
                                     unit=r'(GeV/c^{2})')
    output['pimz_m'] = hnew.SELECTER(center=1.5,
                                     width=1.5,
                                     center_show=1.5,
                                     width_show=1.5,
                                     inter=60,
                                     title=r'M_{#pi^{-}#pi^{0}}',
                                     unit=r'(GeV/c^{2})')
    #
    output['pip_p'] = hnew.SELECTER(inter=50,
                                    title=r'p_{#pi^{+}}/p_{beam}')
    output['pim_p'] = hnew.SELECTER(inter=50,
                                    title=r'p_{#pi^{-}}/p_{beam}')
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
    output['pimz_p'] = hnew.SELECTER(inter=50,
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


def docuts():
    output = ['pip_ep', 'pim_ep', 'pip_pid_pi', 'pim_pid_pi',
              'chisq',
              'a_pippim',
              'gamma1_heli', 'gamma2_heli',
              'piz_m']
    return output
