import math
import argparse
import asciimare

def explore(file):
  class game(asciimare.GameTemplate):
    def start(self):
      self.scene = asciimare.voxfield.loadGox(file)
      self.player = asciimare.charctrl.newchar()
      self.player['rot'] = asciimare.v3.Vec(-math.pi/6,math.pi/4,0)

    def update(self):
      asciimare.charctrl.update(self.player,self.scene,gravity=False)

    def draw(self):
      S = asciimare.charctrl.camera(self.player,self.scene, asciimare.getdimensions())
      for i in range(S['size'].x):
        for j in range(S['size'].y):
          asciimare.drawchr(i,j,S[i,j][0],col=S[i,j][1])

    def keypressed(self,c):
      if c == ord('a'):   asciimare.charctrl.turn_left(self.player)
      elif c == ord('d'): asciimare.charctrl.turn_right(self.player)
      elif c == ord('q'): asciimare.charctrl.look_up(self.player)
      elif c == ord('e'): asciimare.charctrl.look_down(self.player)

      elif c == ord('w'):
        if not asciimare.charctrl.move_forw(self.player,fly=True):asciimare.beep()

      elif c == ord('s'):
        if not asciimare.charctrl.move_back(self.player,fly=True):asciimare.beep()

  asciimare.run(game)

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Load a map to explore...')
  parser.add_argument('-i','--input',dest='input_path',
    action='store',nargs='?',type=str,
    help='Load map from file')
  args = parser.parse_args()
  if args.input_path == None:
    parser.print_help()
  else:
    asciimare.run(explore(args.input_path))