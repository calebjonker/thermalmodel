import numpy as np
from thermalmodel.materials import Material, material_list 

class Stage(object):
    """A class for specifying stage dimensions."""
    def __init__(self, standoff_material, height, cross_section, angle):
        self.standoff_material = standoff_material
        self.height = height
        self.cross_section = cross_section
        self.angle = angle
    
    def g(self):
        return np.cos(np.pi*self.angle/180.0)*self.cross_section / self.height
    
    def standoff_heat_transfer(self, temp1, temp2):
        return self.g() * self.standoff_material.int_thermal_conductivity(temp1, temp2)[0]
    
if __name__ == '__main__':
    CPtoMC = Stage(material_list[2], 0.035, 9.29E-6, 5.5E1)
    print("Standoff heat transfer is {:.2e} W ".format(CPtoMC.standOffHeatTransfer(0.015,0.15)))

