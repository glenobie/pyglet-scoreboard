from game_state import TimedGameState
from game_state import TeamState
from scoreboard import Scoreboard
from functools import partial


######################
class LacrosseTeamState(TeamState) :
    def __init__(self, score, maxScore=19) :
        TeamState.__init__(self, score, maxScore)
 

###########################
class LacrosseGameState(TimedGameState) :
    
    def __init__(self):
        #invoking the __init__ of the parent class 
        TimedGameState.__init__(self) 
        self.maxScore = 19
        self.teams = [LacrosseTeamState(0, self.getMaxScore()), 
                      LacrosseTeamState(0, self.getMaxScore())]
        self.TIME_INTERVAL = 60
        self.MINUTES_PER_PERIOD = 15
        self.MAX_SECONDS = self.MINUTES_PER_PERIOD * 60
        self.seconds = self.MAX_SECONDS
        self.timeDivisionName = "Quarter"
        self.maxPeriods = 4

    def resetHalf(self):
        for team in self.teams :
            team.resetScore()
        self.seconds = self.MAX_SECONDS

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
       
#################################################
class LacrosseScoreboard(Scoreboard) :
    def __init__(self) :
        self.state = LacrosseGameState()        
        Scoreboard.__init__(self)

        self.addLargeElement(2, Scoreboard.LEFT_CENTER, 470 + Scoreboard.OFFSET_FROM_BOTTOM, 'GUEST', partial(self.state.getScore, 0), Scoreboard.RED)
        self.addLargeElement(2, Scoreboard.RIGHT_CENTER, 470 + Scoreboard.OFFSET_FROM_BOTTOM, 'HOME', partial(self.state.getScore, 1), Scoreboard.RED)
        self.addClock(440 + Scoreboard.OFFSET_FROM_BOTTOM)
        self.addPeriod(300 + Scoreboard.OFFSET_FROM_BOTTOM, maxDigits=1)

