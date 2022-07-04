import pyglet
from die import Die
from bordered_dice_set import BorderedDiceSet
from fac_set import FACSet

class IP_DiceSet :
    BORDER_SPACING = 24
    LABEL_SPACING = 8
    SPACE = 8

    def __init__(self, title = '', batch=None) :
        self.dice = []
        self.batch = batch
        
        self.red = Die(Die.D_RED, text_color=Die.T_WHITE, sides=6, batch=self.batch)
        self.red.scale(0.8)
        self.dice.append(self.red)
        self.white = Die(Die.D_WHITE, sides=6, batch=self.batch)
        self.white.scale(0.8)
        self.dice.append(self.white)
        self.d20 = Die(Die.D_BLUE, text_color=Die.T_WHITE, sides=20, batch=self.batch)
        self.d20.setInteriorSpacingPct(0.4)
        self.d20.scale(0.8)
        self.dice.append(self.d20)

        self.title = pyglet.text.Label(title, 'Arial', 22, batch=self.batch)
        self.title.anchor_x = 'left'
        self.title.anchor_y = 'center'


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
        self.lines.append(pyglet.shapes.Line(x, y, x, y + height, width=1, batch=self.batch))  
        self.lines.append(pyglet.shapes.Line(x+width, y, x+width, y + height, width=1, batch=self.batch))  
        self.lines.append(pyglet.shapes.Line(x, y, x+width, y, width=1, batch=self.batch))  
 
        if len(self.title.text) > 0 :
            title_x = x + (width - self.title.content_width) // 2
            title_y = y + height 
            self.title.position = (title_x, title_y)
            self.lines.append(pyglet.shapes.Line(x, y+height, title_x - IP_DiceSet.LABEL_SPACING, 
                                                 y + height, width=1, batch=self.batch))       
            self.lines.append(pyglet.shapes.Line(title_x + self.title.content_width + IP_DiceSet.LABEL_SPACING, y+height, x+width, 
                                                 y + height, width=1, batch=self.batch))       
        else :
            self.lines.append(pyglet.shapes.Line(x, y+height, x+width, y+height, width=1, batch=self.batch))       
           


class InsidePitchSet(FACSet) :

    def __init__(self, loader) :
        FACSet.__init__(self, loader)
        self.decisionNumber = 1
        self.batch = pyglet.graphics.Batch()
        self.createDice()

    def createDice(self) :
        self.pitcher = IP_DiceSet(title= 'Pitcher', batch=self.batch)
        self.pitcher.setTopLeft(36, 460)

        self.hitter = IP_DiceSet(title= 'Hitter',batch=self.batch)
        self.hitter.setTopLeft(286, 460)

        self.ballpark = IP_DiceSet(title= 'Ballpark',batch=self.batch)
        self.ballpark.setTopLeft(540, 460)


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

        b1 = Die(Die.D_GRAY, Die.T_WHITE, 6, self.batch)
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
