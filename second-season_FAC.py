import pyglet
from die import Die
from dice_set import DiceSet, BorderedDiceSet
from fac_set import FACSet
from text_box import BorderedTextBox

class SecondSeasonSet(FACSet) :

    DD_NORMAL            = 0 # first 1-19, second 1-10
    DD_EARLY_LONG        = 1 # first more than 19, second more than 10
    DD_LATE_SHORT        = 2 # third, fourth, 1-3
    DD_LATE_MEDIUM_SHORT = 3 # third, fourth, 4-6
    DD_LATE_MEDIUM_LONG  = 4 # third, fourth, 7-9
    DD_LATE_LONG         = 5 # third, fourth, 10-14
    DD_LATE_VERY_LONG    = 6 # third, fourth, 15-19
    DD_LATE_SUPER_LONG   = 7 # third, fourth, 20 +
    SS_A                 = 8 # Special situation A
    SS_B                 = 9
    SS_C                 = 10
    SS_D                 = 11

    DEFENSE_COORD_FILE = 'ss-DEF-coord.txt'

    def __init__(self, loader) :
        FACSet.__init__(self, loader)
        self.batch = pyglet.graphics.Batch()
        self.createDice()

        self.defPlayCall = BorderedTextBox('Just testing', 200, 50, self.batch)
        self.defPlayCall.setPosition(600, 100)

        self.down = 1
        self.distance = 10
        self.quarter = 1
        self.secondsLeft = 0
        self.guestScore = 0
        self.homeScore = 0

        self.situation = 1
        self.defensiveCalls = []

        self.processDefenseFile(SecondSeasonSet.DEFENSE_COORD_FILE)

    def processDefenseFile(self, filename) :
        f = self.loader.file(filename, mode='r')
        for j in range(0,20) :
            list = f.readline().split(',')
            self.defensiveCalls.append(list)
            print(list)

    def createDice(self) :
        
        self.red = Die(Die.D_RED, text_color=Die.T_WHITE, sides=6, batch=self.batch)
        self.white = Die(Die.D_WHITE, sides=6, batch=self.batch)

        self.chartDice = BorderedDiceSet([self.red, self.white], self.batch)
        self.chartDice.setTitle('Chart Dice')
        self.chartDice.setPosition(20, 380, 16)

        self.finderDie = Die(Die.D_BLUE, text_color=Die.T_WHITE, sides=20, batch=self.batch)
        self.playerSet = BorderedDiceSet([self.finderDie], self.batch)
        self.playerSet.setTitle("Finder")
        self.playerSet.setPosition(490,380)        

        self.defenseDie = Die(Die.D_AQUA, text_color=Die.T_WHITE, sides=20, batch=self.batch)
        self.defenseSet = BorderedDiceSet([self.defenseDie], self.batch)
        self.defenseSet.setTitle("Defense")
        self.defenseSet.setPosition(40, 200)    


    def downChanged(self, down) :
        self.down = down
        self.situation = self.getSituation()

    def distanceChanged(self, distance):
        self.distance = distance
        self.situation = self.getSituation()

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
        self.chartDice.roll()
        self.playerSet.roll()
        self.defenseSet.roll()

        print(self.defensiveCalls[self.finderDie.getValue()-1][self.situation])

    def handle_K(self) :
        self.chartDice.roll()

    def isSpecialSituation(self) :
        return -1

    def getSituation(self) :
        if self.isSpecialSituation < 0 :
            return self.getDD_Situation()

    def getDD_Situation(self) :
        situation = -1
        if self.down == 1 :
            if self.distance < 20 :
                situation = SecondSeasonSet.DD_NORMAL
            else :
                situation = SecondSeasonSet.DD_EARLY_LONG
        elif self.down == 2 :
            if self.distance < 11 :
                situation = SecondSeasonSet.DD_NORMAL
            else :
                situation = SecondSeasonSet.DD_EARLY_LONG
        else :
            if self.distance < 4 :
                situation = SecondSeasonSet.DD_LATE_SHORT
            elif self.distance < 7 :
                situation = SecondSeasonSet.DD_LATE_MEDIUM_SHORT
            elif self.distance < 10 :
                situation = SecondSeasonSet.DD_LATE_MEDIUM_LONG
            elif self.distance < 15 :
                situation = SecondSeasonSet.DD_LATE_LONG
            elif self.distance < 20 :
                situation = SecondSeasonSet.DD_LATE_VERY_LONG
            else :
                situation = SecondSeasonSet.DD_LATE_SUPER_LONG
        
        return situation