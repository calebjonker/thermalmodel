import numpy as np
import pkg_resources
import csv
from scipy.interpolate import interp1d
from scipy.integrate import quad

class Material(object):
    """A class of materials used in the cryostat."""
    def __init__(self, thermal_conductivity, name):
        self.thermal_conductivity = thermal_conductivity
        self.name = name

    def int_thermal_conductivity(self,temp1, temp2):
        return quad(self.thermal_conductivity, temp1, temp2)
    
    def __repr__(self):
        return self.name

def k_BeCu(temp):
        coeff = np.array([-0.50015, 1.93190, -1.69540, 0.71218, 1.27880, 1.61450, 0.68722, -0.10501, 0])
        logs = np.array([np.log10(temp)**n for n in range(9)])
        k = 10**np.dot(coeff, logs)
        return k

def k_Ti15333_wikus(temp):
    Tc = 3.89
    alpha = 0.043
    beta = 0.27
    delta = 0.4
    if temp <= Tc:
        k = alpha * temp * np.exp(-beta * Tc / temp)
    elif temp >= Tc:
        k = alpha * Tc**(1-delta) * np.exp(-beta) * temp**0.4
    return k

def k_graphlite_runyan(temp): # 0.3 - 4.2 K
    alpha = 0.00839
    beta =  2.12
    gamma = -1.05
    n = 0.181
    k = alpha * temp ** (beta + gamma*temp**n)
    return k

def k_kapton_rule(temp): # 4.2 - 300 K
    coeff = np.array([3.0792762*10**-2, -3.2061706*10**-2, 12.444129*10**-3, -10.070564*10**-4])
    logs = np.array([np.log(temp+1)**(n+1) for n in range(4)])
    k = np.dot(coeff, logs)
    return k

def k_kapton_barucci(temp): # 0.2 - 5 K
    return

def k_kapton_epoxy_kellaris(temp): # 0.07 - 1 K
    k = 10**(1.81+1.01*np.log10(temp)-0.348*np.log10(temp)**2) * 10**-4
    return k

def k_SS316_nist(temp): # 4-300K
    coeff = np.array([-1.4087,1.3982,0.2543,-0.6260,0.2334,0.4256,-0.4658,0.1650,-0.0199])
    logs = np.array([np.log10(temp)**n for n in range(9)])
    k = 10**np.dot(coeff, logs)
    return k

def k_SS316_barucci(temp): # 0.045-4.3K
    k = 0.0556 * temp**1.15
    return k

def k_NbTi_olson(temp): # 0.05 - 2K
    A = 150*10**-4
    B = 2.0
    k = A*temp**B
    return k


#k_graphlite_runyan = interp1d(*np.loadtxt('graphlite_runyan.csv', delimiter='\t', unpack=True, usecols=(0,1)), kind ='cubic')
k_POCO_AXM5Q = interp1d(*list(zip(*[map(float, line.split(', ')) for line in \
              pkg_resources.resource_string('thermalmodel.data', 'POCO_AXM-5Q.csv')\
              .decode('utf-8').split('\r\n')])), kind='cubic')

k_Ti15333_runyan = interp1d(*list(zip(*[map(float, line.split('\t')) for line in \
              pkg_resources.resource_string('thermalmodel.data', 'Ti15333_runyan.csv')\
              .decode('utf-8').split('\r\n')]))[:-1], kind='cubic')

BeCu = Material(k_BeCu, '98Cu-2Be, NIST')
Ti15333_wikus = Material(k_Ti15333_wikus, 'Ti15333, Wikus')
Ti15333_runyan = Material(k_Ti15333_runyan, 'Ti15333, Runyan')
graphlite_runyan = Material(k_graphlite_runyan,'Graphlite, Runyan')
kapton_rule = Material(k_kapton_rule, 'Kapton HN, Rule')
kapton_barucci = Material(k_kapton_barucci, 'Kapton HN, Barucci')
kapton_epoxy_kellaris = Material(k_kapton_epoxy_kellaris, 'Kapton Epoxy, Kellaris')
SS316_nist = Material(k_SS316_nist, 'SS316, NIST')
SS316_barucci = Material(k_SS316_barucci, 'SS316, Barucci')
NbTi_olson = Material(k_NbTi_olson, 'NbTi, Olson')
POCO_AXM5Q = Material(k_POCO_AXM5Q, 'POCO AXM-5Q, Woodcraft')

material_list = [BeCu, Ti15333_wikus, Ti15333_runyan, graphlite_runyan, kapton_rule, kapton_barucci, kapton_epoxy_kellaris, SS316_nist, SS316_barucci, NbTi_olson, POCO_AXM5Q]

material_dict = {repr(mat):mat for mat in material_list}

if __name__ == '__main__':
    print(Ti15333_runyan.int_thermal_conductivity(0.015,0.15))
    print('The integrated thermal conductivity of Ti15333 between 0.15 and 0.015 K is {:.3e} W/m'\
          .format(Ti15333_runyan.int_thermal_conductivity(0.015,0.15)[0]))
