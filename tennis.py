from scoreboard import Scoreboard
from game_state import GameState

class TennisPlayer() :

    POINTS = [" 0", "15", "30", "40", "AD"] #99 for AD
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
    def __init__(self) :
        Scoreboard.__init__(self)
        self.state = TennisGameState()