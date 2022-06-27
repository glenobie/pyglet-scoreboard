import socket
import pyglet
from pyglet import font
from key_handler import KeyHandler

####################################################################
class FastActionWindow(KeyHandler, pyglet.window.Window) :

    def __init__(self, width, height, fullscreen = False) :
        pyglet.window.Window.__init__(self, width, height, fullscreen=fullscreen)
        
        self.batch = pyglet.graphics.Batch()

        self.label = pyglet.text.Label('Testing', 'Built Titling', 40, batch = self.batch)
        self.label.position = (100,100)
        

    def on_draw(self) :
        self.clear()
        self.batch.draw()