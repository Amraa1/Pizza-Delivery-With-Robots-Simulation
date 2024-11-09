from Station import Station
from Ecosystem import Ecosystem

############################################
# @title Grid_Charger Class [code] {display-mode: "code"} 
############################################

class Grid_Charger(Station):
  """
  Grid Charger has more power readily available for charging.  
  However it comes with a cost.   
  it needs an INFRASTRUCTURE and a SOURCE. 

   
  {SOURCE MAX POWER = 1000}  
  ---
  The SOURCE can only provide max power of 
  1000 unit at any given time. Grid Charger can supply 345  
  unit of power at max. Maximum power of SOURCE must be divided 
  between the grid chargers, so when above ~3 grid chargers are used simultaneously, they cannot utilize 
  their max power.  
  `
  if (Grid Chargers > 3) then Grid Charger Power < Grid Charger Max Power  
  `
  

  {INFRASTRUCTURE POWER LOSS depends on the DISTANCE between two closest chargers}  
  ---
  The INFRASTRUCTURE is not perfect and it loses power as it travels farther.
  The power loss depends on the distance between two closest grid chargers.  
  `
  Power out = Power in * ( diameter of ecosystem - Distance ) / diameter of ecosystem
  `
  NOTE: 1 Grid Charger won't loose any power but you won't utilize MAX SOURCE POWER

  {HAVING A LARGE INFRASTRUCTURE CAN DAMAGE THE ECOSYSTEM}
  ---  
  The more grid chargers there are, the higher the chance of robots being damaged.  
  `
  Chance of damage for squares(1, 1) immediately surrounding the Grid Charger =  0.14
  Chance of damage for squares around the immediate surrounding the Grid Charger = 0.07
  Chance of damage for square along the shortest path between two closest charger = 0.1
  `

  """
  def __init__(self, ecosystem:Ecosystem, name = "gazza", *args, **kwargs):
    super().__init__(ecosystem, name, *args, **kwargs)
    self.kind = "Grid_Charger"
    self.MAX_POWER = 333
    # Important for power regulation
    self.power_use = 0
    self.available_power = 0
  
  # METHODS
  def charge(self):
    # Open the station
    if (self.occupant == None and not self.reserved):
      self.reset()

    elif(self.occupant != None):
      if (self.reserved):
        if (self.occupant.capacity >= self.occupant.soc + self.available_power):
          self.power_use = self.available_power
        else:
          # use less than available power
          self.power_use = self.occupant.capacity - self.occupant.soc
        self.occupant.soc += self.power_use
      else:
        # Someone forgot to book and blocked the entrance
        self.activity = "busy"

    elif(self.reserved):
      self.prepare()