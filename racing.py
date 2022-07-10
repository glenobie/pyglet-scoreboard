from game_state import GameState
from scoreboard import Scoreboard

###########################
class RaceState(GameState) :
    
    def __init__(self):
        #invoking the __init__ of the parent class 
        GameState.__init__(self) 
        self.totalTurns = 20
        self.currentTurn = 1

    def getCurrentTurn(self) :
        return self.currentTurn

    def getTotalTurns(self) :
        return self.totalTurns

    def modifyPeriod(self) :
        0
 
    def modifyTime(self, doDecrement=False) :
        if doDecrement :
            if self.currentTurn > 1 :
                self.currentTurn -= 1
        else:
            if self.currentTurn < self.getTotalTurns() :
                self.currentTurn += 1

    def modifyTotalTurns(self, doDecrement=False) :
        if doDecrement :
            if self.totalTurns > 1 :
                self.totalTurns -= 1
        else:
            self.totalTurns += 1

    def isPitTurn(self) :
        return self.currentTurn % 7 == 0

    def getPitMessage(self) :
        if self.isPitTurn() :
            return 'PIT'
        elif self.currentTurn == self.totalTurns :
            return 'END'
        else :
            return '  '
        
    def restoreFromList(self, stateList) :
        self.currentTurn = int(stateList[0].strip('\n'))
        self.totalTurns = int(stateList[1].strip('\n'))

    def getStateAsList(self) :
        stateList = []
        stateList.append(str(self.currentTurn) +'\n')
        stateList.append(str(self.totalTurns)+'\n')
        return stateList

#######################################
class RacingScoreboard(Scoreboard) :
   
    def __init__(self) :
        self.state = RaceState()
        Scoreboard.__init__(self)
        
        self.addLargeElement(2, Scoreboard.CENTER, 460, 'Current Turn', self.state.getCurrentTurn, Scoreboard.GREEN)
        self.addMediumElement(2, Scoreboard.RIGHT_CENTER, 240, 'Total Turns', self.state.getTotalTurns, Scoreboard.RED)
        self.addMediumElement(3, Scoreboard.LEFT_CENTER, 240, 'Message', self.state.getPitMessage, Scoreboard.YELLOW)
  
    # handle keys
    def handle_Q(self, modified = False) :
        self.state.modifyTotalTurns(modified)
        self.updateElements()
 