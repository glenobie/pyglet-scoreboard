from die import Die
from bordered_dice_set import BorderedDiceSet
from functools import partial

from fac_set import FACSet
class InsideVolleySet(FACSet) :

    def __init__(self, loader) :
        FACSet.__init__(self, loader)
        self.createDice()

    def createDice(self) :
        
        player = Die(Die.D_DARK_GREEN, sides=100, text_color=Die.T_WHITE,batch=self.batch)
        player.setInteriorSpacingPct(0.2)
        self.playerDice = BorderedDiceSet([player], batch=self.batch)
        self.playerDice.setTitle('Who?')
        self.playerDice.setPosition(160, 260, 16)
        self.playerDice.attachBooleanFunctionLabel( ( partial(self.playerDice.totalEquals, 1), 'Event'))
        self.playerDice.attachBooleanFunctionLabel( ( partial(self.playerDice.totalEquals, 100), 'Event'))

        aqua = Die(Die.D_AQUA, sides=6, text_color=Die.T_WHITE, batch=self.batch)
        blue = Die(Die.D_LIGHT_BLUE, sides=6, text_color=Die.T_WHITE, batch=self.batch)
        self.whatDice = BorderedDiceSet([aqua, blue],  batch=self.batch)
        self.whatDice.setPosition(400, 260, 16)
        self.whatDice.setTitle('What?')


    def draw(self) :
        self.batch.draw()

    def handle_L(self) :
        self.whatDice.roll()
        self.playerDice.roll()

    def handle_K(self) :
        self.testDice.roll()