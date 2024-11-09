from queue import Queue
from Globals import kinds, default_width, default_height, delivered_fade, motion_efficiency, system_efficiency, max_damage, c_fade, delivered_fade_rate, m_fade
from Grid_Charger import Grid_Charger
from robot_default import robot_default
from random import randint
from display import display
from copy import copy, deepcopy
from Utilities import validation, onarena

########################################################
# @title Ecosystem Class [code] {display-mode: "code"}
########################################################

class Ecosystem:
  """
  Ecosystem class for simulating the arena.

  Properties
  ---
  self.duration : Amount of hour in a day  
  self.hour : int = 24
     current hour  
  self.robots : list[Robot | Droid | Drone]
    list of registered robots  
  self.display_on_update : display arena after update  
  self.register : Registry book for registered robot, stations, and deliverables  
  self.messages : Message Queue  
  self.cache : 

  """
  def __init__(self):
    self._duration = 24
    self._hour = 0
    self._robots = []
    self.display_on_update = False
    self._register = {}
    self.markers = []
    self._messages = Queue()
    self._cache = {}
    self._registerable = [ kind for kind in kinds]
    self.random_coordinates = True
    self.message_types = [ 'damage', 'error', 'info', 'broken']     #''warning''
    self._display_parameters = {}
    self._delivered = {}  #cache of delivered objects transferred from live register
    
    
    self.pizza_assignment = {}   #added so that assigning robot to pizza is clear
    self.deliverable_list = []   #list of pizzas that waiting to be collected then deleted once assigned
    self.station_list = []
    self.grid_chargers: list[Grid_Charger] = []
    self.robot_proximity_pizza_selection = False
    self.scrap_metal = 0
    self.SOURCE_POWER = 1000

 ####################
 ##   Properties   ##
 ####################

  @property 
  def display_parameters(self):
    return self._display_parameters
  @display_parameters.setter
  def display_parameters(self, parameters):
    self._display_parameters = parameters
  @property
  def has_message(self):
    return not self._messages.empty()   #while not q1.empty():
  @property
  def messages(self):
    text = ''
    while self.has_message:
      #messages are a tuple of 5 objects
      message_type, kind, name, function, comment = self.message
      try:
        text += f'{message_type:<10} {kind:<8} {str(name):<16} {function[:12]} {comment}' + '\n'
      except:
        text += str([message_type, kind, name, function, comment])
    return text
  @property
  def message(self):
      if self._messages.empty():
        return False
      else:
        return self._messages.get()
  @message.setter
  def message(self, value):
    try:
      if value[0] in self.message_types:
        self._messages.put(value)
    except TypeError:
      pass
  @property
  def robots(self):
      return [robot for robot in self._robots if robot.kind in ['Robot', 'Droid', 'Drone']]
  def things (self, kind):
      return [thing for thing in self._robots if thing.kind == kind]
  @property
  def robot_register(self):
    return self._register
  @property
  def duration(self):
      return self._duration
  @duration.setter
  def duration(self, value):
      self._duration = value
  @property
  def hour(self):
      return self._hour
  @property
  def count_operational(self):
    count = len([value for value in self._register.values() if value['status'] == 'on'])
    return count
  @property
  def stop(self):
    return self._hour>self._duration
  @property
  def operational(self):
    return self.count(status = 'on')
  @property
  def broken (self):
    return self.count(status = 'broken')

####################
##   Object       ##
####################

  def create(self, kind, coordinates = [0,0,0]):
    """
    Creates a default kind in kinds list and registers that in the ecosystem.

    Parameters
    ---
    kind : string
      One of kinds list.
    coordinates : list[int, int, int]
      starting coordinates
    """
    def object_init(self,dictionary):
      for k, v in dictionary.items():
        setattr(self, k, v)

    try:
      if kind in self._registerable:       #<-Check if a registerable object
        register = robot_default(kind)
        New_Object = type(kind,(),{"__init__":object_init})   #lambda self,dictionary: (setattr(self, k, v) for k, v in dictionary.items()) tried to use but Lambda cannot return None which init expects
        new_object = New_Object(register)

        if new_object.kind_class == 'Deliverable':
          if coordinates != [0,0,0]:
            raise ValueError("Robot controllers cannot decide where to collect a " + kind)
          new_object.target = [randint(0,default_width), randint(0,default_height), 0]

        new_object.coordinates[0] = coordinates [0]
        new_object.coordinates[1] = coordinates [1]
        new_object.start = self.hour
        self.register(new_object)
        return new_object
      else:
        raise TypeError("The ecosystem can't create a " + str(kind))
    except Exception as error:
      print('>>', 'create error')
      self.message = ('error', kind, 'None', 'create', error)

####################
##   METHODS      ##
####################
  def help(self):
    """
    Prints all public properties and methods
    """
    for a in [a for a in dir(self) if not a.startswith('_') and callable(getattr(self, a))]:
      print (a)

  def count (self, **kwargs):
    count = len(self.registry(**kwargs))
    return count

  #Filters
  def registry(self, **kwargs):
    """
    Returns registry book if no key arguments are given. \n  
    Key arguments can be used to filter the registry book and get
    specific items.
    """
    if kwargs == {}:
      return self._register
    else:
      try:
        return {key: value for key, value in self._register.items() if (False not in [value[filter_key] == filter_value for filter_key, filter_value in kwargs.items()])}
      except Exception as error:
        return "Could not filter register using "   + str(kwargs) + ' ' + str(error)


##   DISPLAY       ##
  def display (self):
    markers = self._get_markers()

    title = self.display_parameters.get('title')
    if title is not None:
      for word in title.split():
        print(word)
        if word[0] == "{" and word[-1] == "}":
          attribute = word[1:-1]
          self.display_parameters[attribute] = getattr(self, attribute,'#error#')
          print (attribute, self.display_parameters[attribute] , getattr(self, attribute,'#error#'))
    display(markers, **self.display_parameters)

##   MARKERS       ##
  def _get_markers(self):
    self.markers = [value for value in self._register.values()]
    return self.markers
 
 ##   REGISTER  ##
  def register (self, *args):
    for robot in args:
      kind = type(robot).__name__
      if kind in self._registerable:       #<-Check if a registerable object
        if robot in self._robots:          #<-Check if already in the register
          self.message = ('warning', kind, robot.name, 'register', 'already registered')
        else:
          try:                            #\>Try get default from cache
            dictionary = self._cache[kind]
          except:                         #/>auto heal the cache
            dictionary = robot_default(kind, 'dictionary')
            self._cache[kind] = dictionary

          #Get a new register copy from the dictionary. Upgrade Caution - index for default values fixed to 1
          register = deepcopy({key: value[1] for key, value in dictionary.items()})
          #Resolve co-ordinate updating
          #if the user has provided coordinates check if these are defaults and if not, set to defaults
          coordinates = getattr(robot,'coordinates', register['coordinates'])    #gets your object coordinates attribute value
          #if the coordinates are defaults and they should be random then randomize x and y.
          if register['coordinates'] == coordinates and self.random_coordinates:  #set random coordinates when self.random_cordinates is True
            coordinates[0] = randint(0,default_width)
            coordinates[1] = randint(0,default_height)
            try:
              #update the object with the new random co-ordinates.
              #do not detect and error here as that will come in the round later
              setattr( robot,'coordinates', coordinates)
            except:
              pass
          #reset xy coordinates in the register to reflect changes and prevent speeding
          #however drones cannot start with z>1 so let error handling pick that up
          register['coordinates'][0] = coordinates[0]
          register['coordinates'][1] = coordinates[1]
          if type(robot).__name__ in ['Robot', 'Droid', 'Drone']:
            register['activity'] = 'available'
            setattr(robot, 'activity', register['activity'])

          for key, register_value in register.items():      #for default values but only coordinates are set if conditions met
            value = dictionary[key]
            #sequence unpack the dictionary value list with indexes  0,2,3
            required, rule, function_name = [value[index] for index in [0,2,3]]
            try:
              new_value = getattr(robot, key)         #exception if not an available instance variable
              valid, new_value, proposed_value, message = validation (new_value, register_value, rule, function_name)
              if valid == False:
                self.message = ('damage', kind, id(robot), 'register', '\'' + key + '\' error: ' + message)
                register['damage'] += 1
                if hasattr (robot,'damage'):
                  setattr(robot,'damage', register['damage'])
              register[key] = copy(new_value)         #even tho proposed_value may be rejected, new_value is always good so update it!'
            except Exception as error:
              if required == 'required':              #required instance variable not present
                self.message = ('error', kind, id(robot), 'register', 'required variable \'' + key + '\' missing. ' + kind + ' not registered')
                break
              elif required == 'recommended':         #recommened instance variable not present
                self.message = ('warning', kind, id(robot), 'register', 'recommended variable \'' + key + '\' missing')
          else:                                       #rare use of else. Register robot if no break executed
            self._robots.append(robot) 
            self._register[id(robot)] = register
            self.message = ('info', kind, id(robot), 'register', kind + ' registered with ' + str(register['damage']) + ' damage points' )
      else:
        self.message = ('error', kind, id(robot), 'register', 'attempt to register an invalid object type')
      #/if kind in self._registerable
      ## Added
      if type(robot).__name__ is 'Pizza':
        pizza = robot
        self.deliverable_list.append(pizza)
      
      if robot.kind_class == 'Station':
        station = robot
        self.station_list.append(station)

      if robot.kind == "Grid_Charger":
        self.grid_chargers.append(robot)
    #/for robot in args  

  def deregister (self, *args):
    for robot in args:
      try:
        del self.robot_register[id(robot)]
        self.robots.remove(robot)
        del robot
      except:
        pass
  
  def _power_regulation(self):
    for c in self.grid_chargers:
      c.power_use
## UPDATE ##
  def update(self):
    """
    validates moves, coordinates, etc and updates the ecosystem for registered robots
    """
    ## Power regulation

    for robot in self.robots:                             #note - robots now contains pizzas, so use the internal property which filters
      dictionary = self._cache[robot.kind]                #get the dictionary for validation purposes
      register = self._register[id(robot)]                #get the current register
      coordinates = copy(register['coordinates'])         #used for later distance calculation
      if register['status'] == 'on':                      #if 'on' update new register from robot, ignore if not present
        for key, register_value in register.items():
          try:
            robot_value = getattr(robot, key)         #exception if not an available instance variable
            if robot_value != register_value:
              value = dictionary[key]
              required, rule, function_name = [value[index] for index in [0,2,3]]
              valid, validated_value, proposed_value, message = validation (robot_value, register_value, rule, function_name)
              #print(">>>", valid, validated_value, proposed_value, message )
              if valid == False:
                self.message = ('damage', robot.kind, id(robot), 'update', '\'' + key + '\' error: ' + message)
                register['damage'] += 1
                if hasattr (robot,'damage'):
                  setattr(robot,'damage', register['damage'])
              #register[key] = copy(validated_value)         #even tho proposed_value may be rejected, new_value is always good so update it!'                  
              #somethings making the coordinates the same so checking this line: with copy
              register[key] = validated_value         #even tho proposed_value may be rejected, new_value is always good so update it!'
          except Exception as error:
            #print (error)
            pass

      # increment age regardless of anything
      register['age'] += 1

      if register['status'] == 'on':
        register['active'] += 1
        cargo_weight = 0
        cargo = register['cargo']
        if cargo is not None:
          if cargo.status == 'awaiting_transport':
            if cargo.coordinates != register['coordinates']:  
              cargo.status = 'awaiting_collection'
          if cargo.status == 'awaiting_collection':
            if cargo.coordinates == register['coordinates']:
              #robot has arrived at collection point, so load up.
              cargo.status = 'in_transit'
              cargo.size = 200
              cargo.shape = 'square'
              cargo.color = 'red'
              cargo_weight = cargo.weight
          if cargo.status == 'in_transit':
            cargo.coordinates = copy(register['coordinates'])
            if cargo.coordinates == cargo.target:
              #arrived at destination
              cargo.status = 'delivered'
              cargo.color = 'white'
              cargo.shape = 'circle'
              cargo.alpha = delivered_fade
              cargo.end = self.hour
              register['service'] += cargo.weight
          self._register[id(cargo)] = cargo.__dict__
        
        #Charging station
        station = register['station']
        if station is not None:  
          if station.status == 'vacant':
            if station.coordinates == register['coordinates']:
              station.status = 'occupied'
              station.occupant = robot
              station.color = 'cyan'
              station.size = 1000
          elif station.status == 'occupied':
            if station.occupant is robot:
              register['soc'] = register['capacity']
              station.status = 'vacant'
              station.occupant = None
              station.color = 'blue'
              station.size = 250
          self._register[id(station)] = station.__dict__
   
        #using cache of coped coordinates becasue validation destroys change for calculation of distance      
        distance = round(((register['coordinates'][0] - coordinates[0])**2 + (register['coordinates'][1] - coordinates[1])**2)**.5,1)      
        register['distance'] += distance
        
        height = max(robot.coordinates[2] - register['coordinates'][2],0) #not used in energy calcs yet!
              
        motion_energy = (register['weight'] + cargo_weight) * distance * motion_efficiency
        system_energy = register['weight'] * system_efficiency
        energy = int(min(system_energy + motion_energy, register['soc']))
        register['energy'] += energy
        register['soc'] = int(register['soc'] - energy)
        #register['soc'] = round(max(register['soc'], 0),2)
        
        

        if onarena(register['coordinates'])[0] == False:
          register['damage'] += max_damage
          self.message = ('damage', robot.kind, robot.name, 'update', 'damage at ecosystem boundary') 
        if register['damage'] >= max_damage:
          self.message = ('broken', robot.kind, robot.name, 'update', 'max damage score')
          register['status'] = 'broken'
        if register['soc'] < 1:
          if station is not None and station.coordinates == register['coordinates']:
            #low charge robot is in queu for charger so do not break
            self.message = ('warning', robot.kind, robot.name, 'update', 'out of power in charger queue') 
          else:
            register['status'] = 'broken'
            self.message = ('broken', robot.kind, robot.name, 'update', 'out of power') 

        if register['status'] == 'broken':
          register['alpha'] = 0.2
          print ('broken', register)
        else:
          #alpha  determines the transparency of robots. Running out of fuel makes robots fade
          register['alpha'] = m_fade * register['soc']/register['capacity'] + c_fade
      # End of status != off block 

      for key, value in register.items():    # updating available Robot attributes
        if hasattr(robot,key):
          if key == 'coordinates':
            setattr(robot,key,copy(value))
          #setattr(robot,key,copy(value))
          else:
            setattr(robot,key,value)

    #remove faded delivered to the delivered cache and
    delivered = {key:value['alpha'] for key, value in self._register.items() if value['status'] == 'delivered'}
    for key, alpha in delivered.items():
      if alpha == 0:
        self._delivered[key] = self.robot_register.pop(key)  #transfer
      else:
        self.robot_register[key]['alpha'] = max(alpha - delivered_fade_rate, 0)

    self._hour += 1  
    if self.display_on_update:
      self.display()

  ## Added Method ##
  def pizza_assign(self):
      #makes robot life easier :)
    def distance_from_pizza(pizza):
      closest_robot = None
      closest_distance = 10**10 # very high number to be changed by conditional
      if pizza.pizza_to_robot_distance() != {}:
        for r, d in pizza.pizza_to_robot_distance().items():
          if d < closest_distance and r.status == 'on' and r.activity == 'available':   #filtering
            closest_robot = r
            closest_distance = d
      return closest_robot, closest_distance
    

    if len(self.deliverable_list) != 0:
      for i in range(len(self.deliverable_list) - 1,-1,-1):
        pizza = self.deliverable_list[i]
        robot, distance = distance_from_pizza(pizza)
        #print(robot, distance)
        if robot != None:
          if self.robot_proximity_pizza_selection:
            if robot.kind == 'Robot' and robot.status == 'on' and robot.activity == 'available':
              if distance < 300 :
                robot.activity = 'busy'
                self.pizza_assignment[robot] = pizza
                self.deliverable_list.pop(i)
            elif robot.status == 'on' and robot.activity == 'available':
              robot.activity = 'busy'
              self.pizza_assignment[robot] = pizza
              self.deliverable_list.pop(i)
            else:
              pass
          elif robot.status == 'on' and robot.activity == 'available':
            robot.activity = 'busy'
            self.pizza_assignment[robot] = pizza
            self.deliverable_list.pop(i)
            pizza.status = "awaiting_collection"
            #print('Assigning pizza to a robot')
            #print(f'{robot} : {pizza}')
          else:
            pass
      return self.pizza_assignment