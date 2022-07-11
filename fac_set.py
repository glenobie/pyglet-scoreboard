import pyglet

class FACSet() :

    W_COLOR_WHITE = (220,220,220)
    W_COLOR_BLACK = (30,30,30)

    TEXT_FONT = 'Roboto'

    def __init__(self, loader) :
        self.loader = loader
        self.batch = pyglet.graphics.Batch()
        self.bg = pyglet.graphics.OrderedGroup(0)

        self.paintBackground(FACSet.W_COLOR_BLACK)
        
    def paintBackground(self, color) :
        self.backdrop = pyglet.shapes.Rectangle(0,0,800,480,color=color, batch=self.batch, group=self.bg)


