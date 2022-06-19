from scoreboard import Scoreboard
from element import ScoreboardElement
from element import ClockElement
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
            
    
    def getLeftTopPenaltySeconds(self) :
        return self.getPenaltySeconds(0, 0)

    def getLeftBottomPenaltySeconds(self) :
        return self.getPenaltySeconds(0, 1) 

    def getRightTopPenaltySeconds(self) :
        return self.getPenaltySeconds(1, 0) 

    def getRightBottomPenaltySeconds(self) :
        return self.getPenaltySeconds(1, 1) 

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
        self.addPenaltyClock('Penalty 1', self.state.getLeftTopPenaltySeconds, Scoreboard.LEFT_CENTER, 290)
        self.addPenaltyClock('Penalty 1', self.state.getRightTopPenaltySeconds, Scoreboard.RIGHT_CENTER, 290)
        self.addPenaltyClock('Penalty 2', self.state.getLeftBottomPenaltySeconds, Scoreboard.LEFT_CENTER, 140)
        self.addPenaltyClock('Penalty 2', self.state.getRightBottomPenaltySeconds, Scoreboard.RIGHT_CENTER, 140)


    def addPenaltyClock(self, text, func, x, y) :
        e = ClockElement(text=text, textFont=Scoreboard.TEXT_FONT, textSize=Scoreboard.MEDIUM_TEXT_SIZE, textColor=Scoreboard.WHITE, 
                              updateFunc=func, digitFont=Scoreboard.DIGIT_FONT,
                              digitSize=Scoreboard.MEDIUM_DIGIT_SIZE, digitColor=Scoreboard.RED, maxDigits=1, 
                              batch=self.batch)

        e.setCenterTop(x, y)
        self.elements.append(e)


    def handle_A(self, modified = False) :
        self.state.modifyPenaltyClock(0, 0) 
        self.updateElements()

    def handle_D(self, modified = False) :
        self.state.modifyPenaltyClock(1, 0) 
        self.updateElements()
 
    def handle_Q(self, modified = False) :
        self.state.modifyPenaltyClock(0, 1) 
        self.updateElements()

    def handle_E(self, modified = False) :
        self.state.modifyPenaltyClock(1, 1) 
        self.updateElements()
 



    
        