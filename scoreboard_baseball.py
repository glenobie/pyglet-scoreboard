from die import Die
from bordered_dice_set import BorderedDiceSet
from functools import partial

from fac_set import FACSet
class ScoreboardBaseballSet(FACSet) :

    def __init__(self, loader) :
        FACSet.__init__(self, loader)
        self.createDice()

    def createDice(self) :
        
        redD20 = Die(Die.D_RED, sides=20, text_color=Die.T_WHITE,batch=self.batch)
        redD20.setInteriorSpacingPct(0.2)
        redD10 = Die(Die.D_RED, sides=10, batch=self.batch, text_color = Die.T_WHITE, startAtZero = True)

        self.playerDice = BorderedDiceSet([redD20, redD10], batch=self.batch)
        self.playerDice.setTitle('Who?')
        self.playerDice.setPosition(100, 360, 16)

        blueD20 = Die(Die.D_BLUE, sides=20, text_color=Die.T_WHITE,batch=self.batch)
        blueD20.setInteriorSpacingPct(0.2)
        blueD10 = Die(Die.D_BLUE, sides=10, batch=self.batch, text_color = Die.T_WHITE, startAtZero = True)

        self.hitDice = BorderedDiceSet([blueD20, blueD10], batch=self.batch)
        self.hitDice.setTitle('Hit Type')
        self.hitDice.setPosition(100, 160, 16)

    def draw(self) :
        self.batch.draw()

    def handle_L(self) :
        self.playerDice.roll()

    def handle_K(self) :
        0