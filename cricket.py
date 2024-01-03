
from scoreboard import Scoreboard
from element import HorizontalElement
from element import ClockElement
from game_state import GameState
from functools import partial

class CricketBatter() :

    def __init__(self, value) :
        self.runs = 0
        self.number = value

    def setNumber(self, value) :
        self.number = value

    def modifyRuns(self, value) :
        self.runs += value
        if (self.runs < 0 ): self.runs = 0

    def resetRuns(self) :
        self.runs = 0
        
    def getNumber(self) :
        return self.number

    def getRuns(self) :
        return self.runs
    

class CricketGameState(GameState) :
    
    MAX_WICKETS = 10
    MAX_BATTERS = 11
    BALLS_PER_OVER = 6
    BALLS_PER_ACTION = 2

    def __init__(self):
        #invoking the __init__ of the parent class 
        GameState.__init__(self) 
        self.maxScore = 999
        self.lastInnings = 0
        self.total = 0
        self.extras = 0
        self.balls = 0
        self.lockedTotal = 0
        self.batters = [CricketBatter(1), CricketBatter(2)]
        self.partnership = 0
        self.timeOfDay = 660 # minutes after midnight

        self.changeSides()
  
    def getOvers(self) :
        return self.overs

    def getBalls(self) :
        return self.balls
    
    def getWickets(self) :
        return self.wickets

    def getExtras(self) :
        return self.extras

    def getPartnership(self) :
        return self.partnership

    def changeSides(self) :
        self.lastInnings = self.total

        self.total = 0
        self.lockedTotal = 0
        self.wickets = 0
        self.lastWicket = 0
        self.overs = 0
        self.extras = 0
        self.balls = 0
        self.batters[0].setNumber(1)
        self.batters[0].resetRuns()
        self.batters[1].setNumber(2)
        self.batters[1].resetRuns()
        self.partnership = 0

    def recordScore(self):
        self.lastWicket = self.total    
        self.partnership = 0    

    def modifyTime(self, doDecrement=False) :
        # add/subtract overs from team in field
        adj = CricketGameState.BALLS_PER_ACTION
        if (doDecrement) : adj = - CricketGameState.BALLS_PER_ACTION
        self.balls += adj
        if self.balls < 0 : 
            self.balls = CricketGameState.BALLS_PER_OVER - CricketGameState.BALLS_PER_ACTION
            self.overs -= 1
            if (self.overs < 0) : 
                self.overs = 0
                self.balls = 0
        elif self.balls >= CricketGameState.BALLS_PER_OVER :
            self.balls = 0
            self.overs += 1            

    def incrementWickets(self) :
        self.wickets = (self.wickets + 1) % CricketGameState.MAX_WICKETS

    def getTotal(self) :
        return self.total

    def getBatterNumber(self, id) :
        return self.batters[id].getNumber()
        
    def getBatterRuns(self, id) :
        return self.batters[id].getRuns()

    def modifyBatterRuns(self, id, doDecrement=False) :
        adj = 1
        if doDecrement : adj = -1
        self.batters[id].modifyRuns(adj)
        self.partnership += adj
        self.total = self.lockedTotal + self.batters[0].getRuns() + self.batters[1].getRuns() + self.extras

    def modifyExtras(self, doDecrement = False) :
        adj = 1
        if doDecrement : adj = -1
        self.extras += adj
        if self.extras < 0 :
            self.extras = 0
        else :
            self.total += adj

    def incrementBatterNumber(self, id) :
        self.batters[id].setNumber((self.batters[id].getNumber()  % CricketGameState.MAX_BATTERS) + 1)

    def getLastInnings(self) :
        return self.lastInnings

    def getLastWicket(self) :
        return self.lastWicket

    def changeBatter(self, id) :
        self.lockedTotal += self.batters[id].getRuns()
        self.batters[id].resetRuns()
        
    def swapBatters(self) :
        temp = self.batters[0]
        self.batters[0] = self.batters[1]
        self.batters[1] = temp

    def restoreFromList(self, stateList) :
        self.total = int(stateList.pop(0).strip('\n'))
        self.balls = int(stateList.pop(0).strip('\n'))
        self.extras = int(stateList.pop(0).strip('\n'))
        self.lastInnings = int(stateList.pop(0).strip('\n'))
        self.lastWicket = int(stateList.pop(0).strip('\n'))
        self.overs = int(stateList.pop(0).strip('\n'))
        self.wickets = int(stateList.pop(0).strip('\n'))
        self.batters[0].number = int(stateList.pop(0).strip('\n'))
        self.batters[0].runs= int(stateList.pop(0).strip('\n'))
        self.batters[1].number = int(stateList.pop(0).strip('\n'))
        self.batters[1].runs = int(stateList.pop(0).strip('\n'))
        self.partnership = int(stateList.pop(0).strip('\n'))
        self.timeOfDay = int(stateList.pop(0).strip('\n'))

    def getStateAsList(self) :
        stateList = []
        stateList.append(str(self.total)+'\n')
        stateList.append(str(self.balls)+'\n')
        stateList.append(str(self.extras)+'\n')
        stateList.append(str(self.lastInnings)+'\n')
        stateList.append(str(self.lastWicket)+'\n')
        stateList.append(str(self.overs)+'\n')
        stateList.append(str(self.wickets)+'\n')
        stateList.append(str(self.batters[0].number)+'\n')
        stateList.append(str(self.batters[0].runs)+'\n')
        stateList.append(str(self.batters[1].number)+'\n')
        stateList.append(str(self.batters[1].runs)+'\n')
        stateList.append(str(self.partnership)+'\n')
        stateList.append(str(self.timeOfDay)+'\n')
        return stateList


##################################
class CricketScoreboard(Scoreboard) :
    def __init__(self) :
        #self.state = CricketGameState()
        Scoreboard.__init__(self)
        
        self.addLargeElement(3, Scoreboard.CENTER, 470 + Scoreboard.OFFSET_FROM_BOTTOM, 'Total', self.state.getTotal, Scoreboard.RED)
        self.addMediumElement(1, Scoreboard.CENTER, 290 + Scoreboard.OFFSET_FROM_BOTTOM, 'Wickets', self.state.getWickets, Scoreboard.GREEN)
        self.addMediumElement(3, Scoreboard.RIGHT_CENTER, 150 + Scoreboard.OFFSET_FROM_BOTTOM, 'Last Innings', self.state.getLastInnings, Scoreboard.GREEN)
        self.addMediumElement(2, Scoreboard.LEFT_CENTER, 290 + Scoreboard.OFFSET_FROM_BOTTOM, 'Extras', self.state.getExtras, Scoreboard.RED)
        self.addMediumElement(3, Scoreboard.RIGHT_CENTER, 290 + Scoreboard.OFFSET_FROM_BOTTOM, 'Last Wicket', self.state.getLastWicket, Scoreboard.RED)
        self.addLargeElement(3, Scoreboard.LEFT_CENTER, 400 + Scoreboard.OFFSET_FROM_BOTTOM, None, partial(self.state.getBatterRuns, 0), Scoreboard.RED)
        self.addLargeElement(3, Scoreboard.RIGHT_CENTER, 400 + Scoreboard.OFFSET_FROM_BOTTOM, None, partial(self.state.getBatterRuns, 1), Scoreboard.RED)
        self.addBatterNumber(450, Scoreboard.LEFT_CENTER, partial(self.state.getBatterNumber, 0))
        self.addBatterNumber(450, Scoreboard.RIGHT_CENTER, partial(self.state.getBatterNumber, 1))

    def addBatterNumber(self, height, x, func) :
        e = HorizontalElement(text='No.', textFont=Scoreboard.TEXT_FONT, textSize=Scoreboard.SMALL_TEXT_SIZE, textColor=Scoreboard.WHITE, 
                              updateFunc=func, digitFont=Scoreboard.DIGIT_FONT,
                              digitSize=Scoreboard.VERY_SMALL_DIGIT_SIZE, digitColor=Scoreboard.RED, maxDigits=2, 
                              batch=self.batch)
        e.setCenterTop(x, height + Scoreboard.OFFSET_FROM_BOTTOM)
        self.elements.append(e)

    # handle keys
        
    def handle_A(self, modified = False) :
        self.state.modifyExtras(modified)
        self.updateElements()

    def handle_S(self, modified=False) :
        self.state.incrementWickets()
        self.updateElements()

    def handle_Q(self, modified = False) :
        if (modified) :
            self.state.changeBatter(0)
        else :
            self.state.incrementBatterNumber(0)
        self.updateElements()

    def handle_E(self, modified = False) :
        if (modified) :
            self.state.changeBatter(1)
        else :
            self.state.incrementBatterNumber(1)
        self.updateElements()

    def handle_Z(self, modified = False) :
        self.state.modifyBatterRuns(0, modified)
        self.updateElements()

    def handle_C(self, modified=False) :
        self.state.modifyBatterRuns(1, modified)
        self.updateElements()

    def handle_D(self, modified=False) :
        if (modified) :
            self.state.changeSides()
        else :
            self.state.recordScore()
        self.updateElements()

#########################################################################

class ODICricketScoreboard(CricketScoreboard) :
    def __init__(self) :
        self.state = CricketGameState()
        CricketScoreboard.__init__(self)    
        self.addMediumElement(2, Scoreboard.CENTER, 150, 'Overs', self.state.getOvers, Scoreboard.GREEN)
        self.addMediumElement(1, Scoreboard.LEFT_CENTER, 150, 'Balls', self.state.getBalls, Scoreboard.GREEN)


#########################################################################

class TestCricketGameState(CricketGameState) :

    ONE_PM = 780

    def __init__(self):
        #invoking the __init__ of the parent class 
        CricketGameState.__init__(self) 
        
    def getTimeInMinutes(self) :

        return self.timeOfDay

    def modifyTime(self, doDecrement=False) :
        if doDecrement :
            self.timeOfDay += 60
        else :
            self.timeOfDay += 1
        if self.timeOfDay >= TestCricketGameState.ONE_PM :
            self.timeOfDay = 60 + self.timeOfDay % 60



################################################################################
class TestCricketScoreboard(CricketScoreboard) :
    def __init__(self) :
        self.state = TestCricketGameState()
        CricketScoreboard.__init__(self)
        e = ClockElement(text="Time", textFont=Scoreboard.TEXT_FONT, textSize=Scoreboard.MEDIUM_TEXT_SIZE, textColor=Scoreboard.WHITE, 
                              updateFunc=self.state.getTimeInMinutes, digitFont=Scoreboard.DIGIT_FONT,
                              digitSize=Scoreboard.MEDIUM_DIGIT_SIZE, digitColor=Scoreboard.YELLOW, maxDigits=2, 
                              batch=self.batch)

        e.setCenterTop(Scoreboard.LEFT_CENTER, 150 + Scoreboard.OFFSET_FROM_BOTTOM)
        self.elements.append(e)

        self.addMediumElement(3, Scoreboard.CENTER, 150 + Scoreboard.OFFSET_FROM_BOTTOM, 'Partnership', self.state.getPartnership, Scoreboard.RED)
