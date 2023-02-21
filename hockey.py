from scoreboard import Scoreboard
from element import ClockElement
from game_state import TeamState
from game_state import TimedGameState
from functools import partial

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
    
    def __init__(self, timeInterval = 20):
        #invoking the __init__ of the parent class 
        TimedGameState.__init__(self) 
        self.maxScore = 19
        
        self.teams = [ HockeyTeamState(0, self.getMaxScore()), HockeyTeamState(0, self.getMaxScore()) ]
    
        self.TIME_INTERVAL = timeInterval
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

    def restoreFromList(self, stateList) :
        self.seconds = int(stateList[0].strip('\n'))
        self.period = int(stateList[1].strip('\n'))
        self.teams[0].score = int(stateList[2].strip('\n'))
        self.teams[0].penaltyClocks = [int(stateList[3].strip('\n')), int(stateList[4].strip('\n'))]
        self.teams[1].score = int(stateList[5].strip('\n'))
        self.teams[1].penaltyClocks = [int(stateList[6].strip('\n')), int(stateList[7].strip('\n'))]

    def getStateAsList(self) :
        stateList = []
        stateList.append(str(self.seconds) +'\n')
        stateList.append(str(self.period)+'\n')
        stateList.append(str(self.teams[0].score)+'\n')
        stateList.append(str(self.teams[0].penaltyClocks[0])+'\n')
        stateList.append(str(self.teams[0].penaltyClocks[1])+'\n')
        stateList.append(str(self.teams[1].score) + '\n')
        stateList.append(str(self.teams[1].penaltyClocks[0])+'\n')
        stateList.append(str(self.teams[1].penaltyClocks[1])+'\n')
        return stateList

##################################################

class HockeyScoreboard(Scoreboard) :
    def __init__(self) :
        self.state = HockeyGameState()
        Scoreboard.__init__(self)
        
        self.addScores(3, 470)
        self.addClock(440)
        self.addPeriod(300)
        self.addPenaltyClock('Penalty 1', Scoreboard.LEFT_CENTER, 300, 0, 0)
        self.addPenaltyClock('Penalty 1', Scoreboard.RIGHT_CENTER, 300, 1, 0)
        self.addPenaltyClock('Penalty 2', Scoreboard.LEFT_CENTER, 160, 0, 1)
        self.addPenaltyClock('Penalty 2', Scoreboard.RIGHT_CENTER, 160, 1, 1)


    def addPenaltyClock(self, text, x, y, team, clock) :
        e = ClockElement(text=text, textFont=Scoreboard.TEXT_FONT, textSize=Scoreboard.MEDIUM_TEXT_SIZE, textColor=Scoreboard.WHITE, 
                              updateFunc=partial(self.state.getPenaltySeconds, team, clock), digitFont=Scoreboard.DIGIT_FONT,
                              digitSize=Scoreboard.MEDIUM_DIGIT_SIZE, digitColor=Scoreboard.YELLOW, maxDigits=1, 
                              batch=self.batch)

        e.setCenterTop(x, y)
        self.elements.append(e)

    # key handlers

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
 

class HockeyScoreboardSubset(Scoreboard) :
    def __init__(self) :
        self.state = HockeyGameState(timeInterval=30)
        Scoreboard.__init__(self)
        
        self.addScores(3, 470)
        self.addClock(440)
        self.addPeriod(300)

 




    
        