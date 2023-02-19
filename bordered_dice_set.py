
import pyglet
from dice_set import DiceSet

#########################################
class BorderedDiceSet(DiceSet) :
    LABEL_SPACING = 8

    def __init__(self, dice, spacing=24, batch=None) :
        DiceSet.__init__(self, dice, batch)
        self.titleLayout.anchor_x = 'left'
        self.x = self.y = self.width = self.height = 0
        self.borderSpacing = spacing
        self.borderColor = (255,255,255)

    # label to left of dice set
    def setTitle(self, title) :
        DiceSet.setTitle(self, title)
        self.drawBorder(self.x, self.y, self.width, self.height)

    def setPosition(self, left, center, spacing=12) :
        self.left = left
        self.center = center
        self.spacing = spacing

        self.x = left

        self.width = 0
        self.height = 0
        for d in self.dice :
            self.width += d.getWidth()
            if d.getWidth() > self.height :
                self.height = d.getWidth()
        self.width += 0 if len(self.dice) == 0 else (len(self.dice) - 1) * self.spacing
        self.width += self.borderSpacing * 2
        self.height += self.borderSpacing * 2

        x = left + self.borderSpacing
        for d in self.dice :
            x += d.getWidth() // 2
            d.setCenter(x, center)
            x += d.getWidth() // 2 + spacing

        self.y = center - self.height // 2
        self.drawBorder(self.x, self.y, self.width, self.height)

    def drawBorder(self, x, y, width, height) :
        self.lines = []
        self.lines.append(pyglet.shapes.Line(x, y, x, y + height, width=1, color=self.borderColor,batch=self.batch, group=self.fg))
        self.lines.append(pyglet.shapes.Line(x+width, y, x+width, y + height, width=1, color=self.borderColor,batch=self.batch, group=self.fg))

        if len(self.titleDoc.text) > 0 :
            title_x = x + (width - self.titleLayout.content_width) // 2
            title_y = y + height
            self.titleLayout.position = (title_x, title_y, 0)
            self.lines.append(pyglet.shapes.Line(x, y+height, title_x - BorderedDiceSet.LABEL_SPACING,
                                    y + height, width=1, color=self.borderColor,batch=self.batch, group=self.fg))
            self.lines.append(pyglet.shapes.Line(title_x + self.titleLayout.content_width + BorderedDiceSet.LABEL_SPACING, y+height, x+width,
                                 y + height, width=1, color=self.borderColor,batch=self.batch, group=self.fg))
        else :
            self.lines.append(pyglet.shapes.Line(x, y+height, x+width, y+height, width=1, color=self.borderColor,batch=self.batch, group=self.fg))


        if len(self.labelDoc.text) > 0 :
            label_x = x + (width - self.labelLayout.content_width) // 2
            self.labelLayout.position = (label_x, y, 0)
            self.lines.append(pyglet.shapes.Line(x, y, label_x - BorderedDiceSet.LABEL_SPACING,
                                    y, width=1, color=self.borderColor,batch=self.batch, group=self.fg))
            self.lines.append(pyglet.shapes.Line(label_x + self.labelLayout.content_width + BorderedDiceSet.LABEL_SPACING,
                                                   y, x+width, y, width=1, color=self.borderColor,batch=self.batch, group=self.fg))

        else :
            self.lines.append(pyglet.shapes.Line(x, y, x+width, y, width=1, color=self.borderColor,batch=self.batch, group=self.fg))

    def valueChanged(self, value):
        super().valueChanged(value)
        self.drawBorder(self.x, self.y, self.width, self.height)

    # alternative to boolean function labels
    def setLabel(self, text) :
        super().setLabel(text)
        self.drawBorder(self.x, self.y, self.width, self.height)

    def setBorderColor(self, color, opacity) :
        self.borderColor=color
        self.drawBorder(self.x, self.y, self.width, self.height)
        temp = list(color)
        temp.append(opacity)
        color= tuple(temp)
        self.titleDoc.set_style(0, len(self.titleDoc.text),  dict(color=color))
        self.labelDoc.set_style(0, len(self.labelDoc.text),  dict(color=color))
