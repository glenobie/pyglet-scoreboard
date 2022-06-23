from audioop import add
from team_state import TeamStateWithTimeouts
from game_state import TimedGameState
from scoreboard import Scoreboard
from element import ScoreboardElement
from functools import partial

#################################################
class BasketballTeamState(TeamStateWithTimeouts):
    def __init__(self, score, maxScore, maxTimeouts, maxTeamFouls) :
        TeamStateWithTimeouts.__init__(self, score, maxScore, maxTimeouts) 
        self.teamFouls = 0
        self.maxTeamFouls = maxTeamFouls

    def modifyTeamFouls(self, value) :
        self.teamFouls += value
        if self.teamFouls > self.maxTeamFouls :
            self.teamFouls = self.maxTeamFouls
        if self.teamFouls < 0 :
                self.teamFouls = 0

    def getTeamFouls(self):
        return self.teamFouls

###################################################        
class BasketballGameState(TimedGameState) :
    
    def __init__(self):
        #invoking the __init__ of the parent class 
        TimedGameState.__init__(self) 
        self.maxScore = 199
        self.teams = [BasketballTeamState(0, self.getMaxScore(), 9, 10 ), 
                      BasketballTeamState(0, self.getMaxScore(), 9, 10)]
        self.TIME_INTERVAL = 12
        self.MINUTES_PER_PERIOD = 12
        self.MAX_SECONDS = self.MINUTES_PER_PERIOD * 60
        self.seconds = self.MAX_SECONDS

    def getTeamFouls(self, team=0) :
        return self.teams[team].getTeamFouls()

    def modifyTeamFouls(self, team, doDecrement=False) :
        if doDecrement :
            self.teams[team].modifyTeamFouls(-1)
        else:
            self.teams[team].modifyTeamFouls(1)

####################################
class BasketballScoreboard(Scoreboard) :
    def __init__(self) :
        Scoreboard.__init__(self)
        self.state = BasketballGameState()
        
        self.addScores(3, 470)
        self.addClock(440)
        self.addPeriod(300)

        self.addMediumElement(2, Scoreboard.LEFT_CENTER, 300, 'Team Fouls', partial(self.state.getTeamFouls, 0), Scoreboard.RED)
        self.addMediumElement(2, Scoreboard.RIGHT_CENTER, 300, 'Team Fouls', partial(self.state.getTeamFouls, 1), Scoreboard.RED)
        self.addMediumElement(1, Scoreboard.LEFT_CENTER, 160, 'Timeouts', partial(self.state.getTimeoutsTaken, 0), Scoreboard.RED)
        self.addMediumElement(1, Scoreboard.RIGHT_CENTER, 160, 'Timeouts', partial(self.state.getTimeoutsTaken, 1), Scoreboard.RED)

     # handle keys

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
 

    
        