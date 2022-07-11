import random
import pyglet
from fac_set import FACSet

class FACField() :
    F_BLUE = (0, 255, 255)
    F_YELLOW = (255,255,150)
    F_GRAY = (180,180,180)
    F_WHITE = (240,240,240)
    F_GREEN = (102, 255, 102)
    B_BLACK = (0,0,0)


    FONT_SIZE = 18
    FONT_COLOR = (0, 0, 0, 255)
    LINE_SPACING = 8


    def __init__(self, font_size, bgColor, width, height, text='', bold=False, 
                              batch=None, fgGroup = None, bgGroup = None) :
        self.border = pyglet.shapes.BorderedRectangle(0, 0, width, height, color = bgColor, border_color=FACField.B_BLACK,
                                                        batch = batch, group = bgGroup)
        self.doc = pyglet.text.document.FormattedDocument(text)

        self.doc.set_style(0, len(self.doc.text), dict(color=FACField.FONT_COLOR, 
                                                       font_size=font_size,
                                                       font_name=FACSet.TEXT_FONT,
                                                       align='center',
                                                       bold=bold,
                                                       line_spacing=font_size+FACField.LINE_SPACING))
        self.layout = pyglet.text.layout.TextLayout(self.doc, multiline=True, width=width, batch=batch, group=fgGroup)
        self.layout.anchor_x = 'left'
        self.layout.anchor_y = 'bottom'    
        #self.layout.content_valign = 'bottom'

    def setPosition(self, left, bottom) :
        self.left = left
        self.bottom = bottom
        self.border.position = (left, bottom)

        #center layout in border
        x = left #+ (self.border.width - self.layout.content_width) / 2
        y = bottom +  (self.border.height - self.layout.content_height + FACField.LINE_SPACING) // 2 
        self.layout.position = (x, y)

    def setText(self, text) :
        # change <= and >=
        pos1 = text.find('>=')
        pos2 = text.find('<=')
        if pos1 > 0 :
            text = text.replace('>=', '>')
            self.doc.text = text
            self.doc.set_style(pos1, pos1+1, dict(baseline=1, underline=FACField.FONT_COLOR))
        elif pos2 > 0 :
            text = text.replace('<=', '<')
            self.doc.text = text
            self.doc.set_style(pos2, pos2+1, dict(baseline=1, underline=FACField.FONT_COLOR))
        else :
            self.doc.text = text
        self.setPosition(self.left, self.bottom)


class InsideSportsSet(FACSet) :

    FIELD_WIDTH = 130
    FIELD_HEIGHT = 61
    SPACE = 3
    
    TEXT_FIELD_COLOR = FACField.F_GRAY
 
    # (color, width, title, index into list of card fields)
    COLUMNS = [ ( (FACField.F_GRAY, 1, 'PENALTY'), (FACField.F_GRAY, 1, 'LOOSE\nPUCK'),
                  (FACField.F_GRAY, 1, 'REBOUND'), (FACField.F_GRAY, 1, 'SHOTS'),
                  (FACField.F_BLUE, 3, 'FLIP'), (FACField.F_BLUE, 3, 'FLIP'),
                  (FACField.F_GRAY, 1, 'PASS TO')), 
                ( (FACField.F_WHITE, 2, 'FLIP'), (FACField.F_WHITE, 2, 'FLIP'),
                  (FACField.F_YELLOW, 2, 'FLIP'), (FACField.F_GREEN, 2, 'FLIP'),
                  None, None, (FACField.F_BLUE, 1, 'FLIP')  ),
                ( None, None, None, None, None, None, (FACField.F_BLUE, 1, 'FLIP') ),
                ( (FACField.F_WHITE, 2, 'FLIP'), (FACField.F_WHITE, 2, 'FLIP'),
                    (FACField.F_YELLOW, 1, 'FLIP'), (FACField.F_GREEN, 3, 'FLIP'),
                    (FACField.F_WHITE, 1, 'FLIP'), (FACField.F_GRAY, 1, 'FO'),
                    (FACField.F_BLUE, 2, 'FLIP')),
                ( None, None, (FACField.F_GRAY, 1, 'SHOOTOUT'), None, 
                 (FACField.F_WHITE, 1, 'FLIP'), (FACField.F_GRAY, 1, 'ASSIST'), None),
                ( (FACField.F_GRAY, 1, 'MAJOR\nMINOR'), (FACField.F_GRAY, 1, 'DUMP INS'),
                  (FACField.F_WHITE, 1, 'FLIP'), None, (FACField.F_WHITE, 1, 'FLIP'), 
                  (FACField.F_GRAY, 1, 'BREAKAWAY'), (FACField.F_GRAY, 1, 'PASS TO')
                ) ]

    def __init__(self, loader) :
        FACSet.__init__(self, loader)
        self.paintBackground(FACSet.W_COLOR_WHITE)
        self.fg = pyglet.graphics.OrderedGroup(62)
        self.FACbg = pyglet.graphics.OrderedGroup(5)

        self.deckIndex = 0
        self.facs = self.readFACSFromFile('crease_FACs', 6)
        random.shuffle(self.facs)

        self.createLayout()


    def createLayout(self)  :    
        self.textFields = []
        self.valueFields = []
        x = InsideSportsSet.SPACE
        for col in InsideSportsSet.COLUMNS :
            y = InsideSportsSet.SPACE           
            for spot in col :
                if not(spot is None) :
                    if spot[0] == InsideSportsSet.TEXT_FIELD_COLOR :

                        f = FACField(16, spot[0], InsideSportsSet.FIELD_WIDTH * spot[1] + InsideSportsSet.SPACE * (spot[1] - 1), 
                                    InsideSportsSet.FIELD_HEIGHT, spot[2], batch=self.batch, fgGroup=self.fg, 
                                    bgGroup=self.FACbg, bold=True)
                        
                        self.textFields.append(f)
                    else :
                        f = FACField(16, spot[0], InsideSportsSet.FIELD_WIDTH * spot[1] + InsideSportsSet.SPACE * (spot[1] - 1), 
                                    InsideSportsSet.FIELD_HEIGHT, spot[2], batch=self.batch, fgGroup=self.fg, 
                                    bgGroup=self.FACbg)
                        self.valueFields.append(f)
                    f.setPosition(x, y)
        
                y += InsideSportsSet.FIELD_HEIGHT + InsideSportsSet.SPACE
            x += InsideSportsSet.FIELD_WIDTH + InsideSportsSet.SPACE

    def readFACSFromFile(self, filename, numFACS) :
        facs = []
        f = self.loader.file(filename, mode='r')
        for j in range(0, numFACS) :
            list = f.readline().split(';')
            strings = []
            for s in list :
                strings.append(s.replace('\n', '').replace('$', '\n'))
            facs.append(strings)
        return facs

    def draw(self) :
        self.batch.draw()

    def flipForward(self) :
        self.deckIndex += 1
        if self.deckIndex >= len(self.facs) :
            random.shuffle(self.facs)
            self.deckIndex = 0

        for fieldIndex in range(8, 17) :
            self.valueFields[fieldIndex].setText(self.facs[self.deckIndex][fieldIndex].strip('\n'))
        for fieldIndex in range(0, 8) :
            self.valueFields[fieldIndex].setText(self.facs[self.deckIndex-1][fieldIndex].strip('\n'))
   
    def handle_L(self) :
        self.flipForward()

    def handle_K(self) :
        0