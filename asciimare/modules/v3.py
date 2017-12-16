# Utility for creating and manipulating 3D vectors

import math
from collections import namedtuple
Vec = namedtuple('Vec', ['x','y','z'])

# standard directions
forward = Vec(0,0,1)
up = Vec(0,1,0)
right = Vec(1,0,0)

# rotate a vector around axis by angle
def rotvec(vec,axis,th):
  l,m,n = axis
  x,y,z = vec
  cos,sin = math.cos(th), math.sin(th)

  mat={}
  mat[1,1]= l*l *(1-cos) +cos
  mat[1,2]= m*l *(1-cos) -n*sin
  mat[1,3]= n*l *(1-cos) +m*sin

  mat[2,1]= l*m *(1-cos) +n*sin
  mat[2,2]= m*m *(1-cos) +cos
  mat[2,3]= n*m *(1-cos) -l*sin

  mat[3,1]= l*n *(1-cos) -m*sin
  mat[3,2]= m*n *(1-cos) +l*sin
  mat[3,3]= n*n *(1-cos) +cos

  return Vec(
    float(x*mat[1,1] + y*mat[1,2] + z*mat[1,3]),
    float(x*mat[2,1] + y*mat[2,2] + z*mat[2,3]),
    float(x*mat[3,1] + y*mat[3,2] + z*mat[3,3]),
  )

# rotate vector by euler angles z x y
def roteuler(vec,rot):
  if rot.z != 0 : vec = rotvec(vec,forward,rot.z)
  if rot.x != 0 :vec = rotvec(vec,right,rot.x)
  if rot.y != 0 :vec = rotvec(vec,up,rot.y)
  return vec

# scale vector by a factor
def scale(vec,p):
  return Vec(vec.x*p,vec.y*p,vec.z*p)

# vector addition
def add(v0,v):
  return Vec(v0.x+v.x,v0.y+v.y,v0.z+v.z)

# magnitude
def mag(v):
  return math.sqrt(v.x*v.x + v.y*v.y + v.z*v.z)

# |v| = 1
def normalize(v):
  p = 1/mag(v)
  return Vec(v.x*p,v.y*p,v.z*p)


