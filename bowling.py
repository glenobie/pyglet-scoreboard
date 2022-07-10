from os import truncate
import pyglet

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
               
    def modifyPins(self, playerIndex, frameID, ballIndex, doDecrement) :
        adj = -1 if doDecrement else 1
        self.bowlers[playerIndex].modifyPins(frameID-1, ballIndex, adj)
              
    def getPins(self, playerIndex, frameID, ballIndex) :
        return self.bowlers[playerIndex].frames[frameID-1].getDisplay(ballIndex)

    def getScore(self, playerIndex, frameID) :
        return self.bowlers[playerIndex].getScore(frameID)

    def restoreFromList(self, stateList) :
        for b in self.bowlers :
            numFramesBowled = int(stateList.pop(0).strip('\n'))
            for f in range(0, numFramesBowled) :
                b.frames[f].balls = [int(stateList.pop(0).strip('\n')),
                                    int(stateList.pop(0).strip('\n')),
                                    int(stateList.pop(0).strip('\n'))]
                b.frames[f].empty = False
            b.computeFrameScores()


    def getStateAsList(self) :
        stateList = []
        for b in self.bowlers :
            numFramesBowled = b.getFirstEmptyFrameNumber() - 1 
            stateList.append(str(numFramesBowled) + '\n')
            for f in range(0, numFramesBowled) :
                for ball in  b.frames[f].balls :
                    stateList.append( str(ball) + '\n' )
        return stateList


###########################################################
class FrameDisplay() :
    SPACING_X = 0
    SPACING_Y = 4
    BALL_FONT_SIZE = 23
    SCORE_FONT_SIZE = 23
    DIMMED_OPACITY = 60
    FULL_OPACITY = 230

    def __init__(self, state, frameID, bowlerID, pinsFunc, scoreFunc, batch) :
        self.pinsFunc = pinsFunc
        self.scoreFunc = scoreFunc
        self.batch = batch
        self.state = state
        self.group = pyglet.graphics.OrderedGroup(23)

        self.pins = []

        self.pins.append(ScoreboardElement(text=None, textFont=Scoreboard.TEXT_FONT, textSize=Scoreboard.VERY_SMALL_TEXT_SIZE, textColor=Scoreboard.WHITE,
                              updateFunc=partial(pinsFunc, bowlerID, frameID, 0), digitFont=Scoreboard.DIGIT_FONT,
                              digitSize=FrameDisplay.BALL_FONT_SIZE, digitColor=Scoreboard.RED, maxDigits=1,batch= self.batch))
        self.pins.append(ScoreboardElement(text=None, textFont=Scoreboard.TEXT_FONT, textSize=Scoreboard.VERY_SMALL_TEXT_SIZE, textColor=Scoreboard.WHITE,
                              updateFunc=partial(pinsFunc, bowlerID, frameID, 1), digitFont=Scoreboard.DIGIT_FONT,
                              digitSize=FrameDisplay.BALL_FONT_SIZE, digitColor=Scoreboard.RED, maxDigits=1, batch=self.batch))
        self.score = ScoreboardElement(text=None, textFont=Scoreboard.TEXT_FONT, textSize=Scoreboard.VERY_SMALL_TEXT_SIZE, textColor=Scoreboard.WHITE,
                              updateFunc=partial(scoreFunc, bowlerID, frameID), digitFont=Scoreboard.DIGIT_FONT,
                              digitSize=FrameDisplay.SCORE_FONT_SIZE, digitColor=Scoreboard.RED, maxDigits=3, batch=self.batch)

        self.height = self.pins[0].getHeight() + self.score.getHeight() + FrameDisplay.SPACING_Y  
    

    def drawBorder(self) :
        self.border = []
        x = self.topLeft[0] - 1 # left
        y = self.topLeft[1] + 6 # top 
        x2 = x + self.getWidth() + 2 # right
        y2 = y - self.getHeight() - 8 # bottom

        self.border.append(pyglet.shapes.Line(x, y, x2, y, 1, batch = self.batch, group=self.group)) #top
        self.border.append(pyglet.shapes.Line(x2, y, x2, y2, 1, batch = self.batch, group=self.group)) #right
        self.border.append(pyglet.shapes.Line(x2, y2, x, y2, 1, batch = self.batch, group=self.group)) #bottom
        self.border.append(pyglet.shapes.Line(x, y2, x, y, 1, batch = self.batch, group=self.group)) #left
        
    def update(self) :
        for p in self.pins :
            p.update()
        self.score.update()

    def getWidth(self) :
        return self.score.getWidth() + 2

    def getHeight(self) :
        return self.height

    def setLeftTop(self, x, y) :
        c = x + self.getWidth() // 2 
        self.score.setCenterTop(c, y-self.pins[0].getHeight() - FrameDisplay.SPACING_Y)

        self.pins[0].setRightTop(c - FrameDisplay.SPACING_X, y)
        self.pins[1].setLeftTop(c + FrameDisplay.SPACING_X, y)
        self.topLeft = (x, y)
        self.drawBorder()

    def setSelected(self, isSelected) :
        opacity = FrameDisplay.FULL_OPACITY if isSelected else FrameDisplay.DIMMED_OPACITY
        for line in self.border :
            line.opacity = opacity

class TenthFrameDisplay(FrameDisplay) :
    SPACING_X = 1
    def __init__(self, state, frameID, bowlerID, pinsFunc, scoreFunc, batch) :
        FrameDisplay.__init__(self, state, frameID, bowlerID, pinsFunc, scoreFunc, batch)
        self.pins.append(ScoreboardElement(text=None, textFont=Scoreboard.TEXT_FONT, textSize=Scoreboard.VERY_SMALL_TEXT_SIZE, textColor=Scoreboard.WHITE,
                              updateFunc=partial(pinsFunc, bowlerID, frameID, 2), digitFont=Scoreboard.DIGIT_FONT,
                              digitSize=FrameDisplay.BALL_FONT_SIZE, digitColor=Scoreboard.RED, maxDigits=1, batch=self.batch))

    def getWidth(self) :
        w = 0
        for p in self.pins :
            w += p.getWidth() + TenthFrameDisplay.SPACING_X
        
        return w + TenthFrameDisplay.SPACING_X

    def setLeftTop(self, x, y) : 
        self.topLeft = (x, y)
        self.score.setCenterTop(x + self.getWidth() // 2, 
                                y - self.pins[0].getHeight() - FrameDisplay.SPACING_Y)
        x += TenthFrameDisplay.SPACING_X 
        for p in self.pins :
            p.setLeftTop(x, y)
            x += p.getWidth() + TenthFrameDisplay.SPACING_X
 
        self.drawBorder()

############################################################
class BowlingScoreboard(Scoreboard) :

    FIRST_COLUMN = 54
    ROWS = [400, 300, 200, 100]
    SPACING = 4
    HEADER_Y = 424
    HEADER_X = 14

    def __init__(self) :
        self.state = BowlingGameState()
        Scoreboard.__init__(self)
        self.selectedFrame = 0
        self.inUpper = True
        gp = pyglet.graphics.Group()

        self.frames = [] # FrameDisplays
        self.labels = []

        for i in range(0, len(self.state.bowlers)) :
            rowLabel = pyglet.text.Label('B'+str(i+1), Scoreboard.TEXT_FONT, Scoreboard.SMALL_TEXT_SIZE, batch=self.batch, group=gp)             
            rowLabel.anchor_x = 'left'
            rowLabel.position = (BowlingScoreboard.HEADER_X, BowlingScoreboard.ROWS[i] - 44)
            
            self.labels.append(rowLabel)

        x = BowlingScoreboard.FIRST_COLUMN
        for i in range(0, BowlingGameState.MAX_FRAMES) :
            frameSet = []
            class_ = TenthFrameDisplay if i == BowlingGameState.MAX_FRAMES-1 else FrameDisplay
            for b in range(0, len(self.state.bowlers)) :  
                f = class_(self.state, i+1, b, self.state.getPins, self.state.getScore, self.batch )
                f.setLeftTop(x, BowlingScoreboard.ROWS[b])
                f.setSelected(False)
                self.elements.append(f)
                frameSet.append(f)
    
            self.frames.append(frameSet)
            columnLabel = pyglet.text.Label(str(i+1), Scoreboard.TEXT_FONT, Scoreboard.SMALL_TEXT_SIZE, batch = self.batch, group=gp)             
            columnLabel.anchor_x = 'center'
            columnLabel.position = (x+self.frames[i][0].getWidth() // 2, BowlingScoreboard.HEADER_Y)
            self.labels.append(columnLabel)
            x += self.frames[i][0].getWidth() + BowlingScoreboard.SPACING

        self.selectFrames(self.selectedFrame, True)


    def selectFrames(self, frameId, isSelected) :
        if self.inUpper :
            self.frames[frameId][0].setSelected(isSelected)
            self.frames[frameId][1].setSelected(isSelected)
        else :
            self.frames[frameId][2].setSelected(isSelected)
            self.frames[frameId][3].setSelected(isSelected)
        
    # handle keys

    def handle_Q(self, modified=False) :
        if modified and self.selectedFrame == 9 :
            bowler = 0 if self.inUpper else 2
            self.state.modifyPins(bowler, self.selectedFrame+1, 2, modified)
            self.frames[self.selectedFrame][bowler].update()
        else :
            self.selectFrames(self.selectedFrame, False)
            self.selectedFrame = (self.selectedFrame - 1) % len(self.frames)
            self.selectFrames(self.selectedFrame, True)

    def handle_E(self, modified=False) :
        self.selectFrames(self.selectedFrame, False)
        self.selectedFrame = (self.selectedFrame + 1) % len(self.frames)
        self.selectFrames(self.selectedFrame, True)

    def handle_X(self, modified=False) :
        self.selectFrames(self.selectedFrame, False)
        self.inUpper = not(self.inUpper)
        self.selectFrames(self.selectedFrame, True)

    def handle_A(self, modified=False) :
        bowler = 0 if self.inUpper else 2
        self.state.modifyPins(bowler, self.selectedFrame+1, 0, modified)
        self.frames[self.selectedFrame][bowler].update()

    def handle_D(self, modified=False) :
        bowler = 0 if self.inUpper else 2
        self.state.modifyPins(bowler, self.selectedFrame+1, 1, modified)
        self.frames[self.selectedFrame][bowler].update()

    def handle_Z(self, modified=False) :
        bowler = 1 if self.inUpper else 3
        self.state.modifyPins(bowler, self.selectedFrame+1, 0, modified)
        self.frames[self.selectedFrame][bowler].update()

    def handle_C(self, modified=False) :
        bowler = 1 if self.inUpper else 3
        self.state.modifyPins(bowler, self.selectedFrame+1, 1, modified)
        self.frames[self.selectedFrame][bowler].update()

    def handle_S(self, modified=False):
        0

