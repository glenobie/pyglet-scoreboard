import pyglet
from die import Die
from dice_set import DiceSet 
from bordered_dice_set import BorderedDiceSet
from functools import partial

from fac_set import FACSet
class APBASoccerSet(FACSet) :

    def __init__(self, loader) :
        FACSet.__init__(self, loader)
        self.createDice()

    def createDice(self) :
        
        time1 = Die(Die.D_RED, sides=10, text_color=Die.T_WHITE, batch=self.batch, startAtZero=True)
        time1.setInteriorSpacingPct(0.2)
        time2 = Die(Die.D_BLUE, sides=10, text_color=Die.T_WHITE, batch=self.batch, startAtZero=True)
        time2.setInteriorSpacingPct(0.2)
        self.timeSet = BorderedDiceSet([time1, time2], batch=self.batch)
        self.timeSet.attachBooleanFunctionLabel((partial(self.timeSet.allEqual), "Double Time"))
        self.timeSet.attachBooleanFunctionLabel((partial(self.timeSet.notAllEqual),  partial(self.timeSet.totalAsString)))
        self.timeSet.setTitle('Time')
        self.timeSet.setPosition(130, 380, 16)

        activity = Die(Die.D_AQUA, sides=20, text_color=Die.T_WHITE, batch=self.batch)
        activity.setInteriorSpacingPct(0.2)
        self.blueSet = BorderedDiceSet([activity], batch=self.batch)
        self.blueSet.setLabelFontSize(16)
        self.blueSet.attachBooleanFunctionLabel((partial(self.blueSet.totalInRange, 1, 12), "Attack!"))
        self.blueSet.attachBooleanFunctionLabel((partial(self.blueSet.totalInRange, 13, 16), "Home Pitch"))
        self.blueSet.attachBooleanFunctionLabel((partial(self.blueSet.totalInRange, 17, 20), "Away Pitch"))
        self.blueSet.setTitle('Activity')
        self.blueSet.setPosition(440, 380, 16)
     
        lookup100 = Die(Die.D_DARK_GREEN, sides=100, text_color=Die.T_WHITE,batch=self.batch)
        lookup100.setInteriorSpacingPct(0.4)
        lookup20 = Die(Die.D_LIGHT_GREEN, sides=20, text_color=Die.T_WHITE,batch=self.batch)
        lookup20.setInteriorSpacingPct(0.4)
        self.tableDice = BorderedDiceSet([lookup100, lookup20], batch=self.batch)
        self.tableDice.setTitle('Tables')
        self.tableDice.setPosition(400, 150, 16)

        control = Die(Die.D_ORANGE, sides=20, text_color=Die.T_WHITE, batch=self.batch)
        control.setInteriorSpacingPct(0.2)
        self.testDice = BorderedDiceSet([control], 20, self.batch)
        self.testDice.setPosition(120, 150, 16)
        self.testDice.setTitle('Control')

    def draw(self) :
        self.batch.draw()

    def handle_L(self) :
        self.timeSet.roll()
        self.blueSet.roll()
        self.tableDice.roll()
        self.testDice.roll()

    def handle_K(self) :
        self.tableDice.roll()