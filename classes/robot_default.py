from Globals import station_statuses, activities, shapes, colors, deliverable_statuses, kinds, modes

#@title Defaults [code] {display-mode: "code"}

####################
## ROBOT_DEFAULTS ##
####################

#robot_default returns a dictionary of robot instance variables, and properties 
#for these attributes

def robot_default (kind, mode = 'default'):

  kind_class = kinds[kind]
  dictionary = {}
  
  dictionary['kind'] = ['required', kind, 0, 'nochange', 'string', 'robot class type']
  if kind_class == 'Station':
    dictionary['coordinates'] = ['required', [0, 0, 0], [0, 0, 0 ], 'validxyz', 'list', 'x, y, z location of a robot']
    dictionary['max'] = ['required', [0, 0, 0], 0, 'nochange', 'list', 'maximum x, y, z velocity']
    dictionary['velocity'] = ['required', [0, 0, 0], [0 ,0 ,0], 'listmax', 'list', 'current  x, y, z velocity']
    dictionary['status'] = ['required', 'vacant',station_statuses, 'inlist', 'string', 'Set to on, off or broken']
    dictionary['activity'] = ['required', 'idle', activities, 'inlist', 'string', 'determines activity of station']
    dictionary['size'] = ['optional', 300, [250,1000], 'inrange', 'integer', 'arena display size']
    dictionary['alpha'] = ['optional', 1, 0, 'nochange', 'float', 'arena display transparency']
    dictionary['damage'] = ['recommended', 0, 0, 'nochange', 'integer', 'damage points accrued by station']
    dictionary['occupant'] = ['recommended', 0, 0, 'nochange', 'integer', 'damage points accrued by station']
    if kind == 'Grid_Charger':
      dictionary['name'] = ['required', 'gazza', [2,20], 'length', 'string', 'named of robot']
      dictionary['shape'] = ['optional', 'diamond', shapes, 'inlist', 'string', 'arena display shape']
      dictionary['color'] = ['optional', 'blue', colors, 'inlist', 'string', 'arena display colour']
    elif kind == 'Solar_Charger':
      dictionary['name'] = ['required', 'sunny', [2,20], 'length', 'string', 'named of robot']
      dictionary['shape'] = ['optional', 'diamond', shapes, 'inlist', 'string', 'arena display shape']
      dictionary['color'] = ['optional', 'green', colors, 'inlist', 'string', 'arena display colour']
    elif kind == 'Repair_Station':
      dictionary['name'] = ['required', 'fixit', [2,20], 'length', 'string', 'named of robot']
      dictionary['shape'] = ['optional', 'diamond', shapes, 'inlist', 'string', 'arena display shape']
      dictionary['color'] = ['optional', 'magenta', colors, 'inlist', 'string', 'arena display colour']
    elif kind == 'Recycling_Station':
      dictionary['name'] = ['required', 'reuse', [2,20], 'length', 'string', 'named of robot']
      dictionary['shape'] = ['optional', 'diamond', shapes, 'inlist', 'string', 'arena display shape']
      dictionary['color'] = ['optional', 'cyan', colors, 'inlist', 'string', 'arena display colour']

  elif kind_class == 'Deliverable':
    dictionary['coordinates'] = ['required', [0, 0, 0], [0, 0, 0 ], 'validxyz', 'list', 'x, y, z location of a robot']
    dictionary['max'] = ['required', [0, 0, 0], 0, 'nochange', 'list', 'maximum x, y, z velocity']
    dictionary['velocity'] = ['required', [0, 0, 0], [0 ,0 ,0], 'listmax', 'list', 'current  x, y, z velocity']
    dictionary['status'] = ['required', 'awaiting_transport',deliverable_statuses, 'inlist', 'string', 'Set to on, off or broken']
    dictionary['activity'] = ['required', 'idle', activities, 'inlist', 'string', 'determines activity of deliverable']
    dictionary['size'] = ['optional', 300, [250,1000], 'inrange', 'integer', 'arena display size']
    dictionary['alpha'] = ['optional', 1, 0, 'nochange', 'float', 'arena display transparency']
    dictionary['weight'] = ['optional', 50, [25,1000], 'nochange', 'integer', 'weight of deliverable']
    dictionary['damage'] = ['recommended', 0, 0, 'nochange', 'integer', 'damage points accrued by deliverable']  
    dictionary['name'] = ['required', 'pizza', [2,20], 'length', 'string', 'named of deliverable']
    dictionary['target'] = ['recommended', None,'none', 'none', 'list', 'x, y, z of delivery destination']    
    dictionary['shape'] = ['optional', 'circle', shapes, 'inlist', 'string', 'arena display shape']
    dictionary['color'] = ['optional', 'white', colors, 'inlist', 'string', 'arena display colour']
    dictionary['transport'] = ['optional', None,'object', 'nochange', 'object', 'object robot is transporting']
    dictionary['start'] = ['optional', 0, 0, 'none', 'float', 'start time stamp']
    dictionary['end'] = ['optional', 0, 0, 'none', 'float', 'end time stamp']

  elif kind_class == 'Robot':
    dictionary['coordinates'] = ['required', [0, 0, 0], [1, 1, 0 ], 'validxyz', 'list', 'x, y, z location of a robot']
    dictionary['max'] = ['required', [1, 1, 0], 0, 'nochange', 'list', 'maximum x, y, z velocity']
    dictionary['velocity'] = ['required', [0, 0, 0], [1 ,1 ,0], 'listmax', 'list', 'current  x, y, z velocity']
    dictionary['status'] = ['required', 'on',0, 'nochange', 'string', 'Set to on, off or broken']
    dictionary['activity'] = ['required', 'idle', activities, 'inlist', 'string', 'determines activity of robot']
    dictionary['name'] = ['required', 'id', [2,20], 'length', 'string', 'named of robot']
    dictionary['target'] = ['recommended', None,'none', 'none', 'list', 'x, y, z of a target destination']
    dictionary['age'] = ['recommended', 0, 0, 'nochange','integer', 'age of robot in hours']
    dictionary['active'] = ['recommended', 0, 0, 'nochange','integer', 'active hours of robot']    
    dictionary['serviced'] = ['recommended', 0, 0, 'nochange','integer', 'age of robot at last service']
    dictionary['soc'] = ['recommended', 600, 0, 'nochange', 'integer', 'state of charge of battery']
    dictionary['capacity'] = ['recommended', 600, 0, 'nochange', 'integer', 'energy capacity of robot battery']
    dictionary['service'] = ['recommended', 0, 0, 'nochange', 'integer', 'service points accrued by robot']
    dictionary['damage'] = ['recommended', 0, 0, 'nochange', 'integer', 'damage points accrued by robot']
    dictionary['on_arena'] = ['optional', 0,0, 'nochange', 'boolean', 'True if robot is on the arena']
    dictionary['shape'] = ['optional', 'square', shapes, 'inlist', 'string', 'arena display shape']
    dictionary['color'] = ['optional', 'blue', colors, 'inlist', 'string', 'arena display colour']
    dictionary['size'] = ['optional', 250, [250,1000], 'inrange', 'integer', 'arena display size']
    dictionary['alpha'] = ['optional', 1, 0, 'nochange', 'float', 'arena display transparency']
    dictionary['weight'] = ['optional', 50, 0, 'nochange', 'integer', 'weight of robot']
    dictionary['payload'] = ['optional', 100, 0, 'nochange', 'integer', 'maximum load of robot']
    dictionary['cargo'] = ['optional', None,'object', 'none', 'object', 'object robot is transporting']
    dictionary['station'] = ['optional', None,'object', 'none', 'object', 'station robot is heading for']
    dictionary['distance'] = ['optional', 0, 0, 'nochange', 'float', 'distance travelled by robot']
    dictionary['energy'] = ['optional', 0, 0, 'nochange', 'float', 'energy consumed by robot']
    
    if kind == 'Droid':
      dictionary['coordinates'][2] = [2, 2, 0 ]
      dictionary['max'][1] = [2, 2, 0 ]
      dictionary['velocity'][2] = [2, 2, 0 ]
      dictionary['soc'][1] = 2000
      dictionary['capacity'][1] = 2000
      dictionary['shape'][1]= 'circle'
      dictionary['color'][1] = 'red'
      dictionary['size'][1] = 300
      dictionary['weight'][1] = 100
      dictionary['payload'][1] = 200
    elif kind == 'Drone':
      dictionary['coordinates'][2] = [3, 3, 1]
      dictionary['max'][1] = [3, 3, 1]     
      dictionary['velocity'][2] = [3, 3, 1 ]    
      dictionary['soc'][1] = 500      
      dictionary['capacity'][1] = 500
      dictionary['shape'][1] = 'triangle'
      dictionary['color'][1] = 'green'
      dictionary['size'][1] = 500
      dictionary['weight'][1] = 25
      dictionary['payload'][1] = 50
  dictionary['kind_class'] = ['optional', kind_class, 0, 'nochange', 'string', 'class of kind']
  
  try:
    if mode == 'dictionary':
      return dictionary
    elif mode == 'keys':
      return tuple(key for key in dictionary)
    else:
      index = modes.index(mode)                                      
      return {key: value[index] for key, value in dictionary.items()}
  except:
    pass
