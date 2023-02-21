from die import Die
from bordered_dice_set import BorderedDiceSet

from fac_set import FACSet
class ScoreboardHockeysSet(FACSet) :

    def __init__(self, loader) :
        FACSet.__init__(self, loader)
        self.createDice()

    def createDice(self) :
        
        redD20 = Die(Die.D_RED, sides=20, text_color=Die.T_WHITE,batch=self.batch)
        redD20.setInteriorSpacingPct(0.1)
        redD10 = Die(Die.D_RED, sides=10, batch=self.batch, text_color = Die.T_WHITE, startAtZero = True)

        self.playerDice = BorderedDiceSet([redD20, redD10], batch=self.batch)
        self.playerDice.setTitle('Who?')
        self.playerDice.setPosition(130, 360, 16)

        whiteD20 = Die(Die.D_WHITE, sides=20, batch=self.batch)
        whiteD20.setInteriorSpacingPct(0.1)
        self.scoreDie = BorderedDiceSet([whiteD20], batch=self.batch)
        self.scoreDie.setTitle('Score?')
        self.scoreDie.setLabel('BB / H+')
        self.scoreDie.setPosition(500, 360, 16)


        greenD20 = Die(Die.D_GREEN, text_color=Die.T_WHITE, sides=20, batch=self.batch)
        greenD20.setInteriorSpacingPct(0.1)
        self.runsDie = BorderedDiceSet([greenD20], batch=self.batch)
        self.runsDie.setTitle('Runs')
        self.runsDie.setLabel('K')
        self.runsDie.setPosition(500, 140, 16)

        blueD20 = Die(Die.D_BLUE, sides=20, text_color=Die.T_WHITE,batch=self.batch)
        blueD20.setInteriorSpacingPct(0.1)
        blueD10 = Die(Die.D_BLUE, sides=10, batch=self.batch, text_color = Die.T_WHITE, startAtZero = True)

        self.hitDice = BorderedDiceSet([blueD20, blueD10], batch=self.batch)
        self.hitDice.setTitle('Hit Type')
        self.hitDice.setPosition(130, 140, 16)

    def draw(self) :
        self.batch.draw()

    def handle_L(self) :
        self.playerDice.roll()
        self.runsDie.roll()
        self.hitDice.roll()
        self.scoreDie.roll()

    def handle_K(self) :
        self.runsDie.roll()