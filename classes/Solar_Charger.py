from Station import Station
from Ecosystem import Ecosystem
from Utilities import irradiance

############################################
# @title Solar_Charger Class [code] {display-mode: "code"} 
############################################

class Solar_Charger(Station):
  def __init__(self, ecosystem: Ecosystem, name = "sunny", *args, **kwargs):
    super().__init__(ecosystem, name, *args, **kwargs)
    self.kind = "Solar_Charger"
    self._shape = "diamond"
    self._color = "green"
    self.MAX_POWER = 222
    
  @property
  def solar_power_factor(self):
    return irradiance(self.ecosystem.hour)
  
  # METHOD
  def charge(self):
    self.occupant.soc += self.MAX_POWER * self.solar_power_factor