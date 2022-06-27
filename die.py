import math
import pyglet
import random


##########################################
class Die :
    
    def __init__(self, color, text_color=(0,0,0,255), sides=6, batch=None) :

        self.batch = batch
        self.sides = sides
        self.bg = pyglet.graphics.OrderedGroup(0)
        self.fg = pyglet.graphics.OrderedGroup(99)
        self.value = 1

        self.border = pyglet.shapes.BorderedRectangle(0,0,40,40,1,color=color, batch=self.batch, group = self.bg)
        
        self.document = pyglet.text.document.UnformattedDocument(str(self.getValue()) )
        self.document.set_style(0, len(self.document.text), dict( dict(font_name = 'Arial', 
                                                                       font_size = 20, 
                                                                        color=text_color)))
        self.layout = pyglet.text.layout.TextLayout(self.document, batch=self.batch, group = self.fg)


        self.roll()

    def getValue(self) :
        return self.value

    def roll(self) :
        self.value = random.randint(1, self.sides)
        self.document.delete_text(0,len(self.document.text))
        self.document.insert_text(0, str(self.getValue()))

    def scale(self, value) :
        0

    def setCenter(self, x, y) :
        self.border.position = (x,y)
        self.layout.position = (x,y)

    def update(self) :
        0