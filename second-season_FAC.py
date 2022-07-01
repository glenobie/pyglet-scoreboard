
import pyglet
from die import Die
from dice_set import DiceSet
from functools import partial

class SecondSeasonSet() :

    def __init__(self) :
        self.batch = pyglet.graphics.Batch()
        self.createDice()

        self.down = 1
        self.distance = 10
        self.quarter = 1
        self.secondsLeft = 0
        self.guestScore = 0
        self.homeScore = 0

    def createDice(self) :
        
        self.track = Die(Die.D_ORANGE, sides=6, text_color=Die.T_WHITE, batch=self.batch)
        self.trackSet = DiceSet([self.track], self.batch)

        self.trackSet.attachBooleanFunctionLabel((partial(self.trackSet.totalEquals, 1), 'TOP Group'))
        self.trackSet.attachBooleanFunctionLabel((partial(self.trackSet.totalEquals, 2), 'TOP Group'))
        self.trackSet.attachBooleanFunctionLabel((partial(self.trackSet.totalEquals, 3), 'MIDDLE Group'))
        self.trackSet.attachBooleanFunctionLabel((partial(self.trackSet.totalEquals, 4), 'MIDDLE Group'))
        self.trackSet.attachBooleanFunctionLabel((partial(self.trackSet.totalEquals, 5), 'BOTTOM Group'))
        self.trackSet.attachBooleanFunctionLabel((partial(self.trackSet.totalEquals, 6), 'DUEL!'))
        self.trackSet.setPosition(20, 420, 16)

        self.black = Die(Die.D_BLACK, sides=6, text_color=Die.T_WHITE,batch=self.batch)
        self.gray = Die(Die.D_GRAY, sides=6, text_color=Die.T_WHITE,batch=self.batch)
        self.course = [self.gray, self.black]

        self.courseDice = DiceSet(self.course, self.batch)
        self.courseDice.setPosition(20, 300, 16)

        self.red = Die(Die.D_RED, text_color=Die.T_WHITE, sides=6, batch=self.batch)
        self.white = Die(Die.D_WHITE, sides=6, batch=self.batch)
        self.blue = Die(Die.D_BLUE, sides=6, text_color=Die.T_WHITE, batch=self.batch)
        self.challenge = [self.red, self.white, self.blue]

        self.challengeDice = DiceSet(self.challenge, self.batch)
        self.challengeDice.setPosition(20, 120, 16)


    def downChanged(self, down) :
        self.down = down

    def distanceChanged(self, distance):
        self.distance = distance

    def scoreChanged(self, guestScore, homeScore) :
        self.guestScore = guestScore
        self.homeScore = homeScore
        
    def quarterChanged(self, quarter) :
        self.quarter = quarter

    def timeChanged(self, secondsLeftInQuarter) :
        self.secondsLeft = secondsLeftInQuarter

    def draw(self) :
        self.batch.draw()

    def handle_L(self) :
        self.trackSet.roll()
        self.challengeDice.roll()
        self.courseDice.roll()

    def handle_K(self) :
        self.challengeDice.roll()
