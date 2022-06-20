from audioop import add
from team_state import TeamStateWithTimeouts
from game_state import TimedGameState
from scoreboard import Scoreboard
from element import ScoreboardElement


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

    def getGuestTeamFouls(self) :
        return self.getTeamFouls(0)

    def getHomeTeamFouls(self) :
        return self.getTeamFouls(1)

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

        self.addTeamFouls(300)
        self.addTimeouts(160)

    def addTimeouts(self, height) :
        e = ScoreboardElement(text='Timeouts', textFont=Scoreboard.TEXT_FONT, textSize=Scoreboard.MEDIUM_TEXT_SIZE, textColor=Scoreboard.WHITE, 
                              updateFunc=self.state.getGuestTimeoutsTaken, digitFont=Scoreboard.DIGIT_FONT,
                              digitSize=Scoreboard.MEDIUM_DIGIT_SIZE, digitColor=Scoreboard.RED, maxDigits=2, 
                              batch=self.batch)
        e.setCenterTop(Scoreboard.LEFT_CENTER, height)
        self.elements.append(e)

        e = ScoreboardElement(text='Timeouts', textFont=Scoreboard.TEXT_FONT, textSize=Scoreboard.MEDIUM_TEXT_SIZE, textColor=Scoreboard.WHITE,
                              updateFunc=self.state.getHomeTimeoutsTaken, digitFont=Scoreboard.DIGIT_FONT,
                              digitSize=Scoreboard.MEDIUM_DIGIT_SIZE, digitColor=Scoreboard.RED, maxDigits=2,  
                              batch=self.batch)
        e.setCenterTop(Scoreboard.RIGHT_CENTER, height)
        self.elements.append(e)


    def addTeamFouls(self, height) :
        e = ScoreboardElement(text='Team Fouls', textFont=Scoreboard.TEXT_FONT, textSize=Scoreboard.MEDIUM_TEXT_SIZE, textColor=Scoreboard.WHITE, 
                              updateFunc=self.state.getGuestTeamFouls, digitFont=Scoreboard.DIGIT_FONT,
                              digitSize=Scoreboard.MEDIUM_DIGIT_SIZE, digitColor=Scoreboard.RED, maxDigits=2, 
                              batch=self.batch)
        e.setCenterTop(Scoreboard.LEFT_CENTER, height)
        self.elements.append(e)

        e = ScoreboardElement(text='Team Fouls', textFont=Scoreboard.TEXT_FONT, textSize=Scoreboard.MEDIUM_TEXT_SIZE, textColor=Scoreboard.WHITE,
                             updateFunc=self.state.getHomeTeamFouls, digitFont=Scoreboard.DIGIT_FONT,
                              digitSize=Scoreboard.MEDIUM_DIGIT_SIZE, digitColor=Scoreboard.RED, maxDigits=2,  
                              batch=self.batch)
        e.setCenterTop(Scoreboard.RIGHT_CENTER, height)
        self.elements.append(e)


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
 

    
        