
import pyglet
from die import Die
from dice_set import DiceSet, SortedDiceSet

class IP_DiceSet :
    SPACE = 8

    def __init__(self, batch) :
        self.dice = []
        self.batch = batch
        
        self.red = Die((200,0, 25), text_color=(255,255,255,255), sides=6, batch=self.batch)
        self.red.scale(0.8)
        self.dice.append(self.red)
        self.white = Die((255,255,255), sides=6, batch=self.batch)
        self.white.scale(0.8)
        self.dice.append(self.white)
        self.d20 = Die((40, 0, 220), text_color = (255,255,255,255), sides=20, batch=self.batch)
        self.d20.setInteriorSpacingPct(0.4)
        self.d20.scale(0.8)
        self.dice.append(self.d20)


    def setTopLeft(self, x, y) :
        self.red.setCenter(x + self.white.getWidth() + self.red.getWidth() // 2 + IP_DiceSet.SPACE, y - self.red.getWidth() // 2)
        self.white.setCenter(x + self.white.getWidth() // 2, y - self.red.getWidth() - self.white.getWidth() // 2 - IP_DiceSet.SPACE)
        self.d20.setCenter(x + self.white.getWidth() + self.d20.getWidth()//2 + IP_DiceSet.SPACE, y - self.red.getWidth() - self.d20.getWidth()//2 - IP_DiceSet.SPACE)

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
        self.pitcher = IP_DiceSet(self.batch)
        self.pitcher.setTopLeft(20, 460)

        self.hitter = IP_DiceSet(self.batch)
        self.hitter.setTopLeft(320, 460)

        self.ballpark = IP_DiceSet(self.batch)
        self.ballpark.setTopLeft(620, 460)


    def draw(self) :
        self.batch.draw()

    def handle_L(self) :
        self.pitcher.roll()
        self.hitter.roll()
        self.ballpark.roll()


    def handle_K(self) :
        self.decisionNumber += 1
