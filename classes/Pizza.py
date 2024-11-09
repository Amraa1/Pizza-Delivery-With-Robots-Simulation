from Ecosystem import Ecosystem
from Deliverable import Deliverable

############################################
# @title Pizza Class [code] {display-mode: "code"} 
############################################

class Pizza(Deliverable):
  """
  Pizza to be delivered by Robots.
  """
  def __init__(self, ecosystem: Ecosystem, *args, **kwargs):
    super().__init__(ecosystem, *args, **kwargs)
    self.kind = "Pizza"
    self.color = "yellow"

  def pizza_to_robot_distance(self):
    x1, y1, z1 = self.coordinates
    distance_dict = {}
    for kind in self.ecosystem.robots:
      if kind:
        if kind.status == 'on':
          x, y, z = kind.coordinates
          d_x = min(abs(x-x1), abs(y-y1)) #((x - x1)**2 + (y - y1)**2 + (y - y1)**2)**0.5
          d_y = max(abs(x-x1), abs(y-y1)) - d_x
          distance = d_x**0.5 + d_y
          distance_dict[kind] = distance
    return distance_dict    #working robots only
    
  '''
  x, y, z = item.coordinates
  d_x = min(abs(x-x1), abs(y-y1)) #((x - x1)**2 + (y - y1)**2 + (y - y1)**2)**0.5
  d_y = max(abs(x-x1), abs(y-y1)) - d_x
  distance = d_x**0.5 + d_y


  def move(self):
    def robot_is_liable():
      for liable_robot in ecosystem.pizza_assignment.keys():
        
        if self == ecosystem.pizza_assignment[liable_robot]:
          print(liable_robot)
          return liable_robot
    
    if robot_is_liable():
      robot = robot_is_liable()
      print(robot)
      if self.target != self.coordinates:
        if robot.coordinates == self.coordinates:
          self.status = 'in_transit'
        if self.status == 'in_transit':
          self.coordinates = robot.coordinates
          
      elif self.target == self.coordinates:
        self.coordinates = self.coordinates
      else:
        pass
    '''
