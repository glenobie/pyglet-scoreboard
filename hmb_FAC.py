
import pyglet
from die import Die
from dice_set import DiceSet, BorderedDiceSet, SortedDiceSet
from fac_set import FACSet

class HistoryMakerBaseballSet(FACSet) :

    def __init__(self, loader) :
        FACSet.__init__(self, loader)
        self.decisionNumber = 1
        self.batch = pyglet.graphics.Batch()
        self.createDice()

    def createDice(self) :
        self.red = Die(Die.D_RED, text_color = Die.T_WHITE, sides=6, batch=self.batch)
        self.blue = Die(Die.D_BLUE, sides=6, text_color=Die.T_WHITE,batch=self.batch)
        self.black = Die(Die.D_BLACK, sides=6, text_color=Die.T_WHITE,batch=self.batch)
        dice = [self.red, self.blue, self.black]
        for d in dice :
            d.scale(0.6)

        self.allDice = DiceSet(dice, self.batch)
        self.allDice.setPosition(570, 60, 12)

        self.decider = Die(Die.D_WHITE, text_color=Die.T_WHITE, sides=2, batch = self.batch)
        self.decider.setInteriorSpacingPct(0.2)
        self.decider.setDieLabels(('YES', 'NO'))
        self.decider.addColorCondition((1, Die.D_DARK_GREEN))
        self.decider.addColorCondition((2, Die.D_RED))

        self.deciderSet = BorderedDiceSet([self.decider], self.batch)
        self.deciderSet.setTitle('Decider')
        self.deciderSet.setPosition(570, 360, 20)
        self.deciderSet.setLabel('Roll #' + str(self.decisionNumber))


        d1 = [self.red.makeClone()]
        self.oneSet = DiceSet(d1, self.batch)
        self.oneSet.setPosition(40, 400, 20)
    
        d2 = [self.black.makeClone(), self.blue.makeClone()]
        self.twoSet = SortedDiceSet(d2, self.batch)
        self.twoSet.setPosition(40,280,20)

        d3 = [self.red.makeClone(), self.blue.makeClone(), self.black.makeClone()]
        self.threeSet = SortedDiceSet(d3, self.batch)
        self.threeSet.attachBooleanFunctionLabel((self.isRarePlayRoll, 'RARE PLAY!'))
        self.threeSet.setPosition(40, 160, 20)


    def isRarePlayRoll(self) :
        if self.threeSet.anyDieEquals(1) and self.threeSet.anyDieEquals(3) and self.threeSet.anyDieEquals(5) :
            return True
        return False
        

    def draw(self) :
        self.batch.draw()

    def handle_L(self) :
        self.allDice.roll()
        self.deciderSet.roll()
        self.decisionNumber = 1
        self.deciderSet.setLabel('Roll #' + str(self.decisionNumber))

    def handle_K(self) :
        self.decisionNumber += 1
        self.deciderSet.roll()
        self.deciderSet.setLabel('Roll #' + str(self.decisionNumber))
