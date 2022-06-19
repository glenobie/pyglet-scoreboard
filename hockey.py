from scoreboard import Scoreboard
from element import ScoreboardElement
from game_state import TeamState
from game_state import TimedGameState

########################################
class HockeyTeamState(TeamState):
    def __init__(self, score, maxScore) : 
        TeamState.__init__(self, score, maxScore)
        self.penaltyClocks = [ 0, 0 ] # two clocks, in seconds

    def setPenaltyClock(self, index, value) :
        self.penaltyClocks[index] = value

    def getPenaltyClock(self, index) :
        return self.penaltyClocks[index]

    def modifyAllPenaltyClocks(self, value) :
        for i in range(len(self.penaltyClocks)) :
            self.penaltyClocks[i] += value
            if self.penaltyClocks[i] <= 0 :
                self.penaltyClocks[i] = 0

###########################################
class HockeyGameState(TimedGameState) :
    
    def __init__(self):
        #invoking the __init__ of the parent class 
        TimedGameState.__init__(self) 
        self.maxScore = 19
        
        self.teams = [ HockeyTeamState(0, self.getMaxScore()), HockeyTeamState(0, self.getMaxScore()) ]
    
        self.TIME_INTERVAL = 20
        self.MINUTES_PER_PERIOD = 20
        self.MAX_SECONDS = self.MINUTES_PER_PERIOD * 60
        
        self.seconds = self.MAX_SECONDS
        self.maxPeriods = 3
        self.timeDivisionName = "Period"
  
    def modifyTime(self, doIncrement=False) :
        TimedGameState.modifyTime(self, doIncrement)
        if doIncrement :
            self.incrementPenaltyClocks(self.TIME_INTERVAL)
        else:
            self.incrementPenaltyClocks(-self.TIME_INTERVAL)
            
    
    def getLeftTopPenaltyMinutes(self) :
        return self.getPenaltySeconds[0].getPenaltyClock(0) // 60

    def getLeftTopPenaltySeconds(self) :
        return self.getPenaltySeconds[0].getPenaltyClock(0) % 60

    def getLeftBottomPenaltyMinutes(self) :
        return self.getPenaltySeconds[0].getPenaltyClock(1) // 60

    def getLeftBottomPenaltySeconds(self) :
        return self.getPenaltySeconds[0].getPenaltyClock(1) % 60

    def getRightTopPenaltyMinutes(self) :
        return self.getPenaltySeconds[1].getPenaltyClock(0) // 60

    def getRightTopPenaltySeconds(self) :
        return self.getPenaltySeconds[1].getPenaltyClock(0) % 60

    def getRightBottomPenaltyMinutes(self) :
        return self.getPenaltySeconds[1].getPenaltyClock(1) // 60

    def getRightBottomPenaltySeconds(self) :
        return self.getPenaltySeconds[1].getPenaltyClock(1) % 60

    def getPenaltySeconds(self, team, index) :
        return self.teams[team].getPenaltyClock(index)

    def modifyPenaltyClock(self, team, index=0) :
        if (self.teams[team].getPenaltyClock(index) == 0) :
            self.teams[team].setPenaltyClock(index, 120)
        elif (self.teams[team].getPenaltyClock(index) == 120) :
            self.teams[team].setPenaltyClock(index, 300)
        else :
            self.teams[team].setPenaltyClock(index, 0)

    def incrementPenaltyClocks(self, interval) :
        for i in range(len(self.teams)) :
            self.teams[i].modifyAllPenaltyClocks(interval)

##################################################

class HockeyScoreboard(Scoreboard) :
    def __init__(self) :
        Scoreboard.__init__(self)
        self.state = HockeyGameState()
        
        self.addScores(3)
        self.addClock(440)
        self.addPeriod(300)

        #self.addTeamFouls(280)
        #self.addTimeouts(140)

    def addTimeouts(self, height) :
        e = ScoreboardElement(text='Timeouts', textFont=Scoreboard.TEXT_FONT, textSize=Scoreboard.MEDIUM_TEXT_SIZE, textColor=Scoreboard.WHITE, 
                              updateFunc=self.state.getGuestTimeoutsTaken, digitFont=Scoreboard.DIGIT_FONT,
                              digitSize=Scoreboard.MEDIUM_DIGIT_SIZE, digitColor=Scoreboard.RED, maxDigits=2, 
                              batch=self.batch)
        e.setCenterTop(Scoreboard.LEFT_CENTER, height)
        self.elements.append(e)

        e = ScoreboardElement(text='Timeouts', textFont=Scoreboard.TEXT_FONT, textSize=Scoreboard.MEDIUM_TEXT_SIZE, textColor=Scoreboard.WHITE,
                              updateFunc=self.state.getHomeTimeoutsTaken, digitFont=Scoreboard.DIGIT_FONT,
                              digitSize=Scoreboard.MEDIUM_DIGIT_SIZE, digitColor=Scoreboard.RED, maxDigits=2,  
                              batch=self.batch)
        e.setCenterTop(Scoreboard.RIGHT_CENTER, height)
        self.elements.append(e)


    def addTeamFouls(self, height) :
        e = ScoreboardElement(text='Team Fouls', textFont=Scoreboard.TEXT_FONT, textSize=Scoreboard.MEDIUM_TEXT_SIZE, textColor=Scoreboard.WHITE, 
                              updateFunc=self.state.getGuestTeamFouls, digitFont=Scoreboard.DIGIT_FONT,
                              digitSize=Scoreboard.MEDIUM_DIGIT_SIZE, digitColor=Scoreboard.RED, maxDigits=2, 
                              batch=self.batch)
        e.setCenterTop(Scoreboard.LEFT_CENTER, height)
        self.elements.append(e)

        e = ScoreboardElement(text='Team Fouls', textFont=Scoreboard.TEXT_FONT, textSize=Scoreboard.MEDIUM_TEXT_SIZE, textColor=Scoreboard.WHITE,
                             updateFunc=self.state.getHomeTeamFouls, digitFont=Scoreboard.DIGIT_FONT,
                              digitSize=Scoreboard.MEDIUM_DIGIT_SIZE, digitColor=Scoreboard.RED, maxDigits=2,  
                              batch=self.batch)
        e.setCenterTop(Scoreboard.RIGHT_CENTER, height)
        self.elements.append(e)


    def handle_A(self, modified = False) :
        self.state.modifyTeamFouls(0, modified)
        self.updateElements()

    def handle_D(self, modified = False) :
        self.state.modifyTeamFouls(1, modified)
        self.updateElements()
 
    def handle_Q(self, modified = False) :
        self.state.modifyTimeoutsTaken(0, modified)
        self.updateElements()

    def handle_E(self, modified = False) :
        self.state.modifyTimeoutsTaken(1, modified)
        self.updateElements()
 

    
        