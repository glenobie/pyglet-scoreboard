from attr import Factory
from scoreboard import Scoreboard
import pyglet
from fac_set import FACSet
from pyglet import font

class FACField() :
    F_LIGHT_BLUE = (0, 255, 255)
    F_YELLOW = (255,255,150)
    F_GRAY = (180,180,180)
    B_BLACK = (0,0,0)

    FONT_SIZE = 20
    FONT_COLOR = (0, 0, 0, 255)


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
                                                       line_spacing=FACField.FONT_SIZE+2))
        self.layout = pyglet.text.layout.TextLayout(self.doc, multiline=True, width=100, batch=batch, group=fgGroup)
        self.layout.anchor_x = 'left'
        self.layout.anchor_y = 'bottom'    
        #self.layout.content_valign = 'bottom'

    def setPosition(self, left, bottom) :
        self.border.position = (left, bottom)

        #center layout in border
        x = left #+ (self.border.width - self.layout.content_width) / 2
        y = bottom +  (self.border.height - self.layout.content_height + 2) // 2 
        self.layout.position = (x, y)

class InsideSportsSet(FACSet) :

    FIELD_WIDTH = 100
    FIELD_HEIGHT = 61
    SPACE = 5
    FONT = 'Showcard Gothic'
 
    LEFT = [(FACField.F_GRAY, 1, 'PEN'), (FACField.F_GRAY, 1, 'LOOSE\nPUCK'),
                 (FACField.F_GRAY, 1, 'REB'), (FACField.F_GRAY, 1, 'SHOTS'),
                 (FACField.F_LIGHT_BLUE, 3, ''), (FACField.F_LIGHT_BLUE, 3, ''),
                 (FACField.F_GRAY, 1, 'PASS\nTO')]

    def __init__(self, loader) :
        FACSet.__init__(self, loader)
        self.fg = pyglet.graphics.OrderedGroup(62)
        self.FACbg = pyglet.graphics.OrderedGroup(5)


        self.paintBackground(FACSet.W_COLOR_WHITE)

        # test
        self.fields = []
        y = InsideSportsSet.SPACE
        for spot in InsideSportsSet.LEFT :
            f = FACField(spot[0], InsideSportsSet.FIELD_WIDTH * spot[1], InsideSportsSet.FIELD_HEIGHT, 
                        spot[2], batch=self.batch, fgGroup=self.fg, bgGroup=self.FACbg)
            f.setPosition(InsideSportsSet.SPACE, y)
            y += InsideSportsSet.FIELD_HEIGHT + InsideSportsSet.SPACE
            self.fields.append(f)




    def draw(self) :
        self.batch.draw()

    def flipFAC(self) :
        0

    def handle_L(self) :
        self.flipFAC()

    def handle_K(self) :
        0