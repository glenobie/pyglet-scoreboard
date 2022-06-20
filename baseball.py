from scoreboard import Scoreboard
from element import ScoreboardElement
from game_state import GameState
from team_state import TeamState


#########################
class BaseballTeamState(TeamState) :
    def __init__(self, score, maxScore) :
        TeamState.__init__(self, score, maxScore)
        self.hits = 0
        self.errors = 0

    def getErrors(self) :
        return self.errors

    def getHits(self) :
        return self.hits

    def modifyHits(self, value) :
        self.hits += value
        if self.hits < 0 :
            self.hits = 0
    
    def modifyErrors(self, value) :
        self.errors += value
        if self.errors < 0 :
            self.errors = 0
  
###########################################
class BaseballGameState(GameState) :
    
    def __init__(self):
        #invoking the __init__ of the parent class 
        GameState.__init__(self) 
        self.maxScore = 99
        self.teams = [BaseballTeamState(0, self.getMaxScore() ), 
                      BaseballTeamState(0, self.getMaxScore() )]
        self.inning = 1
        self.outs = 0
        self.teamAtBat = GameState.GUEST_INDEX

    def getHits(self, team) :
        return self.teams[team].getHits()

    def getLeftHits(self) :
        return self.getHits(0)
    
    def getRightHits(self) :
        return self.getHits(1)

    def getErrors(self, team) :
        return self.teams[team].getErrors()

    def getLeftErrors(self) :
        return self.getErrors(0)
    
    def getRightErrors(self) :
        return self.getErrors(1)

    def changeSides(self) :
        self.teamAtBat = (self.teamAtBat + 1) % 2
        if self.teamAtBat == GameState.GUEST_INDEX :
                self.inning += 1

    def undoSideChange(self) :
        if not(self.isGameStart()) :
            self.teamAtBat = (self.teamAtBat - 1) % 2
            if (self.teamAtBat == GameState.HOME_INDEX) :
                self.inning -= 1

    def modifyHits(self, team, doDecrement=False) :
        if doDecrement :
            self.teams[team].modifyHits(-1)
        else:
            self.teams[team].modifyHits(1)

    def modifyErrors(self, team, doDecrement=False) :
        if doDecrement :
            self.teams[team].modifyErrors(-1)
        else:
            self.teams[team].modifyErrors(1)

    def isGameStart(self) :
        return (self.inning == 1 and self.teamAtBat == GameState.GUEST_INDEX)
 
    def modifyTime(self, doDecrement=False) :
        if (doDecrement) :
            self.undoSideChange()
        else:
            self.changeSides()
            
    def modifyOuts(self) :
        self.outs = (self.outs+1) % 3

    def modifyPeriod(self) :
        self.modifyOuts()

    def getOuts(self) :
        return self.outs
    
    def getInning(self) :
        return self.inning

    def getHalfInning(self) :
        if self.teamAtBat == GameState.GUEST_INDEX :
            s = "TOP"
        else :
            s = "BTM"
        return s

    def getTeamAtBat(self) :
        return self.teamAtBat
    
##################################
class BaseballScoreboard(Scoreboard) :
    def __init__(self) :
        Scoreboard.__init__(self)
        self.state = BaseballGameState()
        
        self.addScores(2, 470)

        self.addHits(300)
        self.addErrors(160)
        self.addOuts(290)
        self.addInnings(460)



        self.top = ScoreboardElement(text=None, textFont=Scoreboard.TEXT_FONT, textSize=Scoreboard.MEDIUM_TEXT_SIZE, textColor=Scoreboard.WHITE, 
                              updateFunc=self.state.getHalfInning, digitFont=Scoreboard.DIGIT_FONT,
                              digitSize=Scoreboard.VERY_SMALL_DIGIT_SIZE, digitColor=Scoreboard.GREEN, maxDigits=3, 
                              batch=self.batch)
        self.top.setCenterTop(300, 395)
        self.elements.append(self.top)
        self.top.setOn(self.state.getTeamAtBat() == GameState.GUEST_INDEX)

        self.bottom = ScoreboardElement(text=None, textFont=Scoreboard.TEXT_FONT, textSize=Scoreboard.MEDIUM_TEXT_SIZE, textColor=Scoreboard.WHITE, 
                              updateFunc=self.state.getHalfInning, digitFont=Scoreboard.DIGIT_FONT,
                              digitSize=Scoreboard.VERY_SMALL_DIGIT_SIZE, digitColor=Scoreboard.GREEN, maxDigits=3, 
                              batch=self.batch)
        self.bottom.setCenterTop(500, 370)
        self.elements.append(self.bottom)
        self.bottom.setOn(self.state.getTeamAtBat() == GameState.HOME_INDEX)

    def addInnings(self, height) :
        e = ScoreboardElement(text='Inning', textFont=Scoreboard.TEXT_FONT, textSize=Scoreboard.MEDIUM_TEXT_SIZE, textColor=Scoreboard.WHITE, 
                              updateFunc=self.state.getInning, digitFont=Scoreboard.DIGIT_FONT,
                              digitSize=Scoreboard.MEDIUM_DIGIT_SIZE, digitColor=Scoreboard.GREEN, maxDigits=2, 
                              batch=self.batch)
        e.setCenterTop(Scoreboard.CENTER, height)
        self.elements.append(e)


    def addOuts(self, height) :
        e = ScoreboardElement(text='Outs', textFont=Scoreboard.TEXT_FONT, textSize=Scoreboard.MEDIUM_TEXT_SIZE, textColor=Scoreboard.WHITE, 
                              updateFunc=self.state.getOuts, digitFont=Scoreboard.DIGIT_FONT,
                              digitSize=Scoreboard.MEDIUM_DIGIT_SIZE, digitColor=Scoreboard.GREEN, maxDigits=1, 
                              batch=self.batch)
        e.setCenterTop(Scoreboard.CENTER, height)
        self.elements.append(e)
       

    def addErrors(self, height) :
        e = ScoreboardElement(text='Errors', textFont=Scoreboard.TEXT_FONT, textSize=Scoreboard.MEDIUM_TEXT_SIZE, textColor=Scoreboard.WHITE, 
                              updateFunc=self.state.getLeftErrors, digitFont=Scoreboard.DIGIT_FONT,
                              digitSize=Scoreboard.MEDIUM_DIGIT_SIZE, digitColor=Scoreboard.RED, maxDigits=2, 
                              batch=self.batch)
        e.setCenterTop(Scoreboard.LEFT_CENTER, height)
        self.elements.append(e)

        e = ScoreboardElement(text='Errors', textFont=Scoreboard.TEXT_FONT, textSize=Scoreboard.MEDIUM_TEXT_SIZE, textColor=Scoreboard.WHITE,
                              updateFunc=self.state.getRightErrors, digitFont=Scoreboard.DIGIT_FONT,
                              digitSize=Scoreboard.MEDIUM_DIGIT_SIZE, digitColor=Scoreboard.RED, maxDigits=2,  
                              batch=self.batch)
        e.setCenterTop(Scoreboard.RIGHT_CENTER, height)
        self.elements.append(e)


    def addHits(self, height) :
        e = ScoreboardElement(text='Hits', textFont=Scoreboard.TEXT_FONT, textSize=Scoreboard.MEDIUM_TEXT_SIZE, textColor=Scoreboard.WHITE, 
                              updateFunc=self.state.getLeftHits, digitFont=Scoreboard.DIGIT_FONT,
                              digitSize=Scoreboard.MEDIUM_DIGIT_SIZE, digitColor=Scoreboard.RED, maxDigits=2, 
                              batch=self.batch)
        e.setCenterTop(Scoreboard.LEFT_CENTER, height)
        self.elements.append(e)

        e = ScoreboardElement(text='Hits', textFont=Scoreboard.TEXT_FONT, textSize=Scoreboard.MEDIUM_TEXT_SIZE, textColor=Scoreboard.WHITE,
                             updateFunc=self.state.getRightHits, digitFont=Scoreboard.DIGIT_FONT,
                              digitSize=Scoreboard.MEDIUM_DIGIT_SIZE, digitColor=Scoreboard.RED, maxDigits=2,  
                              batch=self.batch)
        e.setCenterTop(Scoreboard.RIGHT_CENTER, height)
        self.elements.append(e)


    def handle_A(self, modified = False) :
        self.state.modifyHits(0, modified)
        self.updateElements()

    def handle_D(self, modified = False) :
        self.state.modifyHits(1, modified)
        self.updateElements()
 
    def handle_Q(self, modified = False) :
        self.state.modifyErrors(0, modified)
        self.updateElements()

    def handle_E(self, modified = False) :
        self.state.modifyErrors(1, modified)
        self.updateElements()
 
    def handle_X(self, modified=False) :
        self.state.modifyTime(modified)
        self.top.setOn(self.state.getTeamAtBat() == GameState.GUEST_INDEX)
        self.bottom.setOn(self.state.getTeamAtBat() == GameState.HOME_INDEX)
        self.updateElements()
