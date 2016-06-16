import numpy as np
from scipy.integrate import quad
from scipy.interpolate import interp1d
from materials import Material

class ThermalModel(object):
    """A class for modeling heat transfer between stages."""
    
    def __init__(self, qChanPDetect=4, detectPTower=6, nTowers=48, roomTemp=300, heatsink40K=50, stage=5, \
    still=0.8, coldplate=0.157, mixingChamber=0.015):
        """Return a new ThermalModel object.
    
        Keyword arguments:
        qChanPDetect -- the number of charge chanels per detector (default 4)
        detectPTower -- the number of detectors per tower (default 6)
        nTowers -- the number of towers (default 48)
        roomTemp -- room temperature (K) (default 300)
        heatsink40K -- 40K heatsink temperature (K) (default 50)
        stage -- 4.2K stage temperature (K) (default 5)
        still -- still temperature (K) (default 0.8)
        coldplate -- cold plate temperature (K) (default 0.157)
        mixingChamber -- mixing chamber temperature (K) (default 0.015)
        """
        
        self.qChanPDetect = qChanPDetect
        self.detectPTower = detectPTower
        self.nTowers = nTowers
        self.roomTemp = roomTemp
        self.heatsink40K = heatsink40K
        self.stage = stage
        self.still = still
        self.coldplate = coldplate
        self.mixingChamber = mixingChamber


    def copper_hc(temp):
        coeff = np.array([4.2610-7, 8.0310-6, 4.9010-6, -2.2710-6, 8.1310-7, -7.0910-8])
        temps = np.array([tempn for n in range(6)])
        hc = np.dot(coeff, temps)
        return hc

    def intK(temp):
        return quad(thermal_conductivity_BeCu, 0.001, temp)

    def heat_transfer(temp1, temp2, k, detectorsPerTower):
        g = detectorspertowerndetectorsAl
        return quad(k, temp1, temp2) * g 
