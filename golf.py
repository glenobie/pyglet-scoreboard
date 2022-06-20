from scoreboard import Scoreboard
from element import ScoreboardElement
from game_state import GameState

#################################
class Golfer() :

    def __init__(self, id, startHole) :
        self.score = 0
        self.id = id
        self.hole = startHole
        self.shotsBack = 0

    def getScore(self) :
        return self.score

    def getScoreAsString(self) :
        if self.score == 0 :
            return "E"
        elif self.score > 0 :
            return "+" + str(self.score)
        return str(self.score)

    def getShotsBack(self) :
        return self.shotsBack

    def adjustScore(self, value) :
        self.score += value

    def getHole(self) :
        return self.hole

    def getHoleAsString(self) :
        if self.hole < 1 :
            return "-"
        elif self.hole > 18 :
            return "18"
        else :
            return str(self.hole)

    def getCompletedHoleAsString(self) :
        c = self.hole - 1
        if c < 1 :
            return "0"
        elif c > 18 :
            return "18"
        else :
            return str(c)
       

    def getID(self) :
        return self.id

    def computeShotsBack(self, leaderScore) :
        self.shotsBack = self.score - leaderScore

    def incrementHole(self) :
        self.hole += 1
    
        
class GolfGameState(GameState) :
    
    NUM_GOLFERS = 12
    START_HOLES = [1, 1, 0, 0, -1, -1, -2, -2, -3, -3, -4, -4]

    def __init__(self):
        #invoking the __init__ of the parent class 
        GameState.__init__(self) 
 
        self.golfers = []
        for i in range(GolfGameState.NUM_GOLFERS) :
            self.golfers.append(Golfer(i+1, GolfGameState.START_HOLES[i]))
            
        self.leaders = sorted(self.golfers, key=lambda golfer: golfer.score)
        self.adjustShotsBack()


    def adjustShotsBack(self) :
        for g in self.golfers :
            g.computeShotsBack(self.leaders[0].getScore())

    def modifyScore(self, golferID, adj) :
        self.golfers[golferID-1].adjustScore(adj)
        self.leaders = sorted(self.golfers, key=lambda golfer: golfer.score)
        self.adjustShotsBack()


    def getLeaderboard(self) :
        return self.leaders

    def getGolfers(self) :
        return self.golfers

    def incrementHoles(self) :
        for g in self.golfers :
            g.incrementHole()

    def getGolfer(self, id) :
        for g in self.golfers :
            if g.getID() == id :
                return g
 
    ##################################
class GolfScoreboard(Scoreboard) :
    def __init__(self) :
        Scoreboard.__init__(self)
        self.state = GolfGameState()
        
      