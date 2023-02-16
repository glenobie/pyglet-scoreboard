from json import load
import pyglet
from pyglet import font
from fac_set import FACSet
from key_handler import KeyHandler
from config_screen import ConfigScreen
from fast_action_window import FastActionWindow
from playing_cards import PlayingCardDeck
from carousel import Carousel
import importlib    
import os
from pyglet import resource
from scoreboard import Scoreboard


class MainWindow(KeyHandler, pyglet.window.Window) :

    INDEX_ICON = 2
    AUTOSAVE_INTERVAL = 60 # scoreboards will autosave every AUTOSAVE_INTERVAL seconds

    def __init__(self, width, height, isPi = False) :

        # create window(s)
        display = pyglet.canvas.get_display()
        screens = display.get_screens()
        pyglet.window.Window.__init__(self, width, height, fullscreen=isPi, screen=screens[0])
        self.displayingFAC = (isPi and len(screens) > 1) or not(isPi)
        
        if self.displayingFAC :
            self.createFACWindow(isPi, width, height)
        
        pyglet.clock.schedule_interval(self.autosave, MainWindow.AUTOSAVE_INTERVAL)

        self.path = ['resources', 'resources/icons', 'resources/fonts']
        self.loader = self.findResources(self.path)
        self.configScreen = ConfigScreen(self.loader)
        self.pickerScreen = GamePicker(self.configScreen.getScoreboards(), self.configScreen.getIconBatch())

        # determine which screen to load first
        if self.configScreen.getNumGamesChosen() > 0 :
            self.activeScreen = self.pickerScreen
        else :
            self.activeScreen = self.configScreen

    
    def findResources(self, path) :        
        loader = resource.Loader(path)
        loader.add_font('digital-7.mono.ttf')
        loader.add_font('title-sb.ttf')
        loader.add_font('Roboto-Regular.ttf')
        loader.add_font('Roboto-Bold.ttf')
        loader.add_font('cool.otf')
        loader.add_font('Fire.ttf')
        loader.add_font('cards.TTF')
        font.load(Scoreboard.DIGIT_FONT)
        font.load(Scoreboard.TEXT_FONT)   
        font.load(FACSet.TEXT_FONT)
        font.load(PlayingCardDeck.CARD_FONT)
        # find user save directory. If does not exist, create it
        dir = pyglet.resource.get_settings_path('Scoreboard')
        if not os.path.exists(dir):
            os.makedirs(dir)
        return loader

    def createFACWindow(self, isPi, width, height) :
        # Ideally, you just find both screens and assign a fullscreen window to each screen. 
        # But this was not consistently putting both windows on different screens.
        # So, I find the other screen using its virtual x coordinate
        # Then continue to create the other window, far away enough to be on the other screen.
        # If not far enough away, close the window and create it again.
        if isPi :
            positionedCorrectly = False
            self.set_exclusive_mouse(True)
            while not(positionedCorrectly) :           
                
                self.windowFAC = FastActionWindow(width, height, fullscreen=False)
                otherX = self.width if self.get_location()[0] == 0 else 0
                self.windowFAC.set_location(otherX, 0)

                if not(self.windowFAC.get_location()[0] == self.get_location()[0]) :
                        positionedCorrectly = True
                else :
                    self.windowFAC.close()

        else : 
            self.windowFAC = FastActionWindow(width, height, fullscreen=False)

    def autosave(self, dt) :
        self.activeScreen.autosave()

    """   
    # called from startup.py, update position of icons
    # can probably remove in pyglet 2.0 and just use app.run(interval=1/30.0)
    def update(self, dt) :
        if self.activeScreen == self.pickerScreen :
            self.pickerScreen.update(dt)
    """
    
    def on_draw(self) :
        self.clear()
        if not self.activeScreen is None :
            self.activeScreen.draw() 

    def on_close(self):
        if self.displayingFAC :
            self.windowFAC.close()
        return super().on_close()


    def on_key_press(self, symbol, modifiers):
        modified = modifiers & pyglet.window.key.LSHIFT
        if symbol == pyglet.window.key.D :
            self.activeScreen.handle_D(modified)
        elif symbol == pyglet.window.key.A :
            self.activeScreen.handle_A(modified)
        elif symbol == pyglet.window.key.S : #special case
            if modified :
                self.handle_modified_S()
            else :
                if self.activeScreen == self.pickerScreen :
                    #self.activeScreen = None
                    self.processSelection()
                else :
                    self.activeScreen.handle_S(modified)
        elif symbol == pyglet.window.key.Z :
            self.activeScreen.handle_Z(modified)
        elif symbol == pyglet.window.key.C :
            if modified and self.activeScreen == self.pickerScreen:
                if self.displayingFAC :
                    self.windowFAC.close()
                self.close()
            self.activeScreen.handle_C(modified)
        elif symbol == pyglet.window.key.X :
            self.activeScreen.handle_X(modified)
        elif symbol == pyglet.window.key.Q :
            if modified :
                if self.activeScreen == self.pickerScreen :
                    self.configScreen.checkForGit()
                    self.activeScreen = self.configScreen
                else :
                    self.activeScreen.handle_Q(modified)
            else :
                self.activeScreen.handle_Q(modified)
        elif symbol == pyglet.window.key.E :
            if modified and self.activeScreen == self.pickerScreen :
                self.processSelection(loadAutoSave=False)

            self.activeScreen.handle_E(modified)
        elif symbol == pyglet.window.key.L :
            if self.displayingFAC :
                self.windowFAC.handle_L()
        elif symbol == pyglet.window.key.K :
            if self.displayingFAC :
                self.windowFAC.handle_K()
        elif symbol == pyglet.window.key.J :
            if self.displayingFAC :
                self.windowFAC.handle_J()

    # handle the modified S key
    def handle_modified_S(self) :
        if self.displayingFAC :
            self.windowFAC.clearFACSet()
        if self.activeScreen == self.configScreen :
            self.configScreen.handleExit()
            if self.configScreen.getNumGamesChosen() > 0 :
                self.pickerScreen = GamePicker(self.configScreen.getScoreboards(), self.configScreen.getIconBatch())
                self.activeScreen = self.pickerScreen
        elif self.activeScreen != self.pickerScreen : # scoreboard is active
            self.activeScreen.handleExit()
            self.activeScreen = self.pickerScreen

    # open the selected scoreboard
    def processSelection(self, loadAutoSave=True) :
        self.activeScreen = None
        picked = self.pickerScreen.scoreboardTuples[self.pickerScreen.getSelection()]
        scoreboardClass = getattr(importlib.import_module(picked[1]), picked[2])
        self.activeScreen = scoreboardClass()
        if loadAutoSave :
            self.activeScreen.loadFromAutosaveFile()
        if self.displayingFAC :
            class_ = getattr(importlib.import_module(picked[4]), picked[5])
            fac = class_(self.loader)
            self.windowFAC.setFACSet(fac)
            self.activeScreen.attachFAC(fac) # for messages bewteen FAC and Scoreboard


##################################################################
class GamePicker(KeyHandler) :

    def __init__(self, scoreboardTuples, batch) :
        self.batch = batch
        self.scoreboardTuples = scoreboardTuples
                # center points for the icons
        self.controlPoints = ( (400, 240, 1),   # 0: front, center
                               (220, 260, 0.6),   # 1: front, left of center
                               (100, 300, 0.48),  # 2: front, just before apex
                               (60, 330, 0.4),    # 3: left apex
                               (120, 340, 0.35),  # 4: back, just after apex
                               (260, 380, 0.3),   # 5: back, left of center
                               (400, 390, 0.24),  # 6: back center
                               (540, 380, 0.3),   # 7: back, right of center
                               (680, 340, 0.35),  # 8: back, just before apex
                               (740, 330, 0.4),   # 9: right apex
                               (700, 300, 0.48),  # 10: right, front, just after apex
                               (580, 260, 0.6),   # 11: front, right of center
                             )
        self.options = Carousel(self.controlPoints, self.scoreboardTuples)
        self.options.initialize()    


    def getBatch(self) :
        return self.batch

    def draw(self) :
        self.batch.draw()

        for t in self.scoreboardTuples :
            t[3].update()

    def getSelection(self) :
        return self.options.getSelection()
   # keyboard event handlers
  
    def handle_A(self, modified = False) :
        self.options.rotate(1)
 
    def handle_D(self, modified = False) :
        self.options.rotate(-1)        

    # only scoreboards do autosave
    def autosave(self) :
        0










