from json import load
import pyglet
from pyglet import font
from fac_set import FACSet
from key_handler import KeyHandler
from config_screen import ConfigScreen
from fast_action_window import FastActionWindow
from carousel import Carousel
import importlib    
import os
from pyglet import resource
from scoreboard import Scoreboard


class GamePicker(KeyHandler, pyglet.window.Window) :

    INDEX_ICON = 2
    AUTOSAVE_INTERVAL = 60 # scoreboards will autosave every AUTOSAVE_INTERVAL seconds

    def __init__(self, width, height, isPi = False) :
        self.findResources()
        self.createWindows(isPi, width, height)

        self.batch = pyglet.graphics.Batch()
        self.configScreen = ConfigScreen(self.loader, self.batch)
        self.timeSinceAutosave = 0
 
        # center points for the icons
        self.controlPoints = ( (400, 240, 0.95),   # 0: front, center
                               (220, 260, 0.6),   # 1: front, left of centerQ
                               (100, 300, 0.44),  # 2: front, just before apex
                               (60, 330, 0.4),    # 3: left apex
                               (120, 340, 0.35),  # 4: back, just after apex
                               (260, 380, 0.3),   # 5: back, left of center
                               (400, 390, 0.24),  # 6: back center
                               (540, 380, 0.3),   # 7: back, right of center
                               (680, 340, 0.35),  # 8: back, just before apex
                               (740, 330, 0.4),   # 9: right apex
                               (700, 300, 0.44),  # 10: right, front, just after apex
                               (580, 260, 0.6),   # 11: front, right of center
                             )
        self.createMenu()
        
        if len(self.scoreboardTuples) > 0 :
            self.activeScreen = self
        else :
            self.activeScreen = self.configScreen
    

    def createWindows(self, isPi, width, height) :
        display = pyglet.canvas.get_display()
        screens = display.get_screens()

        self.displayingFAC = (isPi and len(screens) > 1) or not(isPi)

        pyglet.window.Window.__init__(self, width, height, fullscreen=isPi, screen=screens[0])
        # Ideally, you just find both screens and assign a fullscreen window to each screen. 
        # But this was not consistently putting both windows on different screens.
        # So, I find the other screen using its virtual x coordinate
        # Then continue to create the other window, far away enough to be on the other screen.
        # If not far enough away, close the window and create it again.
        if self.displayingFAC :
            if isPi :
                positionedCorrectly = False
                self.set_exclusive_mouse(True)
                while not(positionedCorrectly) :           
                    
                    self.windowFAC = FastActionWindow(width, height, fullscreen=False)
                    self.windowFAC.switch_to()
                    otherX = self.width if self.get_location()[0] == 0 else 0
                    self.windowFAC.set_location(otherX, 0)

                    if not(self.windowFAC.get_location()[0] == self.get_location()[0]) :
                            positionedCorrectly = True
                    else :
                        self.windowFAC.close()

            elif not(isPi) : 
                self.windowFAC = FastActionWindow(width, height, fullscreen=False)
    
    def findResources(self) :
        self.path = ['resources', 'resources/icons', 'resources/fonts']
        self.loader = resource.Loader(self.path)
        self.loader.add_font('digital-7.mono.ttf')
        self.loader.add_font('title-sb.ttf')
        self.loader.add_font('Roboto-Regular.ttf')
        self.loader.add_font('Roboto-Bold.ttf')
        self.loader.add_font('cool.otf')
        font.load(Scoreboard.DIGIT_FONT)
        font.load(Scoreboard.TEXT_FONT)   
        font.load(FACSet.TEXT_FONT)
        # find user save directory. If does not exist, create it
        dir = pyglet.resource.get_settings_path('Scoreboard')
        if not os.path.exists(dir):
            os.makedirs(dir)


    def createMenu(self) :
        # (title for config screen, scoreboard, icon,  FAC)
        self.scoreboardTuples = self.configScreen.getScoreboards()

        self.options = Carousel(self.controlPoints, self.scoreboardTuples)
        self.options.initialize()      
    
    # open the selected scoreboard
    def processSelection(self, loadAutoSave=True) :
        picked = self.scoreboardTuples[self.options.getSelection()]
        scoreboardClass = getattr(importlib.import_module(picked[1]), picked[2])
        self.activeScreen = scoreboardClass()
        if loadAutoSave :
            self.activeScreen.loadFromAutosaveFile()
        if self.displayingFAC :
            class_ = getattr(importlib.import_module(picked[4]), picked[5])
            fac = class_(self.loader)
            self.windowFAC.setFACSet(fac)
            self.activeScreen.attachFAC(fac) # for messages bewteen FAC and Scoreboard

    def getBatch(self) :
        return self.batch

    def autosave(self) :
        0

    def on_draw(self) :
        self.clear()
        self.activeScreen.getBatch().draw()
 
    def update(self, dt) :
        self.timeSinceAutosave += dt
        if (self.timeSinceAutosave > GamePicker.AUTOSAVE_INTERVAL) :
            self.activeScreen.autosave()
            self.timeSinceAutosave = 0

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
            if self.displayingFAC :
                self.windowFAC.clearFACSet()
            if self.activeScreen.handleExit(self) > 0 :
                self.activeScreen = self
        else :
            self.activeScreen.handle_S(modified)

    def handle_Q(self, modified=False) :
        if modified :
            self.batch = pyglet.graphics.Batch()
            self.configScreen.setIconBatch(self.batch)
            self.activeScreen = self.configScreen


    def handle_E(self, modified=False) :
        if modified :
            self.processSelection(loadAutoSave=False)

    def handle_C(self, modified=False) :
        if modified :
            if self.displayingFAC :
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
            if self.displayingFAC :
                self.windowFAC.handle_L()
        elif symbol == pyglet.window.key.K :
            if self.displayingFAC :
                self.windowFAC.handle_K()

    def on_close(self):
        if self.displayingFAC :
            self.windowFAC.close()
        return super().on_close()




