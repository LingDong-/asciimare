import asciimare

class game(asciimare.GameTemplate):
  # use this for initialization
  def start(self):
    # load a scene from Goxel txt export.
    self.scene = asciimare.voxfield.loadGox("maps/demo.txt")
    # Create a character controller
    self.player = asciimare.charctrl.newchar()

  # update is called once per frame
  def update(self):
    # update character controller (checks collision, gravity, etc.)
    asciimare.charctrl.update(self.player,self.scene)

  # draw stuff
  def draw(self):
    # get a rendering of the scene from player's camera
    S = asciimare.charctrl.camera(self.player,self.scene, asciimare.getdimensions())
    # draw all the 'pixels'
    for i in range(S['size'].x):
      for j in range(S['size'].y):
        asciimare.drawchr(i,j,S[i,j][0],col=S[i,j][1])

  # get pressed key
  def keypressed(self,c):
    # navigate around the scene using character controller
    if c == ord('a'):   asciimare.charctrl.turn_left(self.player)
    elif c == ord('d'): asciimare.charctrl.turn_right(self.player)
    elif c == ord('q'): asciimare.charctrl.look_up(self.player)
    elif c == ord('e'): asciimare.charctrl.look_down(self.player)

    elif c == ord('w'):
      if not asciimare.charctrl.move_forw(self.player):asciimare.beep()

    elif c == ord('s'):
      if not asciimare.charctrl.move_back(self.player):asciimare.beep()

    elif c == ord(' '):
      if not asciimare.charctrl.jump(self.player):asciimare.beep()

# run the game!
asciimare.run(game)


