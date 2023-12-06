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
        
        die1 = Die(Die.D_RED, sides=6, text_color=Die.T_WHITE, batch=self.batch)
        die1.setInteriorSpacingPct(0.2)
        die2 = Die(Die.D_WHITE, sides=6, text_color=Die.T_BLACK, batch=self.batch)
        die2.setInteriorSpacingPct(0.2)
        self.diceSet = BorderedDiceSet([die1, die2], batch=self.batch)
        self.diceSet.setPosition(290, 380+FACSet.OFFSET_FROM_BOTTOM, 16)

     

    def draw(self) :
        self.batch.draw()

    def handle_L(self) :
        self.diceSet.roll()
        
    def handle_K(self) :
        self.diceSet.roll()

 