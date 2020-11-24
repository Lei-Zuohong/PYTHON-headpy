# -*- coding: UTF-8 -*-
# Public package
# Private package


class PARTICLE():
    def __init__(self,
                 mass, mass_err, width, width_err,
                 j=0, p=0, c=0, i=0, g=0):
        self.name = ''
        self.title = ''
        self.mass = mass
        self.mass_err = mass_err
        self.width = width
        self.width_err = width_err
        self.j = j
        self.p = p
        self.c = c
        self.i = i
        self.g = g
        self.decay = {}

    def set_decay(self, name, branch_ratio):
        self.decay[name] = branch_ratio


# pi
pipm = PARTICLE(0.13957039, 0.00018, 0, 0, j=0)
piz = PARTICLE(0.1349768, 0.0005, 0, 0, j=0)
piz.set_decay('gammagamma', 0.98823)
# omega
omega782 = PARTICLE(0.78265, 0.00012, 0.00849, 0.00008, j=1)
omega782.set_decay('pippimpiz', 0.893)
omega1420 = PARTICLE(1.41, 0.06, 0.29, 0.19, j=1)
omega1650 = PARTICLE(1.67, 0.03, 0.315, 0.035, j=1)
omega1670 = PARTICLE(1.667, 0.004, 0.168, 0.01, j=3)
# rho
rho770n = PARTICLE(0.77526, 0.00025, 0.1478, 0.0009, j=1)
rho770c = PARTICLE(0.77511, 0.00034, 0.1491, 0.0008, j=1)
rho770 = PARTICLE((rho770n.mass + rho770c.mass) / 2,
                  (rho770n.mass_err + rho770c.mass_err) / 2,
                  (rho770n.width + rho770c.width) / 2,
                  (rho770n.width_err + rho770c.width_err) / 2)
rho1450 = PARTICLE(1.465, 0.025, 0.4, 0.06, j=1)
rho1570 = PARTICLE(1.57, 0.072, 0.144, 0.086, j=1)
rho1700 = PARTICLE(1.72, 0.02, 0.25, 0.1, j=1)
rho1690 = PARTICLE(1.6888, 0.0021, 0.161, 0.01, j=3)


def pdg():
    '''
    作用: 提供PDG网页上的各种参数\n
    '''
    output = {}
    output['m_omega'] = omega782.mass
    output['m_pi0'] = piz.mass
    output['m_pipm'] = pipm.mass
    output['br_omega'] = omega782.decay['pippimpiz']
    output['br_pi0'] = piz.decay['gammagamma']
    return output


def energy_list():
    '''
    作用: 提供tQCD合作做所使用的能量点信息\n
    格式为:\n
        {energy:[runnumber_lower,\n
                runnumber_upper,\n
                luminosity,\n
                luminosity string for latex,\n
                Nhadron,\n
                Rvalue,\n
                Sigam(dimu)]}\n
    '''
    out_list = {2.0000: [41729, 41909, 10.077, '10.1$\pm$0.1', 189905829, 59.8488, 21.71259],
                2.0500: [41911, 41958, 3.351, '3.34$\pm$0.03', 70554265, 56.678, 20.66644],
                2.1000: [41588, 41727, 12.167, '12.2$\pm$0.1', 184156283, 54.0492, 19.69412],
                2.1250: [42004, 43253, 108.49, '108$\pm$1', 1431718908, 0.5 * (54.0492 + 51.7206), 0.5 * (19.69412 + 18.78883)],
                2.1500: [41533, 41570, 2.849, '2.84$\pm$0.02', 63163310, 51.7206, 18.78883],
                2.1750: [41416, 41532, 10.641, '10.6$\pm$0.1', 146758176, 48.1291, 18.35941],
                2.2000: [40989, 41121, 13.670, '13.7$\pm$0.1', 179089129, 49.5067, 17.94455],
                2.2324: [41122, 41239, 11.858, '11.9$\pm$0.1', 174097483, 48.1291, 17.42749],
                2.3094: [41240, 41411, 21.080, '21.1$\pm$0.1', 306121093, 45.0105, 16.28479],
                2.3864: [40806, 40951, 22.588, '22.5$\pm$0.2', 224667182, 42.1015, 15.25090],
                2.3960: [40459, 40769, 66.893, '66.9$\pm$0.5', 601167461, 41.7542, 15.12894],
                2.5000: [40771, 40776, 1.099, '1.10$\pm$0.01', 10132267, 38.1827, 13.89644],
                2.6444: [40128, 40296, 33.650, '33.7$\pm$0.2', 262821831, 33.8272, 12.42027],
                2.6464: [40300, 40435, 34.064, '34.0$\pm$0.3', 320673713, 33.7716, 12.40150],
                2.7000: [40436, 40439, 1.035, '1.03$\pm$0.01', 8004137, 32.3361, 11.91402],
                2.8000: [40440, 40443, 1.008, '1.01$\pm$0.01', 8207632, 29.9136, 11.07823],
                2.9000: [39775, 40069, 105.53, '105$\pm$1', 473251776, 27.8232, 10.32741],
                2.9500: [39619, 39650, 15.960, '15.9$\pm$0.1', 78242909, 26.8938, 9.98030],
                2.9810: [39651, 39679, 16.046, '16.1$\pm$0.1', 56260525, 26.3425, 9.77381],
                3.0000: [39680, 39710, 15.849, '15.9$\pm$0.1', 57711853, 26.0048, 9.65040],
                3.0200: [39711, 39738, 17.315, '17.3$\pm$0.1', 58678979, 25.6407, 9.52301],
                3.0800: [39355, 39618, 126.21, '126$\pm$1', 522838948, 23.4594, 9.15560]
                }
    return out_list


def energy_sort():
    in_energy_list = energy_list()
    out_energy_list = in_energy_list.keys()
    out_energy_list.sort()
    return out_energy_list
