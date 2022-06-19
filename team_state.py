# 

class TeamState :
    def __init__(self, score, maxScore) : 
        self.score = score
        self.maxScore = maxScore

    def getScore(self) :
        return self.score

    def decrementScore(self) :
        self.score -= 1
        if self.score < 0 :
            self.score = 0

    def incrementScore(self) :
        if (self.score < self.maxScore) :
            self.score += 1 

    def resetScore(self) :
        self.score = 0

##############################################################

class TeamStateWithTimeouts(TeamState) :
    def __init__(self, score, maxScore, maxTimeouts) :
        TeamState.__init__(self, score, maxScore) 
        self.maxTimeouts = maxTimeouts
        self.timeoutsTaken = 0

    def modifyTimeoutsTaken(self, value) :
        self.timeoutsTaken += value
        if (self.timeoutsTaken > self.maxTimeouts) :
            self.timeoutsTaken = self.maxTimeouts
        elif (self.timeoutsTaken < 0) :
            self.timeoutsTaken = 0
  
    def getTimeoutsTaken(self):
        return self.timeoutsTaken