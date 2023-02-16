
import pyglet
from pyglet import shapes
from pyglet import font 

class ShadowBorder() :

    BORDER_SPACING = 3
    BG_COLOR = (22,22,22)

    def __init__(self, width, textHeight, batch, bg, fg) :
        self.batch = batch
        self.fg = fg
        self.bg = bg
        self.width = width + ShadowBorder.BORDER_SPACING * 2
        self.height = textHeight + ShadowBorder.BORDER_SPACING * 2


    def drawLines(self) :
        self.border = shapes.Rectangle(self.x1, self.y1, self.width, self.height, color=ShadowBorder.BG_COLOR, batch=self.batch, group=self.bg  )
        x2 = self.x1 + self.getWidth()
        y2 = self.y1 + self.getHeight()

        self.l0 = pyglet.shapes.Line(self.x1, self.y1, self.x1, y2, 1,  batch=self.batch, group = self.fg)
        self.l0.opacity = 10
        self.l1 = pyglet.shapes.Line(self.x1, y2, x2, y2, 1,  batch=self.batch, group = self.fg)
        self.l1.opacity = 10
        self.l6 = pyglet.shapes.Line(x2,y2, x2, self.y1, 1, batch=self.batch, group = self.fg)
        self.l6.opacity = 30
        self.l7 = pyglet.shapes.Line(x2, self.y1, self.x1+2, self.y1, 1, batch=self.batch, group = self.fg)
        self.l7.opacity = 30

        self.l2 = pyglet.shapes.Line(self.x1+2, self.y1, self.x1+2, y2-2, 4, color=(0,0,0), batch=self.batch, group = self.fg)
        self.l3 = pyglet.shapes.Line(self.x1+2, y2-3, x2-1, y2-3, 4, color=(0,0,0), batch=self.batch, group = self.fg)
        self.l4 = pyglet.shapes.Line(x2-1, y2-1, x2-1, self.y1+2, 1, batch=self.batch, group = self.fg)
        self.l4.opacity = 10
        self.l5 = pyglet.shapes.Line(x2-1, self.y1+1, self.x1+1, self.y1+1, 1, batch=self.batch, group = self.fg)
        self.l5.opacity = 20
     
    def getHeight(self) :
        return self.height

    def getVerticalTextOffsetFromBottom(self) :
        return ShadowBorder.BORDER_SPACING+1

    def getWidth(self) :
        return self.width

    # sets bottom left
    def setPosition(self, pos) :
        self.x1 = pos[0]
        self.y1 = pos[1]
        self.drawLines()
        #self.border.position = pos

############################################
# A border around a layout with digits filled by a function that returns an integer
# maybe with a label above it
class ScoreboardElement :

    DIGIT_KERNING = 6
    VERTICAL_SPACING = -2
    FUDGE = 0 # not sure why needed

    def __init__(self, text=None, textFont='', textSize=44, textColor=None, 
                   updateFunc=None, digitFont='', digitSize=80, digitColor=None, 
                   maxDigits=2, displayLeadingZeroes=False, batch=None) :

        # border will go in the background group, all others foreground
        self.bg = pyglet.graphics.OrderedGroup(3)
        self.fg = pyglet.graphics.OrderedGroup(24)

        self.isOn = True
        self.updateFunc = updateFunc
        self.maxDigits = maxDigits
        self.label = None
        self.displayLeadingZeroes = displayLeadingZeroes
        self.height = 0
        self.width = 0

        if not(text is None) :
            self.label = pyglet.text.Label(text, font_name=textFont, font_size=textSize, color=textColor, batch=batch, group=self.fg)

        self.doc = self.createDocument(digitFont, digitSize, digitColor, maxDigits)
        self.layout = pyglet.text.layout.TextLayout(self.doc, batch=batch, group=self.fg)
        # store max Height and max Width in the document
        self.doc.set_style(0, len(self.doc.text), dict(maxWidth=self.layout.content_width, maxHeight = self.layout.content_height))

        width = self.layout.document.get_style('maxWidth', 0)
        height = self.doc.get_font(0).ascent # was self.layout.document.get_style('maxHeight', 0) 
        self.border = ShadowBorder( width, height, batch, self.bg, self.fg)

        self.computeHeight()
        self.update()

    # base class just creates a single document
    def createDocument(self, fontName, fontSize, fontColor, maxDigits) :
        text = ''
        for i in range(0, maxDigits) :
            text += '0'
        document = pyglet.text.document.UnformattedDocument(text)
        document.set_style(0, len(document.text), dict(font_name = fontName, 
                                                       font_size = fontSize, 
                                                       color=fontColor,
                                                       align='right',
                                                       kerning=ScoreboardElement.DIGIT_KERNING))
        return document

    def setOn(self, value) :
        self.isOn = value
        self.update()

   # base class assumes a single document
    def update(self) :
        self.doc.delete_text(0, len(self.doc.text))
        if self.isOn :
            value = str(self.updateFunc())

            missingDigits = self.maxDigits - len(value)
            if self.displayLeadingZeroes & missingDigits > 0 :
                for i in range(0, missingDigits) :
                    value = '0' + value
        else :
            value = ''

        self.doc.insert_text(0, value)

    def getCenter(self) :
        return self.center

    def getTop(self) :
        return self.top

    def setFontColor(self, fontColor) :
        self.doc.set_style(0, len(self.doc.text), dict(color=fontColor))

    def setLabelColor(self, fontColor) :
        self.label.color = fontColor

    def computeHeight(self) :
        self.height = self.border.getHeight()
        if not(self.label is None) :
            self.height += self.label.content_height 

   # base class assumes a single layout
    def setCenterTop(self, x, y) :
        self.top = y
        self.center = x
        if not (self.label is None) :
            self.label.anchor_x = 'center'
            self.label.anchor_y = 'top'
            self.label.position = (x, y)
            y = y - self.label.content_height - ScoreboardElement.VERTICAL_SPACING
        self.positionBorderAndLayoutFromBottomLeft(x - self.border.getWidth() // 2, y - self.border.getHeight())
        
    
   # base class assumes a single layout
   # right justify
    def setRightTop(self, x, y) :
        self.top = y
        self.center = x - self.border.getWidth() // 2
        if self.label != None :
            self.label.anchor_x = 'right'
            self.label.anchor_y = 'top'
            self.label.position = (x, y)
            y = y - self.label.content_height - ScoreboardElement.VERTICAL_SPACING
        self.positionBorderAndLayoutFromBottomLeft(x - self.border.getWidth(), y - self.border.getHeight())


   # base class assumes a single layout
    def setLeftTop(self, x, y) :
        self.top = y
        self.center = x + self.border.getWidth() // 2
        if self.label != None :
            self.label.anchor_x = 'left'
            self.label.anchor_y = 'top'
            self.label.position = (x, y)
            y = y - self.label.content_height - ScoreboardElement.VERTICAL_SPACING
        self.positionBorderAndLayoutFromBottomLeft(x, y - self.border.getHeight())


    def positionBorderAndLayoutFromBottomLeft(self, x, y) :
        self.border.setPosition((x, y))

        self.layout.anchor_x = 'right'
        self.layout.anchor_y = 'baseline'

        width = self.layout.document.get_style('maxWidth', 0)
        self.layout.position = ( x + self.border.getWidth() - (self.border.getWidth() - width) // 2,
                                     y  + self.border.getVerticalTextOffsetFromBottom() ) 
 
    def getHeight(self) :
        return self.height

    def getWidth(self) :
        return self.border.getWidth()

    def setVisible(self, value) :
        self.layout.visible = value
        

############################################
 
class HorizontalElement(ScoreboardElement) :

    SPACING = 10

    def __init__(self, text=None, textFont='', textSize=44, textColor=None, 
                   updateFunc=None, digitFont='', digitSize=80, digitColor=None, 
                   maxDigits=2, displayLeadingZeroes=False, batch=None) :

        ScoreboardElement.__init__(self, text=text, textFont=textFont, textSize=textSize, 
                                    textColor=textColor, updateFunc=updateFunc, digitFont=digitFont,
                                    digitSize=digitSize, digitColor=digitColor, maxDigits=maxDigits,
                                    displayLeadingZeroes=displayLeadingZeroes, batch=batch)

    def setCenterTop(self, x, y) :
        self.layout.anchor_x = 'left'
        self.layout.anchor_y = 'top'
        layoutWidth = self.layout.document.get_style('maxWidth', 0)
        totalWidth = layoutWidth
        if not(self.label is None) :
            self.label.anchor_x = 'left'
            self.label.anchor_y = 'top'
            totalWidth += HorizontalElement.SPACING + self.label.content_width
            x -= totalWidth // 2
            self.label.position = (x, y)
            x += HorizontalElement.SPACING + self.label.content_width
        else :
            x -= totalWidth // 2

        self.positionBorderAndLayoutFromBottomLeft(x, y - self.border.getHeight())   

        self.height = self.border.getHeight() if self.label.content_height > self.height else  self.label.content_height 

################################
# Creates two ScoreboardElements to fill via one function that gets seconds
# maxDigits only refers to minutes
# adds colon label between layouts

class ClockElement(ScoreboardElement) :

    SPACE_AROUND_COLON = -4
    
    def __init__(self, text=None, textFont='', textSize=44, textColor=None, 
                   updateFunc=None, digitFont='', digitSize=80, digitColor=None, 
                   maxDigits=2, displayLeadingZeroes=False, batch=None) :

        self.minutesElement = None
        self.secondsElement = None
        ScoreboardElement.__init__(self, text, textFont, textSize, textColor, updateFunc, digitFont, digitSize, digitColor, maxDigits, displayLeadingZeroes, batch=batch)
        self.setVisible(False)

        self.minutesElement = ScoreboardElement(None, textFont, textSize, textColor, self.getMinutes, digitFont, digitSize, digitColor, maxDigits, displayLeadingZeroes, batch)
        self.secondsElement = ScoreboardElement(None, textFont, textSize, textColor, self.getSeconds, digitFont, digitSize, digitColor, 2, True, batch)
        self.colon = pyglet.text.Label(':', font_name=digitFont, font_size=digitSize, color=textColor, batch=batch, group=self.fg)

    def getMinutes(self) :
        seconds = self.updateFunc()
        return seconds // 60

    def getSeconds(self) :
        seconds = self.updateFunc()
        return seconds % 60

    def update(self) :
        if not(self.minutesElement is None) :
            self.minutesElement.update()
            self.secondsElement.update()

    def setCenterTop(self, x, y) :
        if not (self.label is None) :
            self.label.anchor_x = 'center'
            self.label.anchor_y = 'top'
    
            self.label.position = (x, y)
            y = y - self.label.content_height - ScoreboardElement.VERTICAL_SPACING

        self.colon.anchor_x = 'left'
        self.colon.anchor_y = 'top'

        totalWidth = self.minutesElement.getWidth() + self.secondsElement.getWidth() + self.colon.content_width + ClockElement.SPACE_AROUND_COLON * 2
        colon_x = (x - totalWidth // 2) + self.minutesElement.getWidth() + ClockElement.SPACE_AROUND_COLON
        self.colon.position = (colon_x,  y)  

        self.minutesElement.setRightTop(colon_x - ClockElement.SPACE_AROUND_COLON, y)
        self.secondsElement.setLeftTop(colon_x + self.colon.content_width + ClockElement.SPACE_AROUND_COLON, y)

