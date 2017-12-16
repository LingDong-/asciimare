# Utility for controlling characters

import voxfield as vf
import v3
import math

# create new character controller
def newchar():
  return {'rot':v3.Vec(0,math.pi/4,0),
          'pos':v3.Vec(0,0,0),
          'forw':v3.forward,
          'hei':5,
          'slopelim':1,
          'block_f':False,
          'block_b':False,
          'grounded':False,
          'v':v3.Vec(0,0,0)}

# add a vector to character vector field
def addto(char,nm,inc):
  char[nm] = v3.Vec(char[nm].x+inc.x,
                    char[nm].y+inc.y,
                    char[nm].z+inc.z)

# rotating and moving around:
def turn_left(char,m=1):
  addto(char,'rot',v3.Vec(0,-0.1*m,0))

def turn_right(char,m=1):
  addto(char,'rot',v3.Vec(0,0.1,0))

def move_forw(char,m=1,fly=False):
  if not char['block_f']:
    f = char['forw']
    f = v3.normalize(v3.Vec(f.x,f.y*fly,f.z))
    addto(char,'pos',v3.scale(f,0.5*m))
    return True
  return False

def move_back(char,m=1,fly=False):
  if not char['block_b']:
    f = char['forw']
    f = v3.normalize(v3.Vec(f.x,f.y*fly,f.z))
    addto(char,'pos',v3.scale(f,-0.5*m))
    return True
  return False

def look_up(char,m=1):
  addto(char,'rot',v3.Vec(0.1*m,0,0))

def look_down(char,m=1):
  addto(char,'rot',v3.Vec(-0.1*m,0,0))

def jump(char,m=1):
  if char['grounded']:
    addto(char,'v',v3.Vec(0,-0.3,0))
    return True
  return False
  
# render a scene L from character's pov
def camera(char,L,size,**kwargs):
  R = vf.raycast(L,char['pos'],char['rot'],win=size,**kwargs)
  return vf.render(R)


# update character controller (check collision, gravity, etc.)
def update(char,L,gravity=True,collision=True):
  char['forw']=v3.roteuler(v3.forward,char['rot'])
  addto(char,'pos',char['v'])

  def check_gravity():
    p = char['pos']
    p = v3.Vec(round(p.x),round(p.y)+char['hei'],round(p.z))
    if vf.check(L,p) == 0 and p.y < L['size'].y:
      char['grounded']=False
      addto(char,'v',v3.Vec(0,0.01,0))
    else:
      char['v']=v3.Vec(0,0,0) 
      char['grounded']=True

  def check_collision():
    p = char['pos']
    f = char['forw']
    char['block_f']=False
    char['block_b']=False
    for i in range(char['hei']-char['slopelim']):
      qf = v3.add(v3.Vec(p.x,p.y+i,p.z),v3.normalize(v3.Vec(f.x,0,f.z)))
      qb = v3.add(v3.Vec(p.x,p.y+i,p.z),v3.normalize(v3.Vec(-f.x,0,-f.z)))

      qf = v3.Vec(int(round(qf.x)),int(round(qf.y)),int(round(qf.z)))
      qb = v3.Vec(int(round(qb.x)),int(round(qb.y)),int(round(qb.z)))

      if vf.check(L,qf) != 0:
        char['block_f']=True
        break

      if vf.check(L,qb) != 0:
        char['block_b']=True
        break

    if char['block_f'] == False:
      for i in range(char['hei']-char['slopelim'],char['hei']):
        q = v3.add(v3.Vec(p.x,p.y+i,p.z),v3.normalize(v3.Vec(f.x,0,f.z)))
        q = v3.Vec(int(round(q.x)),int(round(q.y)),int(round(q.z)))
        if vf.check(L,q) != 0:
          addto(char,'pos',v3.Vec(0,-1,0))

  if gravity: check_gravity()
  if collision: check_collision()






