from team_state import TeamState, TeamStateWithTimeouts

class GameState :
    HOME_INDEX = 0
    GUEST_INDEX = 1
    
    def __init__(self) : 
        self.maxScore = 99
        self.teams = [TeamState(0, self.getMaxScore()), TeamState(0, self.getMaxScore())]

    def modifyScore(self, index, doDecrement=False):
        if doDecrement :
            self.teams[index].decrementScore()
        else :
            self.teams[index].incrementScore()

    def modifyHomeScore(self, doDecrement=False) :
        self.modifyScore(GameState.HOME_INDEX, doDecrement)

    def modifyGuestScore(self, doDecrement=False) :
        self.modifyScore(GameState.GUEST_INDEX, doDecrement)

    def getMaxScore(self) :
        return self.maxScore
        
    def getScore(self, team) :
        return self.teams[team].getScore()

###########################   
class TimedGameState(GameState):
    def __init__(self) : 
        GameState.__init__(self)
        self.teams = [TeamStateWithTimeouts(0, self.getMaxScore(), 9), 
                      TeamStateWithTimeouts(0, self.getMaxScore(), 9)]
        self.period = 1
        self.maxPeriods = 4  
        self.seconds = 0
        self.timeDivisionName = "Quarter"

    def getTimeoutsTaken(self, team=0) :
        return self.teams[team].getTimeoutsTaken()

    def modifyTimeoutsTaken(self, team, doDecrement=False) :
        if doDecrement :
            self.teams[team].modifyTimeoutsTaken(-1)
        else:
            self.teams[team].modifyTimeoutsTaken(1)

    def getSeconds(self) :
        return self.seconds
 
    def getPeriod(self) :
        return self.period

    def modifyPeriod(self) :
        self.period = self.period % self.maxPeriods + 1

    def getTimeDivisionName(self) :
        return self.timeDivisionName

    def modifyTime(self, doIncrement=False):
        if doIncrement :
            self.seconds += self.TIME_INTERVAL
            if self.seconds > self.MAX_SECONDS :
                self.seconds = self.MAX_SECONDS
        else :
            self.seconds -= self.TIME_INTERVAL
            if self.seconds < 0 :
                self.seconds = self.MAX_SECONDS


