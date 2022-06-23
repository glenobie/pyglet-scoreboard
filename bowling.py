from scoreboard import Scoreboard
from element import ScoreboardElement
from game_state import GameState
from functools import partial

class Frame() :
    SPARE = 10
    STRIKE = 11
    PINS = [ "-", "1", "2", "3", "4", "5", "6", "7", "8", "9", "/", "X"]
    VALUES = [0,1,2,3,4,5,6,7,8,9,10,10]
    BALL_1_SCORES = 10
    NUM_SCORES = 12
  
    def __init__(self, value) :
        self.balls = [0,0,0] # index into PINS
        self.value = value # number of frame: 1 to 10
        self.empty = True
     
    def numPins(value) :
        if value > 10 :
            return 10
        else :
            return value

    def isSpare(self) :
        return self.balls[1] == Frame.SPARE

    def isStrike(self) :
        return self.balls[1] == Frame.STRIKE
    
    def isEmpty( self ) :
        return self.empty

    def getDisplay(self, index) :
        if self.isEmpty() : 
            return " "
        else :
            return Frame.PINS[self.balls[index]]

    def isTenth(self) :
        return self.value == 10

    def modifyPins(self, ballIndex, value) :
        self.empty = False
        if (ballIndex == 0 and not(self.isTenth())) :
            self.balls[ballIndex] = ( self.balls[ballIndex] + value) % Frame.BALL_1_SCORES
        else :
            self.balls[ballIndex] = ( self.balls[ballIndex] + value ) % Frame.NUM_SCORES
 
    def getBalls(self) :
        ballsList = []
        if self.isTenth() :
            ballsList.append(Frame.VALUES[self.balls[0]])
            ballsList.append(Frame.VALUES[self.balls[1]])
            ballsList.append(Frame.VALUES[self.balls[2]])

        elif self.isStrike() :
            ballsList.append(10)
        elif not(self.isEmpty()):
            ballsList.append( self.balls[0] )
            if self.isSpare() :
                ballsList.append(10-self.balls[0])
            else :
                ballsList.append( self.balls[1] )
        return ballsList

#############################################################################
             
class Bowler() :

    def __init__(self) :
        self.frames = []
        for i in range(BowlingGameState.MAX_FRAMES) :
            self.frames.append( Frame(i+1) )
        self.scores = [0,0,0,0,0,0,0,0,0,0]

    def modifyPins(self, frameIndex, ballIndex, value) :
        # can only change empty frame if its first empty frame
        if frameIndex < self.getFirstEmptyFrameNumber() :
          self.frames[frameIndex].modifyPins(ballIndex, value)
          self.computeFrameScores()

    def computeStrikeFrame(self, frameIndex) :
        frameNum = frameIndex + 1       
        score = 0 
        if (frameNum < BowlingGameState.MAX_FRAMES)  :
            next2Balls = self.frames[frameIndex+1].getBalls()
            if (frameNum < 9) :
                f2Balls = self.frames[frameIndex+2].getBalls()
                for b in f2Balls :
                    next2Balls.append(b)            
            if len(next2Balls) > 1 :
                score = 10 + next2Balls[0] + next2Balls[1]
        return score        

    def computeSpareFrame(self, frameIndex) :
        frameNum = frameIndex + 1
        score = 0
        if (frameNum < BowlingGameState.MAX_FRAMES)  :
            nextBalls = self.frames[frameIndex+1].getBalls()
            if len(nextBalls) > 0 :
                score += 10 + nextBalls[0]
        return score

    def computeTenthFrame(self) :
        nextBalls = self.frames[9].getBalls()
        score = 0
        for b in nextBalls :
            score += b
        return score

    def computeFrameScores(self) :
        self.scores = []
        score = 0
        index = 0
        for f in self.frames :
            if f.isTenth() :
                score += self.computeTenthFrame()
            elif f.isStrike() :
                score += self.computeStrikeFrame(index)
            elif f.isSpare() :
                score += self.computeSpareFrame(index)
            else :
                for b in f.getBalls() :
                    score += b
            self.scores.append (score)
            index += 1

    def getScore(self, frameNumber) :
        if frameNumber >= self.getFirstEmptyFrameNumber()  :
            return "-"
        else :
            return self.scores[frameNumber-1]

    def getFirstEmptyFrameNumber(self) :
        for i in range(BowlingGameState.MAX_FRAMES) :
            if self.frames[i].isEmpty() :
                return i+1
        return BowlingGameState.MAX_FRAMES+1

################################################################      
class BowlingGameState(GameState) :

    MAX_FRAMES = 10

    def __init__(self):
        #invoking the __init__ of the parent class 
        GameState.__init__(self) 
        self.bowlers = [Bowler(), Bowler(), Bowler(), Bowler()]

    def modifyTime(self, t=False) :
        0
        
    def getPlayerFrames(self, playerIndex ):
        return self.bowlers[playerIndex].frames
               
    def modifyPins(self, playerIndex, frameIndex, ballIndex, doDecrement) :
        adj = 1
        if doDecrement : adj = -1
        p = self.bowlers[playerIndex].modifyPins(frameIndex, ballIndex, adj)
              
    def getPins(self, playerIndex, frameIndex, ballIndex) :
        return self.bowlers[playerIndex].frames[frameIndex-1].getDisplay(ballIndex)

    def getScore(self, playerIndex, frameIndex) :
        return self.bowlers[playerIndex].getScore(frameIndex)
    

###########################################################
class FrameDisplay() :
    SPACING_X = 8
    SPACING_Y = 4
    BALL_FONT_SIZE = 24
    SCORE_FONT_SIZE = 24

    def __init__(self, state, frameID, bowlerID, pinsFunc, scoreFunc, batch) :
        self.pinsFunc = pinsFunc
        self.scoreFunc = scoreFunc
        
        self.pins1 = ScoreboardElement(text=None, textFont=Scoreboard.TEXT_FONT, textSize=Scoreboard.VERY_SMALL_TEXT_SIZE, textColor=Scoreboard.WHITE,
                              updateFunc=partial(pinsFunc, bowlerID, frameID, 0), digitFont=Scoreboard.DIGIT_FONT,
                              digitSize=FrameDisplay.BALL_FONT_SIZE, digitColor=Scoreboard.RED, maxDigits=1, batch=batch)
        self.pins2 = ScoreboardElement(text=None, textFont=Scoreboard.TEXT_FONT, textSize=Scoreboard.VERY_SMALL_TEXT_SIZE, textColor=Scoreboard.WHITE,
                              updateFunc=partial(pinsFunc, bowlerID, frameID, 1), digitFont=Scoreboard.DIGIT_FONT,
                              digitSize=FrameDisplay.BALL_FONT_SIZE, digitColor=Scoreboard.RED, maxDigits=1, batch=batch)
        self.score = ScoreboardElement(text=None, textFont=Scoreboard.TEXT_FONT, textSize=Scoreboard.VERY_SMALL_TEXT_SIZE, textColor=Scoreboard.WHITE,
                              updateFunc=partial(scoreFunc, bowlerID, frameID), digitFont=Scoreboard.DIGIT_FONT,
                              digitSize=FrameDisplay.SCORE_FONT_SIZE, digitColor=Scoreboard.RED, maxDigits=3, batch=batch)
                            
    def update(self) :
        self.pins1.update()
        self.pins2.update()
        self.score.update()

    def getWidth(self) :
        return self.score.getWidth()

    def setCenterTop(self, x, y) :
        self.pins1.setRightTop(x - FrameDisplay.SPACING_X, y)
        self.pins2.setLeftTop(x + FrameDisplay.SPACING_X, y)
        self.score.setCenterTop(x, y-self.pins1.getHeight() - FrameDisplay.SPACING_Y)

class BowlingScoreboard(Scoreboard) :

    FIRST_COLUMN = 100
    ROWS = [100, 200, 300, 400]
    SPACING = 4

    def __init__(self) :
        Scoreboard.__init__(self)
        self.state = BowlingGameState()

        self.frames = []

        for i in range(0, BowlingGameState.MAX_FRAMES) :
            for b in range(0, len(self.state.bowlers)) :
                f = FrameDisplay(self.state, i+1, b, self.state.getPins, self.state.getScore, self.batch )
                f.setCenterTop(BowlingScoreboard.FIRST_COLUMN + i*f.getWidth()+i*BowlingScoreboard.SPACING, BowlingScoreboard.ROWS[b])
                self.frames.append(f)

        