
import pyglet
from pyglet import shapes
from pyglet import font 

class ShadowBorder() :

    BORDER_SPACING = (5, 8)
    BG_COLOR = (18,18,18)

    def __init__(self, width, height, batch, bg, fg) :
        self.batch = batch
        self.fg = fg
        self.bg = bg
        self.width = width + ShadowBorder.BORDER_SPACING[0] * 2
        self.height = height + ShadowBorder.BORDER_SPACING[1] * 2 + 3 # why 3? don't know

    def drawLines(self) :
        self.border = shapes.Rectangle(0, 0, self.width, self.height, color=ShadowBorder.BG_COLOR, batch=self.batch, group=self.bg  )
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

    def getWidth(self) :
        return self.width

    # sets bottom left
    def setPosition(self, pos) :
        self.x1 = pos[0]
        self.y1 = pos[1]
        self.drawLines()
        #self.border.position = pos


class ScoreboardElement :

    DIGIT_KERNING = 6
    VERTICAL_SPACING = 2

    def __init__(self, text=None, textFont='', textSize=44, textColor=None, 
                   updateFunc=None, digitFont='', digitSize=80, digitColor=None, 
                   maxDigits=2, displayLeadingZeroes=False, batch=None) :

        # border will go in the background group, all others foreground
        self.bg = pyglet.graphics.OrderedGroup(1)
        self.fg = pyglet.graphics.OrderedGroup(2)

        self.isOn = True
        self.updateFunc = updateFunc
        self.maxDigits = maxDigits
        self.label = None
        self.displayLeadingZeroes = displayLeadingZeroes
        self.height = 0
        self.width = 0

        if not(text is None) :
            self.label = pyglet.text.Label(text, font_name=textFont, 
                                        font_size=textSize, color=textColor, batch=batch, group=self.fg)

        self.docs = self.createDocuments(digitFont, digitSize, digitColor, maxDigits)

        self.layouts = []
        for d in self.docs :
            self.layouts.append(self.createLayout(d, batch, self.fg))

        self.borders = []
        for l in self.layouts :
            self.borders.append(ShadowBorder( l.width, l.height-(l.height//10), batch, self.bg, self.fg))        
        
        self.computeHeight()
        self.update()

    # base class just creates a single document
    def createDocuments(self, fontName, fontSize, fontColor, maxDigits) :
        docs = []
        document = pyglet.text.document.UnformattedDocument('0')
        document.set_style(0, len(document.text), dict(font_name = fontName, 
                                                       font_size = fontSize, 
                                                       color=fontColor,
                                                       align='right',
                                                       kerning=ScoreboardElement.DIGIT_KERNING,
                                                       maxDigits=maxDigits))
        docs.append(document)
        return docs

    def setOn(self, value) :
        self.isOn = value
        self.update()

    def createLayout(self, doc, batch, group) :
        # find  width of a character at this size            
        #                                              
            maxDigits = doc.get_style('maxDigits')
            charWidth = doc.get_font(0).get_glyphs('0')[0].advance
            self.numberWidth = self.numberWidth = charWidth*maxDigits + ScoreboardElement.DIGIT_KERNING*(maxDigits-1)
                
            self.numberHeight = self.docs[0].get_font(0).ascent #fudge
        
            layout = pyglet.text.layout.TextLayout(doc, width=self.numberWidth, height=self.numberHeight, 
                                                        batch=batch, multiline=True, group=group)
            return layout

    # base class assumes a single document
    def update(self) :
        self.docs[0].delete_text(0, len(self.docs[0].text))
        if self.isOn :
            value = str(self.updateFunc())

            missingDigits = self.maxDigits - len(value)
            if self.displayLeadingZeroes & missingDigits > 0 :
                for i in range(0, missingDigits) :
                    value = '0' + value
        else :
            value = ''

        self.docs[0].insert_text(0, value)

    def getCenter(self) :
        return self.center

    def getTop(self) :
        return self.top

    def setFontColor(self, fontColor) :
        for d in self.docs :
            d.set_style(0, len(d.text), dict(color=fontColor))

    def setLabelColor(self, fontColor) :
        self.label.color = fontColor

    def computeHeight(self) :
        self.height = self.borders[0].getHeight()
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
        
        self.layouts[0].anchor_x = 'center'
        self.layouts[0].anchor_y = 'top'
        self.layouts[0].position = (x, y)
 
        y = y - self.numberHeight - ShadowBorder.BORDER_SPACING[1]
        x = x - self.numberWidth // 2 - ShadowBorder.BORDER_SPACING[0]
        self.borders[0].setPosition((x, y))
    
   # base class assumes a single layout
    def setRightTop(self, x, y) :
        self.top = y
        if self.label != None :
            self.label.anchor_x = 'right'
            self.label.anchor_y = 'top'
    
            self.label.position = (x, y)
            y = y - self.label.content_height - ScoreboardElement.VERTICAL_SPACING
        
        self.layouts[0].anchor_x = 'right'
        self.layouts[0].anchor_y = 'top'
        self.layouts[0].position = (x, y)
        
        y = y - self.numberHeight - ShadowBorder.BORDER_SPACING[1]
        x = x - self.numberWidth  - ShadowBorder.BORDER_SPACING[0]
        self.borders[0].setPosition((x, y))


   # base class assumes a single layout
    def setLeftTop(self, x, y) :
        self.top = y
        if self.label != None :
            self.label.anchor_x = 'left'
            self.label.anchor_y = 'top'
    
            self.label.position = (x, y)
            y = y - self.label.content_height - ScoreboardElement.VERTICAL_SPACING
        
        self.layouts[0].anchor_x = 'left'
        self.layouts[0].anchor_y = 'top'
        self.layouts[0].position = (x, y)
        
        y = y - self.numberHeight - ShadowBorder.BORDER_SPACING[1]
        x = x  - ShadowBorder.BORDER_SPACING[0]
        self.borders[0].setPosition((x, y))

    def getHeight(self) :
        return self.height

    def getWidth(self) :
        return self.borders[0].getWidth()



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
        totalWidth = self.layouts[0].width 
        self.layouts[0].anchor_x = 'left'
        self.layouts[0].anchor_y = 'top'
        
 
        if not(self.label is None) :
            self.label.anchor_x = 'left'
            self.label.anchor_y = 'top'
            totalWidth = totalWidth + HorizontalElement.SPACING + self.label.content_width
            x = x - totalWidth // 2
            self.label.position = (x, y)
            x = x + HorizontalElement.SPACING + self.label.content_width
            self.layouts[0].position = (x,y)
        else :
            x = x - self.numberWidth // 2
            self.layouts[0].position = (x,y)
            
        y = y - self.numberHeight - ShadowBorder.BORDER_SPACING[1]
        x = x - ShadowBorder.BORDER_SPACING[0]
        self.borders[0].setPosition((x, y))

        self.height = self.borders[0].getHeight()
        if (self.label.content_height > self.height) :
            self.height = self.label.content_height 

################################
# Creates two layouts to fill via one function that gets seconds
# maxDigits only refers to minutes
# adds colon label between layouts

class ClockElement(ScoreboardElement) :

    SPACE_AROUND_COLON = -6
    
    def __init__(self, text=None, textFont='', textSize=44, textColor=None, 
                   updateFunc=None, digitFont='', digitSize=80, digitColor=None, 
                   maxDigits=2, displayLeadingZeroes=False, batch=None) :

        ScoreboardElement.__init__(self, text=text, textFont=textFont, textSize=textSize, 
                                    textColor=textColor, updateFunc=updateFunc, digitFont=digitFont,
                                    digitSize=digitSize, digitColor=digitColor, maxDigits=maxDigits,
                                    displayLeadingZeroes=displayLeadingZeroes, batch=batch)
        
        f = font.load(digitFont, digitSize)
       
        self.colon = pyglet.text.Label(':', font_name=digitFont, font_size=digitSize, color=textColor, batch=batch, group=self.fg)

 

    # uses update function to get total seconds, then inserts seconds and minutes into the 2 layouts
    def update(self) :

        totalSeconds = self.updateFunc()
        self.docs[0].delete_text(0, len(self.docs[0].text))
        self.docs[1].delete_text(0, len(self.docs[1].text))

        seconds = str(totalSeconds % 60)
        minutes = str(totalSeconds // 60)

        if  len(seconds) < 2 :
            seconds = '0' + seconds

        self.docs[0].insert_text(0, seconds)

        self.docs[1].insert_text(0, minutes)

    # override base class to create two documents, docs[0] for seconds and docs[1] for minutes
    def createDocuments(self, fontName, fontSize, fontColor, maxDigits) :
        docs = []
        secondsDoc = pyglet.text.document.UnformattedDocument('00')
        secondsDoc.set_style(0, len(secondsDoc.text), dict(font_name = fontName, 
                                                           font_size = fontSize, 
                                                           color=fontColor,
                                                           align='right',
                                                           kerning=ScoreboardElement.DIGIT_KERNING,
                                                           maxDigits=2))
        docs.append(secondsDoc)
        
        minutesDoc = pyglet.text.document.UnformattedDocument('0')
        minutesDoc.set_style(0, len(minutesDoc.text), dict(font_name = fontName, 
                                                           font_size = fontSize, 
                                                           color=fontColor,
                                                           align='right',
                                                           kerning=ScoreboardElement.DIGIT_KERNING,
                                                           maxDigits=maxDigits))
        docs.append(minutesDoc)
        return docs


    def setCenterTop(self, x, y) :
        self.top = y
        self.center = x

        colon_width = self.colon.content_width + ClockElement.SPACE_AROUND_COLON * 2
        totalWidth = colon_width 
        for l in self.layouts :
            totalWidth = totalWidth + l.width
 
        if not (self.label is None) :
            self.label.anchor_x = 'center'
            self.label.anchor_y = 'top'
    
            self.label.position = (x, y)
            y = y - self.label.content_height - ScoreboardElement.VERTICAL_SPACING

        x = x - totalWidth // 2
            
        # minutes
        self.layouts[1].anchor_x = 'left'
        self.layouts[1].anchor_y = 'top'
        self.layouts[1].position = (x, y)

        colon_x = x + self.layouts[1].width
        x = colon_x +ClockElement.SPACE_AROUND_COLON
        

        self.colon.anchor_x = 'left'
        self.colon.anchor_y = 'top'
        self.colon.position = (x,y)

        x = x + self.colon.content_width + ClockElement.SPACE_AROUND_COLON

        #seconds
        self.layouts[0].anchor_x = 'left'
        self.layouts[0].anchor_y = 'top'
        self.layouts[0].position = (x, y)


        y = y - self.numberHeight - ShadowBorder.BORDER_SPACING[1]
        self.borders[0].setPosition((colon_x + colon_width - ShadowBorder.BORDER_SPACING[0], y))
        self.borders[1].setPosition((colon_x - self.layouts[1].width - ShadowBorder.BORDER_SPACING[0], y))
