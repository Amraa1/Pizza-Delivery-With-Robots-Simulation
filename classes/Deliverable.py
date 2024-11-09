from Utilities import rand_coordinates
from Ecosystem import Ecosystem

class Deliverable:
    """
    Base class for deliverable items.
    """
    def __init__(self, ecosystem: Ecosystem, *args, **kwargs):
        self.kind = "Deliverable"
        self.kind_class = "Deliverable"
        self.coordinates = rand_coordinates()
        self.max = 0
        self.velocity = [0, 0, 0]
        self.status = "awaiting_transport"
        self.activity = "idle"
        self.size = 300
        self.alpha = 1.0
        self.weight = 50
        self.damage = 0
        self.name = "Pizza"
        self.target = rand_coordinates()
        self.shape = "circle"
        self.color = "white"
        self.transport = None
        self.start = 0
        self.end = 0
        self.ecosystem = ecosystem