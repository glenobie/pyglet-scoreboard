import pyglet
from key_handler import KeyHandler
from die import Die
from random import seed
import time

####################################################################
class FastActionWindow(KeyHandler, pyglet.window.Window) :

    def __init__(self, width, height, fullscreen = False) :
        pyglet.window.Window.__init__(self, width, height, fullscreen=fullscreen)
        
        self.batch = pyglet.graphics.Batch()

        self.dice = []

        d1 = Die((255,0,0), sides=6, batch=self.batch)
        d1.setCenter(300,300)
        self.dice.append(d1)
        d1 = Die((255,255,0), sides=8, batch=self.batch)
        d1.setCenter(500,300)
        self.dice.append(d1)


        seed(time.time_ns())

    def on_draw(self) :
        self.clear()
        self.batch.draw()

    def setFACSet(self, fac):
        self.fac = fac

    def handle_L(self, modified = False) :
        for d in self.dice :
            d.roll()

    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.L :
            self.handle_L(modifiers & pyglet.window.key.LSHIFT)
        elif symbol == pyglet.window.key.K :
            self.handle_K(modifiers & pyglet.window.key.LSHIFT)

