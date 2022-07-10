from scoreboard import Scoreboard
from element import ScoreboardElement
from element import HorizontalElement
from game_state import GameState
from functools import partial
import pyglet

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

    def decrementHole(self) :
        self.hole -= 1
    
        
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

    def decrementHoles(self) :
        for g in self.golfers :
            g.decrementHole()

    def getGolfer(self, id) :
        for g in self.golfers :
            if g.getID() == id :
                return g

    def getScoreAsString(self, id) :
        return self.getGolfer(id).getScoreAsString()

    def getHoleAsString(self, id) :
        return self.getGolfer(id).getHoleAsString()

    def getThruAsString(self, id) :
        return self.getGolfer(id).getCompletedHoleAsString()

    def getIDAsString(self, id) :
        return str(self.getGolfer(id).getID())
    
    def getShotsBackAsString(self, id) :
        return str(self.getGolfer(id).getShotsBack())

    def restoreFromList(self, stateList) :
        for g in self.golfers :
            g.id = int(stateList.pop(0).strip('\n'))
            g.score = int(stateList.pop(0).strip('\n'))
            g.hole = int(stateList.pop(0).strip('\n'))
        self.leaders = sorted(self.golfers, key=lambda golfer: golfer.score)
        self.adjustShotsBack()


    def getStateAsList(self) :
        stateList = []
        for g in self.golfers :
            stateList.append(str(int(g.id)) + '\n')
            stateList.append(str(int(g.score)) + '\n')
            stateList.append(str(int(g.hole))  + '\n')
        return stateList
 
##################################

class GolfHole() :
    # position passed is center

    WIDTH = 200
    INTERIOR_SPACING = (4, 0)
    EXTERIOR_SPACING = (2,8)
    DEFAULT_OPACITY = 100
    HIGHLIGHT_OPACITY = 255
    DEFAULT_LABEL = (255,255, 255, 255)
    DIMMED_LABEL = (255,255,255, 180)
    DEFAULT_DIGIT = (255, 0, 0, 255)
    DIMMED_DIGIT = (255,0,0, 200)

    def __init__(self, leftGolfer, rightGolfer, state, position, batch) :

        self.batch = batch
        self.position = position
        self.leftGolfer = leftGolfer
        self.rightGolfer = rightGolfer
        self.group = pyglet.graphics.OrderedGroup(23)
        
        self.leftScore = ScoreboardElement(text=str(leftGolfer), textFont=Scoreboard.TEXT_FONT, textSize=Scoreboard.VERY_SMALL_TEXT_SIZE, textColor=Scoreboard.WHITE,
                              updateFunc=partial(state.getScoreAsString, leftGolfer), digitFont=Scoreboard.DIGIT_FONT,
                              digitSize=Scoreboard.SMALL_DIGIT_SIZE, digitColor=Scoreboard.RED, maxDigits=3, 
                              batch=self.batch)
        self.rightScore = ScoreboardElement(text=str(rightGolfer), textFont=Scoreboard.TEXT_FONT, textSize=Scoreboard.VERY_SMALL_TEXT_SIZE, textColor=Scoreboard.WHITE,
                              updateFunc=partial(state.getScoreAsString, rightGolfer), digitFont=Scoreboard.DIGIT_FONT,
                              digitSize=Scoreboard.SMALL_DIGIT_SIZE, digitColor=Scoreboard.RED, maxDigits=3, 
                              batch=self.batch)

        self.interiorWidth = self.leftScore.getWidth() + self.rightScore.getWidth() + GolfHole.INTERIOR_SPACING[0] 

        self.leftScore.setCenterTop(position[0] - self.interiorWidth // 4, position[1])
        self.rightScore.setCenterTop(position[0] + self.interiorWidth // 4, position[1])

        self.holeNum = HorizontalElement(text=str('On Hole:'), textFont=Scoreboard.TEXT_FONT, textSize=Scoreboard.VERY_SMALL_TEXT_SIZE, textColor=Scoreboard.WHITE,
                              updateFunc=partial(state.getHoleAsString, rightGolfer), digitFont=Scoreboard.DIGIT_FONT,
                              digitSize=Scoreboard.VERY_SMALL_DIGIT_SIZE, digitColor=Scoreboard.RED, maxDigits=2, 
                              batch=self.batch)
        self.holeNum.setCenterTop(position[0], position[1]- GolfHole.INTERIOR_SPACING[1] - self.leftScore.getHeight())

        self.border = self.getBorder((255,255,255))
        self.setSelection(False)

    def setSelection(self, value) :
        if value :
            self.setBorderOpacity(GolfHole.HIGHLIGHT_OPACITY)
            self.setBorderColor((10, 200, 40))
            self.holeNum.setLabelColor(GolfHole.DEFAULT_LABEL)
            self.leftScore.setLabelColor(GolfHole.DEFAULT_LABEL)
            self.rightScore.setLabelColor(GolfHole.DEFAULT_LABEL)
        else :
            self.setBorderOpacity(GolfHole.DEFAULT_OPACITY)
            self.setBorderColor((255,255,255))
            self.holeNum.setLabelColor(GolfHole.DIMMED_LABEL)
            self.leftScore.setLabelColor(GolfHole.DIMMED_LABEL)
            self.rightScore.setLabelColor(GolfHole.DIMMED_LABEL)

    def setBorderOpacity(self, value) :
        for shape in self.border :
            shape.opacity = value

    def setBorderColor(self, color) :
        for shape in self.border :
            shape.color = color
        
        
    def getBorder(self, color) :
        lines = []
        width = self.interiorWidth + GolfHole.EXTERIOR_SPACING[0] * 2
        height = self.leftScore.getHeight() + self.holeNum.getHeight() + GolfHole.EXTERIOR_SPACING[1] * 2
        # bottom left to top left
        lines.append(pyglet.shapes.Line(self.position[0] - width // 2, self.position[1] - height, 
                                        self.position[0] - width // 2, self.position[1], 
                                        width=2, color=color, batch=self.batch, group=self.group))
        #top left to top right
        lines.append(pyglet.shapes.Line(self.position[0] - width // 2, self.position[1], 
                                        self.position[0] + width // 2, self.position[1],
                                        width=2, color=color, batch=self.batch, group=self.group))
        #top right to bottom right
        lines.append(pyglet.shapes.Line(self.position[0] + width // 2, self.position[1],
                                        self.position[0] + width // 2, self.position[1] - height,
                                        width=2, color=color, batch=self.batch, group=self.group))
        #bottom right to bottom left
        lines.append(pyglet.shapes.Line(self.position[0] + width // 2, self.position[1] - height,
                                        self.position[0] - width // 2, self.position[1] - height, 
                                        width=2, color=color, batch=self.batch, group=self.group))
        return lines

    def update(self) :
        self.leftScore.update()
        self.rightScore.update()
        self.holeNum.update()

    def getLeftGolferID(self) :
        return self.leftGolfer
    
    def getRightGolferID(self) :
        return self.rightGolfer


###################################################
class GolfScoreboard(Scoreboard) :
    
    NUM_PAIRINGS = 6
    LEADERBOARD_FONT = 'Built Titling'
    LEADERBOARD_FONT_SIZE = 22
    GREEN = (10, 200, 40, 255)


    POSITIONS = ( (120, 474), (360, 474), (120, 316), (360, 316), (120, 158), (360, 158)  )
    LEADERBOARD_COLS = (540, 610, 690, 770)

    def __init__(self) :
        self.state = GolfGameState()

        Scoreboard.__init__(self)
        self.holes = []
        self.selectedHole = 0

        for i in range(0, GolfScoreboard.NUM_PAIRINGS ) :
            self.holes.append(GolfHole(i*2+1, i*2+2, self.state, GolfScoreboard.POSITIONS[i], self.batch ) )
        
        self.holes[self.selectedHole].setSelection(True)

        self.leaderLabels = []

        self.createLeaderboard()


 
    def createLeaderboard(self) :   
        for label in self.leaderLabels :
            label.delete()

        self.createLeaderBoardColumn(GolfScoreboard.LEADERBOARD_COLS[0], '#', self.state.getIDAsString)
        self.createLeaderBoardColumn(GolfScoreboard.LEADERBOARD_COLS[1], 'THRU', self.state.getThruAsString)
        self.createLeaderBoardColumn(GolfScoreboard.LEADERBOARD_COLS[2], 'PAR', self.state.getScoreAsString)
        self.createLeaderBoardColumn(GolfScoreboard.LEADERBOARD_COLS[3], 'BACK', self.state.getShotsBackAsString)

    def createLeaderBoardColumn(self, x, title, func) :

        header = pyglet.text.Label(title, GolfScoreboard.LEADERBOARD_FONT, GolfScoreboard.LEADERBOARD_FONT_SIZE,
                                        batch=self.batch  )
        header.position = (x, 450)
        header.anchor_x = 'right'
        self.leaderLabels.append(header)
        
        nextRow = 450 - header.content_height
        
        for g in self.state.getLeaderboard() :
            selectedGolfer = (g.getID() == self.holes[self.selectedHole].getLeftGolferID()) or (g.getID() == self.holes[self.selectedHole].getRightGolferID())
            value = func(g.getID())
            golfer =  pyglet.text.Label(value, GolfScoreboard.LEADERBOARD_FONT, GolfScoreboard.LEADERBOARD_FONT_SIZE, color=Scoreboard.OFF_WHITE,
                                        batch=self.batch  )  
            if selectedGolfer :
                golfer.color = GolfScoreboard.GREEN
      
            golfer.position = (x, nextRow)
            golfer.anchor_x = 'right'
            nextRow = nextRow - golfer.content_height
            self.leaderLabels.append(golfer)



    def updateElements(self) :
        for e in self.holes :
            e.update()
        self.createLeaderboard()


    def handle_Z(self, modified=False) :
        self.state.modifyScore(self.holes[self.selectedHole].getLeftGolferID(), -1)
        self.updateElements()

    def handle_A(self, modified=False) :
        self.state.modifyScore(self.holes[self.selectedHole].getLeftGolferID(), 1)
        self.updateElements()

    def handle_D(self, modified=False) :
        self.state.modifyScore(self.holes[self.selectedHole].getRightGolferID(), 1)
        self.updateElements()

    def handle_C(self, modified=False) :
        self.state.modifyScore(self.holes[self.selectedHole].getRightGolferID(), -1)
        self.updateElements()

    def handle_Q(self, modified=False) :
        self.holes[self.selectedHole].setSelection(False)
        self.selectedHole = (self.selectedHole - 1) % len(self.holes)
        self.holes[self.selectedHole].setSelection(True)
        self.updateElements()

    def handle_E(self, modified=False) :
        self.holes[self.selectedHole].setSelection(False)
        self.selectedHole = (self.selectedHole + 1) % len(self.holes)
        self.holes[self.selectedHole].setSelection(True)
        self.updateElements()

    def handle_X(self, modified=False) :
        if modified :
            self.state.decrementHoles()
        else :
            self.state.incrementHoles()
        self.updateElements()

    def handle_S(self, modified=False) :
        self.updateElements()

        
      