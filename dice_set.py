import pyglet
from die import Die
from fac_set import FACSet
import types

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
        self.labelDoc.set_style(0, len(self.labelDoc.text),  dict(font_name = FACSet.TEXT_FONT,
                                                                       font_size = 20,
                                                                       color=(255,255,255,255)))
        self.labelLayout = pyglet.text.layout.TextLayout(self.labelDoc, batch=batch, group = self.fg)
        self.labelLayout.anchor_y = 'center'

        self.titleDoc = pyglet.text.document.UnformattedDocument('')
        self.titleDoc.set_style(0, len(self.titleDoc.text), dict(font_name = FACSet.TEXT_FONT,
                                                                         font_size = 20,
                                                                         color=(255,255,255,255)))
        self.titleLayout = pyglet.text.layout.TextLayout(self.titleDoc, batch=batch, group = self.fg)
        self.titleLayout.anchor_y = 'center'

    def setTitleFontSize(self, value) :
        self.titleDoc.set_style(0, len(self.titleDoc.text), dict(font_size = value))

    def setLabelFontSize(self, value) :
        self.labelDoc.set_style(0, len(self.labelDoc.text), dict(font_size = value))

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

    def totalAsString(self) :
        return str(self.computeTotal())

    def valueChanged(self, value) :
        self.computeTotal()
        self.updateLabels()

    def computeTotal(self) :
        self.total = 0
        for d in self.dice :
            self.total += d.getValue()
        return self.total

    # instead of boolean function labels
    def setLabel(self, text) :
        self.labelDoc.text = text

    def updateLabels(self) :
        newLabel = ''
        wasPreviousLabel = False
        for b in self.booleanFunctionLabels :
            if b[0]() :
                if wasPreviousLabel :
                    newLabel += ' / '
                if callable(b[1]) :
                    newLabel += b[1]()
                else :
                    newLabel += b[1]
                wasPreviousLabel = True

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

    # pair is a (booleanFunction, text) pair or a (booleanFunction, stringFunction) pair
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
