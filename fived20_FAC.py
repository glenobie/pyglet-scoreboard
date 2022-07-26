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

    def __init__(self, loader) :
        FACSet.__init__(self, loader)
        self.createDice()

        #self.defPlayCall = BorderedTextBox('Defense', 300, 110, self.batch)
        #self.defPlayCall.setPosition(200, 184)

        #self.offPlayCall = BorderedTextBox('Offense', 400, 110, self.batch)
        #self.offPlayCall.setPosition(280, 26)

        self.down = 1
        self.distance = 10
        self.quarter = 1
        self.secondsLeft = 0
        self.differential = 0 # score of team possessing minus score of other team


        self.situation = self.getSituation()
        self.callPlays()


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
        self.playDice.setTitle('Offense Dice')
        self.playDice.attachBooleanFunctionLabel(( partial(self.fumbleCheck, self.offSet),  "Snap Fumbled?"))
        self.playDice.attachBooleanFunctionLabel((partial(self.penaltyCheck, self.offSet), partial(self.getPenaltyReport, "Snap Penalty?", self.offSet)))
        self.playDice.setPosition(40, 394, 16)

        self.offPen = Die(Die.D_YELLOW, sides=20, batch=self.batch)
        self.offPen.scale(FiveD20Set.SCALE)
        self.offPenaltyDice = BorderedDiceSet([self.offPen], spacing=18, batch=self.batch)
        self.offPenaltyDice.setTitle("Penalty")
        self.offPenaltyDice.setTitleFontSize(16)
        self.offPenaltyDice.setPosition(640, 394, 16)


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
        self.defDice.attachBooleanFunctionLabel((self.homeFieldCheck, "Home Field Advantage?"))
        self.defDice.attachBooleanFunctionLabel(( partial(self.fumbleCheck, self.defSet),  "Fumble?"))
        self.defDice.attachBooleanFunctionLabel((partial(self.penaltyCheck, self.defSet), partial(self.getPenaltyReport, "Penalty?", self.defSet)))
        self.defDice.setLabelFontSize(18)
        self.defDice.setTitle('Defense Dice')
        self.defDice.setPosition(40, 234, 16)

        self.defPen = Die(Die.D_YELLOW, sides=20, batch=self.batch)
        self.defPen.scale(FiveD20Set.SCALE)
        self.defPenaltyDice = BorderedDiceSet([self.defPen], spacing=18, batch=self.batch)
        self.defPenaltyDice.setTitle("Penalty")
        self.defPenaltyDice.setTitleFontSize(16)
        self.defPenaltyDice.setPosition(640, 234, 16)

    def homeFieldCheck(self) :
        return self.defWhite.getValue() == 1 or self.defWhite.getValue() == 20

    def fumbleCheck(self, dice) :
        return dice[FiveD20Set.BLACK].getValue() == dice[FiveD20Set.YELLOW].getValue()

    def penaltyCheck(self, dice) :
        return dice[FiveD20Set.RED].getValue() == dice[FiveD20Set.BLUE].getValue() or dice[FiveD20Set.RED].getValue() == dice[FiveD20Set.WHITE].getValue() or  dice[FiveD20Set.BLUE].getValue() == dice[FiveD20Set.WHITE].getValue()

    def callPlays(self) :
        0

    def getPenaltyReport(self, text, dice) :
        report = text + " ["
        if not (dice[FiveD20Set.RED].getValue() == dice[FiveD20Set.BLUE].getValue() or dice[FiveD20Set.RED].getValue() == dice[FiveD20Set.WHITE]) :
            report += str(dice[FiveD20Set.BLUE].getValue())
        else :
            report += str(dice[FiveD20Set.RED].getValue())
        report += "]"
        return report

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


    def getSituation(self) :
        return 5

    def handle_L(self) :
        self.playDice.roll()
        self.defDice.roll()
        self.defPenaltyDice.roll()
        self.offPenaltyDice.roll()
        self.callPlays()

    def handle_K(self) :
        self.playDice.roll()
