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
        self.MINUTES_PER_PERIOD = 45
        self.MAX_SECONDS = self.MINUTES_PER_PERIOD * 60
        self.seconds = self.MAX_SECONDS
        self.timeDivisionName = "Half"
        self.maxPeriods = 2

    def resetHalf(self):
        for team in self.teams :
            team.resetScore()
        self.seconds = self.MAX_SECONDS
        

class LacrosseScoreboard(Scoreboard) :
   
    def __init__(self) :
        Scoreboard.__init__(self)
        self.state = LacrosseGameState()
        
        self.addLargeElement(2, Scoreboard.LEFT_CENTER, 470, 'GUEST', partial(self.state.getScore, 0), Scoreboard.RED)
        self.addLargeElement(2, Scoreboard.RIGHT_CENTER, 470, 'HOME', partial(self.state.getScore, 1), Scoreboard.RED)
        self.addClock(440)
        self.addPeriod(300, maxDigits=1)

