import pyglet
from die import Die
from bordered_dice_set import BorderedDiceSet
from fac_set import FACSet

class IP_DiceSet :
    BORDER_SPACING = 24
    LABEL_SPACING = 8
    SPACE = 8

    def __init__(self, title = '', label = '', batch=None) :
        self.dice = []
        self.batch = batch
        self.fg = pyglet.graphics.OrderedGroup(4)
        
        self.red = Die(Die.D_RED, text_color=Die.T_WHITE, sides=6, batch=self.batch)
        self.red.scale(0.8)
        self.dice.append(self.red)
        self.white = Die(Die.D_WHITE, sides=6, batch=self.batch)
        self.white.scale(0.8)
        self.dice.append(self.white)
        self.d20 = Die(Die.D_BLUE, text_color=Die.T_WHITE, sides=20, batch=self.batch)
        self.d20.setInteriorSpacingPct(0.2)
        self.d20.scale(0.8)
        self.dice.append(self.d20)

        self.title = pyglet.text.Label(title, FACSet.TEXT_FONT, 22, batch=self.batch, group=self.fg)
        self.title.anchor_x = 'left'
        self.title.anchor_y = 'center'

        self.label = pyglet.text.Label(label, FACSet.TEXT_FONT, 18, batch=self.batch, group=self.fg)
        self.label.anchor_x = 'left'
        self.label.anchor_y = 'center'


    def setTopLeft(self, x, y) :
        dice_x = x + IP_DiceSet.BORDER_SPACING
        self.red.setCenter(dice_x + self.white.getWidth() + self.red.getWidth() // 2 + IP_DiceSet.SPACE, 
                           y - IP_DiceSet.BORDER_SPACING - self.red.getWidth() // 2)

        y2 = y - (self.red.getWidth() + self.d20.getWidth()//2 + IP_DiceSet.SPACE + IP_DiceSet.BORDER_SPACING)

        self.white.setCenter(dice_x + self.white.getWidth() // 2, y2)
        self.d20.setCenter(dice_x + self.white.getWidth() + self.d20.getWidth()//2 + IP_DiceSet.SPACE, y2 )
        
        width = IP_DiceSet.SPACE + self.white.getWidth() + self.d20.getWidth() + IP_DiceSet.BORDER_SPACING*2
        
        self.drawBorder(x, y - width, width, width)

    def roll(self) :
        self.red.roll()
        self.white.roll()
        self.d20.roll()

    def drawBorder(self, x, y, width, height) :
        self.lines = []
        self.lines.append(pyglet.shapes.Line(x, y, x, y + height, width=1, batch=self.batch, group=self.fg))  
        self.lines.append(pyglet.shapes.Line(x+width, y, x+width, y + height, width=1, batch=self.batch, group=self.fg))  
        #self.lines.append(pyglet.shapes.Line(x, y, x+width, y, width=1, batch=self.batch, group=self.fg))  
 
        if len(self.title.text) > 0 :
            title_x = x + (width - self.title.content_width) // 2
            title_y = y + height 
            self.title.position = (title_x, title_y)
            self.lines.append(pyglet.shapes.Line(x, y+height, title_x - IP_DiceSet.LABEL_SPACING, 
                                                 y + height, width=1, batch=self.batch, group=self.fg))       
            self.lines.append(pyglet.shapes.Line(title_x + self.title.content_width + IP_DiceSet.LABEL_SPACING, y+height, x+width, 
                                                 y + height, width=1, batch=self.batch, group=self.fg))       
        else :
            self.lines.append(pyglet.shapes.Line(x, y+height, x+width, y+height, width=1, batch=self.batch, group=self.fg))      

        if len(self.label.text) > 0 :
            label_x = x + (width - self.label.content_width) // 2
            self.label.position = (label_x, y)
            self.lines.append(pyglet.shapes.Line(x, y, label_x - BorderedDiceSet.LABEL_SPACING, 
                                    y, width=1, batch=self.batch, group=self.fg))       
            self.lines.append(pyglet.shapes.Line(label_x + self.label.content_width + BorderedDiceSet.LABEL_SPACING, 
                                                   y, x+width, y, width=1, batch=self.batch, group=self.fg))       
             
        else :
            self.lines.append(pyglet.shapes.Line(x, y, x+width, y, width=1, batch=self.batch, group=self.fg))       
 
           


class InsidePitchSet(FACSet) :

    def __init__(self, loader) :
        FACSet.__init__(self, loader)
        self.decisionNumber = 1
        self.createDice()

    def createDice(self) :
        self.pitcher = IP_DiceSet(title= 'Pitcher', label='WP/HR?/??', batch=self.batch)
        self.pitcher.setTopLeft(36, 454)

        self.hitter = IP_DiceSet(title= 'Hitter', label='HBP/K/W/HR', batch=self.batch)
        self.hitter.setTopLeft(286, 454)

        self.ballpark = IP_DiceSet(title= 'Ballpark', label='H?/E/Strategy', batch=self.batch)
        self.ballpark.setTopLeft(540, 454)


        starLine = Die(Die.D_AQUA, Die.T_WHITE, 6, self.batch)
        starLine.scale(0.8)
        self.starSet = BorderedDiceSet([starLine], batch=self.batch)
        self.starSet.setTitle('**')
        self.starSet.setPosition(28, 100, 10)


        range = Die(Die.D_GREEN, Die.T_WHITE, 6, self.batch)
        range.scale(0.8)
        self.rangeSet = BorderedDiceSet([range], batch=self.batch)
        self.rangeSet.setTitle('Range')
        self.rangeSet.setPosition(172, 100, 10)


        field = Die(Die.D_DARK_GREEN, Die.T_WHITE, 6, self.batch)
        field.scale(0.8)
        self.fieldSet = BorderedDiceSet([field], batch=self.batch)
        self.fieldSet.setTitle('DP/SF')
        self.fieldSet.setPosition(316, 100, 10)

        b1 = Die(Die.D_GOLD, Die.T_BLACK, 6, self.batch)
        b2 = Die(Die.D_ORANGE, Die.T_WHITE, 6, self.batch)
        b3 = Die(Die.D_BROWN, Die.T_WHITE, 6, self.batch)
        d = [b1, b2, b3]
        for br in d :
            br.scale(0.8)


        self.baseRunningSet = BorderedDiceSet(d, batch= self.batch)
        self.baseRunningSet.setTitle('Running')
        self.baseRunningSet.setPosition(460, 100, 10)



    def draw(self) :
        self.batch.draw()

    def handle_L(self) :
        self.pitcher.roll()
        self.hitter.roll()
        self.ballpark.roll()
        self.rangeSet.roll()
        self.fieldSet.roll()
        self.starSet.roll()
        self.baseRunningSet.roll()


    def handle_K(self) :
        0
