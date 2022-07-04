from http.cookies import Morsel
import pyglet
from die import Die
from bordered_dice_set import BorderedDiceSet
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

    SITUATION_ROWS =  [-14, -10, -7, -3, 0, 8, 17, 100]
        
    # -SS values indicate that offense will use Down/Distance chart, but defense will use
    SITUATION_GRID = [ [-SS_B, SS_C, SS_C, SS_C],
                       [-SS_A, -SS_B, SS_C, SS_C],
                       [-1, -SS_A, -SS_B, SS_C ],
                       [-1, -1, -SS_A, SS_C],
                       [-1, -1, -1, -SS_B],
                       [-1, -1, -SS_D, SS_D],
                       [-1, -SS_D, SS_D, SS_D],
                       [-SS_D, SS_D, SS_D, SS_D]
                    ]
        
    SITUATION_COLS = [9, 5, 3, 0] # minutes left in fourth quarter

    DEFENSE_COORD_FILE = 'ss-DEF-coord.txt'
    OFFENSE_COORD_FILE = 'ss-OFF-coord.txt'

    def __init__(self, loader) :
        FACSet.__init__(self, loader)
        self.batch = pyglet.graphics.Batch()
        self.createDice()

        self.defPlayCall = BorderedTextBox('Defense', 300, 110, self.batch)
        self.defPlayCall.setPosition(200, 184)

        self.offPlayCall = BorderedTextBox('Offense', 400, 110, self.batch)
        self.offPlayCall.setPosition(280, 26)

        self.down = 1
        self.distance = 10
        self.quarter = 1
        self.secondsLeft = 0
        self.differential = 0 # score of team possessing minus score of other team


        self.defensiveCalls = self.processCoordinatorFile(SecondSeasonSet.DEFENSE_COORD_FILE, 20)
        self.offensiveCalls = self.processCoordinatorFile(SecondSeasonSet.OFFENSE_COORD_FILE, 36)
        self.situation = self.getSituation()
        self.callPlays()

    def processCoordinatorFile(self, filename, rows) :
        calls = []
        f = self.loader.file(filename, mode='r')
        for j in range(0,rows) :
            list = f.readline().split(',')
            calls.append(list)
            print(list)
        return calls

    def createDice(self) :
        self.red = Die(Die.D_RED, text_color=Die.T_WHITE, sides=6, batch=self.batch)
        self.red.scale(0.8)
        self.white = Die(Die.D_WHITE, sides=6, batch=self.batch)
        self.white.scale(0.8)

        self.chartDice = BorderedDiceSet([self.red, self.white], 24 , self.batch)
        self.chartDice.setTitle('Chart Dice')
        self.chartDice.setPosition(40, 400, 16)

        self.finderDie = Die(Die.D_BLUE, text_color=Die.T_WHITE, sides=20, batch=self.batch)
        self.finderDie.scale(0.8)
        self.playerSet = BorderedDiceSet([self.finderDie], 24, self.batch)
        self.playerSet.setTitle("Finder")
        self.playerSet.setPosition(490,400)        

        self.defenseDie = Die(Die.D_AQUA, text_color=Die.T_WHITE, sides=20, batch=self.batch)
        self.defenseDie.scale(0.7)
        self.defenseSet = BorderedDiceSet([self.defenseDie], 20, self.batch)
        self.defenseSet.setTitleFontSize(16)
        self.defenseSet.setTitle("Defense")
        self.defenseSet.setPosition(40, 240)    

        self.o1 = Die(Die.D_GREEN, text_color=Die.T_WHITE, sides=6, batch=self.batch)
        self.o1.scale(0.7)
        self.o2 = Die(Die.D_ORANGE, text_color=Die.T_WHITE, sides=6, batch=self.batch)
        self.o2.scale(0.7)
        self.offenseSet = BorderedDiceSet([self.o1,self.o2], 20, self.batch)
        self.offenseSet.setTitle('Offense')
        self.offenseSet.setTitleFontSize(16)
        self.offenseSet.setPosition(40, 80)

    def callPlays(self) :
        defense = self.defensiveCalls[self.defenseDie.getValue()-1][self.situation]
        row = self.getOffenseRowFromDice(self.o1, self.o2)
        offense = self.offensiveCalls[self.getOffenseRowFromDice(self.o1, self.o2)][self.situation]
        self.defPlayCall.setText(defense.replace('\n', ''))
        self.offPlayCall.setText(offense.replace('\n',''))
        print(defense)

    def downChanged(self, down) :
        self.down = down
        self.situation = self.getSituation()

    def distanceChanged(self, distance):
        self.distance = distance
        self.situation = self.getSituation()

    def differentialChanged(self, differential) :
        self.differential = differential
        self.situation = self.getSituation()

    def quarterChanged(self, quarter) :
        self.quarter = quarter
        self.situation = self.getSituation()

    def timeChanged(self, secondsLeftInQuarter) :
        self.secondsLeft = secondsLeftInQuarter
        self.situation = self.getSituation()

    def draw(self) :
        self.batch.draw()

    def getOffenseRowFromDice(self, d1, d2) :
        return (d1.getValue() - 1) * 6 + (d2.getValue() - 1)

    # based on team on offense, their lead(trail) points, and the time remaining
    def isSpecialSituation(self) :
        row=column=0
        minutesLeft = self.secondsLeft // 60
        situation = -1
        if (self.quarter == 3 and self.differential < -19) :
            situation = -SecondSeasonSet.SS_A
        elif self.quarter == 4 :
            for row in range(0, len(SecondSeasonSet.SITUATION_ROWS)) :
                if self.differential < SecondSeasonSet.SITUATION_ROWS[row] :
                    break
            # adding one because ultimately indexing into SITUATION
            for column in range(0, len(SecondSeasonSet.SITUATION_COLS)) :
                if minutesLeft > SecondSeasonSet.SITUATION_COLS[column] :
                    break
            
        
            situation = SecondSeasonSet.SITUATION_GRID[row][column]
            if situation < -1 :
                situation = -1 if self.down > 2 else -situation

        return situation


    def getSituation(self) :
        situation = self.isSpecialSituation() 
        return self.getDD_Situation() if situation < 0 else situation 

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


    def handle_L(self) :
        self.chartDice.roll()
        self.playerSet.roll()
        self.defenseSet.roll()
        self.offenseSet.roll()
        self.callPlays()

    def handle_K(self) :
        self.chartDice.roll()

