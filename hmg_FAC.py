
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

        self.white = Die(Die.D_WHITE, sides=6, batch=self.batch)
        dice.append(self.white)
        self.green = Die(Die.D_GREEN, sides=6, text_color=Die.T_WHITE,batch=self.batch)
        dice.append(self.green)
        self.black = Die(Die.D_BLACK, sides=6, text_color=Die.T_WHITE,batch=self.batch)
        dice.append(self.black)
        self.gray = Die(Die.D_ORANGE, sides=6, text_color=Die.T_WHITE,batch=self.batch)
        dice.append(self.gray)

        d = []
        self.decider = Die(Die.D_WHITE, text_color=Die.T_WHITE, sides=2, batch = self.batch)
        self.decider.setInteriorSpacingPct(0.2)
        self.decider.setDieLabels(('YES', 'NO'))
        self.decider.addColorCondition((1, Die.D_DARK_GREEN))
        self.decider.addColorCondition((2, Die.D_RED))
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
