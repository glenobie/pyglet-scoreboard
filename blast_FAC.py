from functools import partial
import pyglet
from die import Die
from dice_set import DiceSet
from bordered_dice_set import  BorderedDiceSet
from fac_set import FACSet

#############################################################################
class BlastSet(FACSet) :

    def __init__(self, loader) :
        FACSet.__init__(self, loader)
        self.batch = pyglet.graphics.Batch()

    def createBlastDice(self, d1, d2, x, y, spacing, title, labels, scale=1.0) :

        d1.scale(scale)
        d2.scale(scale)

        dice = BorderedDiceSet([d1, d2], 26 * scale, self.batch)
        dice.setTitleFontSize(20 * scale)
        dice.setLabelFontSize(20 * scale)

        for j in range(0,len(labels)) :
            dice.attachBooleanFunctionLabel((partial(dice.totalEquals, j+1), labels[j]))
        dice.setPosition(x, y, spacing)
        dice.setTitle(title)

        return dice

    def draw(self) :
        self.batch.draw()

###############################################################################
class HockeyBlastSet(BlastSet) :

    NORMAL = ['None', 'Fight?', 'Play', 'Odd Man Rush!', 'Penalty Event', 'Zoom!', 'Lull', 'Ice Blast!',
                'Momentum', 'Turnover', 'Play', 'Spectacular Save!']

    POWER = ['None', 'Spectacular Save!', 'Power Play', 'Odd Man Rush!', 'Penalty Event', 'Zoom!', 'Power Play',
                'Ice Blast!', 'Play', 'Turnover', 'Possession Battle', 'Spectacular Save!']

    EMPTY_NET =  ['None', 'Spectacular Save!', 'Man-Adv. Play', 'Odd Man Rush!', 'Turnover', 'Zoom!', 'Empty Netter',
                'Ice Blast!', 'Play', 'Turnover', 'Possession Battle', 'Spectacular Save!']

    THREE_ON_3 =  ['None', 'Spectacular Save!', 'Play', 'Odd Man Rush!', 'Turnover', 'Ice Blast!', 'Breakaway',
                'Ice Blast!', 'Momentum', 'Turnover', 'Play!', 'Spectacular Save!']


    def __init__(self, loader) :
        FACSet.__init__(self, loader)
        self.batch = pyglet.graphics.Batch()
        white = Die(Die.D_WHITE, sides=6, batch=self.batch)
        black = Die(Die.D_BLACK, sides=6, text_color=Die.T_WHITE,batch=self.batch)
        self.normalDice = self.createBlastDice(white, black,100, 380, 16, 'Normal Minutes', HockeyBlastSet.NORMAL)


        self.powerDice = self.createBlastDice(white.makeClone(), black.makeClone(),  500, 400, 16, 
                                                'Power', HockeyBlastSet.POWER, 0.76)
        self.powerDice.setBorderColor((255,0,0), 255)
        self.emptyNetDice = self.createBlastDice(white.makeClone(), black.makeClone(), 500, 248, 16, 
                                                'Empty Net', HockeyBlastSet.EMPTY_NET, 0.76)
        self.emptyNetDice.setBorderColor((255,255,0), 255)
        self.threeOn3Dice = self.createBlastDice(white.makeClone(), black.makeClone(),  500, 90, 16, 
                                                '3 on 3', HockeyBlastSet.THREE_ON_3, 0.76)
        self.threeOn3Dice.setBorderColor((0,255,255), 255)
        red = Die(Die.D_RED, sides=6, text_color=Die.T_WHITE, batch=self.batch)
        blue = Die(Die.D_BLUE, sides=6, text_color=Die.T_WHITE, batch=self.batch)

        self.d6s = DiceSet([red, blue], self.batch)
        self.d6s.setPosition(120, 96, 16) 
        self.green = Die(Die.D_GREEN, text_color=Die.T_WHITE, sides=6, batch=self.batch) 
        self.green.setCenter(170, 220)


    def handle_L(self) :
        self.normalDice.roll()
        self.green.roll()
        self.d6s.roll()

    def handle_K(self) :
        self.d6s.roll()

################################################################
class SoccerBlastSet(BlastSet) :

    NORMAL = ['None', 'Attack!', 'Highlight Reel', 'Home Advantage', 'Referee','Take On', 'Midfield Battle', 'Build-up', 
                'Sideline Battle','Tackle', 'Corner Kick', 'Counter Attack']

    def __init__(self, loader) :
        FACSet.__init__(self, loader)
        self.batch = pyglet.graphics.Batch()
        white = Die(Die.D_WHITE, sides=6, batch=self.batch)
        black = Die(Die.D_BLACK, sides=6, text_color=Die.T_WHITE,batch=self.batch)
        self.normalDice = self.createBlastDice(white, black,100, 380, 16, 'Pitch Action', SoccerBlastSet.NORMAL)


        red = Die(Die.D_RED, sides=6, text_color=Die.T_WHITE, batch=self.batch)
        blue = Die(Die.D_BLUE, sides=6, text_color=Die.T_WHITE, batch=self.batch)

        self.d6s = DiceSet([red, blue], self.batch)
        self.d6s.setPosition(120, 96, 16) 
        self.green = Die(Die.D_GREEN, text_color=Die.T_WHITE, sides=6, batch=self.batch) 
        self.green.setCenter(170, 220)
        self.gold = Die(Die.D_GOLD, sides=6, batch=self.batch)
        self.goldSet = BorderedDiceSet([self.gold], batch=self.batch)
        self.goldSet.setTitle('Optional')
        self.goldSet.setPosition(500, 380)


    def handle_L(self) :
        self.normalDice.roll()
        self.green.roll()
        self.d6s.roll()
        self.gold.roll()

    def handle_K(self) :
        self.d6s.roll()


###############################################################################
class LacrosseBlastSet(BlastSet) :

    NORMAL = ['None', 'Fight?', 'Play', 'Goal Charge', 'Penalty Event', 'Crash', 'Boxla Blast', 'Scramble',
                'Loose Ball', 'Turnover', 'Play/Clock', 'Spectacular Save!']

    POWER = ['None', 'Penalty Event', 'Power Play', 'Goal Charge', 'Penalty Kill', 'Crash', 'Power Play',
                'Scramble', 'Play', 'Turnover', 'Loose Ball', 'Spectacular Save!']

    EMPTY_NET =  ['None', 'Spectacular Save!', 'Man-Adv. Play', 'Goal Crash', 'Penalty Event', 'Crash', 'Man-Adv. Play',
                'Scramble', 'Play', 'Turnover', 'Loose Ball', 'Spectacular Save!']

    def __init__(self, loader) :
        FACSet.__init__(self, loader)
        self.batch = pyglet.graphics.Batch()
        white = Die(Die.D_WHITE, sides=6, batch=self.batch)
        black = Die(Die.D_BLACK, sides=6, text_color=Die.T_WHITE,batch=self.batch)
        self.normalDice = self.createBlastDice(white, black,100, 380, 16, 'Normal Minutes', LacrosseBlastSet.NORMAL)


        self.powerDice = self.createBlastDice(white.makeClone(), black.makeClone(),  500, 320, 16, 
                                                'Power', LacrosseBlastSet.POWER, 0.76)
        self.powerDice.setBorderColor((255,0,0), 255)
        self.emptyNetDice = self.createBlastDice(white.makeClone(), black.makeClone(), 500, 128, 16, 
                                                'Empty Net', LacrosseBlastSet.EMPTY_NET, 0.76)
        self.emptyNetDice.setBorderColor((255,255,0), 255)

        red = Die(Die.D_RED, sides=6, text_color=Die.T_WHITE, batch=self.batch)
        blue = Die(Die.D_BLUE, sides=6, text_color=Die.T_WHITE, batch=self.batch)

        self.d6s = DiceSet([red, blue], self.batch)
        self.d6s.setPosition(120, 96, 16) 
        self.green = Die(Die.D_GREEN, text_color=Die.T_WHITE, sides=6, batch=self.batch) 
        self.green.setCenter(170, 220)


    def handle_L(self) :
        self.normalDice.roll()
        self.green.roll()
        self.d6s.roll()

    def handle_K(self) :
        self.d6s.roll()
