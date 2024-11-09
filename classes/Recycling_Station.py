from Station import Station
from Ecosystem import Ecosystem

############################################
# @title Recycling_Station Class [code] {display-mode: "code"} 
############################################

class Recycling_Station(Station):
  """
  Recycling station can recycle a broken robot and provide some scrap metal.\n
  You can BUY robots with scrap metal.\n
  +++
  (SHOP)  
  Robot = 100 scrap metal,  
  Droid = 300 scrap metal,  
  Drone = 300 scrap metal,  
  +++\n
  +++
  (RECYCLING)  
  Robot --> 25 scrap metal,  
  Droid --> 25 scrap metal,  
  Drone --> 25 scrap metal,  
  +++
  """
  def __init__(self, ecosystem: Ecosystem, name="reuse", *args, **kwargs):
    super().__init__(self, ecosystem, name, *args, **kwargs)
    self.kind = "Recycling_Station"
    self._color = 'cyan'
    
  # METHOD
  def recycle(self):
    if (self.occupant == None and not self.reserved):
      self.reset()
    elif (self.occupant != None and self.reserved):
      # first turn into pieces
      self.ecosystem.deregister(self.occupant)

      # second send the scrap metal to central system
      self.ecosystem.scrap_metal += 25
    elif (self.reserved):
      self.prepare()