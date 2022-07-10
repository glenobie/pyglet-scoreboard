from attr import Factory
from scoreboard import Scoreboard
import pyglet
from fac_set import FACSet
from pyglet import font

class FACField() :
    F_BLUE = (0, 255, 255)
    F_YELLOW = (255,255,150)
    F_GRAY = (180,180,180)
    F_WHITE = (240,240,240)
    F_GREEN = (102, 255, 102)
    B_BLACK = (0,0,0)


    FONT_SIZE = 20
    FONT_COLOR = (0, 0, 0, 255)
    LINE_SPACING = 6


    def __init__(self, bgColor, width, height, text='', fillFunc=None, 
                                batch=None, fgGroup = None, bgGroup = None) :
        self.fillFunc = fillFunc


        self.border = pyglet.shapes.BorderedRectangle(0, 0, width, height, color = bgColor, border_color=FACField.B_BLACK,
                                                        batch = batch, group = bgGroup)
        self.doc = pyglet.text.document.UnformattedDocument(text)

        self.doc.set_style(0, len(self.doc.text), dict(color=FACField.FONT_COLOR, 
                                                       font_size=FACField.FONT_SIZE,
                                                       font_name=FACSet.TEXT_FONT,
                                                       align='center',
                                                       line_spacing=FACField.FONT_SIZE+FACField.LINE_SPACING))
        self.layout = pyglet.text.layout.TextLayout(self.doc, multiline=True, width=width, batch=batch, group=fgGroup)
        self.layout.anchor_x = 'left'
        self.layout.anchor_y = 'bottom'    
        #self.layout.content_valign = 'bottom'

    def setPosition(self, left, bottom) :
        self.border.position = (left, bottom)

        #center layout in border
        x = left #+ (self.border.width - self.layout.content_width) / 2
        y = bottom +  (self.border.height - self.layout.content_height + FACField.LINE_SPACING) // 2 
        self.layout.position = (x, y)

    def setText(self, text) :
        self.doc.text = text


class InsideSportsSet(FACSet) :

    FIELD_WIDTH = 128
    FIELD_HEIGHT = 61
    SPACE = 5
    
    TEXT_FIELD_COLOR = FACField.F_GRAY
 
    # (color, width, title, index into list of card fields)
    COLUMNS = [ ( (FACField.F_GRAY, 1, 'PEN'), (FACField.F_GRAY, 1, 'LOOSE PUCK'),
                  (FACField.F_GRAY, 1, 'REB'), (FACField.F_GRAY, 1, 'SHOTS'),
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
                ( None, None, (FACField.F_GRAY, 1, 'REB'), None, 
                 (FACField.F_WHITE, 1, 'FLIP'), (FACField.F_GRAY, 1, 'AST'), None),
                ( (FACField.F_GRAY, 1, 'MAJOR\nMINOR'), (FACField.F_GRAY, 1, 'DUMP INS'),
                  (FACField.F_WHITE, 1, 'FLIP'), None, (FACField.F_WHITE, 1, 'FLIP'), 
                  (FACField.F_GRAY, 1, 'BREAK AWAY'), (FACField.F_GRAY, 1, 'PASS TO')
                ) ]

    def __init__(self, loader) :
        FACSet.__init__(self, loader)
        self.fg = pyglet.graphics.OrderedGroup(62)
        self.FACbg = pyglet.graphics.OrderedGroup(5)

        # test
        self.index = 1

        self.paintBackground(FACSet.W_COLOR_WHITE)

        # test
        self.textFields = []
        self.valueFields = []
        x = InsideSportsSet.SPACE
        for col in InsideSportsSet.COLUMNS :
            y = InsideSportsSet.SPACE           
            for spot in col :
                if not(spot is None) :
                    f = FACField(spot[0], InsideSportsSet.FIELD_WIDTH * spot[1] + InsideSportsSet.SPACE * (spot[1] - 1), 
                                InsideSportsSet.FIELD_HEIGHT, spot[2], batch=self.batch, fgGroup=self.fg, 
                                bgGroup=self.FACbg)
                    f.setPosition(x, y)
                    if spot[0] == InsideSportsSet.TEXT_FIELD_COLOR :
                        self.textFields.append(f)
                    else :
                        self.valueFields.append(f)
                y += InsideSportsSet.FIELD_HEIGHT + InsideSportsSet.SPACE
            x += InsideSportsSet.FIELD_WIDTH + InsideSportsSet.SPACE




    def draw(self) :
        self.batch.draw()

    def flipFAC(self) :
        for f in self.valueFields :
            f.setText(str(self.index))
            self.index += 1

    def handle_L(self) :
        self.flipFAC()

    def handle_K(self) :
        0