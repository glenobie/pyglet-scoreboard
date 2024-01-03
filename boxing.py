from game_state import TimedGameState
from game_state import TeamState
from scoreboard import Scoreboard
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
        
    def restoreFromList(self, stateList) :
        self.seconds = int(stateList[0].strip('\n'))
        self.period = int(stateList[1].strip('\n'))
        self.teams[0].score = int(stateList[2].strip('\n'))
        self.teams[0].endurance = int(stateList[3].strip('\n'))
        self.teams[0].tkoPoints = int(stateList[4].strip('\n'))
        self.teams[1].score = int(stateList[5].strip('\n'))
        self.teams[1].endurance = int(stateList[6].strip('\n'))
        self.teams[1].tkoPoints = int(stateList[7].strip('\n'))

    def getStateAsList(self) :
        stateList = []
        stateList.append(str(self.seconds) +'\n')
        stateList.append(str(self.period)+'\n')
        stateList.append(str(self.teams[0].score)+'\n')
        stateList.append(str(self.teams[0].endurance)+'\n')
        stateList.append(str(self.teams[0].tkoPoints)+'\n')
        stateList.append(str(self.teams[1].score) + '\n')
        stateList.append(str(self.teams[1].endurance)+'\n')
        stateList.append(str(self.teams[1].tkoPoints)+'\n')
        return stateList

class BoxingScoreboard(Scoreboard) :

   
    def __init__(self) :
        self.state = BoxingGameState()
        Scoreboard.__init__(self)

        
        self.addLargeElement(2, Scoreboard.LEFT_CENTER, 470 + Scoreboard.OFFSET_FROM_BOTTOM, 'RED', partial(self.state.getScore, 0), Scoreboard.RED)
        self.addLargeElement(2, Scoreboard.RIGHT_CENTER, 470 + Scoreboard.OFFSET_FROM_BOTTOM, 'BLUE', partial(self.state.getScore, 1), Scoreboard.BLUE)
        self.addClock(440 + Scoreboard.OFFSET_FROM_BOTTOM, 1)
        self.addPeriod(300 + Scoreboard.OFFSET_FROM_BOTTOM, maxDigits=2)

        self.addMediumElement(2, Scoreboard.LEFT_CENTER, 300 + Scoreboard.OFFSET_FROM_BOTTOM, 'Endurance', partial(self.state.getEndurance, 0), Scoreboard.RED)
        self.addMediumElement(2, Scoreboard.RIGHT_CENTER, 300 + Scoreboard.OFFSET_FROM_BOTTOM, 'Endurance', partial(self.state.getEndurance, 1), Scoreboard.BLUE)
        self.addMediumElement(2, Scoreboard.LEFT_CENTER, 160 + Scoreboard.OFFSET_FROM_BOTTOM, 'TKO Points', partial(self.state.getTkoPoints, 0), Scoreboard.RED)
        self.addMediumElement(2, Scoreboard.RIGHT_CENTER, 160 + Scoreboard.OFFSET_FROM_BOTTOM, 'TKO Points', partial(self.state.getTkoPoints, 1), Scoreboard.BLUE)
 
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
 