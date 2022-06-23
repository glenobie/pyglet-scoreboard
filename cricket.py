
from scoreboard import Scoreboard
from element import HorizontalElement
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
        self.changeSides()
  
    def getOvers(self) :
        return self.overs

    def getBalls(self) :
        return self.balls
    
    def getWickets(self) :
        return self.wickets

    def getExtras(self) :
        return self.extras

    def changeSides(self) :
        self.lastInnings = self.total

        self.total = 0
        self.lockedTotal = 0
        self.wickets = 0
        self.lastWicket = 0
        self.overs = 0
        self.extras = 0
        self.batters[0].setNumber(1)
        self.batters[1].setNumber(2)

    def recordScore(self):
        self.lastWicket = self.total        

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
        self.leftBatter.resetRuns()
        
    def swapBatters(self) :
        temp = self.batters[0]
        self.batters[0] = self.batters[1]
        self.batters[1] = temp

##################################
class CricketScoreboard(Scoreboard) :
    def __init__(self) :
        Scoreboard.__init__(self)
        self.state = CricketGameState()
        
        self.addLargeElement(3, Scoreboard.CENTER, 470, 'Total', self.state.getTotal, Scoreboard.RED)
        self.addMediumElement(1, Scoreboard.CENTER, 290, 'Wickets', self.state.getWickets, Scoreboard.GREEN)
        self.addMediumElement(2, Scoreboard.CENTER, 150, 'Overs', self.state.getOvers, Scoreboard.GREEN)
        self.addMediumElement(1, Scoreboard.LEFT_CENTER, 150, 'Balls', self.state.getBalls, Scoreboard.GREEN)
        self.addMediumElement(3, Scoreboard.RIGHT_CENTER, 150, 'Last Innings', self.state.getLastInnings, Scoreboard.GREEN)
        self.addMediumElement(2, Scoreboard.LEFT_CENTER, 290, 'Extras', self.state.getExtras, Scoreboard.RED)
        self.addMediumElement(3, Scoreboard.RIGHT_CENTER, 290, 'Last Wicket', self.state.getLastWicket, Scoreboard.RED)
        self.addLargeElement(3, Scoreboard.LEFT_CENTER, 400, None, partial(self.state.getBatterRuns, 0), Scoreboard.RED)
        self.addLargeElement(3, Scoreboard.RIGHT_CENTER, 400, None, partial(self.state.getBatterRuns, 1), Scoreboard.RED)
        self.addBatterNumber(450, Scoreboard.LEFT_CENTER, partial(self.state.getBatterNumber, 0))
        self.addBatterNumber(450, Scoreboard.RIGHT_CENTER, partial(self.state.getBatterNumber, 1))

    def addBatterNumber(self, height, x, func) :
        e = HorizontalElement(text='No.', textFont=Scoreboard.TEXT_FONT, textSize=Scoreboard.SMALL_TEXT_SIZE, textColor=Scoreboard.WHITE, 
                              updateFunc=func, digitFont=Scoreboard.DIGIT_FONT,
                              digitSize=Scoreboard.VERY_SMALL_DIGIT_SIZE, digitColor=Scoreboard.RED, maxDigits=2, 
                              batch=self.batch)
        e.setCenterTop(x, height)
        self.elements.append(e)

    # handle keys
        
    def handle_A(self, modified = False) :
        self.state.modifyExtras(modified)
        self.updateElements()

    def handle_S(self, modified=False) :
        self.state.incrementWickets()
        self.updateElements()

    def handle_Q(self, modified = False) :
        self.state.incrementBatterNumber(0)
        self.updateElements()

    def handle_E(self, modified = False) :
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
