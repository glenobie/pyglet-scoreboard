
from scoreboard import Scoreboard
from element import ScoreboardElement
from element import HorizontalElement
from game_state import GameState

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
        self.leftBatter = CricketBatter(1)
        self.rightBatter =  CricketBatter(2)

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

    def getLeftBatterNumber(self) :
        return self.leftBatter.getNumber()

    def getRightBatterNumber(self) :
        return self.rightBatter.getNumber()
        
    def getLeftBatterRuns(self) :
        return self.leftBatter.getRuns()

    def getRightBatterRuns(self) :
        return self.rightBatter.getRuns()

    def modifyLeftBatterRuns(self, doDecrement=False) :
        adj = 1
        if doDecrement : adj = -1
        self.leftBatter.modifyRuns(adj)
        self.total = self.lockedTotal + self.leftBatter.getRuns() + self.rightBatter.getRuns() + self.extras

    def modifyRightBatterRuns(self, doDecrement=False) :
        adj = 1
        if doDecrement : adj = -1
        self.rightBatter.modifyRuns(adj)
        self.total = self.lockedTotal + self.leftBatter.getRuns() + self.rightBatter.getRuns() + self.extras

    def modifyExtras(self, doDecrement = False) :
        adj = 1
        if doDecrement : adj = -1
        self.extras += adj
        if self.extras < 0 :
            self.extras = 0
        else :
            self.total += adj

    def incrementLeftBatterNumber(self) :
        self.leftBatter.setNumber((self.leftBatter.getNumber()  % CricketGameState.MAX_BATTERS) + 1)

    def incrementRightBatterNumber(self) :
        self.rightBatter.setNumber((self.rightBatter.getNumber()  % CricketGameState.MAX_BATTERS) + 1)

    def getLastInnings(self) :
        return self.lastInnings

    def getLastWicket(self) :
        return self.lastWicket

    def changeRightBatter(self) :
        self.lockedTotal += self.rightBatter.getRuns()
        self.rightBatter.resetRuns()

    def changeLeftBatter(self) :
        self.lockedTotal += self.leftBatter.getRuns()
        self.leftBatter.resetRuns()
        
    def swapBatters(self) :
        temp = self.leftBatter
        self.leftBatter = self.rightBatter
        self.rightBatter = temp

##################################
class CricketScoreboard(Scoreboard) :
    def __init__(self) :
        Scoreboard.__init__(self)
        self.state = CricketGameState()
        
        self.addTotal(470)
        self.addWickets(290)
        self.addOvers(150)
        self.addBalls(150)
        self.addLastInnings(150)
        self.addExtras(290)
        self.addLastWicket(290)
        self.addRuns(400, Scoreboard.LEFT_CENTER, self.state.getLeftBatterRuns)
        self.addRuns(400, Scoreboard.RIGHT_CENTER, self.state.getRightBatterRuns)
        self.addBatterNumber(450, Scoreboard.LEFT_CENTER, self.state.getLeftBatterNumber)
        self.addBatterNumber(450, Scoreboard.RIGHT_CENTER, self.state.getRightBatterNumber)

    def addBatterNumber(self, height, x, func) :
        e = HorizontalElement(text='No.', textFont=Scoreboard.TEXT_FONT, textSize=Scoreboard.SMALL_TEXT_SIZE, textColor=Scoreboard.WHITE, 
                              updateFunc=func, digitFont=Scoreboard.DIGIT_FONT,
                              digitSize=Scoreboard.VERY_SMALL_DIGIT_SIZE, digitColor=Scoreboard.RED, maxDigits=2, 
                              batch=self.batch)
        e.setCenterTop(x, height)
        self.elements.append(e)


    def addRuns(self, height, x, func) :
        e = ScoreboardElement(text=None, textFont=Scoreboard.TEXT_FONT, textSize=Scoreboard.LARGE_TEXT_SIZE, textColor=Scoreboard.WHITE, 
                              updateFunc=func, digitFont=Scoreboard.DIGIT_FONT,
                              digitSize=Scoreboard.SCORE_SIZE, digitColor=Scoreboard.RED, maxDigits=3, 
                              batch=self.batch)
        e.setCenterTop(x, height)
        self.elements.append(e)


    def addTotal(self, height) :
        e = ScoreboardElement(text='Total', textFont=Scoreboard.TEXT_FONT, textSize=Scoreboard.LARGE_TEXT_SIZE, textColor=Scoreboard.WHITE, 
                              updateFunc=self.state.getTotal, digitFont=Scoreboard.DIGIT_FONT,
                              digitSize=Scoreboard.SCORE_SIZE, digitColor=Scoreboard.RED, maxDigits=3, 
                              batch=self.batch)
        e.setCenterTop(Scoreboard.CENTER, height)
        self.elements.append(e)
       
    def addWickets(self, height) :
        e = ScoreboardElement(text='Wickets', textFont=Scoreboard.TEXT_FONT, textSize=Scoreboard.MEDIUM_TEXT_SIZE, textColor=Scoreboard.WHITE, 
                              updateFunc=self.state.getWickets, digitFont=Scoreboard.DIGIT_FONT,
                              digitSize=Scoreboard.MEDIUM_DIGIT_SIZE, digitColor=Scoreboard.GREEN, maxDigits=1, 
                              batch=self.batch)
        e.setCenterTop(Scoreboard.CENTER, height)
        self.elements.append(e)

    def addOvers(self, height) :
        e = ScoreboardElement(text='Overs', textFont=Scoreboard.TEXT_FONT, textSize=Scoreboard.MEDIUM_TEXT_SIZE, textColor=Scoreboard.WHITE, 
                              updateFunc=self.state.getOvers, digitFont=Scoreboard.DIGIT_FONT,
                              digitSize=Scoreboard.MEDIUM_DIGIT_SIZE, digitColor=Scoreboard.GREEN, maxDigits=2, 
                              batch=self.batch)
        e.setCenterTop(Scoreboard.CENTER, height)
        self.elements.append(e)

    def addBalls(self, height) :
        e = ScoreboardElement(text='Balls', textFont=Scoreboard.TEXT_FONT, textSize=Scoreboard.MEDIUM_TEXT_SIZE, textColor=Scoreboard.WHITE, 
                              updateFunc=self.state.getBalls, digitFont=Scoreboard.DIGIT_FONT,
                              digitSize=Scoreboard.MEDIUM_DIGIT_SIZE, digitColor=Scoreboard.GREEN, maxDigits=1, 
                              batch=self.batch)
        e.setCenterTop(Scoreboard.LEFT_CENTER, height)
        self.elements.append(e)

    def addLastInnings(self, height) :
        e = ScoreboardElement(text='Last Innings', textFont=Scoreboard.TEXT_FONT, textSize=Scoreboard.MEDIUM_TEXT_SIZE, textColor=Scoreboard.WHITE, 
                              updateFunc=self.state.getLastInnings, digitFont=Scoreboard.DIGIT_FONT,
                              digitSize=Scoreboard.MEDIUM_DIGIT_SIZE, digitColor=Scoreboard.GREEN, maxDigits=3, 
                              batch=self.batch)
        e.setCenterTop(Scoreboard.RIGHT_CENTER, height)
        self.elements.append(e)
        
    def addExtras(self, height) :
        e = ScoreboardElement(text='Extras', textFont=Scoreboard.TEXT_FONT, textSize=Scoreboard.MEDIUM_TEXT_SIZE, textColor=Scoreboard.WHITE, 
                              updateFunc=self.state.getExtras, digitFont=Scoreboard.DIGIT_FONT,
                              digitSize=Scoreboard.MEDIUM_DIGIT_SIZE, digitColor=Scoreboard.RED, maxDigits=1, 
                              batch=self.batch)
        e.setCenterTop(Scoreboard.LEFT_CENTER, height)
        self.elements.append(e)

    def addLastWicket(self, height) :
        e = ScoreboardElement(text='Last Wicket', textFont=Scoreboard.TEXT_FONT, textSize=Scoreboard.MEDIUM_TEXT_SIZE, textColor=Scoreboard.WHITE, 
                              updateFunc=self.state.getLastWicket, digitFont=Scoreboard.DIGIT_FONT,
                              digitSize=Scoreboard.MEDIUM_DIGIT_SIZE, digitColor=Scoreboard.RED, maxDigits=3, 
                              batch=self.batch)
        e.setCenterTop(Scoreboard.RIGHT_CENTER, height)
        self.elements.append(e)
        
    def handle_A(self, modified = False) :
        self.state.modifyExtras(modified)
        self.updateElements()

    def handle_S(self, modified=False) :
        self.state.incrementWickets()
        self.updateElements()

    def handle_Q(self, modified = False) :
        self.state.incrementLeftBatterNumber()
        self.updateElements()

    def handle_E(self, modified = False) :
        self.state.incrementRightBatterNumber()
        self.updateElements()

    def handle_Z(self, modified = False) :
        self.state.modifyLeftBatterRuns(modified)
        self.updateElements()

    def handle_C(self, modified=False) :
        self.state.modifyRightBatterRuns(modified)
        self.updateElements()

    def handle_D(self, modified=False) :
        if (modified) :
            self.state.changeSides()
        else :
            self.state.recordScore()
        self.updateElements()
