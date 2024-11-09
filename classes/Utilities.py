from random import randint
from Globals import arena_limits
import math


def rand_coordinates() -> list:
    """
    List of random coordinates within the arena limits
    """
    return [randint(0,m) for m in list(arena_limits[:2]) + [0]]

# @title Utility functions [code] {display-mode: "code"}

#randsign generates a random -1 or +1 to give a random sign of a vector
def randsign():
  return [-1,1][randint(0,1)]

#sign returns the sign x 1 of a number.
def sign(i):
  #return [-1,1][i>0]
  return [-1,0,1][0 if i < 0 else 1 if i == 0 else 2]

#Returns the name of a variable in the namespace which points to the passed object.
#If more than name points to the object the first is returned or all if return_all is true
def namestr(obj, return_all = False):
  namespace = globals()
  if return_all:
    return [name for name in namespace if namespace[name] is obj]
  else:
    try:
      return [name for name in namespace if namespace[name] is obj][0]
    except:
      return obj # probably a literal so no name to give!
    

# @title Irradiance [code] {display-mode: "code"}
#Not a real estimate of irradiance since it isn't gaussian
def normpdf(x, mean, sd):
    var = float(sd)**2
    denom = (2*math.pi)**.5*sd
    num = math.exp(-(float(x)-float(mean))**2/(2*var))
    pdf = num/denom
    return pdf

def irradiance(hour):
    hour = hour % 24
    mean = 12     #mid-day
    sd = 3        #standard dev of irradiance
    normalised_pdf  = normpdf(hour,mean,sd)/normpdf(mean,mean,sd)
    moonlight = 0.2
    a = moonlight + (1-moonlight)*normalised_pdf
    return a

#@title Validation Functions [code] {display-mode: "code"}
#nv = new value
# v = old value
#av = rule parameters 
length = lambda nv,v,av: (av[0] <= len(nv) <= av[1],nv if av[0] <= len(nv) <= av[1] else v)  #return old value if new invalid
inlist = lambda nv,v,av: (nv in av, nv if nv in av else v)     
nochange = lambda nv,v,av: (nv == v, v)
inrange = lambda nv,v,av: (av[0] <= nv <= av[1],nv if av[0] <= nv <= av[1] else v)
listdelta = lambda nv,v,av:(False not in [abs(i_nv - i_v) <= i_av for i_nv, i_v, i_av in zip(nv,v,av)], v)
listmaxdelta = lambda nv,v,av:(False not in [abs(i_nv - i_v) <= i_av for i_nv, i_v, i_av in zip(nv,v,av)], [ i_v + [-1,1][i_nv > i_v]*min(i_av,abs(i_nv-i_v)) for i_nv, i_v, i_av in zip(nv,v,av)])
onarena = lambda coordinates: (False not in [0 <= i_c <= i_l for i_c, i_l in zip(coordinates, arena_limits)], [i_c if 0 <= i_c <= i_l else -1 if i_c < 0 else i_l + 1 for i_c, i_l in zip(coordinates, arena_limits)])
listmax = lambda nv,v,av: (False not in [abs(nv[i]) <= av[i] for i in [0, 1, 2]], [nv[i] if abs(nv[i]) <= av[i] else av[i]*sign(nv[i]) for i in [0, 1, 2]])
none = lambda nv,v,av: (True,nv)

def validxyz(nv,v,av):
  #nv for new robot receives v = nv
  #av = [dx,dy,dz]  where dz >= 1 means volitant and cannnot move on the ground
  if av[2] >= 1 and nv[2] == 0 and v[2] == 0:    #volitant is on the ground and was previously
    return nv == v, v                            # if not equal then this is false so bad move
  else:    
    deltaOK, cnv = listmaxdelta(nv,v,av)  #corrected new values wrt to vector increments
    on_arena, anv = onarena(cnv)
    return deltaOK and on_arena, anv

validation_functions = {'none': none, 'listmax': listmax, 'inlist': inlist, 'nochange': nochange, 'inrange': inrange, 'listdelta': listdelta, 'listmaxdelta': listmaxdelta, 'onarena': onarena, 'validxyz': validxyz, 'length': length }

def validation(new_value, old_value, rule, function_name, verbose = True):
  proposed_value = new_value
  function = validation_functions[function_name]
  valid, new_value = function (new_value, old_value, rule)
  if verbose:
    if valid:
      if old_value == new_value:
        message = 'Value \'' + str(old_value) + '\' retained'
      else:
        message = 'Value \'' + str(old_value) + '\' set to \'' + str(new_value) + '\''
    else:
      message = 'Value \'' + str(proposed_value) + '\' rejected. ' 
      if function_name == 'length':
        message += 'Length must be between ' + str(rule[0]) + ' and ' + str(rule[1])
      if function_name == 'inrange':
        message += 'Must be between ' + str(rule[0]) + ' and ' + str(rule[1])
      elif function_name == 'inlist':
        message += 'Must be in list ' + str(rule)
      elif function_name == 'nochange':
        message += 'Cannot be changed from \'' + str(old_value) + '\''
      elif function_name == 'validxyz':
        message += 'Coordinate value or change not permitted'
      message += '. Set to ' + str(new_value) + '.'
  else:
    message = ''
  return valid, new_value, proposed_value, message
