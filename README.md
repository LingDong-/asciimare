# asciimare

*A 3D engine powered by ASCII art.*

![alt text](screenshots/gif1.gif)


asciimare uses ASCII characters to display 3D graphics directly in the terminal. It is powered by python [curses](https://docs.python.org/2/library/curses.html), and renders by raycasting on voxels.

asciimare utilizes the combination of 95 printable ASCII characters 8 ANSI colors in the terminal to emulate a variety of hues and brightness. It first analyzes a given font and generate a continous and uniform range of shades, e.g.

```
Menlo.ttc
          ````````````````````````'''''''''''''......-------
-,,,,,______::::::::^^^^^!!~~~"""""";;;;;;rrrrr++++||()\==>>
>>lllll???iiiccv[]ttzzjj7*ff{{}ssYYTJJJ111unnnnyyyyIIFFFFFFF
oooooowe22h3Zaa44XXX%%%555PPPP$$$mmGGAAUUUUbbbppKKK96O##H&&D
DDDRRRRRRQQ88888800000000WWWWMMMBBB@@@@@@@@@@@@@NNNNNNNNNNNN
```
and then plays with some color theory to create an illusion of depth.


## Dependencies
- PyPy 2 ([pypy.org](pypy.org)) (Python works but will be slow)

##Usage

Try it out by typing

```bash
$ pypy demo.py
```
or 

```bash
$ pypy explore.py -i maps/demo.txt
```
in your terminal. 

###  Loading models

You can explore different maps by loading them into the second command. Currently, asciimare supports models exported from [Goxel](http://guillaumechereau.github.io/goxel/) (plain text) or a batch of csv files each describing a slice along the y-axis.



### Importing asciimare as a module
To use asciimare as a module, place the `asciimare` subfolder under your project folder and simply do `import asciimare`. Then, you can define your game class with some standard events and asciimare will figure out the rest. See `demo.py` for details.


```python
import asciimare

class game(asciimare.GameTemplate):
  def start(self): pass         # use this for initialization
  def update(self): pass        # update called once per frame
  def draw(self): pass          # things to render upon redraw
  def keypressed(self,c): pass  # get pressed key
  
# run the game!
asciimare.run(game)
```
