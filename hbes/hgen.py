# -*- coding: UTF-8 -*-
# Public package
import math
# Private package
import headpy.hbes.hconst as hconst

# region 定义常数
pi = math.pi
mpipm = hconst.pipm.mass
mpip = hconst.pipm.mass
mpim = hconst.pipm.mass
mpiz = hconst.piz.mass
delta = ((-1.0, 0.0, 0.0, 0.0),
         (0.0, -1.0, 0.0, 0.0),
         (0.0, 0.0, -1.0, 0.0),
         (0.0, 0.0, 0.0, 1.0))
gelta = ((-1.0, 0.0, 0.0, 0.0),
         (0.0, -1.0, 0.0, 0.0),
         (0.0, 0.0, -1.0, 0.0),
         (0.0, 0.0, 0.0, 0.0))
unit_real = 1.0 + 0.0j
unit_imag = 0.0 + 1.0j
# endregion
# region GS model


def fundecaymomentum(mr_2, m1_2, m2_2):
    mr = math.sqrt(mr_2)
    m1 = math.sqrt(m1_2)
    m2 = math.sqrt(m2_2)
    poly = mr_2**2 + m1_2**2 + m2_2**2 - 2 * m1_2 * m2_2 - 2 * mr_2 * m2_2 - 2 * m1_2 * mr_2
    if(poly < 0.0 and poly > -0.00001): poly = 0.0
    output = math.sqrt(poly) / (2 * mr)
    if(m1 + m2 > mr):
        output = 0.0
    return output


def fundecaymomentum2(mr_2, m1_2, m2_2):
    mr = math.sqrt(mr_2)
    m1 = math.sqrt(m1_2)
    m2 = math.sqrt(m2_2)
    poly = mr_2**2 + m1_2**2 + m2_2**2 - 2 * m1_2 * m2_2 - 2 * mr_2 * m2_2 - 2 * m1_2 * mr_2
    if(poly < 0.0 and poly > -0.00001): poly = 0.0
    output = poly / (4 * mr_2)
    if(m1 + m2 > mr):
        output = 0.0
    return output


def h(m, q):
    output = 2.0 / pi * q / m * math.log((m + 2.0 * q) / (2.0 * mpipm))
    return output


def dh(m0, q0):
    output = h(m0, q0) * (1.0 / (8.0 * q0 * q0) - 1.0 / (2.0 * m0 * m0)) + 1.0 / (2.0 * pi * m0 * m0)
    return output


def f(m0, sx, q0, q):
    m = math.sqrt(sx)
    output = m0 * m0 / (q0 * q0 * q0) * (q * q * (h(m, q) - h(m0, q0)) + (m0 * m0 - sx) * q0 * q0 * dh(m0, q0))
    return output


def d(m0, q0):
    part1 = 3.0 / pi * mpipm * mpipm / (q0 * q0) * math.log((m0 + 2.0 * q0) / (2.0 * mpipm))
    part2 = m0 / (2.0 * pi * q0)
    part3 = (mpipm * mpim * m0) / (pi * q0 * q0 * q0)
    output = part1 + part2 - part3
    return output


def wid(mass, sa, sb, sc, r, l):
    widm = 1.0
    sa0 = mass * mass
    m = math.sqrt(sa)
    q = fundecaymomentum2(sa, sb, sc)
    q0 = fundecaymomentum2(sa0, sb, sc)
    z = q * r * r
    z0 = q0 * r * r
    F = 0.0
    if (l == 0):
        F = 1.0
    if (l == 1):
        F = math.sqrt((1.0 + z0) / (1.0 + z))
    if (l == 2):
        F = math.sqrt((9.0 + 3.0 * z0 + z0 * z0) / (9.0 + 3.0 * z + z * z))
    t = math.sqrt(q / q0)
    for i in range(2 * l + 1):
        widm = widm * t
    widm = widm * (mass / m * F * F)
    return widm


def kernelGS(mx2, mr, wr, m1_2, m2_2, r, l):
    mr2 = mr * mr
    q = fundecaymomentum(mx2, m1_2, m2_2)
    q0 = fundecaymomentum(mr2, m1_2, m2_2)
    numer = 1.0 + d(mr, q0) * wr / mr
    denom_real = mr2 - mx2 + wr * f(mr, mx2, q0, q)
    denom_imag = mr * wr * wid(mr, mx2, m1_2, m2_2, r, l)
    denom = denom_real * denom_real + denom_imag * denom_imag
    x = denom_real * numer / denom
    y = denom_imag * numer / denom
    output = x * unit_real + y * unit_imag
    return output


# endregion
# region BW massdependent
def kernelmassdependentbreitwigner0(mx2, mr, mr2, wr, pmr, m1_2, m2_2):
    diff = mr2 - mx2
    p_s = fundecaymomentum(mx2, m1_2, m2_2)
    mx = math.sqrt(mx2)
    ws = wr * (mr2 / mx2) * (p_s / pmr)
    denom = diff * diff + mx2 * ws * ws
    x = diff / denom
    y = mx * ws / denom
    output = x * unit_real + y * unit_imag
    return output


def kernelmassdependentbreitwigner1(mx2, mr, mr2, wr, pmr, m1_2, m2_2):
    p_s = fundecaymomentum(mx2, m1_2, m2_2)
    ppart = (p_s / pmr)
    ppart3 = ppart * ppart * ppart
    diff = mr2 - mx2
    mx = math.sqrt(mx2)
    ws = wr * (mr2 / mx2) * ppart3
    denom = diff * diff + mx2 * ws * ws
    x = diff / denom
    y = mx * ws / denom
    output = x * unit_real + y * unit_imag
    return output


def kernelmassdependentbreitwigner2(mx2, mr, mr2, wr, pmr, m1_2, m2_2):
    p_s = fundecaymomentum(mx2, m1_2, m2_2)
    ppart = (p_s / pmr)
    ppart2 = ppart * ppart
    diff = mr2 - mx2
    mx = math.sqrt(mx2)
    ppart5 = ppart2 * ppart2 * ppart
    ws = wr * (mr2 / mx2) * ppart5
    denom = diff * diff + mx2 * ws * ws
    x = diff / denom
    y = mx * ws / denom
    output = x * unit_real + y * unit_imag
    return output


def kernelmassdependentbreitwigner3(mx2, mr, mr2, wr, pmr, m1_2, m2_2):
    p_s = fundecaymomentum(mx2, m1_2, m2_2)
    ppart = (p_s / pmr)
    ppart3 = ppart * ppart * ppart
    diff = mr2 - mx2
    mx = math.sqrt(mx2)
    ppart7 = ppart3 * ppart3 * ppart
    ws = wr * (mr2 / mx2) * ppart7
    denom = diff * diff + mx2 * ws * ws
    x = diff / denom
    y = mx * ws / denom
    output = x * unit_real + y * unit_imag
    return output


def kernelmassdependentbreitwigner4(mx2, mr, mr2, wr, pmr, m1_2, m2_2):
    p_s = fundecaymomentum(mx2, m1_2, m2_2)
    ppart = (p_s / pmr)
    ppart2 = ppart * ppart
    ppart4 = ppart2 * ppart2
    diff = mr2 - mx2
    mx = math.sqrt(mx2)
    ppart9 = ppart4 * ppart4 * ppart
    ws = wr * (mr2 / mx2) * ppart9
    denom = diff * diff + mx2 * ws * ws
    x = diff / denom
    y = mx * ws / denom
    output = x * unit_real + y * unit_imag
    return output


def kernelmassdependentbreitwigner(mx2, mr, wr, m1_2, m2_2, l):
    pmr = fundecaymomentum(mr**2, m1_2, m2_2)
    output = 0 + 0j
    if(l == 0):
        output = kernelmassdependentbreitwigner0(mx2, mr, mr * mr, wr, pmr, m1_2, m2_2)
    elif(l == 1):
        output = kernelmassdependentbreitwigner1(mx2, mr, mr * mr, wr, pmr, m1_2, m2_2)
    elif(l == 2):
        output = kernelmassdependentbreitwigner2(mx2, mr, mr * mr, wr, pmr, m1_2, m2_2)
    elif(l == 3):
        output = kernelmassdependentbreitwigner3(mx2, mr, mr * mr, wr, pmr, m1_2, m2_2)
    elif(l == 4):
        output = kernelmassdependentbreitwigner4(mx2, mr, mr * mr, wr, pmr, m1_2, m2_2)
    else:
        print('invalid value for the angular momentum!')
    return output


# endregion
# region Generator
def epsilon(A, B, C, D):
    if(A == B or A == C or A == D or B == C or B == D or C == D):
        output = 0.0
    else:
        g = 0
        if(A > B): g += 1
        if(A > C): g += 1
        if(A > D): g += 1
        if(B > C): g += 1
        if(B > D): g += 1
        if(C > D): g += 1
        output = pow(-1.0, g)
    return output


def scalar(p1, p2):
    output = 0.0
    for i in range(4):
        output += p1[i] * p2[i] * delta[i][i]
    return output


def q_function(sa, sb, sc):
    output = ((sa + sb - sc)**2 / (4.0 * sa)) - sb
    return output


def b_function(q, l):
    ps2 = q
    ps4 = q**2
    ps6 = q**3
    ps8 = q**4
    pz2 = (0.197321 / 0.728656)**2
    pz4 = pz2**2
    pz6 = pz2**3
    pz8 = pz2**4
    output = 0.0
    if(l == 1):
        output = math.sqrt(2.0 / (ps2 + pz2))
    if(l == 2):
        output = math.sqrt(13.0 / (ps4 + 3.0 * ps2 * pz2 + 9.0 * pz4))
    if(l == 3):
        output = math.sqrt(277.0 / (ps6 + 6.0 * ps4 * pz2 + 45.0 * ps2 * pz4 + 225.0 * pz6))
    if(l == 4):
        output = math.sqrt(12746.0 / (ps8 + 10.0 * ps6 * pz2 + 135.0 * ps4 * pz4 + 1575.0 * ps2 * pz6 + 11025.0 * pz8))
    return output


def amplitude(v1, v2, v3,
              a1, b1,
              a2, b2,
              a3, b3,
              a4, b4,
              a5, b5):
    # region set v r s m
    v12 = [0.0] * 4
    v13 = [0.0] * 4
    v23 = [0.0] * 4
    v123 = [0.0] * 4
    r_1_2 = [0.0] * 4
    r_1_3 = [0.0] * 4
    r_2_3 = [0.0] * 4
    r_12_3 = [0.0] * 4
    r_13_2 = [0.0] * 4
    r_23_1 = [0.0] * 4
    for i in range(4):
        v12[i] = v1[i] + v2[i]
        v13[i] = v1[i] + v3[i]
        v23[i] = v2[i] + v3[i]
        v123[i] = v1[i] + v2[i] + v3[i]
        r_1_2[i] = v1[i] - v2[i]
        r_1_3[i] = v1[i] - v3[i]
        r_2_3[i] = v2[i] - v3[i]
        r_12_3[i] = v12[i] - v3[i]
        r_13_2[i] = v13[i] - v2[i]
        r_23_1[i] = v23[i] - v1[i]
    s1 = scalar(v1, v1)
    s2 = scalar(v2, v2)
    s3 = scalar(v3, v3)
    s12 = scalar(v12, v12)
    s13 = scalar(v13, v13)
    s23 = scalar(v23, v23)
    s123 = scalar(v123, v123)
    m1 = math.sqrt(s1)
    m2 = math.sqrt(s2)
    m3 = math.sqrt(s3)
    m12 = math.sqrt(s12)
    m13 = math.sqrt(s13)
    m23 = math.sqrt(s23)
    m123 = math.sqrt(s123)
    # endregion
    # region set vr
    vr_1_2 = [0.0] * 4
    vr_1_3 = [0.0] * 4
    vr_2_3 = [0.0] * 4
    vr_12_3 = [0.0] * 4
    vr_13_2 = [0.0] * 4
    vr_23_1 = [0.0] * 4
    for i in range(4):
        for j in range(4):
            vr_1_2[i] += r_1_2[j] * delta[j][j] * (delta[i][j] - v12[i] * v12[j] / s12)
            vr_1_3[i] += r_1_3[j] * delta[j][j] * (delta[i][j] - v13[i] * v13[j] / s13)
            vr_2_3[i] += r_2_3[j] * delta[j][j] * (delta[i][j] - v23[i] * v23[j] / s23)
            vr_12_3[i] += r_12_3[j] * gelta[i][j] * delta[j][j]
            vr_13_2[i] += r_13_2[j] * gelta[i][j] * delta[j][j]
            vr_23_1[i] += r_23_1[j] * gelta[i][j] * delta[j][j]
    # endregion
    # region set q_function
    q_all_rhop_pim = q_function(s123, s13, s2)
    q_all_rhom_pip = q_function(s123, s23, s1)
    q_all_rhoz_piz = q_function(s123, s12, s3)
    q_rhop_pip_piz = q_function(s13, s1, s3)
    q_rhom_pim_piz = q_function(s23, s2, s3)
    q_rhoz_pip_pim = q_function(s12, s1, s2)
    # endregion
    # region set b_function
    b1_all_rhop_pim = b_function(q_all_rhop_pim, 1)
    b1_all_rhom_pip = b_function(q_all_rhom_pip, 1)
    b1_all_rhoz_piz = b_function(q_all_rhoz_piz, 1)
    b1_rhop_pip_piz = b_function(q_rhop_pip_piz, 1)
    b1_rhom_pim_piz = b_function(q_rhom_pim_piz, 1)
    b1_rhoz_pip_pim = b_function(q_rhoz_pip_pim, 1)
    b3_all_rhop_pim = b_function(q_all_rhop_pim, 3)
    b3_all_rhom_pip = b_function(q_all_rhom_pip, 3)
    b3_all_rhoz_piz = b_function(q_all_rhoz_piz, 3)
    b3_rhop_pip_piz = b_function(q_rhop_pip_piz, 3)
    b3_rhom_pim_piz = b_function(q_rhom_pim_piz, 3)
    b3_rhoz_pip_pim = b_function(q_rhoz_pip_pim, 3)
    # endregion
    # region set t_function
    t1_all_rhop_pim = [0.0] * 4
    t1_all_rhom_pip = [0.0] * 4
    t1_all_rhoz_piz = [0.0] * 4
    t1_rhop_pip_piz = [0.0] * 4
    t1_rhom_pim_piz = [0.0] * 4
    t1_rhoz_pip_pim = [0.0] * 4
    t3_all_rhop_pim = [[[0.0 for i in range(4)] for j in range(4)] for k in range(4)]
    t3_all_rhom_pip = [[[0.0 for i in range(4)] for j in range(4)] for k in range(4)]
    t3_all_rhoz_piz = [[[0.0 for i in range(4)] for j in range(4)] for k in range(4)]
    t3_rhop_pip_piz = [[[0.0 for i in range(4)] for j in range(4)] for k in range(4)]
    t3_rhom_pim_piz = [[[0.0 for i in range(4)] for j in range(4)] for k in range(4)]
    t3_rhoz_pip_pim = [[[0.0 for i in range(4)] for j in range(4)] for k in range(4)]
    for i in range(4):
        t1_all_rhop_pim[i] = vr_13_2[i] * b1_all_rhop_pim
        t1_all_rhom_pip[i] = vr_23_1[i] * b1_all_rhom_pip
        t1_all_rhoz_piz[i] = vr_12_3[i] * b1_all_rhoz_piz
        t1_rhop_pip_piz[i] = vr_1_3[i] * b1_rhop_pip_piz
        t1_rhom_pim_piz[i] = vr_2_3[i] * b1_rhom_pim_piz
        t1_rhoz_pip_pim[i] = vr_1_2[i] * b1_rhoz_pip_pim
    for i in range(4):
        for j in range(4):
            for k in range(4):
                t3_all_rhop_pim[i][j][k] = b3_all_rhop_pim * (vr_13_2[i] * vr_13_2[j] * vr_13_2[k] - 0.2 * scalar(vr_13_2, vr_13_2) * (gelta[i][j] * vr_13_2[k] + gelta[j][k] * vr_13_2[i] + gelta[k][i] * vr_13_2[j]))
                t3_all_rhom_pip[i][j][k] = b3_all_rhom_pip * (vr_23_1[i] * vr_23_1[j] * vr_23_1[k] - 0.2 * scalar(vr_23_1, vr_23_1) * (gelta[i][j] * vr_23_1[k] + gelta[j][k] * vr_23_1[i] + gelta[k][i] * vr_23_1[j]))
                t3_all_rhoz_piz[i][j][k] = b3_all_rhoz_piz * (vr_12_3[i] * vr_12_3[j] * vr_12_3[k] - 0.2 * scalar(vr_12_3, vr_12_3) * (gelta[i][j] * vr_12_3[k] + gelta[j][k] * vr_12_3[i] + gelta[k][i] * vr_12_3[j]))
                t3_rhop_pip_piz[i][j][k] = b3_rhop_pip_piz * (vr_1_3[i] * vr_1_3[j] * vr_1_3[k] - 0.2 * scalar(vr_1_3, vr_1_3) * (gelta[i][j] * vr_1_3[k] + gelta[j][k] * vr_1_3[i] + gelta[k][i] * vr_1_3[j]))
                t3_rhom_pim_piz[i][j][k] = b3_rhom_pim_piz * (vr_2_3[i] * vr_2_3[j] * vr_2_3[k] - 0.2 * scalar(vr_2_3, vr_2_3) * (gelta[i][j] * vr_2_3[k] + gelta[j][k] * vr_2_3[i] + gelta[k][i] * vr_2_3[j]))
                t3_rhoz_pip_pim[i][j][k] = b3_rhoz_pip_pim * (vr_1_2[i] * vr_1_2[j] * vr_1_2[k] - 0.2 * scalar(vr_1_2, vr_1_2) * (gelta[i][j] * vr_1_2[k] + gelta[j][k] * vr_1_2[i] + gelta[k][i] * vr_1_2[j]))
    # endregion
    # region set propagator
    prop_rho770pi_p = kernelGS(s13, hconst.rho770.mass, hconst.rho770.width, mpip**2, mpiz**2, 3.0, 1)
    prop_rho770pi_m = kernelGS(s23, hconst.rho770.mass, hconst.rho770.width, mpim**2, mpiz**2, 3.0, 1)
    prop_rho770pi_z = kernelGS(s12, hconst.rho770.mass, hconst.rho770.width, mpip**2, mpim**2, 3.0, 1)
    prop_rho1450pi_p = kernelmassdependentbreitwigner(s13, hconst.rho1450.mass, hconst.rho1450.width, mpip**2, mpiz**2, 1)
    prop_rho1450pi_m = kernelmassdependentbreitwigner(s23, hconst.rho1450.mass, hconst.rho1450.width, mpim**2, mpiz**2, 1)
    prop_rho1450pi_z = kernelmassdependentbreitwigner(s12, hconst.rho1450.mass, hconst.rho1450.width, mpip**2, mpim**2, 1)
    prop_rho1700pi_p = kernelmassdependentbreitwigner(s13, hconst.rho1700.mass, hconst.rho1700.width, mpip**2, mpiz**2, 1)
    prop_rho1700pi_m = kernelmassdependentbreitwigner(s23, hconst.rho1700.mass, hconst.rho1700.width, mpim**2, mpiz**2, 1)
    prop_rho1700pi_z = kernelmassdependentbreitwigner(s12, hconst.rho1700.mass, hconst.rho1700.width, mpip**2, mpim**2, 1)
    prop_rho1690pi_p = kernelmassdependentbreitwigner(s13, hconst.rho1690.mass, hconst.rho1690.width, mpip**2, mpiz**2, 3)
    prop_rho1690pi_m = kernelmassdependentbreitwigner(s23, hconst.rho1690.mass, hconst.rho1690.width, mpim**2, mpiz**2, 3)
    prop_rho1690pi_z = kernelmassdependentbreitwigner(s12, hconst.rho1690.mass, hconst.rho1690.width, mpip**2, mpim**2, 3)
    prop_omega782pi = kernelmassdependentbreitwigner(s12, hconst.omega782.mass, hconst.omega782.width, mpip**2, mpim**2, 1)
    # endregion
    # region set fCF fCP pa fu
    nwaves = 5
    fCF = [[0.0 + 0.0j for i in range(2)] for j in range(nwaves)]
    fCP = [0.0 + 0.0j] * nwaves
    for i in range(nwaves):
        fCF[i][0] = 0.0 + 0.0j
        fCF[i][1] = 0.0 + 0.0j
        fCP[i] = 0.0 + 0.0j
    pa = [[0.0 for i in range(5)] for j in range(5)]
    fu = [[0.0 for i in range(5)] for j in range(5)]
    fCP[0] = (a1 * math.cos(b1)) * unit_real + (a1 * math.sin(b1)) * unit_imag
    fCP[1] = (a2 * math.cos(b2)) * unit_real + (a2 * math.sin(b2)) * unit_imag
    fCP[2] = (a3 * math.cos(b3)) * unit_real + (a3 * math.sin(b3)) * unit_imag
    fCP[3] = (a4 * math.cos(b4)) * unit_real + (a4 * math.sin(b4)) * unit_imag
    fCP[4] = (a5 * math.cos(b5)) * unit_real + (a5 * math.sin(b5)) * unit_imag
    for i in range(nwaves):
        for j in range(nwaves):
            temp = fCP[i] * fCP[j].conjugate()
            if(i == j):
                pa[i][j] = temp.real
            elif(i < j):
                pa[i][j] = 2.0 * temp.real
            else:
                pa[i][j] = 2.0 * temp.imag
    # endregion
    # region calculate waves
    cf_rho770pi_p = [0.0 + 0.0j] * 3
    cf_rho770pi_m = [0.0 + 0.0j] * 3
    cf_rho770pi_z = [0.0 + 0.0j] * 3
    cf_rho1450pi_p = [0.0 + 0.0j] * 3
    cf_rho1450pi_m = [0.0 + 0.0j] * 3
    cf_rho1450pi_z = [0.0 + 0.0j] * 3
    cf_rho1700pi_p = [0.0 + 0.0j] * 3
    cf_rho1700pi_m = [0.0 + 0.0j] * 3
    cf_rho1700pi_z = [0.0 + 0.0j] * 3
    cf_rho1690pi_p = [0.0 + 0.0j] * 3
    cf_rho1690pi_m = [0.0 + 0.0j] * 3
    cf_rho1690pi_z = [0.0 + 0.0j] * 3
    cf_omega782pi = [0.0 + 0.0j] * 3
    # rho770pi
    for I in range(2):
        for J in range(4):
            for K in range(4):
                cf_rho770pi_p[I] += m123 * epsilon(I, J, K, 3) * t1_rhop_pip_piz[K] * t1_all_rhop_pim[J] * delta[J][J] * delta[K][K] * prop_rho770pi_p
                cf_rho770pi_m[I] += m123 * epsilon(I, J, K, 3) * t1_rhom_pim_piz[K] * t1_all_rhom_pip[J] * delta[J][J] * delta[K][K] * prop_rho770pi_m
                cf_rho770pi_z[I] += m123 * epsilon(I, J, K, 3) * t1_rhoz_pip_pim[K] * t1_all_rhoz_piz[J] * delta[J][J] * delta[K][K] * prop_rho770pi_z
    # rho1450pi
    for I in range(2):
        for J in range(4):
            for K in range(4):
                cf_rho1450pi_p[I] += m123 * epsilon(I, J, K, 3) * t1_rhop_pip_piz[K] * t1_all_rhop_pim[J] * delta[J][J] * delta[K][K] * prop_rho1450pi_p
                cf_rho1450pi_m[I] += m123 * epsilon(I, J, K, 3) * t1_rhom_pim_piz[K] * t1_all_rhom_pip[J] * delta[J][J] * delta[K][K] * prop_rho1450pi_m
                cf_rho1450pi_z[I] += m123 * epsilon(I, J, K, 3) * t1_rhoz_pip_pim[K] * t1_all_rhoz_piz[J] * delta[J][J] * delta[K][K] * prop_rho1450pi_z
    # rho1700pi
    for I in range(2):
        for J in range(4):
            for K in range(4):
                cf_rho1700pi_p[I] += m123 * epsilon(I, J, K, 3) * t1_rhop_pip_piz[K] * t1_all_rhop_pim[J] * delta[J][J] * delta[K][K] * prop_rho1700pi_p
                cf_rho1700pi_m[I] += m123 * epsilon(I, J, K, 3) * t1_rhom_pim_piz[K] * t1_all_rhom_pip[J] * delta[J][J] * delta[K][K] * prop_rho1700pi_m
                cf_rho1700pi_z[I] += m123 * epsilon(I, J, K, 3) * t1_rhoz_pip_pim[K] * t1_all_rhoz_piz[J] * delta[J][J] * delta[K][K] * prop_rho1700pi_z
    # rho1690pi
    for I in range(2):
        for J in range(4):
            for M in range(4):
                for K in range(4):
                    for L in range(4):
                        cf_rho1690pi_p[I] += m123 * epsilon(I, J, M, 3) * t3_all_rhop_pim[J][K][L] * t3_rhop_pip_piz[M][K][L] * delta[J][J] * delta[L][L] * delta[K][K] * delta[M][M] * prop_rho1690pi_p
                        cf_rho1690pi_m[I] += m123 * epsilon(I, J, M, 3) * t3_all_rhom_pip[J][K][L] * t3_rhom_pim_piz[M][K][L] * delta[J][J] * delta[L][L] * delta[K][K] * delta[M][M] * prop_rho1690pi_m
                        cf_rho1690pi_z[I] += m123 * epsilon(I, J, M, 3) * t3_all_rhoz_piz[J][K][L] * t3_rhoz_pip_pim[M][K][L] * delta[J][J] * delta[L][L] * delta[K][K] * delta[M][M] * prop_rho1690pi_z
    # omegapi
    for I in range(2):
        for J in range(4):
            for K in range(4):
                cf_omega782pi[I] += m123 * epsilon(I, J, K, 3) * t1_rhoz_pip_pim[K] * t1_all_rhoz_piz[J] * delta[J][J] * delta[K][K] * prop_omega782pi
    # endregion
    # region calculate amplitude
    for i in range(2):
        fCF[0][i] = cf_rho770pi_m[i] + cf_rho770pi_z[i] - cf_rho770pi_p[i]
        fCF[1][i] = cf_rho1450pi_m[i] + cf_rho1450pi_z[i] - cf_rho1450pi_p[i]
        fCF[2][i] = cf_rho1700pi_m[i] + cf_rho1700pi_z[i] - cf_rho1700pi_p[i]
        fCF[3][i] = cf_rho1690pi_m[i] + cf_rho1690pi_z[i] - cf_rho1690pi_p[i]
        fCF[4][i] = cf_omega782pi[i]
    for i in range(nwaves):
        for j in range(nwaves):
            temp = 0.0 + 0.0j
            for u in range(2):
                temp += 0.5 * fCF[i][u] * fCF[j][u].conjugate()
            if(i == j):
                fu[i][j] += temp.real
            if(i < j):
                fu[i][j] += temp.real
            if(i > j):
                fu[i][j] += -temp.imag
    output = 0.0
    for i in range(nwaves):
        for j in range(nwaves):
            output += pa[i][j] * fu[i][j]
    if(output < 0.0):
        output = 0.00000001
    return output
    # endregion
# endregion
