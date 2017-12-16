# asciimare main engine

import time
import curses
import v3, colors, grays, noise, voxfield, charctrl
from abc import ABCMeta, abstractmethod

size = v3.Vec(0,0,0)
canvas = None
t = 0

# abstract class for a game
class GameTemplate(object):
  __metaclass__ = ABCMeta
  @abstractmethod
  def start(self):pass
  @abstractmethod
  def update(self):pass
  @abstractmethod
  def draw(self):pass
  @abstractmethod
  def keypressed(self,c):pass

# get terminal size (in characters)
def getdimensions():
  return size

# current frame #
def framecount():
  return t

# terminal-specific beep sound
def beep():
  curses.beep()

# draw character ch at position x, y
def drawchr(x,y,ch,col=0):
  canvas.addch(y,x,ch,curses.color_pair(col))

# draw string st at position x, y
def drawstr(x,y,st,col=0):
  canvas.addstr(y,x,st,curses.color_pair(col))

def main(stdscr,game):
  global size,t,canvas
  assert issubclass(game,GameTemplate)
  height,width = stdscr.getmaxyx()
  size = v3.Vec(min(100,width),min(30,height),0)
  canvas = curses.newpad(size.y+1, size.x+1)

  # initialize colors
  for k in colors.pairs.keys():
    v = colors.pairs[k]
    curses.init_pair(k,v[0],v[1])

  G = game()
  G.start()

  # main loop
  while True:
    t += 1
    stdscr.nodelay(1)
    c = stdscr.getch()
    G.update()
    G.draw()
    G.keypressed(c)
    try:
      canvas.refresh(0,0, 0,0, size.y-1, size.x-1)
    except:
      pass

# load and run a game
def run(game):
  print"""
     +-----------+
       ASCIIMARE
   +---------------+

   .--.@@@@@@@@@@@@@
 <|x  o|>@@@@@@@@@@@@)
  |   /@@@@@@:====:@@@
  `Y_/@@@@@@@|>_  |@@@
    @@@@@@@@@|____|@@
     @@@@@@@@@@@@@@@
      \/\/     \/\/
"""
  print 'Powered by asciimare: a 3D ASCII art engine'
  def f(stdstr):
    main(stdstr,game)
  try:
    curses.wrapper(f)
  except KeyboardInterrupt:
    print "bye."
    quit()







