import pyglet
import random
import math

##########################################
class Die :

    D_GREEN = (0, 153,0)
    D_BLUE = (0,0,204)
    D_WHITE = (255,255,255)
    D_GRAY = (160,160,160)
    D_BLACK = (20,20,20)
    D_PINK = (153, 0, 76)
    D_ORANGE = (204, 102, 0)
    D_RED = (204, 0, 0)
    D_WHITE = (230,230,230)
    D_LIGHT_GREEN = (100,255,100)
    D_LIGHT_BLUE = (102, 178, 255)
    D_PURPLE = (76,0, 153)
    D_BROWN = (102, 51, 0 )
    D_AQUA = (0,150,150)
    D_DARK_GREEN = (0,80,0)
    D_GOLD = (255,215,0)

    T_WHITE = (255,255,255,255)
    T_BLACK = (0,0,0,255)

    WIDTH = 100
    HEIGHT = 100
    TEXT_SIZE = 80
    INTERIOR_SPACING_PCT = 0.5
    FONT = 'Arial'
    
    def __init__(self, color, text_color=(0,0,0,255), sides=6, batch=None) :
        self.bg = pyglet.graphics.OrderedGroup(4)
        self.fg = pyglet.graphics.OrderedGroup(99)
        self.batch = batch

        self.listeners = []

        self.sides = sides
        self.color = color
        self.text_color = text_color
        self.value = 1
        self.dieLabels = []
        self.colorConditions = []
        self.center = (0,0)

        self.baseTextSize = Die.TEXT_SIZE
        self.interiorSpacingPct = Die.INTERIOR_SPACING_PCT

        self.border = pyglet.shapes.BorderedRectangle(0, 0, Die.WIDTH, Die.HEIGHT, 1, 
                            border_color = (255,255,255), color=color, batch=self.batch, group = self.bg)
        self.document = pyglet.text.document.UnformattedDocument(str(self.sides) )
        self.document.set_style(0, len(self.document.text), dict( dict(font_name = Die.FONT,  font_size = self.baseTextSize, color=text_color)))
        self.layout = pyglet.text.layout.TextLayout(self.document, batch=self.batch, group = self.fg)
        self.layout.anchor_x = 'center'
        self.layout.anchor_y = 'bottom'
        self.layout.content_valign = 'center'

        self.adjustBaseTextSize()
        self.roll()

  
    def addColorCondition(self, pair) :
        self.colorConditions.append(pair)
        self.update()

    def setInteriorSpacingPct(self, value) :
        self.interiorSpacingPct = value
        self.adjustBaseTextSize()
        self.update()

    def adjustBaseTextSize(self) :
        # find longest possible string
        testString = str(self.sides)
        for t in self.dieLabels :
            if len(t) > len(testString) :
                testString = t

        desiredSpacing = self.border.width * self.interiorSpacingPct
        self.document.text = testString
        while self.border.width - self.layout.content_width < desiredSpacing :
            self.baseTextSize -= 1
            self.document.set_style(0, len(self.document.text), dict(font_size=self.baseTextSize))
        

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

    def setDieLabels(self, array) :
        self.dieLabels = array
        self.update()
        self.adjustBaseTextSize()

    def update(self) :
        if len(self.dieLabels) > 0 :
            text = self.dieLabels[self.value-1]
        else :
            text = str(self.value)
        for c in self.colorConditions :
            if c[0] == self.value :
                self.border.color = c[1]

        self.document.delete_text(0,len(self.document.text))
        self.document.insert_text(0, text)


    def scale(self, value) :
        self.border.width = math.floor(Die.WIDTH * value)
        self.border.height = math.floor(Die.HEIGHT * value)
        self.adjustBaseTextSize()
        self.setCenter(self.center[0], self.center[1])
        self.update()

    def setCenter(self, x, y) :
        self.center = (x, y)
        self.border.position = (x - self.border.width // 2 , y - self.border.height // 2)

        layout_y = self.border.y + (self.border.height  - self.layout.content_height) // 2

        self.layout.position = (x, layout_y)

    def getWidth(self) :
        return self.border.width

#######################################
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




        
        
