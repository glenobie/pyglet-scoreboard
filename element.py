
import pyglet
from pyglet import shapes
from pyglet import font 

class ScoreboardElement :

    DIGIT_KERNING = 6
    BORDER_SPACING = (4, 8)
    BG_COLOR = (10,10,20)

    def __init__(self, text=None, textFont='', textSize=44, textColor=None, 
                   updateFunc=None, digitFont='', digitSize=80, digitColor=None, 
                   maxDigits=2, displayLeadingZeroes=False, batch=None) :

        bg = pyglet.graphics.OrderedGroup(0)
        fg = pyglet.graphics.OrderedGroup(1)

        self.updateFunc = updateFunc
        self.maxDigits = maxDigits
        self.label = None
        self.displayLeadingZeroes = displayLeadingZeroes

        if not(text is None) :
            f = font.load(textFont, textSize)
            self.labelHeight = f.ascent
       
            self.label = pyglet.text.Label(text, font_name=textFont, 
                                        font_size=textSize, color=textColor, batch=batch, group=fg)

        self.docs = self.createDocuments(digitFont, digitSize, digitColor)

        self.layouts = []
        for d in self.docs :
            self.layouts.append(self.createLayout(d, batch, fg))

        self.borders = []
        for l in self.layouts :
            self.borders.append(self.createBorder( l.width, l.height-8, batch, bg))        
        
        self.update()

    def createBorder(self, width, height, batch, group) :
        self.border = shapes.BorderedRectangle(0, 0, width, height, 
                                               color=ScoreboardElement.BG_COLOR, 
                                               border_color=(255,255,255), border=1, 
                                               batch=batch, group=group)  
        self.border.width = self.border.width + ScoreboardElement.BORDER_SPACING[0] * 2
        self.border.height = self.border.height + ScoreboardElement.BORDER_SPACING[1] * 2


    # base class just creates a single document
    def createDocuments(self, fontName, fontSize, fontColor) :
        docs = []
        document = pyglet.text.document.UnformattedDocument('0')
        document.set_style(0, len(document.text), dict(font_name = fontName, 
                                                                 font_size = fontSize, 
                                                                 color=fontColor,
                                                                 align='right',
                                                                 kerning=ScoreboardElement.DIGIT_KERNING))
        docs.append(document)
        return docs

    # base class just creates a single layout
    def createLayout(self, doc, batch, group) :
        # find  width of a character at this size                                                         
            charWidth = doc.get_font(0).get_glyphs('0')[0].advance
            self.numberWidth = self.numberWidth = charWidth*self.maxDigits + ScoreboardElement.DIGIT_KERNING*(self.maxDigits-1)
                
            self.numberHeight = self.docs[0].get_font(0).ascent 
        
            layout = pyglet.text.layout.TextLayout(doc, width=self.numberWidth, height=self.numberHeight, 
                                                        batch=batch, multiline=True, group=group)
            return layout

    # base class assumes a single document
    def update(self) :
        value = str(self.updateFunc())
        self.docs[0].delete_text(0, len(self.docs[0].text))

        missingDigits = self.maxDigits - len(value)
        if self.displayLeadingZeroes & missingDigits > 0 :
            for i in range(0, missingDigits) :
                value = '0' + value

        self.docs[0].insert_text(0, value)

    def getCenter(self) :
        return self.center

    def getTop(self) :
        return self.top


   # base class assumes a single layout
    def setCenterTop(self, x, y) :
        self.top = y
        self.center = x
        if not (self.label is None) :
            self.label.anchor_x = 'center'
            self.label.anchor_y = 'top'
    
            self.label.position = (x, y)
            y = y - self.labelHeight - 10 # TODO SPACING
        
        self.layouts[0].anchor_x = 'center'
        self.layouts[0].anchor_y = 'top'
        self.layouts[0].position = (x, y)
 
        
        y = y - self.numberHeight - ScoreboardElement.BORDER_SPACING[1]
        x = x - self.numberWidth // 2 - ScoreboardElement.BORDER_SPACING[0]
        self.border.position = (x, y)

    
   # base class assumes a single layout
    def setRightTop(self, x, y) :
        self.top = y
        if self.label != None :
            self.label.anchor_x = 'right'
            self.label.anchor_y = 'top'
    
            self.label.position = (x, y)
            y = y - self.labelHeight - 10 # TODO SPACING
        
        self.layouts[0].anchor_x = 'right'
        self.layouts[0].anchor_y = 'top'
        self.layouts[0].position = (x, y)
        
        y = y - self.numberHeight - ScoreboardElement.BORDER_SPACING[1]
        x = x - self.numberWidth  - ScoreboardElement.BORDER_SPACING[0]
        self.border.position = (x, y)

   # base class assumes a single layout
    def setLeftTop(self, x, y) :
        self.top = y
        if self.label != None :
            self.label.anchor_x = 'left'
            self.label.anchor_y = 'top'
    
            self.label.position = (x, y)
            y = y - self.labelHeight - 10 # TODO SPACING
        
        self.layouts[0].anchor_x = 'left'
        self.layouts[0].anchor_y = 'top'
        self.layouts[0].position = (x, y)
        
        y = y - self.numberHeight - ScoreboardElement.BORDER_SPACING[1]
        x = x  - ScoreboardElement.BORDER_SPACING[0]
        self.border.position = (x, y)


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
            
        y = y - self.numberHeight - ScoreboardElement.BORDER_SPACING[1]
        x = x - ScoreboardElement.BORDER_SPACING[0]
        self.border.position = (x, y)

################################
# Creates to fields to fill via one function that gets seconds
# maxDigits only refers to minutes
class ClockElement(ScoreboardElement) :
    
    def __init__(self, text=None, textFont='', textSize=44, textColor=None, 
                   updateFunc=None, digitFont='', digitSize=80, digitColor=None, 
                   maxDigits=2, displayLeadingZeroes=False, batch=None) :
        ScoreboardElement.__init__(self, text=text, textFont=textFont, textSize=textSize, 
                                    textColor=textColor, updateFunc=updateFunc, digitFont=digitFont,
                                    digitSize=digitSize, digitColor=digitColor, maxDigits=maxDigits,
                                    displayLeadingZeroes=displayLeadingZeroes, batch=batch)

    def update(self) :
        value = str(self.updateFunc())
        self.document.delete_text(0, len(self.document.text))

        missingDigits = self.maxDigits - len(value)
        if self.displayLeadingZeroes & missingDigits > 0 :
            for i in range(0, missingDigits) :
                value = '0' + value

        self.document.insert_text(0, value)
