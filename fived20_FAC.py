from die import Die
from bordered_dice_set import BorderedDiceSet
from fac_set import FACSet
from text_box import BorderedTextBox
from functools import partial

class FiveD20Set(FACSet) :

    SCALE = 0.75
    RED = 0
    WHITE = 1
    BLUE = 2
    BLACK = 3
    YELLOW = 4


    MINUTES_LEFT =  [5, 10, 15, 20, 90]
    SCORE_DIFF = [-2, -1, 0, 1, 2, 10]


    SITUATION_GRID = [ [-7, -5, -3, -1, 0], [-4, -2, -1, 0, 0], [0, 0, 0, 0, 0],
                        [4, 2, 1, 0, 0], [7, 5, 3, 1, 1], [7, 5, 3, 3, 1]]

    def __init__(self, loader) :
        FACSet.__init__(self, loader)
        self.kicking = False
        self.down = 1
        self.distance = 10
        self.quarter = 1
        self.secondsLeft = 0
        self.differential = 0 # score of team possessing minus score of other team

        self.createDice()

        self.defPlayCall = BorderedTextBox('Def Adj', 100, 100, batch=self.batch, text_size = 26)
        self.defPlayCall.setTitleFontSize(16)
        self.defPlayCall.setPosition(600, 30 + FACSet.OFFSET_FROM_BOTTOM)

        self.offPlayCall = BorderedTextBox('Off Adj', 100, 100, text_size = 26, batch=self.batch)
        self.offPlayCall.setTitleFontSize(16)
        self.offPlayCall.setPosition(450, 30 + FACSet.OFFSET_FROM_BOTTOM)
        self.situation = self.updateSituation()


    def createDice(self) :
        self.offRed = Die(Die.D_RED, text_color=Die.T_WHITE, sides=20, batch=self.batch)
        self.offRed.scale(FiveD20Set.SCALE)
        self.offWhite = Die(Die.D_WHITE, sides=20, batch=self.batch)
        self.offWhite.scale(FiveD20Set.SCALE)
        self.offBlue = Die(Die.D_BLUE, text_color=Die.T_WHITE, sides=20, batch=self.batch)
        self.offBlue.scale(FiveD20Set.SCALE)
        self.offBlack = Die(Die.D_BLACK, text_color=Die.T_WHITE, sides=20, batch=self.batch)
        self.offBlack.scale(FiveD20Set.SCALE)
        self.offYellow = Die(Die.D_YELLOW, sides=20, batch=self.batch)
        self.offYellow.scale(FiveD20Set.SCALE)

        self.offSet = [self.offRed, self.offWhite, self.offBlue, self.offBlack, self.offYellow]

        self.playDice = BorderedDiceSet(self.offSet, spacing=18, batch=self.batch)
        self.playDice.setLabelFontSize(18)

        self.offPen = Die(Die.D_YELLOW, sides=20, batch=self.batch)
        self.offPen.scale(FiveD20Set.SCALE)
        self.offPenaltyDice = BorderedDiceSet([self.offPen], spacing=18, batch=self.batch)
        self.offPenaltyDice.setTitle("Penalty")
        self.offPenaltyDice.setTitleFontSize(16)


        self.defRed = Die(Die.D_RED, text_color=Die.T_WHITE, sides=20, batch=self.batch)
        self.defRed.scale(FiveD20Set.SCALE)
        self.defWhite = Die(Die.D_WHITE, sides=20, batch=self.batch)
        self.defWhite.scale(FiveD20Set.SCALE)
        self.defBlue = Die(Die.D_BLUE, text_color=Die.T_WHITE, sides=20, batch=self.batch)
        self.defBlue.scale(FiveD20Set.SCALE)
        self.defBlack = Die(Die.D_BLACK, text_color=Die.T_WHITE, sides=20, batch=self.batch)
        self.defBlack.scale(FiveD20Set.SCALE)
        self.defYellow = Die(Die.D_YELLOW, sides=20, batch=self.batch)
        self.defYellow.scale(FiveD20Set.SCALE)

        self.defSet = [self.defRed, self.defWhite, self.defBlue, self.defBlack, self.defYellow]

        self.defDice = BorderedDiceSet(self.defSet, batch=self.batch, spacing=18)
        self.defDice.setLabelFontSize(18)

        self.defPen = Die(Die.D_YELLOW, sides=20, batch=self.batch)
        self.defPen.scale(FiveD20Set.SCALE)
        self.defPenaltyDice = BorderedDiceSet([self.defPen], spacing=18, batch=self.batch)
        self.defPenaltyDice.setTitle("Penalty")
        self.defPenaltyDice.setTitleFontSize(16)
        self.defPenaltyDice.setPosition(640, 234 + FACSet.OFFSET_FROM_BOTTOM, 16)

        self.retBlack = Die(Die.D_BLACK, text_color=Die.T_WHITE, sides=20, batch=self.batch)
        self.retBlack.scale(FiveD20Set.SCALE)
        self.retWhite = Die(Die.D_WHITE, sides=20, batch=self.batch)
        self.retWhite.scale(FiveD20Set.SCALE)

        self.returnDice = BorderedDiceSet([self.retWhite, self.retBlack], spacing = 18, batch=self.batch)
        self.returnDice.setLabelFontSize(16)
        self.returnDice.setTitleFontSize(16)

        self.changeMode(kicking=True)
        self.playDice.setPosition(40, 394 + FACSet.OFFSET_FROM_BOTTOM, 16)
        self.defDice.setPosition(40, 234 + FACSet.OFFSET_FROM_BOTTOM, 16)
        self.returnDice.setPosition(40, 84 + FACSet.OFFSET_FROM_BOTTOM, 16)
        self.offPenaltyDice.setPosition(640, 394 + FACSet.OFFSET_FROM_BOTTOM, 16)

    def homeFieldCheck(self) :
        return self.defWhite.getValue() == 1 or self.defWhite.getValue() == 20

    def fumbleCheck(self, dice) :
        return dice[FiveD20Set.BLACK].getValue() == dice[FiveD20Set.YELLOW].getValue()

    def penaltyCheck(self, dice) :
        return dice[FiveD20Set.RED].getValue() == dice[FiveD20Set.BLUE].getValue() or dice[FiveD20Set.RED].getValue() == dice[FiveD20Set.WHITE].getValue() or  dice[FiveD20Set.BLUE].getValue() == dice[FiveD20Set.WHITE].getValue()


    def getPenaltyReport(self, text, dice) :
        report = text + " ["
        if not (dice[FiveD20Set.RED].getValue() == dice[FiveD20Set.BLUE].getValue() or dice[FiveD20Set.RED].getValue() == dice[FiveD20Set.WHITE] ) :
            report += str(dice[FiveD20Set.BLUE].getValue())
        else :
            report += str(dice[FiveD20Set.RED].getValue())
        report += "]"
        return report

    def downChanged(self, down) :
        self.down = down
        self.updateSituation()

    def distanceChanged(self, distance):
        self.distance = distance
        self.updateSituation()

    def differentialChanged(self, differential) :
        self.differential = differential
        self.updateSituation()

    def quarterChanged(self, quarter) :
        self.quarter = quarter
        self.updateSituation()

    def timeChanged(self, secondsLeftInQuarter) :
        self.secondsLeft = secondsLeftInQuarter
        self.updateSituation()

    def draw(self) :
        self.batch.draw()

    def addPositiveSign(self, value) :
        s = str(value)
        if value > 0 :
            s = '+' + s
        return s

    # returns offensive play adjustment
    def updateSituation(self) :
        offAdj = '0'
        defAdj = '0'

        minutesToGo = (4 - self.quarter) * 15 + self.secondsLeft // 60
        tdsAhead = self.differential // 7
        print(str(minutesToGo))
        print(str(tdsAhead))

        if minutesToGo <= 20 :
            print("calculating adjustments")
            column = 0
            for minutes in FiveD20Set.MINUTES_LEFT :
                if  minutes >= minutesToGo :
                    break
                column += 1
            row = 0
            for diff in FiveD20Set.SCORE_DIFF :
                if diff >= tdsAhead :
                    break
                row += 1


            offAdj = self.addPositiveSign(FiveD20Set.SITUATION_GRID[row][column])
            defAdj = self.addPositiveSign(- FiveD20Set.SITUATION_GRID[row][column])

        self.offPlayCall.setText(offAdj)
        self.defPlayCall.setText(defAdj)

    def changeMode(self, kicking=False) :
        if not(kicking == self.kicking) : # changing modes
            self.kicking = kicking
            self.playDice.clearBooleanFunctionLabels()
            self.defDice.clearBooleanFunctionLabels()
            self.returnDice.clearBooleanFunctionLabels()
            if (self.kicking) :
                self.playDice.setTitle('Kick/Punt Dice')
                self.playDice.attachBooleanFunctionLabel(( partial(self.fumbleCheck, self.offSet),  "Blocked? / KR Fumble?"))
                self.playDice.attachBooleanFunctionLabel((partial(self.penaltyCheck, self.offSet), partial(self.getPenaltyReport, "Penalty?", self.offSet)))

                self.defDice.setTitle('Blocked Kick/Punt Dice')
                self.defDice.attachBooleanFunctionLabel(( partial(self.fumbleCheck, self.defSet),  "Fumbled Return of Block?"))
                self.defDice.attachBooleanFunctionLabel((partial(self.penaltyCheck, self.defSet), partial(self.getPenaltyReport, "Penalty?", self.defSet)))

                self.returnDice.setTitle('Punt Return')
                self.returnDice.attachBooleanFunctionLabel(( self.returnDice.allEqual,  "Fumbled Return?"))

            else :
                self.playDice.setTitle('Offense Dice')
                self.playDice.attachBooleanFunctionLabel(( partial(self.fumbleCheck, self.offSet),  "Snap Fumbled?"))
                self.playDice.attachBooleanFunctionLabel((partial(self.penaltyCheck, self.offSet), partial(self.getPenaltyReport, "Snap Penalty?", self.offSet)))

                self.defDice.setTitle('Defense Dice')
                self.defDice.attachBooleanFunctionLabel((self.homeFieldCheck, "Home Field Advantage?"))
                self.defDice.attachBooleanFunctionLabel(( partial(self.fumbleCheck, self.defSet),  "Fumble?"))
                self.defDice.attachBooleanFunctionLabel((partial(self.penaltyCheck, self.defSet), partial(self.getPenaltyReport, "Penalty?", self.defSet)))

                self.returnDice.setTitle('INT Return / YAC')

    def rollAllOfTheDice(self) :
        self.playDice.roll()
        self.defDice.roll()
        self.defPenaltyDice.roll()
        self.offPenaltyDice.roll()
        self.returnDice.roll()


    def handle_L(self) :
        self.changeMode(kicking=False)
        self.rollAllOfTheDice()

    def handle_K(self) :
        self.changeMode(kicking=True)
        self.rollAllOfTheDice()
