
import pyglet
from pyglet import shapes
from pyglet import font 

class ScoreboardElement :

    DIGIT_KERNING = 6
    BORDER_SPACING = (4, 8)
    VERTICAL_SPACING = 10
    BG_COLOR = (10,10,20)

    def __init__(self, text=None, textFont='', textSize=44, textColor=None, 
                   updateFunc=None, digitFont='', digitSize=80, digitColor=None, 
                   maxDigits=2, displayLeadingZeroes=False, batch=None) :

        # border will go in the background group, all others foreground
        self.bg = pyglet.graphics.OrderedGroup(0)
        self.fg = pyglet.graphics.OrderedGroup(1)


        self.updateFunc = updateFunc
        self.maxDigits = maxDigits
        self.label = None
        self.displayLeadingZeroes = displayLeadingZeroes

        if not(text is None) :
            f = font.load(textFont, textSize)
            self.labelHeight = f.ascent
       
            self.label = pyglet.text.Label(text, font_name=textFont, 
                                        font_size=textSize, color=textColor, batch=batch, group=self.fg)

        self.docs = self.createDocuments(digitFont, digitSize, digitColor, maxDigits)

        self.layouts = []
        for d in self.docs :
            self.layouts.append(self.createLayout(d, batch, self.fg))

        self.borders = []
        for l in self.layouts :
            self.borders.append(self.createBorder( l.width, l.height-8, batch, self.bg))        
        
        self.update()

    def createBorder(self, width, height, batch, group) :
        border = shapes.BorderedRectangle(0, 0, width, height, 
                                               color=ScoreboardElement.BG_COLOR, 
                                               border_color=(255,255,255), border=1, 
                                               batch=batch, group=group)  
        border.width = border.width + ScoreboardElement.BORDER_SPACING[0] * 2
        border.height = border.height + ScoreboardElement.BORDER_SPACING[1] * 2
        return border


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

    
    def createLayout(self, doc, batch, group) :
        # find  width of a character at this size            
        #                                              
            maxDigits = doc.get_style('maxDigits')
            charWidth = doc.get_font(0).get_glyphs('0')[0].advance
            self.numberWidth = self.numberWidth = charWidth*maxDigits + ScoreboardElement.DIGIT_KERNING*(maxDigits-1)
                
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
            y = y - self.labelHeight - ScoreboardElement.VERTICAL_SPACING
        
        self.layouts[0].anchor_x = 'center'
        self.layouts[0].anchor_y = 'top'
        self.layouts[0].position = (x, y)
 
        y = y - self.numberHeight - ScoreboardElement.BORDER_SPACING[1]
        x = x - self.numberWidth // 2 - ScoreboardElement.BORDER_SPACING[0]
        self.borders[0].position = (x, y)

    
   # base class assumes a single layout
    def setRightTop(self, x, y) :
        self.top = y
        if self.label != None :
            self.label.anchor_x = 'right'
            self.label.anchor_y = 'top'
    
            self.label.position = (x, y)
            y = y - self.labelHeight - ScoreboardElement.VERTICAL_SPACING
        
        self.layouts[0].anchor_x = 'right'
        self.layouts[0].anchor_y = 'top'
        self.layouts[0].position = (x, y)
        
        y = y - self.numberHeight - ScoreboardElement.BORDER_SPACING[1]
        x = x - self.numberWidth  - ScoreboardElement.BORDER_SPACING[0]
        self.borders[0].position = (x, y)

   # base class assumes a single layout
    def setLeftTop(self, x, y) :
        self.top = y
        if self.label != None :
            self.label.anchor_x = 'left'
            self.label.anchor_y = 'top'
    
            self.label.position = (x, y)
            y = y - self.labelHeight - ScoreboardElement.VERTICAL_SPACING
        
        self.layouts[0].anchor_x = 'left'
        self.layouts[0].anchor_y = 'top'
        self.layouts[0].position = (x, y)
        
        y = y - self.numberHeight - ScoreboardElement.BORDER_SPACING[1]
        x = x  - ScoreboardElement.BORDER_SPACING[0]
        self.borders[0].position = (x, y)


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
        self.borders[0].position = (x, y)

################################
# Creates to fields to fill via one function that gets seconds
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
        self.labelHeight = f.ascent
       
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
            y = y - self.labelHeight - ScoreboardElement.VERTICAL_SPACING

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


        y = y - self.numberHeight - ScoreboardElement.BORDER_SPACING[1]
        self.borders[0].position = (colon_x + colon_width - ScoreboardElement.BORDER_SPACING[0], y)
        self.borders[1].position = (colon_x - self.layouts[1].width - ScoreboardElement.BORDER_SPACING[0], y)
