from team_state import TeamStateWithTimeouts
from game_state import TimedGameState
from game_state import GameState
from scoreboard import Scoreboard
from element import ScoreboardElement
from element import HorizontalElement

################################
class FootballTeamState(TeamStateWithTimeouts) :
    def __init__(self, score, maxScore, maxTimeouts) :
        TeamStateWithTimeouts.__init__(self, score, maxScore, maxTimeouts)
    
#################################
class FootballGameState(TimedGameState) :

    DOWN_STRINGS = ("1ST", "2ND", "3RD", "4TH")

    GOAL_TO_GO = -1000
    
    def __init__(self, maxDowns=4, fieldSize=100):
        #invoking the __init__ of the parent class 
        TimedGameState.__init__(self) 
        self.teams = [FootballTeamState(0, self.getMaxScore(), 3), 
                       FootballTeamState(0, self.getMaxScore(), 3)]

        self.TIME_INTERVAL = 15
        self.MINUTES_PER_PERIOD = 15
        self.MAX_SECONDS = self.MINUTES_PER_PERIOD * 60
        self.seconds = self.MAX_SECONDS
        self.MaxDowns = maxDowns

        self.lineOfScrimmage = 20 # 1 to 99
        self.down = 1
        self.yardsToGain = 10
        self.fieldSize = fieldSize

        self.teamPossessingBall = GameState.HOME_INDEX

    def getDownAsString(self) :
        return FootballGameState.DOWN_STRINGS[self.down-1]

    def getDown(self) :
        return self.down

    def getYardsToGain(self) :
        if self.yardsToGain < 0 :
            return 'G'
        else :
            return self.yardsToGain

    def modifyDown(self) :
        self.down += 1
        if (self.down > self.MaxDowns) :
            self.down = 1
        
    def getPossessingTeam(self) :
        return self.teamPossessingBall

    def changePossessingTeam(self) :
        self.teamPossessingBall = (self.teamPossessingBall + 1) % 2
        self.lineOfScrimmage = self.fieldSize - self.lineOfScrimmage

    # between 0 and 50
    def getLineOfScrimmage(self) :
        halfFieldYard = self.lineOfScrimmage
        if (halfFieldYard > self.fieldSize / 2) :
            halfFieldYard = self.fieldSize - halfFieldYard
        return halfFieldYard


    def modifyLineOfScrimmage(self, value, doDecrement = False) :
        if (doDecrement) :
            self.lineOfScrimmage -= value
            self.yardsToGain += value
            if self.lineOfScrimmage < 0 :
                self.lineOfScrimmage = 0
            if self.yardsToGain > self.fieldSize - 1 :
                self.yardsToGain = self.fieldSize -1
            elif self.yardsToGain < 0 :
                self.yardsToGain = FootballGameState.GOAL_TO_GO
        else :
            self.lineOfScrimmage += value
            self.yardsToGain -= value
            if self.lineOfScrimmage > self.fieldSize - 1 :
                self.lineOfScrimmage = self.fieldSize - 1
            if self.yardsToGain < 0 :
                self.yardsToGain = FootballGameState.GOAL_TO_GO

    def resetDownAndDistance(self) :
        self.yardsToGain = 10
        if self.fieldSize - self.lineOfScrimmage < 10 : 
            self.yardsToGain = FootballGameState.GOAL_TO_GO
        self.down = 1

    def getYardsToEndzone(self) :
        return self.fieldSize - self.lineOfScrimmage

    def getLineToGain(self) :
        line = self.lineOfScrimmage + self.yardsToGain
        if line > self.fieldSize / 2 :
            line = self.fieldSize - line
        if line < 0 :
            line = 0
        return line

###################################
class FootballScoreboard(Scoreboard) :
    def __init__(self) :
        Scoreboard.__init__(self)
        self.state = FootballGameState()
        
        self.addElements()
    
    def addElements(self) :
        self.addScores(2, 470)
        self.addClock(450)
        self.addPeriod(340, horizontal=True)
        self.addHorizontalElement(1, Scoreboard.CENTER, 242, 'Down:', self.state.getDown, Scoreboard.YELLOW )
        self.addHorizontalElement(2, Scoreboard.CENTER, 162, 'Yards to Go:', self.state.getYardsToGain, Scoreboard.YELLOW )
        self.addYardsToEndzone(70)
        self.ballMarker = self.addBallLocation(250)

 
    def changePossessingTeam(self) :
        pos = self.ballMarker.getCenter()
        if pos == Scoreboard.LEFT_CENTER :
            self.ballMarker.setCenterTop(Scoreboard.RIGHT_CENTER, self.ballMarker.getTop())
        else :
            self.ballMarker.setCenterTop(Scoreboard.LEFT_CENTER, self.ballMarker.getTop())        

    def addBallLocation(self, height) :
        e = ScoreboardElement(text='Ball On', textFont=Scoreboard.TEXT_FONT, 
                                textSize=Scoreboard.MEDIUM_TEXT_SIZE, textColor=Scoreboard.WHITE, 
                                updateFunc=self.state.getLineOfScrimmage, digitFont=Scoreboard.DIGIT_FONT,
                                digitSize=Scoreboard.MEDIUM_DIGIT_SIZE, digitColor=Scoreboard.RED, maxDigits=2, 
                                displayLeadingZeroes=False, batch=self.batch)
        e.setCenterTop(Scoreboard.LEFT_CENTER, height)
        self.elements.append(e)
        return e

    def addYardsToEndzone(self, height) :
        e = HorizontalElement(text='Yards To Endzone:', textFont=Scoreboard.TEXT_FONT, 
                                textSize=Scoreboard.SMALL_TEXT_SIZE, textColor=Scoreboard.WHITE, 
                                updateFunc=self.state.getYardsToEndzone, digitFont=Scoreboard.DIGIT_FONT,
                                digitSize=Scoreboard.SMALL_DIGIT_SIZE, digitColor=Scoreboard.YELLOW, maxDigits=2, 
                                displayLeadingZeroes=False, batch=self.batch)
        e.setCenterTop(Scoreboard.CENTER, height)
        self.elements.append(e)

    def handle_A(self, modified = False) :
        self.state.modifyLineOfScrimmage(1, modified)
        self.updateElements()

    def handle_D(self, modified = False) :
        if modified :
            self.state.resetDownAndDistance()
        else :
            self.state.modifyDown()

        if not(self.attachedFAC is None) :
            self.attachedFAC.downChanged(self.state.getDown())
        self.updateElements()
 
    def handle_Q(self, modified = False) :
        self.state.modifyLineOfScrimmage(10, modified)
        self.updateElements()

    def handle_E(self, modified = False) :
        self.state.changePossessingTeam()
        self.changePossessingTeam()
        self.updateElements()
 
#################################
class CFLScoreboard(FootballScoreboard) :
    def __init__(self) :
        Scoreboard.__init__(self)
        self.state = FootballGameState(maxDowns = 3, fieldSize = 110)        
        self.addElements()