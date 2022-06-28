import colorsys
import math
import pyglet
import random


##########################################
class Die :

    WIDTH = 100
    HEIGHT = 100
    TEXT_SIZE = 50
    FONT = 'Arial'
    
    def __init__(self, color, text_color=(0,0,0,255), sides=6, batch=None) :
        self.batch = batch
        self.sides = sides
        self.bg = pyglet.graphics.OrderedGroup(1)
        self.fg = pyglet.graphics.OrderedGroup(99)
        self.color = color
        self.text_color = text_color
        self.value = 1

        self.listeners = []

        self.border = pyglet.shapes.BorderedRectangle(0, 0, Die.WIDTH, Die.HEIGHT, 1, 
                            border_color = (255,255,255), color=color, batch=self.batch, group = self.bg)
        self.document = pyglet.text.document.UnformattedDocument(str(self.getValue()) )
        self.document.set_style(0, len(self.document.text), dict( dict(font_name = Die.FONT, 
                                                                       font_size = Die.TEXT_SIZE, 
                                                                       color=text_color)))
        self.layout = pyglet.text.layout.TextLayout(self.document, batch=self.batch, group = self.fg)
        self.layout.anchor_x = 'center'
        self.layout.anchor_y = 'center'

        self.clones = []
        self.roll()


    def getValue(self) :
        return self.value

    def addValueChangedListener(self, ear) :
        self.listeners.append(ear)

    def makeClone(self) :
        c = DieClone(self.color, self.text_color, self.sides, self.batch)
        self.addValueChangedListener(c)
        c.valueChanged(self.value)
        return c

    def roll(self) :
        self.value = random.randint(1, self.sides)
        for ear in self.listeners :
            ear.valueChanged(self.value)
        self.update()

    def update(self) :
        self.document.delete_text(0,len(self.document.text))
        self.document.insert_text(0, str(self.getValue()))

    def scale(self, value) :
        self.border.width = Die.WIDTH * value
        self.border.height = Die.HEIGHT * value

        self.document.set_style(0, len(self.document.text), dict(font_size=Die.TEXT_SIZE * value))

    def setCenter(self, x, y) :
        self.center = (x, y)
        self.border.position = (x - self.border.width // 2 , y - self.border.height // 2)
        self.layout.position = (x,y)

    def getWidth(self) :
        return self.border.width


class DieClone(Die) :
    def __init__(self, color, text_color=(0,0,0,255), sides=6, batch=None) :
        Die.__init__(self, color, text_color, sides, batch)

    def valueChanged(self, value) :
        self.value = value
        for ear in self.listeners :
            ear.valueChanged(self.value)

        self.update()


    def roll(self) :
        0 # don't roll the clones



########################################################
class DiceSet :

    # pass me a list of Die objects
    def __init__(self, dice, batch) :
        
        self.fg = pyglet.graphics.OrderedGroup(59)
        self.dice = dice

        for d in self.dice :
            d.addValueChangedListener(self)
        self.valueLabels = []

        self.labelDoc = pyglet.text.document.UnformattedDocument('')  
        self.labelDoc.set_style(0, len(self.labelDoc.text), dict( dict(font_name = Die.FONT, 
                                                                       font_size = 22, 
                                                                       color=(255,255,255,255))))
        self.labelLayout = pyglet.text.layout.TextLayout(self.labelDoc, batch=batch, group = self.fg)
        self.labelLayout.anchor_y = 'center'
        
    # assuming one die
    # TODO more dice
    def valueChanged(self, value) :
        newLabel = ''
        for p in self.valueLabels :
            if p[0] == value :
                newLabel = p[1]
        self.labelDoc.text = newLabel
        ##self.labelDoc.delete_text(0, len(self.labelDoc.text))
        #self.labelDoc.insert_text(0, newLabel)

    def setPosition(self, left, center, spacing) :
        for d in self.dice :
            x = left + d.getWidth() // 2
            d.setCenter(x, center)
            left = x + d.getWidth() // 2 + spacing

        self.labelLayout.position = (left, center)

    # a list of labels that will show to right of dice set when certain value occur
    def attachValueLabel(self, pair) :
        self.valueLabels.append(pair)
        
    def roll(self) :
        for d in self.dice :
            d.roll()
        
#################################################
class SortedDiceSet(DiceSet) :

    # pass me a list of Die objects
    def __init__(self, dice, batch) :
        DiceSet.__init__(self, dice, batch)
        self.sortedList = sorted(self.dice, key=lambda die: die.value)
    
    def setPosition(self, left, center, spacing) :
        self.left = left
        self.center = center
        self.spacing = spacing
        for d in self.sortedList :
            x = left + d.getWidth() // 2
            d.setCenter(x, center)
            left = x + d.getWidth() // 2 + spacing

    def valueChanged(self, value) :
        self.sortedList = sorted(self.dice, key=lambda die: die.value)
        self.setPosition(self.left, self.center, self.spacing)


        
        
