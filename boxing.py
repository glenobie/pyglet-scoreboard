from game_state import TimedGameState
from game_state import TeamState
from scoreboard import Scoreboard
from element import ScoreboardElement


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

    def getLeftEndurance(self) :
        return self.getEndurance(0)
    
    def getRightEndurance(self) :
        return self.getEndurance(1)

    def getTkoPoints(self, team) :
        return self.teams[team].getTkoPoints()
 
    def getLeftTkoPoints(self) :
        return self.getTkoPoints(0)

    def getRightTkoPoints(self) :
        return self.getTkoPoints(1)

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

    LEFT_DIGIT_COLOR = (255,0,0,255)
    RIGHT_DIGIT_COLOR = (0,0,255,255)
    
    def __init__(self) :
        Scoreboard.__init__(self)
        self.state = BoxingGameState()
        
        self.addScores(2, leftLabel='RED', rightLabel='Blue')
        self.addClock(440)
        self.addPeriod(300, maxDigits=2)

        self.addEndurance(280)
        self.addTkoPoints(140)

    def addScores(self, maxDigits, leftLabel='GUEST', rightLabel='HOME') :
        e = ScoreboardElement(text=leftLabel, textFont=Scoreboard.TEXT_FONT, textSize=Scoreboard.LARGE_TEXT_SIZE, textColor=Scoreboard.WHITE,
                              updateFunc=self.state.getGuestScore, digitFont=Scoreboard.DIGIT_FONT,
                              digitSize=Scoreboard.SCORE_SIZE, digitColor=BoxingScoreboard.LEFT_DIGIT_COLOR, maxDigits=maxDigits, 
                              batch=self.batch)
        e.setCenterTop(Scoreboard.LEFT_CENTER,460)
        self.elements.append(e)

        e = ScoreboardElement(text=rightLabel, textFont=Scoreboard.TEXT_FONT, textSize=Scoreboard.LARGE_TEXT_SIZE, textColor=Scoreboard.WHITE,
                              updateFunc=self.state.getHomeScore, digitFont=Scoreboard.DIGIT_FONT,
                              digitSize=Scoreboard.SCORE_SIZE, digitColor=BoxingScoreboard.RIGHT_DIGIT_COLOR, maxDigits=maxDigits,  
                              batch=self.batch)
        e.setCenterTop(Scoreboard.RIGHT_CENTER,460)
        self.elements.append(e)


    def addEndurance(self, height) :
        e = ScoreboardElement(text='Endurance', textFont=Scoreboard.TEXT_FONT, textSize=Scoreboard.MEDIUM_TEXT_SIZE, textColor=Scoreboard.WHITE, 
                              updateFunc=self.state.getLeftEndurance, digitFont=Scoreboard.DIGIT_FONT,
                              digitSize=Scoreboard.MEDIUM_DIGIT_SIZE, digitColor=BoxingScoreboard.LEFT_DIGIT_COLOR, maxDigits=2, 
                              batch=self.batch)
        e.setCenterTop(Scoreboard.LEFT_CENTER, height)
        self.elements.append(e)

        e = ScoreboardElement(text='Endurance', textFont=Scoreboard.TEXT_FONT, textSize=Scoreboard.MEDIUM_TEXT_SIZE, textColor=Scoreboard.WHITE,
                              updateFunc=self.state.getRightEndurance, digitFont=Scoreboard.DIGIT_FONT,
                              digitSize=Scoreboard.MEDIUM_DIGIT_SIZE, digitColor=BoxingScoreboard.RIGHT_DIGIT_COLOR, maxDigits=2,  
                              batch=self.batch)
        e.setCenterTop(Scoreboard.RIGHT_CENTER, height)
        self.elements.append(e)


    def addTkoPoints(self, height) :
        e = ScoreboardElement(text='TKO Points', textFont=Scoreboard.TEXT_FONT, textSize=Scoreboard.MEDIUM_TEXT_SIZE, textColor=Scoreboard.WHITE, 
                              updateFunc=self.state.getLeftTkoPoints, digitFont=Scoreboard.DIGIT_FONT,
                              digitSize=Scoreboard.MEDIUM_DIGIT_SIZE, digitColor=BoxingScoreboard.LEFT_DIGIT_COLOR, maxDigits=2, 
                              batch=self.batch)
        e.setCenterTop(Scoreboard.LEFT_CENTER, height)
        self.elements.append(e)

        e = ScoreboardElement(text='TKO Points', textFont=Scoreboard.TEXT_FONT, textSize=Scoreboard.MEDIUM_TEXT_SIZE, textColor=Scoreboard.WHITE,
                             updateFunc=self.state.getRightTkoPoints, digitFont=Scoreboard.DIGIT_FONT,
                              digitSize=Scoreboard.MEDIUM_DIGIT_SIZE, digitColor=BoxingScoreboard.RIGHT_DIGIT_COLOR, maxDigits=2,  
                              batch=self.batch)
        e.setCenterTop(Scoreboard.RIGHT_CENTER, height)
        self.elements.append(e)


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
 