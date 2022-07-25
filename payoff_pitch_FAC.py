import pyglet
from die import Die
from bordered_dice_set import BorderedDiceSet
from fac_set import FACSet


class PayoffPitchSet(FACSet) :

    def __init__(self, loader) :
        FACSet.__init__(self, loader)
        self.createDice()

    def createDice(self) :
        #self.pitcher = IP_DiceSet(title= 'Pitcher', label='WP/HR?/??', batch=self.batch)
        #self.pitcher.setTopLeft(36, 454)

        #self.hitter = IP_DiceSet(title= 'Hitter', label='HBP/K/W/HR', batch=self.batch)
        #self.hitter.setTopLeft(286, 454)

        #self.ballpark = IP_DiceSet(title= 'Ballpark', label='H?/E/Strategy', batch=self.batch)
        #self.ballpark.setTopLeft(540, 454)


        p1 = Die(Die.D_WHITE, Die.T_BLACK, 6, self.batch)
        p2 = Die(Die.D_WHITE, Die.T_BLACK, 6, self.batch)
        d = [p1,p2]
        for br in d :
            br.scale(0.8)


        self.pitchSet = BorderedDiceSet(d, batch= self.batch)
        self.pitchSet.setTitle('Pitch')
        self.pitchSet.attachBooleanFunctionLabel((self.always, self.pitchSet.totalAsString))
        self.pitchSet.setPosition(60, 400, 10)

        h1 = Die(Die.D_RED, Die.T_WHITE, 100, self.batch)
        h1.scale(0.8);

        self.hitSet = BorderedDiceSet([h1], batch= self.batch)
        self.hitSet.setTitle('Hit')
        self.hitSet.setPosition(360, 400, 10)

    def draw(self) :
        self.batch.draw()

    def always(self) :
        return True

    def handle_L(self) :
        self.pitchSet.roll()


    def handle_K(self) :
        0
