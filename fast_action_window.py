import pyglet
from die import Die
from random import seed
import time

####################################################################
class FastActionWindow(pyglet.window.Window) :

    def __init__(self, width, height, fullscreen, screen=None) :
        pyglet.window.Window.__init__(self, width, height, fullscreen=fullscreen, screen=screen)

        self.batch = pyglet.graphics.Batch()
        self.bg = pyglet.graphics.OrderedGroup(0)

        self.background = pyglet.shapes.Rectangle(0,0,800,480, (18,18,18), self.batch, self.bg)

        seed(time.time_ns())
        self.fac = None


    def on_draw(self) :
        self.clear()
        if self.fac is None :
            self.displayMessage('Choose a Game')
        else:
            self.fac.draw()
 
    def setFACSet(self, fac):
        self.fac = fac

    def handle_L(self) :
        if not(self.fac is None) :
            self.fac.handle_L()

    def handle_K(self) :
        if not(self.fac is None) :
            self.fac.handle_K()
    
    def clearFACSet(self) :
        self.fac = None

    def displayMessage(self, text) :
        msgDoc = pyglet.text.document.UnformattedDocument(text)
        msgDoc.set_style(0,len(msgDoc.text), dict(color=(255,255,255,255), font_name = Die.FONT,  font_size = 28 ))
        self.msgLayout = pyglet.text.layout.TextLayout(msgDoc)
        self.msgLayout.anchor_x = 'center'
        self.msgLayout.position = (400, 300)
        self.msgLayout.draw()
