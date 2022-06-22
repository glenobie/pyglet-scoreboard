import socket
import pyglet
from pyglet import font
from key_handler import KeyHandler
from config_screen import ConfigScreen

class ScoreboardPicker(KeyHandler) :
    POSITIONS = ( (160, 470), (400, 470), (640, 470),
                  (160, 312), (400, 312), (640, 312),
                  (160, 164),  (400, 164), (640, 164) )

    def __init__(self):
        self.batch = pyglet.graphics.Batch()
        self.configScreen = ConfigScreen(self.batch)

        
        self.scoreboardTuples = self.configScreen.getScoreboards()
        if len(self.scoreboardTuples) > 0 :
            self.initializeMenu()
            self.activeScreen = self
        else :
            self.activeScreen = self.configScreen
    
    def initializeMenu(self) :
        i = 0
        for t in self.scoreboardTuples :
             t[2].setCenterTop(ScoreboardPicker.POSITIONS[i][0], ScoreboardPicker.POSITIONS[i][1])
             i = i+1
            
        if len(t) > 0  :
            self.scoreboardTuples[0][2].setSelected(True)
            self.selectedOption = 0
  
    def selectNew(self, jump) :
        self.scoreboardTuples[self.selectedOption][2].setSelected(False)
        self.selectedOption = (self.selectedOption + jump) % len(self.scoreboardTuples)
        self.scoreboardTuples[self.selectedOption][2].setSelected(True)

    def processSelection(self) :
         self.activeScreen = self.scoreboardTuples[self.selectedOption][1]
 
    def getBatch(self) :
        return self.batch

    def draw(self) :
        self.activeScreen.getBatch().draw()
 
    def update(self, dt) :
        self.draw()
   
    def handle_A(self, modified = False) :
        if self.activeScreen == self :
            self.selectNew(-1)
        else :
            self.activeScreen.handle_A(modified)

    def handle_D(self, modified = False) :
        if self.activeScreen == self :
            self.selectNew(1)
        else :
            self.activeScreen.handle_D(modified) 

    def handle_S(self, modified = False) :
        if self.activeScreen == self :
            self.processSelection()
        else :
            if (modified) : # 'kill' other screen
                self.activeScreen.handleExit()
                self.scoreboardTuples = self.configScreen.getScoreboards()
                if len(self.scoreboardTuples) > 0 :
                    self.initializeMenu()
                    self.activeScreen = self 
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
