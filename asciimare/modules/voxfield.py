# Utility for generating, manipulating and rendering voxels

import math
import random
import v3
import grays
import noise

# make an empty voxel field
def zero(size):
  L = {'size':size}
  for xi in range(size.x):
    for yi in range(size.y):
      for zi in range(size.z):
        L[xi,yi,zi]=0
  return L

# load voxels from multiple csv files
# each file specifies a horizontal slice
# each value specifies an ANSI color (1-8)
def loadCsv(size,lvls):
  L = {'size':size}
  for yi in range(size.y):
    lvls[yi]=open(lvls[yi],'r').read().replace("\r","\n").replace("\n\n","\n").split("\n")
    for zi in range(size.z):
      lvls[yi][zi] = lvls[yi][zi].split(',')
      for xi in range(size.x):
        try:
          L[xi,yi,zi]=int(str(lvls[yi][zi][xi]))
        except:
          print "ERR", "'"+lvls[yi][zi][xi]+"'"
          L[xi,yi,zi]=0
  return L

# load voxels from a Goxel .txt export
# (http://guillaumechereau.github.io/goxel/)
# colors are approximated to the closest ANSI color
def loadGox(file):
  L = {}
  l = []
  lvls = open(file,'r').read().replace("\r","\n").replace("\n\n","\n").split("\n")
  for i in range(len(lvls)):

    if lvls[i].startswith('#') or lvls[i].strip()=='':
      continue

    pos=lvls[i][:-7].split(' ')
    pos=(int(pos[0]),int(pos[2]),int(pos[1]))
    col=lvls[i][-6:]
    r,g,b = int(col[:2],16), int(col[2:4],16), int(col[4:],16)
    ansi = [None,(0,0,0),(255,0,0),(0,255,0),(255,255,0),(0,0,255),(255,0,255),(0,255,255),(255,255,255)]
    mindist = 500
    minind = 0
    for j in range(1,len(ansi)):
      d = math.sqrt((r-ansi[j][0])**2 + (g-ansi[j][1])**2 + (b-ansi[j][2])**2)
      if d <= mindist:
        minind = j
        mindist = d
    col = minind
    l.append((pos, col))

  xmin, xmax, ymin, ymax, zmin, zmax = None, None, None, None, None, None
  for i in range(len(l)):
    if xmin == None or l[i][0][0] < xmin: xmin = l[i][0][0]
    if xmax == None or l[i][0][0] > xmax: xmax = l[i][0][0]
    if ymin == None or l[i][0][1] < ymin: ymin = l[i][0][1]
    if ymax == None or l[i][0][1] > ymax: ymax = l[i][0][1]
    if zmin == None or l[i][0][2] < zmin: zmin = l[i][0][2]
    if zmax == None or l[i][0][2] > zmax: zmax = l[i][0][2]

  print xmin, xmax, ymin, ymax, zmin, zmax
  size = v3.Vec(xmax-xmin+1,ymax-ymin+1,zmax-zmin+1)

  for i in range(len(l)):
    p = l[i][0]
    L[p[0]-xmin,size.y-(p[1]-ymin)-1,p[2]-zmin]=l[i][1]

  L['size']=size
  return L

# fill a 3d range of voxels with color b
def box(L,x0,y0,z0,x1,y1,z1,b=1):
  for xi in range(x0,x1):
    for yi in range(y0,y1):
      for zi in range(z0,z1):
        L[xi,yi,zi]=b

# print vox field as string (for testing)
def tostr2d(L):
  s = ""
  for zi in range(L['size'].z):
    for yi in range(L['size'].y):
      for xi in range(L['size'].x):
        s += ["#","."][check(L,v3.Vec(xi,yi,zi))==0]
      s += " "
    s += "\n"
  return s

# check the value of a coordinate in field
def check(L,v):
  try:
    return L[int(v.x),int(v.y),int(v.z)]
  except KeyError:
    return 0

# raycasting
# cam specifies aperture configuration (width, height, distance)
# win specifies 2D projection size (in characters)
def raycast(L,pos,rot,maxdist=128,cam=v3.Vec(0.3,0.2,0.3),win=v3.Vec(10,10,0)):
  field = {}
  step = 1
  forw = v3.roteuler(v3.Vec(0,0,1),rot)

  def ray(v,forwstep):
    backstep = v3.scale(forwstep,-0.1)
    for k in range(0,int(maxdist/step)):
      n = k*step
      v = v3.add(v,forwstep)
      b = check(L,v)
      if b != 0:
        for m in range(10):
          v = v3.add(v,backstep)
          if check(L,v) == 0:
            return n-m*0.1,v,b
          b = check(L,v)
        return n,v,b

    return -1,v,1

  for i in range(-win.x/2,win.x/2):
    for j in range(-win.y/2,win.y/2):
      xi = i/(win.x/2.0) * (cam.x/2.0)
      yi = j/(win.y/2.0) * (cam.y/2.0)
      v = v3.Vec(xi,yi,cam.z)
      v = v3.roteuler(v,rot)

      fs = v3.scale(v3.normalize(v),step)
      v = v3.add(pos,v)
      n,p,b = ray(v,fs)
      field[i+win.x/2,j+win.y/2]=(n,b)
  field['size']=win
  return field


# renders a raycasting result (using ASCII characters and ANSI colors)
def render(R,maxdist=80):

  def mapval(value,istart,istop,ostart,ostop):
    return ostart + (ostop - ostart) * ((value - istart)*1.0 / (istop - istart))

  S = {'size':R['size']}
  for i in range(R['size'].x):
    for j in range(R['size'].y):
      if (i,j) in R.keys():
        if R[i,j][0] == -1:
          if i % 2 == 0:
            S[i,j] = ("$",100)
          else:
            S[i,j] = ("$",100)
        elif R[i,j][0] < maxdist/4:
          S[i,j] = (grays.getshade( 1-mapval(R[i,j][0],0,maxdist/4,0,1) ),10+R[i,j][1])
        elif R[i,j][0] < maxdist/2:
          S[i,j] = (grays.getshade(  mapval(R[i,j][0],maxdist/4,maxdist/2,0,1) ),20+R[i,j][1])
        elif R[i,j][0] < maxdist*3/4:
          S[i,j] = (grays.getshade( 1-mapval(R[i,j][0],maxdist/2,maxdist*3/4,0,1) ),30+R[i,j][1])
        else:
          S[i,j] = (grays.getshade( 1-mapval(R[i,j][0],maxdist*3/4,maxdist,0,1) ),40+R[i,j][1])

      else:
        S[i,j] = ("?",0)
  return S


