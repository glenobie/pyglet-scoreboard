import pyglet
from key_handler import KeyHandler
from die import Die
from random import seed
import time
import importlib

####################################################################
class FastActionWindow(pyglet.window.Window) :

    def __init__(self, width, height, fullscreen = False) :
        pyglet.window.Window.__init__(self, width, height, fullscreen=fullscreen)

        self.batch = pyglet.graphics.Batch()
        self.bg = pyglet.graphics.OrderedGroup(0)

        self.background = pyglet.shapes.Rectangle(0,0,800,480, (18,18,18), self.batch, self.bg)

        seed(time.time_ns())
        self.fac = None

    def on_draw(self) :
        self.clear()
        if not(self.fac is None) :
            self.fac.draw()

    def setFACSet(self, facModule, facClass):
        class_ = getattr(importlib.import_module(facModule), facClass)
        self.fac = class_()

    def handle_L(self) :
        if not(self.fac is None) :
            self.fac.handle_L()


