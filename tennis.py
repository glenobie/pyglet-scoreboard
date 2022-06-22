from scoreboard import Scoreboard
from game_state import GameState
from element import ScoreboardElement
from element import HorizontalElement

from functools import partial

class TennisPlayer() :

    POINTS = ["0", "15", "30", "40", "AD"] #99 for AD
    NUM_POINTS = 5

    def __init__(self, serving) :
        self.pointsIndex = 0
        self.sets = [0,0,0,0,0]
        self.serving = serving

    def changeServing(self) :
        self.serving = not(self.serving)
    

class TennisGameState(GameState) :
    
    MAX_GAMES = 7
    NUM_SETS = 5

    def __init__(self):
        #invoking the __init__ of the parent class 
        GameState.__init__(self) 
 
        self.players = [TennisPlayer(True), TennisPlayer(False)]

    def modifyTime(self, t=False) :
        for p in self.players :
            p.changeServing()
        
    def getPlayerSets(self, playerIndex ):
        return self.players[playerIndex].sets

    def getGames(self, playerIndex, setIndex) :
        return self.players[playerIndex].sets[setIndex]

    def getServing(self, playerIndex) :
        if self.players[playerIndex].serving :
            return '*'
        else :
            return ''


    def modifyGames(self, playerIndex, setIndex, doDecrement) :
        adj = 1
        if doDecrement : adj = -1
        self.players[playerIndex].sets[setIndex] = (self.players[playerIndex].sets[setIndex] + adj) % (TennisGameState.MAX_GAMES + 1)
                
    def modifyPoints(self, playerIndex, doDecrement) :
        adj = 1
        if doDecrement : adj = -1
        self.players[playerIndex].pointsIndex = (self.players[playerIndex].pointsIndex + adj) % TennisPlayer.NUM_POINTS

    def getPoints(self, playerIndex) :
        return TennisPlayer.POINTS[self.players[playerIndex].pointsIndex]

##################################
class TennisScoreboard(Scoreboard) :

    P1_Y = 360
    P2_Y = 240

    COLS = [194, 418, 498, 578, 658, 738]
  
    def __init__(self) :
        Scoreboard.__init__(self)
        self.state = TennisGameState()
        self.state.modifyPoints(0,False)
        self.selectedSet = 0

        self.P1_sets = []
        self.P2_sets = []

        self.addPoints(TennisScoreboard.COLS[0], TennisScoreboard.P1_Y, 0, 'Player 1')
        self.addPoints(TennisScoreboard.COLS[0], TennisScoreboard.P2_Y, 1, 'Player 2')

        self.addBall(12, TennisScoreboard.P1_Y-20, 0)
        self.addBall(12, TennisScoreboard.P2_Y-20, 1)

        for i in range(0, len(self.state.getPlayerSets(0)) ) :
            self.P1_sets.append(self.addGames(TennisScoreboard.COLS[i+1], TennisScoreboard.P1_Y, 0, i))
            self.P2_sets.append(self.addGames(TennisScoreboard.COLS[i+1], TennisScoreboard.P2_Y, 1, i))

        self.colorSet(self.selectedSet, Scoreboard.GREEN)
    
    def colorSet(self, setNum, color) :
        self.P1_sets[setNum].setFontColor(color)
        self.P2_sets[setNum].setFontColor(color)

    def addBall(self, x, y, player) :
        e = ScoreboardElement(text=None, textFont='', textSize=Scoreboard.VERY_SMALL_DIGIT_SIZE, textColor=Scoreboard.WHITE,
                              updateFunc=partial(self.state.getServing, player), digitFont=Scoreboard.DIGIT_FONT,
                              digitSize=Scoreboard.VERY_SMALL_DIGIT_SIZE, digitColor=Scoreboard.YELLOW, maxDigits=1, 
                              batch=self.batch)
        e.setLeftTop(x,y)
        self.elements.append(e)
         

    def addGames(self, x, y, player, set) :
        e = ScoreboardElement(text=None, textFont=Scoreboard.TEXT_FONT, textSize=Scoreboard.LARGE_TEXT_SIZE, textColor=Scoreboard.WHITE,
                              updateFunc=partial(self.state.getGames, player, set), digitFont=Scoreboard.DIGIT_FONT,
                              digitSize=Scoreboard.SCORE_SIZE, digitColor=Scoreboard.RED, maxDigits=1, 
                              batch=self.batch)
        e.setCenterTop(x,y)
        self.elements.append(e)
        return e


    def addPoints(self, x, y, player, text) :

        e = HorizontalElement(text=text, textFont=Scoreboard.TEXT_FONT, textSize=Scoreboard.LARGE_TEXT_SIZE, textColor=Scoreboard.WHITE,
                              updateFunc=partial(self.state.getPoints, player), digitFont=Scoreboard.DIGIT_FONT,
                              digitSize=Scoreboard.SCORE_SIZE, digitColor=Scoreboard.GREEN, maxDigits=2, 
                              batch=self.batch)
        e.setCenterTop(x,y)
        self.elements.append(e)

    def handle_Z(self, modified=False) :
        self.state.modifyPoints(0, modified)
        self.updateElements()

    def handle_C(self, modified=False) :
        self.state.modifyPoints(1, modified)
        self.updateElements()

    def handle_A(self, modified=False) :
        self.state.modifyGames(0, self.selectedSet, modified)
        self.updateElements()

    def handle_D(self, modified=False) :
        self.state.modifyGames(1, self.selectedSet, modified)
        self.updateElements()

    def handle_Q(self, modified=False) :
        self.colorSet(self.selectedSet, Scoreboard.RED)
        self.selectedSet = (self.selectedSet - 1) % len(self.state.getPlayerSets(0))
        self.colorSet(self.selectedSet, Scoreboard.GREEN)

        self.updateElements()

    def handle_E(self, modified=False) :
        self.colorSet(self.selectedSet, Scoreboard.RED)
        self.selectedSet = (self.selectedSet + 1) % len(self.state.getPlayerSets(0))
        self.colorSet(self.selectedSet, Scoreboard.GREEN)
        self.updateElements()

    def handle_S(self, modified=False) :
        self.updateElements()
