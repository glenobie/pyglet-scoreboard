import pyglet

from fac_set import FACSet

#########################################
class BorderedTextBox :
    BORDER_SPACING = 24
    LABEL_SPACING = 8

    def __init__(self, title='', width=100, height=100, batch=None) :
        self.batch = batch
        self.width = width
        self.height = height
        # labels will fall below background without a group
        self.fg = pyglet.graphics.OrderedGroup(4)

        self.x = self.y = 0
        self.title = pyglet.text.Label(title, FACSet.TEXT_FONT, 20, batch=self.batch, group=self.fg)
        self.title.anchor_x = 'left'
        self.title.anchor_y = 'center'

        self.contents = pyglet.text.Label('', FACSet.TEXT_FONT, 22, batch=self.batch, group= self.fg)
        self.contents.anchor_x = 'center'
        self.contents.anchor_y = 'center'

    # label to left of dice set
    def setTitle(self, title) :
        self.title.text =  title
        self.drawBorder(self.x, self.y, self.width, self.height)

    def setText(self, text) :
        self.contents.text = text

    def setPosition(self, left, bottom) :
        self.x = left
        self.y = bottom
        self.contents.position = (self.x + self.width // 2, self.y + self.height // 2)

        self.drawBorder(self.x, self.y, self.width, self.height)
 
    def drawBorder(self, x, y, width, height) :
        self.lines = []
        self.lines.append(pyglet.shapes.Line(x, y, x, y + height, width=1, batch=self.batch, group=self.fg))  
        self.lines.append(pyglet.shapes.Line(x+width, y, x+width, y + height, width=1, batch=self.batch, group=self.fg))  
        self.lines.append(pyglet.shapes.Line(x, y, x+width, y, width=1, batch=self.batch, group=self.fg))  
        
        if len(self.title.text) > 0 :
            title_x = x + (width - self.title.content_width) // 2
            self.title.position = (title_x, y+height)
            self.lines.append(pyglet.shapes.Line(x, y+height, title_x - BorderedTextBox.LABEL_SPACING, 
                                    y + height, width=1, batch=self.batch, group=self.fg))       
            self.lines.append(pyglet.shapes.Line(title_x + self.title.content_width + BorderedTextBox.LABEL_SPACING, y+height, x+width, 
                                 y + height, width=1, batch=self.batch, group=self.fg))       
        else :
            self.lines.append(pyglet.shapes.Line(x, y+height, x+width, y+height, width=1, batch=self.batch, group=self.fg))       
           
         

    def valueChanged(self, value):
        super().valueChanged(value)
        self.drawBorder(self.x, self.y, self.width, self.height)

    # instead of boolean function labels
    def setLabel(self, text) :
        super().setLabel(text)
        self.drawBorder(self.x, self.y, self.width, self.height)
