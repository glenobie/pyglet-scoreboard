from die import Die
from bordered_dice_set import BorderedDiceSet
from dice_set import DiceSet

from fac_set import FACSet
class ScoreboardHockeySet(FACSet) :

    def __init__(self, loader) :
        FACSet.__init__(self, loader)
        self.createDice()

    def createDice(self) :
        

        redD6 = Die(Die.D_RED, sides=6, batch=self.batch, text_color = Die.T_WHITE, startAtZero = False)
        self.timeDie = BorderedDiceSet([redD6], batch=self.batch)
        self.timeDie.setTitle('Time')
        self.timeDie.setPosition(24,380,16)

        awayD20 = Die(Die.D_RED, sides=20, text_color=Die.T_WHITE,batch=self.batch)
        awayD20.setInteriorSpacingPct(0.1)
        awayD6 = redD6.makeClone()
        self.playerDice = BorderedDiceSet([awayD20, awayD6], batch=self.batch)
        self.playerDice.setTitle('Away')
        self.playerDice.setPosition(216, 380, 16)

        homeD20 = Die(Die.D_WHITE, sides=20, batch=self.batch)
        homeD20.setInteriorSpacingPct(0.1)
        homeD6 = redD6.makeClone()
        self.scoreDie = BorderedDiceSet([homeD20, homeD6], batch=self.batch)
        self.scoreDie.setTitle('Home')
        self.scoreDie.setPosition(506, 380, 16)

        greenD20 = Die(Die.D_GREEN, text_color=Die.T_WHITE, sides=20, batch=self.batch)
        greenD20.setInteriorSpacingPct(0.1)
        self.runsDie = BorderedDiceSet([greenD20], batch=self.batch)
        self.runsDie.setTitle('Positions')
        self.runsDie.setPosition(200, 200, 16)

        blueD20 = Die(Die.D_BLUE, sides=20, text_color=Die.T_WHITE,batch=self.batch)
        blueD20.setInteriorSpacingPct(0.1)
     
        self.hitDice = BorderedDiceSet([blueD20], batch=self.batch)
        self.hitDice.setTitle('Lines')
        self.hitDice.setPosition(24, 200, 16)

        allDice = [redD6.makeClone(), awayD20.makeClone(), homeD20.makeClone(),blueD20.makeClone() , greenD20.makeClone()]
        for d in allDice :
            d.scale(0.6)
        self.allOfTheDice = BorderedDiceSet(allDice, batch=self.batch)
        self.allOfTheDice.setTitle('Action Execution')
        self.allOfTheDice.setPosition(380, 180, 12)
        self.allOfTheDice.setLabelFontSize(10)

    def draw(self) :
        self.batch.draw()

    def handle_L(self) :
        self.playerDice.roll()
        self.runsDie.roll()
        self.hitDice.roll()
        self.scoreDie.roll()
        self.timeDie.roll()

    def handle_K(self) :
        #self.runsDie.roll()
        0