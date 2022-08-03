import pyglet

class FACSet() :

    W_COLOR_WHITE = (220,220,220)
    W_COLOR_BLACK = (30,30,30)

    TEXT_FONT = 'Roboto'
    DINGBAT_FONT = 'Fire'

    def __init__(self, loader=None) :
        self.loader = loader
        self.batch = pyglet.graphics.Batch()
        self.bg = pyglet.graphics.OrderedGroup(0)

        self.paintBackground(FACSet.W_COLOR_BLACK)

        self.msgDoc = pyglet.text.document.UnformattedDocument('Choose a game')
        self.msgDoc.set_style(0,len(self.msgDoc.text), dict(color=(255,255,255,255), font_name=FACSet.TEXT_FONT,  font_size = 28 ))
        self.msgLayout = pyglet.text.layout.TextLayout(self.msgDoc)
        self.msgLayout.anchor_x = 'center'
        self.msgLayout.position = (400, 300)
        
    def paintBackground(self, color) :
        self.backdrop = pyglet.shapes.Rectangle(0, 0, 800, 480, color=color, batch=self.batch, group=self.bg)

    def draw(self) :
        self.msgLayout.draw()

    def handle_L(self) :
        0

    def handle_K(self):
        0




