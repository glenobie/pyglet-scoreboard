import pyglet

#########################################
class BorderedTextBox :
    BORDER_SPACING = 24
    LABEL_SPACING = 8

    def __init__(self, title='', width=100, height=100, batch=None) :
        self.batch = batch
        self.x = self.y = self.width = self.height = 0
        self.title = pyglet.text.Label(title, 'Arial', 22, batch=self.batch)
        self.title.anchor_x = 'left'
        self.title.anchor_y = 'center'
        self.width = width
        self.height = height



    # label to left of dice set
    def setTitle(self, title) :
        self.title.text =  title
        self.drawBorder(self.x, self.y, self.width, self.height)

    def setPosition(self, left, bottom) :
        self.x = left
        self.y = bottom
        self.drawBorder(self.x, self.y, self.width, self.height)
 
    def drawBorder(self, x, y, width, height) :
        self.lines = []
        self.lines.append(pyglet.shapes.Line(x, y, x, y + height, width=1, batch=self.batch))  
        self.lines.append(pyglet.shapes.Line(x+width, y, x+width, y + height, width=1, batch=self.batch))  
        self.lines.append(pyglet.shapes.Line(x, y, x+width, y, width=1, batch=self.batch))  
        
        if len(self.title.text) > 0 :
            title_x = x + (width - self.title.content_width) // 2
            self.title.position = (title_x, y+height)
            self.lines.append(pyglet.shapes.Line(x, y+height, title_x - BorderedTextBox.LABEL_SPACING, 
                                    y + height, width=1, batch=self.batch))       
            self.lines.append(pyglet.shapes.Line(title_x + self.title.content_width + BorderedTextBox.LABEL_SPACING, y+height, x+width, 
                                 y + height, width=1, batch=self.batch))       
        else :
            self.lines.append(pyglet.shapes.Line(x, y+height, x+width, y+height, width=1, batch=self.batch))       
           
         

    def valueChanged(self, value):
        super().valueChanged(value)
        self.drawBorder(self.x, self.y, self.width, self.height)

    # instead of boolean function labels
    def setLabel(self, text) :
        super().setLabel(text)
        self.drawBorder(self.x, self.y, self.width, self.height)
