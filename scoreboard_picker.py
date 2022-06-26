import socket
import pyglet
from pyglet import font
from key_handler import KeyHandler
from config_screen import ConfigScreen

class MenuLocationNode :
    IS_EMPTY = -1

    def __init__(self, location) :
        self.location = location
        self.setFront(self)
        self.setBack(self) 
        self.stagedIndex = MenuLocationNode.IS_EMPTY
        self.index = MenuLocationNode.IS_EMPTY

    def setIndex(self, index) :
        self.index = index
    
    def setStagedIndex(self, staged) :
        self.stagedIndex = staged
    
    def updateIndex(self) :
        self.index = self.stagedIndex

    def getIndex(self) :
        return self.index

    def getLocation(self) :
        return self.location

    def isEmpty(self) :
        return self.index <= MenuLocationNode.IS_EMPTY

    def setFront(self, node) :
        self.front = node
    
    def setBack(self, node) :
        self.back = node

    def getFront(self) :
        return self.front

    def getBack(self) :
        return self.back

class Carousel :
    def __init__(self, controlPoints, scoreboards)  :
        self.scoreboards = scoreboards
        self.conotrlPoints = controlPoints
        self.listFront = None
        self.build()

    def build(self) :
        tempFront = None
        for c in self.conotrlPoints :
            newNode = MenuLocationNode(c)
            if self.listFront is None :
                self.listFront = newNode
                tempFront = self.listFront
            else :
                self.insertInFrontOf(tempFront, newNode)
                tempFront = newNode

        self.backCenter = self.listFront
        for i in range(0, len(self.conotrlPoints) // 2) :
            self.backCenter = self.backCenter.getFront()
        
        size = len(self.scoreboards)
        end = size # position of final item to be placed
        if size > 0 :
            self.listFront.setIndex(0)   # always one in front
        if size > 1 :
            self.listFront.getBack().setIndex(1) 
        if size > 2 :
            self.listFront.getFront().setIndex(2)
        if size > 3 and size % 2 == 0 : #put end of list in center back, if even number of items
            self.backCenter.setIndex(size-1)
            end -= 1
        if size > 6 : # add 3 and 4 to the 'front'
            self.listFront.getBack().getBack().setIndex(3)
            self.listFront.getFront().getFront().setIndex(4)
            
            # Now, 5 items in front, one in back if even number, and an even number of leftover items
            # add half of those leftovers to each side

            # find range to add to each side
            # left range is 5 to  5 + number of items/2 - 1
            numPerSide = (end - 5) / 2
            leftmostNode = self.backCenter.getBack().getBack()
            rightmostNode = self.backCenter.getFront().getFront()
            self.scatterRemains(5, 5 + numPerSide - 1, leftmostNode, self.backCenter) 
            self.scatterRemains(5 + numPerSide, end-1,  self.backCenter, rightmostNode)
        elif size == 5 :  # 4 or 5 items in list 
            self.backCenter.getBack().setIndex(3)
            self.backCenter.getFront().setIndex(4)
    
    # TODO: spread the remainder between back left and back right
    # will always have an even number of elements to distribute
    # always one node between leftNode and rightNode
    def scatterRemains(self, startIndex, endIndex, leftNode, rightNode) :
        # if odd number to place (1, 3, 5, etc) place one in gap node
        # odd number to place if end - start is even
        gapNode = leftNode.getFront()
        if (endIndex - startIndex) % 2 == 0 :
            gapNode.setIndex(startIndex)   
            startIndex += 1
             
        # if more than 1 node left, need new nodes in gaps
        if (endIndex - startIndex) > 0 : 
            self.createNewNode(leftNode, gapNode)   
            self.createNewNode(gapNode, rightNode)
            nodesPerSide = (1 + endIndex - startIndex ) / 2
            self.scatterRemains(startIndex, startIndex + nodesPerSide - 1, leftNode, gapNode)
            self.scatterRemains(startIndex + nodesPerSide, endIndex, gapNode, rightNode)

            # if odd number to place, place middle one in gap node,  recurse
            
    def createNewNode(self, leftNode, rightNode) :
        location = self.calculateLocation(leftNode.getLocation(), rightNode.getLocation())
        newNode = MenuLocationNode(location)
        self.insertInFrontOf(leftNode, newNode)
        
        
    # average position and scale between two points
    def calculateLocation(self, leftLoc, rightLoc) :
        x = (rightLoc[0] - leftLoc[0]) / 2
        y = (rightLoc[1] - leftLoc[1]) / 2
        s = (rightLoc[2] - leftLoc[2]) / 2
        return (x, y, s)

    def insertInFrontOf(self, frontNode, newNode) :
        frontNode.getFront().setBack(newNode)
        newNode.setFront(frontNode.getFront())
        frontNode.setFront(newNode)
        newNode.setBack(frontNode)
 
    def tracePath(self, t, traceFunc) :
        index = t.getIndex()
        t = traceFunc(t)
        path = []  
        while True :
            path.append(t.getLocation())
            if not(t.isEmpty()) :
                t.setStagedIndex(index)
                return (path)
            t = traceFunc(t)

            
    def rotate(self, direction=1) :
        traceFunc = MenuLocationNode.getFront if direction == 1 else MenuLocationNode.getBack
        t = self.listFront
        circumnavigated = False
        while not(circumnavigated) :
            if not(t.isEmpty()) : # found a location that has an index to an icon
                path =  self.tracePath(t, traceFunc)
                self.scoreboards[t.getIndex()][ScoreboardPicker.INDEX_ICON].moveTo(path)
            t = t.getFront()
            if t == self.listFront :
                circumnavigated = True

        circumnavigated = False
        while not(circumnavigated) :
            t.updateIndex()
            t = t.getFront()
            if t == self.listFront :
                circumnavigated = True


    # after one call to initialize, just use the move functions
    def initialize(self) :
        t = self.listFront
        circumnavigated = False
        if not(t is None) :
            while not(circumnavigated) :
                if not(t.isEmpty()) :
                    self.scoreboards[t.getIndex()][ScoreboardPicker.INDEX_ICON].setCenterAndScale(t.getLocation())
                t = t.getFront()
                if t == self.listFront : 
                    circumnavigated = True


    def printList(self) :
        t = self.listFront
        print ("Start of List")
        while True :
          print(str(t.getIndex()) + " ")
          t = t.getFront()
          if t == self.listFront : break
        print("End of List")

    def getSelection(self) :
        return self.listFront.getIndex()
    


class ScoreboardPicker(KeyHandler) :
    INDEX_SCOREBOARD = 1
    INDEX_ICON = 2

    ICON_WIDTH = 122

    def __init__(self) :
        self.batch = pyglet.graphics.Batch()
        self.configScreen = ConfigScreen(self.batch)

        # center points for the icons

        self.controlPoints = ( (400, 240, 0.9),   # 0: front, center
                               (220, 260, 0.6),   # 1: front, left of center
                               (100, 320, 0.4),     # 2: front, just before apex
                               (80, 330, 0.4),     # 3: left apex
                               (100, 340, 0.35),    # 4: back, just after apex
                               (260, 380, 0.3),    # 5: back, left of center
                               (400, 400, 0.25),   # 6: back center
                               (540, 380, 0.3),    # 7: back, right of center
                               (700, 340, 0.35),   # 8: back, just before apex
                               (720, 330, 0.4),    # 9: right apex
                               (700, 320, 0.4),    # 10: right, front, just after apex
                               (580, 260, 0.6),    # 11: front, right of center
                               )

        self.handleEntry()

        

    def handleEntry(self) :
        # (title for config screen, scoreboard, icon, FUTURE: FAC)
        self.scoreboardTuples = self.configScreen.getScoreboards()
        self.options = Carousel(self.controlPoints, self.scoreboardTuples)
        self.options.initialize()

        self.options.printList()

        if len(self.scoreboardTuples) > 0 :
            self.activeScreen = self
        else :
            self.activeScreen = self.configScreen
    
    # open the selected scoreboard
    def processSelection(self) :
        self.activeScreen = self.scoreboardTuples[self.options.getSelection()][ScoreboardPicker.INDEX_SCOREBOARD]
 
    def getBatch(self) :
        return self.batch

    def draw(self) :
        self.activeScreen.getBatch().draw()
 
    def update(self, dt) :
        for t in self.scoreboardTuples :
            t[2].update(dt)
        self.draw()
   
 
   # keyboard event handlers
  
    def handle_A(self, modified = False) :
        if self.activeScreen == self :
            self.options.rotate(1)
            #self.options.printList()
        else :
            self.activeScreen.handle_A(modified)

 
    def handle_D(self, modified = False) :
        if self.activeScreen == self :
            self.options.rotate(-1)    
            #self.options.printList()      
        else :
            self.activeScreen.handle_D(modified) 

    def handle_S(self, modified = False) :
        if self.activeScreen == self :
            self.processSelection()
        else :
            if (modified) : # 'kill' other screen
                self.activeScreen.handleExit()
                self.handleEntry()
            else :
                self.activeScreen.handle_S(modified)

    def handle_Q(self, modified=False) :
        if modified :
            self.batch = pyglet.graphics.Batch()
            self.configScreen.setIconBatch(self.batch)
            self.activeScreen = self.configScreen

    def handle_C(self, modified=False) :
        if modified :
            window.close()


##################################################
# start me up!

# Make full screen on Raspberry Pi as long as its hostname = raspberrypi
isPi = socket.gethostname() == "raspberrypi"
window = pyglet.window.Window(800, 480, fullscreen=isPi)


#####################################################################
# Pyglet Window Events

@window.event
def on_key_press(symbol, modifiers):
    if symbol == pyglet.window.key.D :
        picker.activeScreen.handle_D(modifiers & pyglet.window.key.LSHIFT)
    elif symbol == pyglet.window.key.A :
        picker.activeScreen.handle_A(modifiers & pyglet.window.key.LSHIFT)
    elif symbol == pyglet.window.key.S : #special case
        picker.handle_S(modifiers & pyglet.window.key.LSHIFT)
    elif symbol == pyglet.window.key.Z :
        picker.activeScreen.handle_Z(modifiers & pyglet.window.key.LSHIFT)
    elif symbol == pyglet.window.key.C :
        picker.activeScreen.handle_C(modifiers & pyglet.window.key.LSHIFT)
    elif symbol == pyglet.window.key.X :
        picker.activeScreen.handle_X(modifiers & pyglet.window.key.LSHIFT)
    elif symbol == pyglet.window.key.Q :
        picker.activeScreen.handle_Q(modifiers & pyglet.window.key.LSHIFT)
    elif symbol == pyglet.window.key.E :
        picker.activeScreen.handle_E(modifiers & pyglet.window.key.LSHIFT)


@window.event
def on_draw():
    window.clear()    
    picker.draw()

##########################################################

font.add_directory('.') 
font.add_file('sports.otf') 
picker = ScoreboardPicker()
pyglet.clock.schedule_interval(picker.update, 1/30.0)
pyglet.app.run()
