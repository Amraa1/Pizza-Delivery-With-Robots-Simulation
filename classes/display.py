from Globals import default_width, default_height, mpl_shapes, mpl_colors
from IPython.display import clear_output
from Utilities import irradiance
import matplotlib.pyplot as plt
import time
from random import randint
from robot_default import robot_default


def display(markers,**kwargs):
  """
  A function to display the arena with matplotlib.\n
  Future Update: display the game on pygame
  """
  cm = 1/2.54
  #ecosystem parameter that can be passed to get useful information
  width = kwargs.get('width', 45)*cm
  height = kwargs.get('height', 22.5)*cm
  pause = kwargs.get('pause', 250)
  title = kwargs.get('title','Ecosystem Display')
  clear = kwargs.get('clear',True)
  hour =  kwargs.get('hour', 12)
  brightness = kwargs.get('brightness', False)
  facecolor =  kwargs.get('facecolor', 'pink')
  annotations = kwargs.get('annotations', [])
  annotate = len(annotations) > 0
  edgecolors = mpl_colors[kwargs.get('edgecolors', "black")]
  ## _display_parameters ##
  #can change where to show annotations
  if annotate:
    try:
      if type(annotations[0]) == tuple:
        dx,dy = annotations[0][0],annotations[0][1]
      else:
        dx,dy = 1, 1
    except:
      pass
  
  try:
    title = title.format(**kwargs)
  except Exception as error:
    title = title + ' #format missing ' + str(error) + '#'

  x_max =  default_width
  y_max =  default_height

  if clear:
    clear_output(wait=True)
 
  a = irradiance(hour) if brightness else 1


  fig = plt.figure(figsize=(width,height))
  fig.patch.set_facecolor('grey')
  fig.patch.set_alpha(0.6)
  ax = fig.add_subplot(111)
  ax.patch.set_facecolor(facecolor)
  ax.patch.set_alpha(a)

  plt.title (title)
  plt.xlim(-2, x_max+2)
  plt.ylim(-2, y_max+2)
  for p in markers:
    try:
      x=p['coordinates'][0]
      y=p['coordinates'][1]
      scale = p['size']
      color = p['color'] 
      shape = p['shape']
      alpha = p['alpha']
      marker_shape = mpl_shapes[shape] 
      ax.scatter(x, y, s=scale, c=color, marker=marker_shape, alpha=alpha, edgecolors=edgecolors)
      #helicopter wing
      if p['coordinates'][2] > 0:
        ax.scatter(x, y, s=scale*3, c='k', marker='1', alpha=alpha, edgecolors=edgecolors)   
      #put annotation into place with its arguments
      if annotate:
        try:
          annotation =  ';'.join(key + ":" + str(value) for key, value in p.items() if key in annotations) #can annotate any key in marker dictionary
          plt.annotate(annotation, (x+dx, y+dy),)
        except:
          pass

    except Exception as error:
      #print("Point error:", p, error)
      continue

  #creating girds
  ax.set_xticks(range(0, x_max + 1, 10))
  ax.set_yticks(range(0, y_max + 1, 10))
  ax.grid(color = 'red', linestyle = '--', linewidth = 0.25)

  plt.show()
  time.sleep(pause/1000)

if __name__ == "__main__":
  points = []

  for kind in ['Robot', 'Drone', 'Droid', 'Grid_Charger', 'Solar_Charger','Repair_Station','Recycling_Station', 'Pizza', 'Pizza']:
    register = robot_default(kind, 'default')
    alt_max = 1 if kind == 'Drone' else 0
    register['coordinates'][0] = randint (0, default_width)
    register['coordinates'][1] = randint (0, default_height)
    register['coordinates'][2] = randint (0, alt_max)
    points.append(register)
     
  display(points, facecolor = 'pink',title = "Ecosystem Display Hour:{hour} Registered:{registered}", annotations = [(1.5,0),'soc','name'], hour = 12, registered = len(points))