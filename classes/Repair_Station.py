from Station import Station
from Ecosystem import Ecosystem
from Globals import max_damage

############################################
# @title Repair_Station Class [code] {display-mode: "code"} 
############################################

class Repair_Station(Station):
  def __init__(self, ecosystem: Ecosystem, name = "fixit", *args, **kwargs):
    super().__init__(self, ecosystem, name, *args, **kwargs)
    self.kind = "Repair_Station"
    self._color = "magenta"
  
  # METHOD
  def _fix(self):
    """
    NOTE Robot with max damage can't be repaired. It should be recycled for extra bonus. \n
    (POLICY 1) Can only reduce damage by one at a time, if you have 3 damage, then it will take 3 turns for full repair \n
    """
    # fixing
    self.activity = "repairing"
    self.occupant.activity = "under_repair"
    if (self.occupant.damage >= max_damage):
      """The robot has blocked the entrance to the repair station"""
      self.activity = "busy"
      # beyond repairable
      self.occupant.activity = "idle"
    else:
      if (self.occupant.damage > 0):
        self.occupant.damage -= 1
      self.occupant.serviced = self.occupant.age
  
  def repair(self):
    # Open the station
    if (self.occupant == None and not self.reserved):
      self.reset()

    elif(self.occupant != None):
      if (self.reserved):
        self._fix()
      else:
        # Someone forgot to book and blocked the entrance
        self.activity = "busy"

    elif(self.reserved):
      self.prepare()
