
import pyglet
from die import Die
from dice_set import DiceSet, SortedDiceSet

class HistoryMakerGolfSet() :

    def __init__(self) :
        self.decisionNumber = 1
        self.batch = pyglet.graphics.Batch()
        self.createDice()

    def createDice(self) :
        dice = []

        self.white = Die((255,255,255), sides=6, batch=self.batch)
        dice.append(self.white)
        self.green = Die((40,200,40), sides=6, text_color=(255,255,255,255),batch=self.batch)
        dice.append(self.green)
        self.black = Die((0,0,0), sides=6, text_color=(255,255,255,255),batch=self.batch)
        dice.append(self.black)
        self.gray = Die((100,100,100), sides=6, text_color=(255,255,255,255),batch=self.batch)
        dice.append(self.gray)

        d = []
        self.decider = Die((255,255,255), sides=2, batch = self.batch)
        self.decider.setInteriorSpacingPct(0.2)
        self.decider.setDieLabels(('YES', 'NO'))
        self.decider.addColorCondition((1, (0,255,0)))
        self.decider.addColorCondition((2, (255,0,0)))
        d.append(self.decider)
        self.deciderSet = DiceSet(d, self.batch)
        self.deciderSet.setTitle('Decision #' + str(self.decisionNumber) + ':  ')
        self.deciderSet.setPosition(470,400, 20)

        for d in dice :
            d.scale(0.6)

        self.allDice = DiceSet(dice, self.batch)
        self.allDice.setPosition(480, 60, 16)

        d = []
        d.append(self.white.makeClone())
        self.controlSet = DiceSet(d, self.batch)
        self.controlSet.attachValueLabel((6, 'Go For It?'))
        self.controlSet.attachValueLabel((4, 'Extra Control?'))
        self.controlSet.setPosition(40, 400, 30)
    
        d = []
        d.append(self.gray.makeClone())
        d.append(self.black.makeClone())
        self.courseSet = SortedDiceSet(d, self.batch)
        self.courseSet.setPosition(40,280,30)

        d = []
        d.append(self.gray.makeClone())
        d.append(self.black.makeClone())
        d.append(self.green.makeClone())
        self.golferSet = SortedDiceSet(d, self.batch)
        self.golferSet.setPosition(40, 160, 30)


    def draw(self) :
        self.batch.draw()

    def handle_L(self) :
        self.allDice.roll()
        self.deciderSet.roll()
        self.decisionNumber = 1
        self.deciderSet.setTitle('Decision #' + str(self.decisionNumber) + ': ')

    def handle_K(self) :
        self.decisionNumber += 1
        self.deciderSet.roll()
        self.deciderSet.setTitle('Decision #' + str(self.decisionNumber)+ ':')
