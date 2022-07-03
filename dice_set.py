import pyglet
from die import Die

########################################################
class DiceSet :

    # pass me a list of Die objects
    def __init__(self, dice, batch) :
        
        self.fg = pyglet.graphics.OrderedGroup(59)
        self.batch = batch
        self.dice = dice
        self.computeTotal()

        for d in self.dice :
            d.addValueChangedListener(self)

        self.booleanFunctionLabels = []

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

    # are all the dice equal in value
    def allEqual(self) :
        d1 = self.dice[0].getValue()
        for d in self.dice :
            if d.getValue() != d1 :
                return False
        return True

    # does the total of the dice equal the value passed
    def totalEquals(self, value) :
        return True if self.total == value else False

    # true if any of the dice in the set equal the valye
    def anyDieEquals(self, value) :
        for d in self.dice :
            if d.getValue() == value :
                return True
        return False

    def valueChanged(self, value) :
        self.computeTotal()
        self.updateLabels()

    def computeTotal(self) :
        self.total = 0
        for d in self.dice :
            self.total += d.getValue()

    # instead of boolean function labels
    def setLabel(self, text) :
        self.labelDoc.text = text

    def updateLabels(self) :
        newLabel = ''
        for b in self.booleanFunctionLabels :
            if b[0]() : 
                newLabel += b[1]
        self.labelDoc.text = newLabel

    def setPositionInternal(self, left, center, spacing, list) :
        self.titleLayout.position = (left, center)
        left += self.titleLayout.content_width
        for d in list :
            x = left + d.getWidth() // 2
            d.setCenter(x, center)
            left += d.getWidth() + spacing
        self.labelLayout.position = (left, center)


    def setPosition(self, left, center, spacing=12) :
        self.setPositionInternal(left, center, spacing, self.dice)

    # pair is a (booleanFunction, text) pair
    def attachBooleanFunctionLabel(self, pair) :
        self.booleanFunctionLabels.append(pair)
        self.updateLabels()
        
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
    
    # redirects with the sorted list
    def setPosition(self, left, center, spacing=12) :
        self.left = left
        self.center = center
        self.spacing = spacing
        self.setPositionInternal(left, center, spacing, self.sortedList)

    def valueChanged(self, value) :
        DiceSet.valueChanged(self, value)
        self.sortedList = sorted(self.dice, key=lambda die: die.value)
        self.setPosition(self.left, self.center, self.spacing)

#########################################
class BorderedDiceSet(DiceSet) :
    BORDER_SPACING = 24
    LABEL_SPACING = 8

    def __init__(self, dice, batch) :
        DiceSet.__init__(self, dice, batch)
        self.titleLayout.anchor_x = 'left'
        self.x = self.y = self.width = self.height = 0

    # label to left of dice set
    def setTitle(self, title) :
        DiceSet.setTitle(self, title)
        self.drawBorder(self.x, self.y, self.width, self.height)

    def setPosition(self, left, center, spacing=12) :
        self.left = left
        self.center = center
        self.spacing = spacing

        self.x = left

        self.width = 0
        self.height = 0
        for d in self.dice :
            self.width += d.getWidth()
            if d.getWidth() > self.height :
                self.height = d.getWidth()
        self.width += 0 if len(self.dice) == 0 else (len(self.dice) - 1) * self.spacing
        self.width += BorderedDiceSet.BORDER_SPACING * 2
        self.height += BorderedDiceSet.BORDER_SPACING * 2      
   
        x = left + BorderedDiceSet.BORDER_SPACING
        for d in self.dice :
            x += d.getWidth() // 2
            d.setCenter(x, center)
            x += d.getWidth() // 2 + spacing

        self.y = center - self.height/2
        self.drawBorder(self.x, self.y, self.width, self.height)
 
    def drawBorder(self, x, y, width, height) :
        self.lines = []
        self.lines.append(pyglet.shapes.Line(x, y, x, y + height, width=1, batch=self.batch))  
        self.lines.append(pyglet.shapes.Line(x+width, y, x+width, y + height, width=1, batch=self.batch))  
 
        if len(self.titleDoc.text) > 0 :
            title_x = x + (width - self.titleLayout.content_width) // 2
            title_y = y + height 
            self.titleLayout.position = (title_x, title_y)
            self.lines.append(pyglet.shapes.Line(x, y+height, title_x - BorderedDiceSet.LABEL_SPACING, 
                                    y + height, width=1, batch=self.batch))       
            self.lines.append(pyglet.shapes.Line(title_x + self.titleLayout.content_width + BorderedDiceSet.LABEL_SPACING, y+height, x+width, 
                                 y + height, width=1, batch=self.batch))       
        else :
            self.lines.append(pyglet.shapes.Line(x, y+height, x+width, y+height, width=1, batch=self.batch))       
           

        if len(self.labelDoc.text) > 0 :
            label_x = x + (width - self.labelLayout.content_width) // 2
            self.labelLayout.position = (label_x, y)
            self.lines.append(pyglet.shapes.Line(x, y, label_x - BorderedDiceSet.LABEL_SPACING, 
                                    y, width=1, batch=self.batch))       
            self.lines.append(pyglet.shapes.Line(label_x + self.labelLayout.content_width + BorderedDiceSet.LABEL_SPACING, 
                                                   y, x+width, y, width=1, batch=self.batch))       
             
        else :
            self.lines.append(pyglet.shapes.Line(x, y, x+width, y, width=1, batch=self.batch))       

    def valueChanged(self, value):
        super().valueChanged(value)
        self.drawBorder(self.x, self.y, self.width, self.height)

    # instead of boolean function labels
    def setLabel(self, text) :
        super().setLabel(text)
        self.drawBorder(self.x, self.y, self.width, self.height)
