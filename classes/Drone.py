from Ecosystem import Ecosystem
from Robot import Robot
from Globals import default_width, default_height, default_altitude

############################################
# @title Drone Class [code] {display-mode: "code"} 
############################################

#Design your drone class here. 

class Drone(Robot):
  def __init__(self, ecosystem: Ecosystem, name="Drone", *args, **kwargs):
    super().__init__(ecosystem, name=name, *args, **kwargs)
    self.kind = "Drone"
    self.max = [3,3,1]
    self.soc = 500
    self.capacity = 500
    self.shape = "triangle"
    self.size = 500
    self.weight = 25
    self.payload = 50
    self.color = 'cyan'

  def move(self):
    if self.target:
      if self.coordinates[2] == 0 and self.coordinates != self.target:
        self.velocity_p = [0, 0, 1]
      elif self.coordinates[2] > 0:
        for i in range(len(self.coordinates)):
          if self.target[i] >= self.coordinates[i] + self.max[i] and self.target[i] - self.coordinates[i] > 0:
            self.velocity_p[i] = self.max[i]
          elif self.target[i] <= self.coordinates[i] - self.max[i] and self.target[i] - self.coordinates[i] < 0:
            self.velocity_p[i] = -self.max[i]
          elif self.target[i] < self.coordinates[i] + self.max[i] or self.target[i] > self.coordinates[i] - self.max[i]:
            self.velocity_p[i] = self.target[i] - self.coordinates[i]
          else:
            self.velocity_p[i] = 0
      
      
      if self.coordinates[2] > 0 and (self.coordinates[0] != self.target[0] or self.coordinates[1] != self.target[1]):
        self.velocity[2] = 0 if self.target[2] == 0 else self.velocity[2]
      
      if self.coordinates[2] == 0 and (self.coordinates[0] == self.target[0] and self.coordinates[1] == self.target[1]):
        self.velocity[2] = 0
      
      self.coordinates[0] += self.velocity[0] if 0 <= self.coordinates[0] <= default_width and abs(self.velocity[0]) <= self.max[0] else 0
      self.coordinates[1] += self.velocity[1] if 0 <= self.coordinates[1] <= default_height and abs(self.velocity[1]) <= self.max[1] else 0
      self.coordinates[2] += self.velocity[2] if 0 <= self.coordinates[2] <= default_altitude and abs(self.velocity[2]) <= self.max[2] else 0
    