from Ecosystem import Ecosystem
from Robot import Robot

############################################
# @title Droid Class [code] {display-mode: "code"} 
############################################

#Design your droid class here. 

class Droid(Robot):
  def __init__(self, ecosystem: Ecosystem, name="Droid", *args, **kwargs):
    super().__init__(ecosystem, name=name, *args, **kwargs)
    self.kind = "Droid"
    self.max = [2,2,0]
    self.soc = 2000
    self.capacity = 2000
    self.shape = "circle"
    self.size = 300
    self.weight = 100
    self.payload = 200
    self.color = 'white'
    
    
  #Same move method as robot
