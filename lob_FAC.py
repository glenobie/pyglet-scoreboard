import pyglet
from die import Die
from dice_set import DiceSet 
from bordered_dice_set import BorderedDiceSet
from functools import partial

from fac_set import FACSet

class LegendsOfBoxingSet(FACSet) :

    def __init__(self, loader) :
        FACSet.__init__(self, loader)
        self.batch = pyglet.graphics.Batch()
        self.createDice()

    def createDice(self) :
        
        redD20 = Die(Die.D_RED, sides=20, text_color=Die.T_WHITE, batch=self.batch)
        redD20.setInteriorSpacingPct(0.2)
        self.redSet = BorderedDiceSet([redD20], batch=self.batch)
        self.redSet.setTitle('Control')
        self.redSet.setPosition(230, 380, 16)

        blueD20 = Die(Die.D_BLUE, sides=20, text_color=Die.T_WHITE, batch=self.batch)
        blueD20.setInteriorSpacingPct(0.2)
        self.blueSet = BorderedDiceSet([blueD20], batch=self.batch)
        self.blueSet.setTitle('Control')
        self.blueSet.setPosition(440, 380, 16)

        punch = Die(Die.D_DARK_GREEN, sides=100, text_color=Die.T_WHITE,batch=self.batch)
        punch.setInteriorSpacingPct(0.4)
        defense = Die(Die.D_GRAY, sides=6, text_color=Die.T_WHITE,batch=self.batch)
        defense.setInteriorSpacingPct(0.2)

        self.punchDice = BorderedDiceSet([punch, defense], batch=self.batch)
        self.punchDice.setTitle('Punch & Defense')
        self.punchDice.setPosition(160, 150, 16)

        d20 = Die(Die.D_AQUA, sides=20, text_color=Die.T_WHITE, batch=self.batch)
        d20.setInteriorSpacingPct(0.2)
        self.testDice = BorderedDiceSet([d20], 20, self.batch)
        self.testDice.setPosition(520, 150, 16)
        self.testDice.setTitle('Tests')

    def draw(self) :
        self.batch.draw()

    def handle_L(self) :
        self.redSet.roll()
        self.blueSet.roll()
        self.punchDice.roll()
        self.testDice.roll()

    def handle_K(self) :
        self.testDice.roll()