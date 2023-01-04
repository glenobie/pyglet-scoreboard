import pyglet
from fac_set import FACSet, ChoiceFAC
from die import Die
from random import seed
import time

####################################################################
class FastActionWindow(pyglet.window.Window) :

    def __init__(self, width, height, fullscreen, screen=None) :
        pyglet.window.Window.__init__(self, width, height, fullscreen=fullscreen, screen=screen)
        seed(time.time_ns())
        self.fac = ChoiceFAC()

    def on_draw(self) :
        self.clear()
        self.fac.draw()
 
    def setFACSet(self, fac):
        self.fac = fac

    def handle_L(self) :
        self.fac.handle_L()

    def handle_K(self) :
        self.fac.handle_K()
    
    def clearFACSet(self) :
        self.fac = ChoiceFAC()


