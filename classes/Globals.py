"""
Global variables for Robot simulation
"""

testing = True

#Ecosystem Boundaries
default_width = 80
default_height = 40
default_altitude = 5

arena_limits = (default_width,default_height,default_altitude)

#Fading of robots  alpha = m_fade * soc/capacity + c_fade
c_fade = 0.1
m_fade = 0.9 - c_fade

#deliverable fading
delivered_fade = 0.33
delivered_fade_rate = .005   #d alpha at -.5% per update

#maximum damage a robot can sustain
max_damage = 5
motion_efficiency = 0.100
system_efficiency = 0.025

NL = "\n"
TB = "\t"
PR = ">"

# Matplotlib colors and shapes semantics # https://matplotlib.org/stable/api/markers_api.html
mpl_shapes = {'square':'s', 'circle':'o','triangle':'^', 'plus':'P', 'star':'*', 'diamond':'D', 'x':'x', 'hexagon':'h'}
mpl_colors = {'blue': 'b', 'green': 'g', 'red': 'r', 'cyan': 'c', 'magenta': 'm', 'yellow': 'y', 'black': 'k', 'white': 'w'}


colors = [color for color in mpl_colors]
shapes = [shape for shape in mpl_shapes]

modes = ['required', 'default', 'validation','function', 'datatype', 'description']

kinds = dict(
  Robot = 'Robot', 
  Droid = 'Robot', 
  Drone = 'Robot', 
  Pizza = 'Deliverable', 
  Grid_Charger = 'Station',
  Solar_Charger = 'Station', 
  Repair_Station = 'Station', 
  Recycling_Station = 'Station')

robot_statuses = [
	'off', 
	'on', 
	'broken']

deliverable_statuses = [
	'awaiting_transport',
	'awaiting_collection', 
	'in_transit',
	'delivered']

station_statuses = [
	'occupied', 
	'vacant']

activities = [
	'idle',
	'available', 
	'charging', 
	'busy', 
	'delivering', 
	'is_cargo', 
	'under_repair',
	'repairing']

