import socket
import pyglet
from pyglet import font
from key_handler import KeyHandler
from config_screen import ConfigScreen

class ScoreboardPicker(KeyHandler) :
    INDEX_SCOREBOARD = 1
    INDEX_ICON = 2

    def __init__(self) :
        self.batch = pyglet.graphics.Batch()
        self.configScreen = ConfigScreen(self.batch)
 
        # will contain lists of (index into gameList, x, y, scale)
        self.locationData = []
        self.handleEntry()


   
    def handleEntry(self) :
        # (title for config screen, scoreboard, icon, FUTURE: FAC)
        self.scoreboardTuples = self.configScreen.getScoreboards()
        # only start the picker if there are games to pick from. Otherwise, start config screen
        if len(self.scoreboardTuples) > 0 :
 
        # determine positions and scales based on number of games
            self.locationData.append([0, 288, 140, 0.8])
            self.locationData.append([4, 128, 180, 0.6])
            
            self.locationData.append([3, 268, 340, 0.2])
            self.locationData.append([2, 488, 340, 0.2])
            self.locationData.append([1, 488, 180, 0.6])

            self.initializeMenu()
            self.activeScreen = self
        else :
            self.activeScreen = self.configScreen
    
    def initializeMenu(self) :
        for t in self.locationData :
            icon = self.scoreboardTuples[t[0]][ScoreboardPicker.INDEX_ICON].getSprite()
            icon.update(x=t[1], y=t[2], scale=t[3] )
 
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
        for d in self.locationData :
            g = (d.pop(0) + direction) % len(self.locationData)
            d.insert(0, g)
            self.scoreboardTuples[g][2].moveTo(d[1], d[2], d[3])

   # keyboard event handlers
  
    def handle_A(self, modified = False) :
        if self.activeScreen == self :
            self.rotate(-1)
        else :
            self.activeScreen.handle_A(modified)

    # TODO: Delete this
    def handle_X(self, modified = False) :
        if self.activeScreen == self :
            self.scoreboardTuples[0][2].moveTo(0, 0)
        else :
            self.activeScreen.handle_Q(modified)

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
