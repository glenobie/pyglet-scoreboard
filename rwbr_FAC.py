import pyglet
from die import Die
from dice_set import DiceSet 
from bordered_dice_set import BorderedDiceSet
from functools import partial

from fac_set import FACSet

class RWBRSet(FACSet) :

    def __init__(self, loader) :
        FACSet.__init__(self, loader)
        self.challengeNumber = 1
        self.batch = pyglet.graphics.Batch()
        self.createDice()

    def createDice(self) :
        
        self.group = Die(Die.D_ORANGE, sides=6, text_color=Die.T_WHITE, batch=self.batch)
        self.groupSet = BorderedDiceSet([self.group], batch=self.batch)

        self.groupSet.attachBooleanFunctionLabel((partial(self.groupSet.totalEquals, 1), 'TOP'))
        self.groupSet.attachBooleanFunctionLabel((partial(self.groupSet.totalEquals, 2), 'TOP'))
        self.groupSet.attachBooleanFunctionLabel((partial(self.groupSet.totalEquals, 3), 'MIDDLE'))
        self.groupSet.attachBooleanFunctionLabel((partial(self.groupSet.totalEquals, 4), 'MIDDLE'))
        self.groupSet.attachBooleanFunctionLabel((partial(self.groupSet.totalEquals, 5), 'BOTTOM'))
        self.groupSet.attachBooleanFunctionLabel((partial(self.groupSet.totalEquals, 6), 'DUEL!'))
        self.groupSet.setTitle('Group')
        self.groupSet.setPosition(140, 380, 16)

        self.black = Die(Die.D_BLACK, sides=6, text_color=Die.T_WHITE,batch=self.batch)
        self.gray = Die(Die.D_GRAY, sides=6, text_color=Die.T_WHITE,batch=self.batch)

        self.courseDice = BorderedDiceSet([self.gray, self.black], batch=self.batch)
        self.courseDice.setTitle('Track')
        self.courseDice.setPosition(440, 380, 16)

        self.red = Die(Die.D_RED, text_color=Die.T_WHITE, sides=6, batch=self.batch)
        self.white = Die(Die.D_WHITE, sides=6, batch=self.batch)
        self.blue = Die(Die.D_BLUE, sides=6, text_color=Die.T_WHITE, batch=self.batch)
        self.challenge = [self.red, self.white, self.blue]

        self.challengeDice = BorderedDiceSet(self.challenge, batch=self.batch)
        self.challengeDice.attachBooleanFunctionLabel((self.challengeDice.allEqual, 'PROBLEM!'))
        self.challengeDice.setTitle('Challenge #' + str(self.challengeNumber) )
        self.challengeDice.setPosition(200, 140, 16)


    def draw(self) :
        self.batch.draw()

    def handle_L(self) :
        self.groupSet.roll()
        self.challengeDice.roll()
        self.courseDice.roll()
        self.challengeNumber = 1
        self.challengeDice.setTitle('Challenge #' + str(self.challengeNumber))

    def handle_K(self) :
        self.challengeDice.roll()
        self.challengeNumber += 1
        self.challengeDice.setTitle('Challenge #' + str(self.challengeNumber) )
