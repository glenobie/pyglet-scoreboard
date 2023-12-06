from game_state import TimedGameState
from game_state import TeamState
from scoreboard import Scoreboard
from functools import partial


######################
class SoccerTeamState(TeamState) :
    def __init__(self, score, maxScore=19) :
        TeamState.__init__(self, score, maxScore)

###########################
class SoccerGameState(TimedGameState) :
    
    def __init__(self, timeInterval = -60):
        #invoking the __init__ of the parent class 
        TimedGameState.__init__(self) 
        self.maxScore = 19
        self.teams = [SoccerTeamState(0, self.getMaxScore()), 
                      SoccerTeamState(0, self.getMaxScore())]
        self.TIME_INTERVAL = timeInterval
        self.MAX_MINUTES = 45
        self.extraTime = 0
        self.MAX_SECONDS = (self.MAX_MINUTES  + self.extraTime) * 60
        self.seconds = 0 
        self.timeDivisionName = "Half"
        self.maxPeriods = 2

    def resetHalf(self):
        self.seconds = 0 # self.MAX_SECONDS
        self.extraTime = 0

    def getExtraTime(self) :
        return self.extraTime
    
    def modifyExtraTime(self, increment=True) :
        value = 1 if increment else -1
        self.extraTime += value
        if self.extraTime < 0 :
            self.extraTime = 0
        self.MAX_SECONDS = (self.MAX_MINUTES + self.extraTime) * 60 

    def restoreFromList(self, stateList) :
        self.seconds = int(stateList[0].strip('\n'))
        self.period = int(stateList[1].strip('\n'))
        self.teams[0].score = int(stateList[2].strip('\n'))
        self.teams[1].score = int(stateList[3].strip('\n'))

    def getStateAsList(self) :
        stateList = []
        stateList.append(str(self.seconds) +'\n')
        stateList.append(str(self.period)+'\n')
        stateList.append(str(self.teams[0].score)+'\n')
        stateList.append(str(self.teams[1].score) + '\n')
        return stateList

 ############################################    
class SoccerScoreboard(Scoreboard) :   
    def __init__(self) :
        self.state = SoccerGameState(timeInterval=-60)
        Scoreboard.__init__(self)
        self.addElements()

    def addElements(self) :        
        self.addScores(2, 470+ Scoreboard.OFFSET_FROM_BOTTOM)
        self.addClock(440+ Scoreboard.OFFSET_FROM_BOTTOM)
        self.addPeriod(300+ Scoreboard.OFFSET_FROM_BOTTOM, maxDigits=1)

        self.addMediumElement(2, Scoreboard.LEFT_CENTER, 200+ Scoreboard.OFFSET_FROM_BOTTOM, 'EXTRA', partial(self.state.getExtraTime), Scoreboard.BLUE)


    def handle_A(self, modified=False) :
        self.state.modifyExtraTime(not(modified))
        self.updateElements()

    def handle_Q(self, modified=False) :
        if modified :
            self.state.resetHalf()
        self.updateElements()


class APBASoccerScoreboard(SoccerScoreboard) :   
    def __init__(self) :
        Scoreboard.__init__(self)
        self.state = SoccerGameState(timeInterval = -30)
        self.addElements()
        