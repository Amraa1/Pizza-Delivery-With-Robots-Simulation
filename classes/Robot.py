from Utilities import rand_coordinates
from Globals import kinds, system_efficiency, motion_efficiency, default_width, default_height, default_altitude
from Ecosystem import Ecosystem
############################################
# @title Robot Class [code] {display-mode: "code"} 
############################################

#Design your robot class here. 

class Robot:
  #Constructor//variables
  def __init__(self, ecosystem: Ecosystem, name="Robot", *args, **kwargs):
    ## Setting default values for Robot
    self.kind = "Robot"
    self.coordinates = rand_coordinates() # set random coordinates as specified in rules
    self.max = [1,1,0]
    self.velocity = [0,0,0]
    self.status = 'on'
    self.activity = 'idle'
    self.name = name
    self.target = None
    self.age = 0
    self.active = 0
    self.serviced = 0
    self.soc = 600
    self.capacity = 600
    self.service = 0
    self.damage = 0
    self.on_arena = False
    self.shape = 'square'
    self.color = 'blue'
    self.size = 250
    self.alpha = 1.0
    self.weight = 50
    self.payload = 100
    self.cargo = None
    self.station = None
    self.distance = 0
    self.energy = 0
    self.number_of_pizza_delivered = 0 # reward system
    self.kind_class = kinds[self.kind]
    self.ecosystem = ecosystem # ecosystem in which it is created / can be useful when accessing ecosystem properties
  
  #Property
  """
  Protecting robot public properties
  """
  @property
  def velocity_p(self):
    return self.velocity
    

  @property
  def target_p(self):
    return self.target

  @property
  def cargo_p(self):
    return self.cargo

  #Setter
  @target_p.setter
  def target_p(self, target):
    self.target = target

  
  @velocity_p.setter
  def velocity_p(self, velocity):
    self.velocity = velocity

  @cargo_p.setter
  def cargo_p(self, cargo):
    self.cargo = cargo

  #Deleter
  @target_p.deleter
  def target_p(self):
    self.target = None

  @cargo_p.deleter
  def cargo_p(self):
    self.cargo = None

  ## Methods ##
  '''
  def find_distance_to_pizza(self):
    x1, y1, z1 = self.coordinates
    distance_dict = {}
    for item in ecosystem.deliverable_list:
      x, y, z = item.coordinates
      distance = (x - x1)**2 + (y - y1)**2 + (y - y1)**2
      distance_dict[item] = distance
    return distance_dict

  def find_nearest_pizza(self):
    x1, y1, z1 = self.coordinates
    
    distance = 0
    shortest_distance = 0
    shortest = type('Placeholder', (), {})  #doesn't give error when my_deliverable_list is empty or doesn't exist
    for item in ecosystem.deliverable_list:
      x, y, z = item.coordinates
      distance = (x - x1)**2 + (y - y1)**2 + (y - y1)**2
      placeholder = distance
      if distance <= placeholder:
        shortest_distance = distance
        shortest = item

    return shortest_distance, shortest
  '''

  def _successful_delivery(self):
    del self.target_p
    self.activity = "available"
    self.cargo = None
    self.number_of_pizza_delivered += 1

  def _assign_order(self):
      self.activity = 'delivering'
      pizza = self.ecosystem.pizza_assignment[self]
      self.cargo = pizza

  def _drop_pizza(self):
    # Robot broke in the middle of delivery
    if self.cargo is not None:
      pizza = self.ecosystem.pizza_assignment.pop(self)
      pizza.activity = 'awaiting_transport'
      self.ecosystem.deliverable_list.append(pizza)
      del self.cargo_p

    # Pizza was assigned to the robot but the robot broke
    elif self.cargo is None and self in self.ecosystem.pizza_assignment.keys():
      pizza = self.ecosystem.pizza_assignment.pop(self)
      self.ecosystem.deliverable_list.append(pizza)
    

  def _deliver_pizza(self):
    self._assign_order()
    
    # go to pizza
    if self.cargo.status == 'awaiting_collection':
      self.target_p = self.cargo.coordinates

    # go to pizza target
    if self.cargo.status == 'in_transit':
      self.target_p = self.cargo.target

    # deliver pizza
    if self.cargo.status == 'delivered':
      self._successful_delivery()

  def deliver(self):
    if self.status == "on" and self in self.ecosystem.pizza_assignment.keys():
      # a pizza is assigned to the robot
      self._deliver_pizza()
      
    elif self.status == 'broken':
      try:
        self._drop_pizza()

      except Exception as expect:
        RuntimeError(str(expect))
        print('cargo is ', self.cargo)

    elif self.status == 'off':
      try:
        self._drop_pizza()
      except Exception as expect:
        RuntimeError(str(expect))
        print('cargo is ', self.cargo)

    
    def distance_station():
      if self.ecosystem.station_list is not []:
        x1, y1, z1 = self.coordinates
        distance_dict = {}
        for item in self.ecosystem.station_list:
          x, y, z = item.coordinates
          d_x = min(abs(x-x1), abs(y-y1)) #((x - x1)**2 + (y - y1)**2 + (y - y1)**2)**0.5
          d_y = max(abs(x-x1), abs(y-y1)) - d_x
          distance = d_x**0.5 + d_y
          distance_dict[item] = distance
        return distance_dict


    def will_it_deliver_pizza():
      if self.cargo:
        '''
        d1 = ((self.cargo.coordinates[0] - self.coordinates[0])**2 + (self.cargo.coordinates[1] - self.coordinates[1])**2 + (self.cargo.coordinates[2] - self.coordinates[2])**2)**0.5
        d2 = ((self.cargo.target[0] - self.cargo.coordinates[0])**2 + (self.cargo.target[1] - self.cargo.coordinates[1])**2 + (self.cargo.target[2] - self.cargo.coordinates[2])**2)**0.5
        '''
        # distance = x**0.5 + y
        x1 = min(abs(self.cargo.coordinates[0] - self.coordinates[0]), abs(self.cargo.coordinates[1] - self.coordinates[1]))
        y1 = max(abs(self.cargo.coordinates[0] - self.coordinates[0]), abs(self.cargo.coordinates[1] - self.coordinates[1])) - x1
        d1 = x1**0.5 + y1

        x2 = min(abs(self.cargo.target[0] - self.cargo.coordinates[0]), abs(self.cargo.target[1] - self.cargo.coordinates[1]))
        y2 = max(abs(self.cargo.target[0] - self.cargo.coordinates[0]), abs(self.cargo.target[1] - self.cargo.coordinates[1])) - x2
        d2 = x2**0.5 + y2

        time_takes1 = max(abs(self.cargo.coordinates[0] - self.coordinates[0])/self.max[0], abs(self.cargo.coordinates[1] - self.coordinates[1])/self.max[1])
        time_takes2 = max(abs(self.cargo.target[0] - self.cargo.coordinates[0])/self.max[0], abs(self.cargo.target[1] - self.cargo.coordinates[1])/self.max[1])
        
        motion_energy1 = (self.weight) * d1 * motion_efficiency
        system_energy1 = self.weight * system_efficiency * time_takes1

        motion_energy2 = (self.weight + self.cargo.weight) * d2 * motion_efficiency
        system_energy2 = self.weight * system_efficiency * time_takes2

        energy1 = int(system_energy1 + motion_energy1)
        energy2 = int(system_energy2 + motion_energy2)
        return energy1, energy2
      else:
        print('No pizza in cargo')


    def will_it_make_station():
      closest_station, closest_distance= closest_distance_station()

      time_takes = max(abs(closest_station.coordinates[0] - self.coordinates[0])/self.max[0], abs(closest_station.coordinates[1] - self.coordinates[1])/self.max[1])
      if self.cargo.status == 'in_transit':
        motion_energy1 = (self.weight + self.cargo.weight) * closest_distance * motion_efficiency
      else:
        motion_energy1 = (self.weight) * closest_distance * motion_efficiency
      
      system_energy1 = self.weight * system_efficiency * time_takes

      energy = int(system_energy1 + motion_energy1)
      return energy

    def closest_distance_station():
      if self.ecosystem.station_list != []:
        closest_station = None
        closest_distance = 10**10 # very high number to be changed by conditional
        for s, d in distance_station().items():
          if d < closest_distance:
            closest_station = s
            closest_distance = d
        closest_distance = round(closest_distance, 1)
        return closest_station, closest_distance


    if self.ecosystem.station_list != []:
      if self.cargo != None:
        emergency_battery = 35
        closest_station, closest_distance = closest_distance_station()
        energy_collection, energy_delivery = will_it_deliver_pizza()
        energy_station = will_it_make_station()
        energy_total = energy_collection + energy_delivery
        #print(self.soc)
        #print('Energy take to collect ', energy_collection)
        #print('Energy take to deliver ', energy_delivery)
        #print('Energy take to get to closest station', energy_station)
        #print('Total Energy', energy_total)
        #print('expected soc', self.soc - energy_total)
        #print(self.soc < energy_collection + energy_station)
        #print(self.soc < energy_total + energy_station)
        '''
        if self.cargo.status is 'awaiting_collection' and self.soc < energy_collection + emergency_battery:
          self.activity = 'charging'  
          self.station = closest_station
          self.target_p = closest_station.coordinates
        elif self.cargo.status is 'in_transit' and self.soc <= energy_delivery + emergency_battery:
          self.activity = 'charging'
          self.station = closest_station
          self.target_p = closest_station.coordinates
        '''

        '''
        if self.soc <= energy_station + emergency_battery:
          self.activity = 'charging'  
          self.station = closest_station
          self.target_p = closest_station.coordinates
        elif self.cargo.status is 'awaiting_collection' and self.soc < energy_collection + emergency_battery:
          self.activity = 'charging'  
          self.station = closest_station
          self.target_p = closest_station.coordinates
        elif self.cargo.status is 'in_transit' and self.soc <= energy_delivery + emergency_battery:
          self.activity = 'charging'
          self.station = closest_station
          self.target_p = closest_station.coordinates
        else:
          #print('maybe can do complete delivery without charging')
          pass
        '''



        '''
        if self.soc <= energy_station + emergency_battery:
          self.activity = 'charging'  
          self.station = closest_station
          self.target_p = closest_station.coordinates
        '''

        
        if self.soc <= self.capacity * 0.36 + emergency_battery:
          self.activity = 'charging'  
          self.station = closest_station
          self.target_p = closest_station.coordinates
        

      #print(self.soc == self.capacity)
      if self.activity == 'charging' and self.status == 'on':
        if self.soc >= self.capacity * 0.95 and self.station.status == 'occupied':
          del self.target_p
          self.station = None

          #print('finished charging')
          if self.cargo != None:
            self.activity = 'busy'
          elif self.cargo == None:
            self.activity = 'available'
          else:
            raise ValueError('something wrong with cargo')
    #print(self.soc)


  def move(self):
    if self.target:
      for i in range(len(self.target)):
        if self.target[i] >= self.coordinates[i] + self.max[i] and self.target[i] - self.coordinates[i] > 0:
          self.velocity_p[i] = self.max[i]
        elif self.target[i] <= self.coordinates[i] - self.max[i] and self.target[i] - self.coordinates[i] < 0:
          self.velocity_p[i] = -self.max[i]
        elif self.target[i] < self.coordinates[i] + self.max[i] or self.target[i] > self.coordinates[i] - self.max[i]:
          self.velocity_p[i] = self.target[i] - self.coordinates[i]
        else:
          self.velocity_p[i] = 0

      self.coordinates[0] += self.velocity[0] if 0 <= self.coordinates[0] <= default_width and abs(self.velocity[0]) <= self.max[0] else 0
      self.coordinates[1] += self.velocity[1] if 0 <= self.coordinates[1] <= default_height and abs(self.velocity[1]) <= self.max[1] else 0
      self.coordinates[2] += self.velocity[2] if 0 <= self.coordinates[2] <= default_altitude and abs(self.velocity[2]) <= self.max[2] else 0