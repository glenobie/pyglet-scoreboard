import pyglet

class FACSet() :

    OFFSET_FROM_BOTTOM = 200

    W_COLOR_WHITE = (220,220,220)
    W_COLOR_BLACK = (30,30,30)

    TEXT_FONT = 'Roboto'
    DINGBAT_FONT = 'Fire'

    def __init__(self, loader=None) :
        self.loader = loader
        self.batch = pyglet.graphics.Batch()
        self.bg = pyglet.graphics.OrderedGroup(0)
        self.fg = pyglet.graphics.OrderedGroup(1)

        #self.paintBackground(FACSet.W_COLOR_BLACK)

        
    def paintBackground(self, color) :
        self.backdrop = pyglet.shapes.Rectangle(0, 0, 800, 480+ FACSet.OFFSET_FROM_BOTTOM, color=color, batch=self.batch, group=self.bg)

    def draw(self) :        
        self.batch.draw()
        
    def getBatch(self) :
        return self.batch

    def handle_J(self) :
        0

    def handle_K(self) :
        0

    def handle_L(self) :
        0


class ChoiceFAC(FACSet) :
    def __init__(self, loader=None) :
        FACSet.__init__(self, loader)
        self.msgDoc = pyglet.text.document.UnformattedDocument('')
        self.msgDoc.set_style(0,len(self.msgDoc.text), dict(color=(255,255,255,255), font_name=FACSet.TEXT_FONT,  font_size = 28 ))
        self.msgLayout = pyglet.text.layout.TextLayout(self.msgDoc, batch=self.batch, group = self.fg)
        self.msgLayout.anchor_x = 'center'
        self.msgLayout.position = (400, 600)


