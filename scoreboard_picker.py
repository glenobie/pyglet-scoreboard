import socket
import pyglet
from pyglet import font
from key_handler import KeyHandler
from config_screen import ConfigScreen
from fast_action_window import FastActionWindow
from carousel import Carousel
import importlib


####################################################################
class ScoreboardPicker(KeyHandler, pyglet.window.Window) :
    INDEX_ICON = 2

    def __init__(self, width, height, fullscreen = False) :
        pyglet.window.Window.__init__(self, width, height, fullscreen=fullscreen)
        
        self.windowFAC = FastActionWindow(800,480)
  
        
        font.add_directory('.') 
        self.batch = pyglet.graphics.Batch()
        self.configScreen = ConfigScreen(self.batch)

        # center points for the icons

        self.controlPoints = ( (400, 240, 0.9),   # 0: front, center
                               (220, 260, 0.6),   # 1: front, left of center
                               (100, 300, 0.44),     # 2: front, just before apex
                               (80, 330, 0.4),     # 3: left apex
                               (100, 340, 0.35),    # 4: back, just after apex
                               (280, 380, 0.3),    # 5: back, left of center
                               (400, 400, 0.20),   # 6: back center
                               (520, 380, 0.3),    # 7: back, right of center
                               (700, 340, 0.35),   # 8: back, just before apex
                               (720, 330, 0.4),    # 9: right apex
                               (700, 300, 0.44),    # 10: right, front, just after apex
                               (580, 260, 0.6),    # 11: front, right of center
                               )
        self.createMenu()
        
        if len(self.scoreboardTuples) > 0 :
            self.activeScreen = self
        else :
            self.activeScreen = self.configScreen
    
    # try to create menu, if no games, send to config screen
    def createMenu(self) :
        # (title for config screen, scoreboard, icon, FUTURE: FAC)
        self.scoreboardTuples = self.configScreen.getScoreboards()

        self.options = Carousel(self.controlPoints, self.scoreboardTuples)
        self.options.initialize()      
 
    
    # open the selected scoreboard
    def processSelection(self) :
        picked = self.scoreboardTuples[self.options.getSelection()]
        scoreboardClass = getattr(importlib.import_module(picked[1]), picked[2])
        self.activeScreen = scoreboardClass()
        self.windowFAC.setFACSet(picked[4], picked[5])


    def getBatch(self) :
        return self.batch

    def on_draw(self) :
        self.clear()
        self.activeScreen.getBatch().draw()
 
    def update(self, dt) :
        for t in self.scoreboardTuples :
            t[3].update(dt)
        self.activeScreen.getBatch().draw()
   
 
   # keyboard event handlers
  
    def handle_A(self, modified = False) :
        if self.activeScreen == self :
            self.options.rotate(1)
        else :
            self.activeScreen.handle_A(modified)

 
    def handle_D(self, modified = False) :
        if self.activeScreen == self :
            self.options.rotate(-1)        
        else :
            self.activeScreen.handle_D(modified) 

    def handle_S(self, modified = False) :
        if self.activeScreen == self :
            self.processSelection()
        elif modified :
            self.windowFAC.clearFACSet()
            if self.activeScreen.handleExit(self) > 0 :
                self.activeScreen = self

    def handle_Q(self, modified=False) :
        if modified :
            self.batch = pyglet.graphics.Batch()
            self.configScreen.setIconBatch(self.batch)
            self.activeScreen = self.configScreen

    def handle_C(self, modified=False) :
        if modified :
            self.windowFAC.close()
            self.close()

    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.D :
            self.activeScreen.handle_D(modifiers & pyglet.window.key.LSHIFT)
        elif symbol == pyglet.window.key.A :
            self.activeScreen.handle_A(modifiers & pyglet.window.key.LSHIFT)
        elif symbol == pyglet.window.key.S : #special case
            self.handle_S(modifiers & pyglet.window.key.LSHIFT)
        elif symbol == pyglet.window.key.Z :
            self.activeScreen.handle_Z(modifiers & pyglet.window.key.LSHIFT)
        elif symbol == pyglet.window.key.C :
            self.activeScreen.handle_C(modifiers & pyglet.window.key.LSHIFT)
        elif symbol == pyglet.window.key.X :
            self.activeScreen.handle_X(modifiers & pyglet.window.key.LSHIFT)
        elif symbol == pyglet.window.key.Q :
            self.activeScreen.handle_Q(modifiers & pyglet.window.key.LSHIFT)
        elif symbol == pyglet.window.key.E :
            self.activeScreen.handle_E(modifiers & pyglet.window.key.LSHIFT)
        elif symbol == pyglet.window.key.L :
            self.windowFAC.handle_L()
        elif symbol == pyglet.window.key.K :
            self.windowFAC.handle_K()

    def on_close(self):
        self.windowFAC.close()
        return super().on_close()

##################################################
# start me up!

isPi = socket.gethostname() == "raspberrypi"
picker = ScoreboardPicker(800, 480, fullscreen=isPi)
picker.activate() # should work on Linux, won't on windows
pyglet.clock.schedule_interval(picker.update, 1/30.0)
pyglet.app.run()
