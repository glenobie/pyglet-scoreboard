import socket
import pyglet
from pyglet import font
from key_handler import KeyHandler
from config_screen import ConfigScreen

class ScoreboardPicker(KeyHandler) :
    INDEX_SCOREBOARD = 1
    INDEX_ICON = 2

    ICON_WIDTH = 122


    def __init__(self) :
        self.batch = pyglet.graphics.Batch()
        self.configScreen = ConfigScreen(self.batch)

        # center points for the icons
        # This list contains duplicate items to fake a circular list
        # the list locationData will index into this list but only to the first 
        # half
        self.controlPoints = ( (400, 240, 0.8),   # 0: front, center
                               (200, 280, 0.6),   # 1: front, left of center
                               (100, 320, 0.4),     # 2: front, just before apex
                               (80, 330, 0.4),     # 3: left apex
                               (100, 340, 0.35),    # 4: back, just after apex
                               (260, 380, 0.3),    # 5: back, left of center
                               (400, 400, 0.25),   # 6: back center
                               (540, 380, 0.3),    # 7: back, right of center
                               (700, 340, 0.35),   # 8: back, just before apex
                               (720, 330, 0.4),    # 9: right apex
                               (700, 320, 0.4),    # 10: right, front, just after apex
                               (600, 280, 0.6),    # 11: front, right of center  
                               (400, 240, 0.8),   # 0: repeated: front, center
                               (200, 280, 0.6),   # 1: repeated: front, left of center
                               (100, 320, 0.4),     # 2: repeated: front, just before apex
                               (80, 330, 0.4),     # 3: repeated: left apex
                               (100, 340, 0.35),    # 4: repeated: back, just after apex
                               (260, 380, 0.3),    # 5: repeated: back, left of center
                               (400, 400, 0.25),   # 6: repeated: back center
                               (540, 380, 0.3),    # 7: repeated: back, right of center
                               (700, 340, 0.35),   # 8: repeated: back, just before apex
                               (720, 330, 0.4),    # 9: repeated: right apex
                               (700, 320, 0.4),    # 10: repeated: right, front, just after apex
                               (600, 280, 0.6),    # 11: repeated: front, right of center
                               )



        # will contain lists of (index into gameList, index into controlPoints)
        self.locationData = []
        self.handleEntry()

        # in clockwise order

    def calculatePositions(self) :
        self.locationData.append([0, 0])
        self.locationData.append([1, 11])
        self.locationData.append([2, 7])
        self.locationData.append([3, 5])
        self.locationData.append([4, 1])



    def handleEntry(self) :
        # (title for config screen, scoreboard, icon, FUTURE: FAC)
        self.scoreboardTuples = self.configScreen.getScoreboards()
        # only start the picker if there are games to pick from. Otherwise, start config screen
        if len(self.scoreboardTuples) > 0 :
 
        # determine positions and scales based on number of games
            self.calculatePositions()

            self.initializeMenu()
            self.activeScreen = self
        else :
            self.activeScreen = self.configScreen
    
    def initializeMenu(self) :
        for t in self.locationData :
            icon = self.scoreboardTuples[t[0]][ScoreboardPicker.INDEX_ICON]
            location = self.controlPoints[t[1]]
            icon.setCenterAndScale(location)
 
    # open the selected scoreboard
    def processSelection(self) :
         #self.activeScreen = self.scoreboardTuples[self.selectedOption][ScoreboardPicker.INDEX_SCOREBOARD]
         # load scoreboard at position 1
         0
 
    def getBatch(self) :
        return self.batch

    def draw(self) :
        self.activeScreen.getBatch().draw()
 
    def update(self, dt) :
        for t in self.scoreboardTuples :
            t[2].update(dt)
        self.draw()
   
    def rotate(self, direction) :
        # TODO: use direction
        for d in self.locationData : 
            icon = self.scoreboardTuples[d[0]][ScoreboardPicker.INDEX_ICON]
            # TODO: make this real
            nextIndex = d[1] + 2

            path = self.controlPoints[d[1]+1 : nextIndex ]
            icon.moveTo(path)
            d.pop(-1)
            d.insert(1, nextIndex)
            


   # keyboard event handlers
  
    def handle_A(self, modified = False) :
        if self.activeScreen == self :
            self.rotate(-1)
        else :
            self.activeScreen.handle_A(modified)

 
    def handle_D(self, modified = False) :
        if self.activeScreen == self :
            self.rotate(1)
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
