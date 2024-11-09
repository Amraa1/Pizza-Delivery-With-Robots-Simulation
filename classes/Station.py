from Ecosystem import Ecosystem
from Utilities import rand_coordinates
from Robot import Robot
from Droid import Droid
from Drone import Drone

class Station:
    """
    Base class for all the station kind.
    ---
    (POLICY 1) To be serviced, you need to book!
    """
    def __init__(self, ecosystem: Ecosystem, name = "Station", *args, **kwargs) -> None:
        self.ecosystem = ecosystem
        self.kind_class = "Station"
        self._coordinates = rand_coordinates()
        self._max = [0, 0, 0]
        self._velocity = [0, 0, 0]
        self._status = "vacant"
        self._activity = "idle"
        self._size = 300
        self._alpha = 0
        self._damage = 0
        self._occupant: Robot | Droid | Drone | None = None
        self._name = name
        self._shape = 'diamond'
        self._color = 'blue'

        self.reserved = False
        
    # PROPERTIES
    @property
    def coordinates(self):
        return self._coordinates
    
    @property
    def max(self):
        return self._max
    
    @property
    def velocity(self):
        return self._velocity
    
    @property
    def status(self):
        return self._status
    
    @property
    def activity(self):
        return self._activity

    @property
    def size(self):
        return self._size
    
    @property
    def alpha(self):
        return self._alpha
    
    @property
    def damage(self):
        return self._damage
    
    @property
    def occupant(self):
        return self._occupant

    @property
    def name(self):
        return self._name
    
    @property
    def shape(self):
        return self._shape
    
    @property
    def color(self):
        return self._color
    
    # SETTERS
    @coordinates.setter
    def coordinates(self, coordinate: list):
        self._coordinates = coordinate

    @status.setter
    def status(self, stat):
        self._status = stat

    @activity.setter
    def activity(self, act):
        self._activity = act

    @size.setter
    def size(self, s):
        self._size = s

    @occupant.setter
    def occupant(self, occup):
        self._occupant = occup

    @name.setter
    def name(self, new_name):
        self._name = new_name

    @shape.setter
    def shape(self, new_shape):
        self._shape = new_shape

    @color.setter
    def color(self, new_color):
        self._color = new_color

    # DELETER
    @occupant.deleter
    def occupant(self):
        self._occupant = None

    # COMMON METHOD
    def prepare(self):
        self.status = "occupied"
  
    def reset(self):
        self.status = "vacant"
        self.activity = "available"