from game_state import TimedGameState
from game_state import TeamState
from scoreboard import Scoreboard
from element import ScoreboardElement
from functools import partial


######################
class BoxerState(TeamState) :
    def __init__(self, score, maxScore=39) :
        TeamState.__init__(self, score, maxScore)
        self.endurance = 20
        self.tkoPoints = 0

    def getEndurance(self) :
        return self.endurance
    
    def getTkoPoints(self) :
        return self.tkoPoints

    def modifyTkoPoints(self, value) :
        self.tkoPoints += value
        if self.tkoPoints < 0 :
            self.tkoPoints = 0

    def modifyEndurance(self, value) :
        self.endurance += value


###########################
class BoxingGameState(TimedGameState) :
    
    def __init__(self):
        #invoking the __init__ of the parent class 
        TimedGameState.__init__(self) 
        self.maxScore = 99
        self.teams = [BoxerState(0, self.getMaxScore()), 
                      BoxerState(0, self.getMaxScore())]
        self.TIME_INTERVAL = 20
        self.MINUTES_PER_PERIOD = 3
        self.MAX_SECONDS = self.MINUTES_PER_PERIOD * 60
        self.seconds = self.MAX_SECONDS
        self.timeDivisionName = "Round"
        self.maxPeriods = 15 

    def getEndurance(self, team) :
        return self.teams[team].getEndurance()

    def getTkoPoints(self, team) :
        return self.teams[team].getTkoPoints()
 
    def modifyEndurance(self, team, doIncrement=False) :
        if doIncrement :
            self.teams[team].modifyEndurance(1)
        else:
            self.teams[team].modifyEndurance(-1)

    def modifyTkoPoints(self, team, doDecrement=False) :
        if doDecrement :
            self.teams[team].modifyTkoPoints(-1)
        else:
            self.teams[team].modifyTkoPoints(1)


    def resetRound(self):
        for team in self.teams :
            team.resetScore()
        self.seconds = self.MAX_SECONDS
        

class BoxingScoreboard(Scoreboard) :

   
    def __init__(self) :
        Scoreboard.__init__(self)
        self.state = BoxingGameState()
        
        self.addLargeElement(2, Scoreboard.LEFT_CENTER, 460, 'RED', partial(self.state.getScore, 0), Scoreboard.RED)
        self.addLargeElement(2, Scoreboard.RIGHT_CENTER, 460, 'BLUE', partial(self.state.getScore, 1), Scoreboard.BLUE)
        self.addClock(440)
        self.addPeriod(300, maxDigits=2)

        self.addMediumElement(2, Scoreboard.LEFT_CENTER, 300, 'Endurance', partial(self.state.getEndurance, 0), Scoreboard.RED)
        self.addMediumElement(2, Scoreboard.RIGHT_CENTER, 300, 'Endurance', partial(self.state.getEndurance, 1), Scoreboard.BLUE)
        self.addMediumElement(2, Scoreboard.LEFT_CENTER, 160, 'TKO Points', partial(self.state.getTkoPoints, 0), Scoreboard.RED)
        self.addMediumElement(2, Scoreboard.RIGHT_CENTER, 160, 'TKO Points', partial(self.state.getTkoPoints, 1), Scoreboard.BLUE)
 
    # handle keys

    def handle_A(self, modified = False) :
        self.state.modifyEndurance(0, modified)
        self.updateElements()

    def handle_D(self, modified = False) :
        self.state.modifyEndurance(1, modified)
        self.updateElements()
 
    def handle_Q(self, modified = False) :
        self.state.modifyTkoPoints(0, modified)
        self.updateElements()

    def handle_E(self, modified = False) :
        self.state.modifyTkoPoints(1, modified)
        self.updateElements()
 