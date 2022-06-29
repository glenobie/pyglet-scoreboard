import pyglet
from die import Die

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

        self.titleDoc = pyglet.text.document.UnformattedDocument('')  
        self.titleDoc.set_style(0, len(self.titleDoc.text), dict( dict(font_name = Die.FONT, 
                                                                         font_size = 22, 
                                                                         color=(255,255,255,255))))
        self.titleLayout = pyglet.text.layout.TextLayout(self.titleDoc, batch=batch, group = self.fg)
        self.titleLayout.anchor_y = 'center'

    # assuming one die for right now
    # TODO more dice
    def valueChanged(self, value) :
        newLabel = ''
        for p in self.valueLabels :
            if p[0] == value :
                newLabel = p[1]
        self.labelDoc.text = newLabel


    def setPosition(self, left, center, spacing) :
        self.titleLayout.position = (left, center)
        left += self.titleLayout.content_width
        for d in self.dice :
            x = left + d.getWidth() // 2
            d.setCenter(x, center)
            left = x + d.getWidth() // 2 + spacing

        self.labelLayout.position = (left, center)

    # a list of labels that will show to right of dice set when certain value occur
    def attachValueLabel(self, pair) :
        self.valueLabels.append(pair)
        
    # label to left of dice set
    def setTitle(self, title) :
        self.title = title
        self.titleDoc.text = self.title

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