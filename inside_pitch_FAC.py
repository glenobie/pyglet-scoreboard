
import pyglet
from die import Die
from dice_set import DiceSet, SortedDiceSet

class IP_DiceSet :
    SPACE = 8

    def __init__(self, label = '', batch=None) :
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

        self.label = pyglet.text.Label(label, 'Arial', 22, batch=self.batch)
        self.label.anchor_x = 'left'
        self.label.anchor_y = 'top'


    def setTopLeft(self, x, y) :
        self.red.setCenter(x + self.white.getWidth() + self.red.getWidth() // 2 + IP_DiceSet.SPACE, y - self.red.getWidth() // 2)
        self.white.setCenter(x + self.white.getWidth() // 2, y - self.red.getWidth() - self.white.getWidth() // 2 - IP_DiceSet.SPACE)
        y -= (self.red.getWidth() + self.d20.getWidth()//2 + IP_DiceSet.SPACE)
        self.d20.setCenter(x + self.white.getWidth() + self.d20.getWidth()//2 + IP_DiceSet.SPACE, y )
        width = IP_DiceSet.SPACE + self.white.getWidth() + self.d20.getWidth()
        self.label.position = (x + (width - self.label.content_width) // 2, y - self.d20.getWidth() // 2 - IP_DiceSet.SPACE)
    

    def roll(self) :
        self.red.roll()
        self.white.roll()
        self.d20.roll()
       

class InsidePitchSet() :

    def __init__(self) :
        self.decisionNumber = 1
        self.batch = pyglet.graphics.Batch()
        self.createDice()

    def createDice(self) :
        self.pitcher = IP_DiceSet(label= 'Pitcher', batch=self.batch)
        self.pitcher.setTopLeft(20, 460)

        self.hitter = IP_DiceSet(label= 'Hitter',batch=self.batch)
        self.hitter.setTopLeft(320, 460)

        self.ballpark = IP_DiceSet(label= 'Ballpark',batch=self.batch)
        self.ballpark.setTopLeft(620, 460)

        range = Die(Die.D_GREEN, Die.T_WHITE, 6, self.batch)
        range.scale(0.6)
        d = [range]
        self.rangeSet = DiceSet(d, self.batch)
        self.rangeSet.setTitle('Range: ')
        self.rangeSet.setPosition(46, 160, 10)

        b1 = Die(Die.D_GRAY, Die.T_WHITE, 6, self.batch)
        b2 = Die(Die.D_ORANGE, Die.T_WHITE, 6, self.batch)
        b3 = Die(Die.D_BROWN, Die.T_WHITE, 6, self.batch)
        d = [b1, b2, b3]
        for br in d :
            br.scale(0.6)


        self.baseRunningSet = DiceSet(d, self.batch)
        self.baseRunningSet.setTitle('Running: ')
        self.baseRunningSet.setPosition(20, 80, 10)



    def draw(self) :
        self.batch.draw()

    def handle_L(self) :
        self.pitcher.roll()
        self.hitter.roll()
        self.ballpark.roll()
        self.rangeSet.roll()
        self.baseRunningSet.roll()


    def handle_K(self) :
        0
