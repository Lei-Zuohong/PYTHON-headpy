# -*- coding: UTF-8 -*-
# Public package
import math
import numpy
# Private package
import headpy.hbes.hconst as hconst


unit_pi = 3.1415926
unit_real = 1.0 + 0.0j
unit_imag = 0.0 + 1.0j


################################################################################
# 通用
################################################################################


def breit_wigner(**argv):
    if('s' in argv):
        e = pow(argv['s'], 0.5)
    elif('m' in argv):
        e = argv['m']
    elif('e' in argv):
        e = argv['e']
    if('mr' in argv):
        mr = argv['mr']
    if('wr' in argv):
        wr = argv['wr']
    part1 = mr * wr
    part2 = mr**2 - e**2 - unit_imag * e * wr
    output = part1 / part2
    return output


def breit_wigner_energydependent(**argv):
    if('s' in argv):
        e = pow(argv['s'], 0.5)
    elif('m' in argv):
        e = argv['m']
    elif('e' in argv):
        e = argv['e']
    if('mr' in argv):
        mr = argv['mr']
    if('wr' in argv):
        wr = argv['wr']
    if('l' in argv):
        l = argv['l']
    if('m1' in argv):
        m1 = argv['m1']
    if('m2' in argv):
        m2 = argv['m2']
    p_mr = decaymomentum(m12=mr, m1=m1, m2=m2)
    p_me = decaymomentum(m12=e, m1=m1, m2=m2)
    width_me = wr * mr * mr / e / e * pow(p_me / p_mr, 2 * l + 1)
    part1 = unit_real
    part2 = e * e - mr * mr + unit_imag * e * width_me
    output = part1 / part2
    return output

################################################################################
# 辅助函数
################################################################################


def decaymomentum(**argv):
    if('s12' in argv):
        m12 = pow(argv['s12'], 0.5)
    elif('m12' in argv):
        m12 = argv['m12']
    if('s1' in argv):
        m1 = pow(argv['s1'], 0.5)
    elif('m1' in argv):
        m1 = argv['m1']
    if('s2' in argv):
        m2 = pow(argv['s2'], 0.5)
    elif('m2' in argv):
        m2 = argv['m2']
    poly = m12**4 + m1**4 + m2**4 - 2 * m1**2 * m2**2 - 2 * m1**2 * m12**2 - 2 * m2**2 * m12**2
    try:
        length = len(poly)
    except:
        length = -1
    if(length == -1):
        if(poly < 0.0):
            poly = 0.0
    if(length >= 0):
        poly[numpy.where(poly < 0.0)] = 0.0
    output = pow(poly, 0.5) / (2 * m12)
    if(length == -1):
        if(m1 + m2 > m12):
            output = 0.0
    if(length >= 0):
        output[numpy.where(m1 + m2 > m12)] = 0.0
    return output


def decaymomentum2(**argv):
    if('s12' in argv):
        m12 = pow(argv['s12'], 0.5)
    elif('m12' in argv):
        m12 = argv['m12']
    if('s1' in argv):
        m1 = pow(argv['s1'], 0.5)
    elif('m1' in argv):
        m1 = argv['m1']
    if('s2' in argv):
        m2 = pow(argv['s2'], 0.5)
    elif('m2' in argv):
        m2 = argv['m2']
    poly = m12**4 + m1**4 + m2**4 - 2 * m1**2 * m2**2 - 2 * m1**2 * m12**2 - 2 * m2**2 * m12**2
    if(poly < 0.0):
        poly = 0.0
    output = poly / (4 * m12**2)
    if(m1 + m2 > m12):
        output = 0.0
    return output


def phase_to_value(phase):
    part_real = math.cos(phase) * unit_real
    part_imag = math.sin(phase) * unit_imag
    output = part_real + part_imag
    return output

################################################################################
# BABAR omegapipi
################################################################################


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
    return output

################################################################################
# SND pipipi
################################################################################


def snd_resonance(e, mr, wr, m1, m2, l, b):
    p_mr = decaymomentum(m12=mr, m1=m1, m2=m2)
    p_me = decaymomentum(m12=e, m1=m1, m2=m2)
    width_me = wr * mr * mr / e / e * pow(p_me / p_mr, 2 * l + 1)
    part1 = wr * pow(mr, 1.5) * pow(12 * unit_pi * b, 0.5) * unit_real
    part2 = mr * mr - e * e - unit_imag * e * width_me
    output = part1 / part2 * pow(p_me, 0.5) / pow(p_mr, 0.5)
    return output


def snd_line_shape(e,
                   mr_phi, wr_phi, b_phi, phase_phi,
                   mr_omega1420, wr_omega1420, b_omega1420, phase_omega1420,
                   mr_omega1650, wr_omega1650, b_omega1650, phase_omega1650,
                   mr_omega_new, wr_omega_new, b_omega_new, phase_omega_new,
                   back, phase_back):
    resonance = 0.0 + 0.0j
    if(1 == 1 and b_phi > 0.0):
        resonance_phi = snd_resonance(e, mr_phi, wr_phi, hconst.rho770.mass, hconst.piz.mass, 1, b_phi)
        phi_phi = phase_to_value(phase_phi)
        resonance += resonance_phi * phi_phi
    if(1 == 1 and b_omega1420 > 0.0):
        resonance_omega1420 = snd_resonance(e, mr_omega1420, wr_omega1420, hconst.rho770.mass, hconst.piz.mass, 1, b_omega1420)
        phi_omega1420 = phase_to_value(phase_omega1420)
        resonance += resonance_omega1420 * phi_omega1420
    if(1 == 1 and b_omega1650 > 0.0):
        resonance_omega1650 = snd_resonance(e, mr_omega1650, wr_omega1650, hconst.rho770.mass, hconst.piz.mass, 1, b_omega1650)
        phi_omega1650 = phase_to_value(phase_omega1650)
        resonance += resonance_omega1650 * phi_omega1650
    if(1 == 1 and b_omega_new > 0.0):
        resonance_omega_new = snd_resonance(e, mr_omega_new, wr_omega_new, hconst.rho770.mass, hconst.piz.mass, 1, b_omega_new)
        phi_omega_new = phase_to_value(phase_omega_new)
        #resonance += resonance_omega_new * phi_omega_new
    if(1 == 1 and back > 0.0):
        phi_back = phase_to_value(phase_back)
        resonance += back * phi_back

    output = abs(resonance)**2 / e**3
    return output
