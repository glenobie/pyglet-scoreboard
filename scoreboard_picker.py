from email import policy
import os
import socket
import pyglet
from pyglet import font
from basketball import BasketballScoreboard
from football import FootballScoreboard
from boxing import BoxingScoreboard
from hockey import HockeyScoreboard

# Make full screen on Raspberry Pi as long as its hostname = raspberrypi
isPi = socket.gethostname() == "raspberrypi"
window = pyglet.window.Window(800, 480, fullscreen=isPi)


class ScoreboardIcon:
    LINE_SPACING = 44
    SELECTED_COLOR = (255,0,0,255) #red
    DEFAULT_COLOR = (255,255,255,100) #white, opaque

    def __init__(self, text,  position, width, batch, scoreboard):
        self.scoreboard = scoreboard

        self.document = pyglet.text.document.FormattedDocument(text[0])
        self.document.set_paragraph_style(0, len(self.document.text), 
                                          dict(color=ScoreboardIcon.DEFAULT_COLOR, 
                                               align='center', 
                                               line_spacing=ScoreboardIcon.LINE_SPACING))
        # first paragraph is dingbat
        self.document.set_paragraph_style(0, 1, dict(font_name = text[1], font_size=80))
        # second paragraph is text
        self.document.set_paragraph_style(1, len(self.document.text), dict(font_name = 'Built Titling', font_size=32))
           
        
        height = (self.document.get_font(0).ascent - self.document.get_font(0).descent) + (self.document.get_font(1).ascent - self.document.get_font(1).descent) +  ScoreboardIcon.LINE_SPACING
                 
        self.layout = pyglet.text.layout.TextLayout(self.document, width, height, batch=batch, multiline=True)
        self.layout.position = position

    def setSelected(self, isSelected) :
        self.isSelected = isSelected
        if self.isSelected :
            c = ScoreboardIcon.SELECTED_COLOR
        else :
            c = ScoreboardIcon.DEFAULT_COLOR
        self.document.set_paragraph_style(0, len(self.document.text), dict(color=c))



##########################################################
class ScoreboardPicker :

    TEXT_FONT_PAIRS = ( ('l'+u'\u2029'+'HOCKEY',     'Go Go Sports'),
                        ('P'+u'\u2029'+'BASKETBALL', 'Go Go Sports'),
                        ('e'+u'\u2029'+'BASEBALL',   'Go Go Sports'),
                        ('y'+u'\u2029'+'FOOTBALL' ,  'Go Go Sports'),
                        ('2'+u'\u2029'+'CRICKET',    'England'),
                        ('L'+u'\u2029'+'BOXING',     'Go Go Sports'),
                        ('v'+u'\u2029'+'TENNIS' ,    'Go Go Sports'),  # or "t" or "o" or "7" or "v"
                        ('A'+u'\u2029'+'BOWLING' ,   'Go Go Sports'),
                        ('B'+u'\u2029'+'GOLF'  ,     'Go Go Sports'))

    POSITIONS = ( (40, 210), (300, 210), (560, 210),
                  (40, 56), (300, 56), (560, 56),
                  (40, -90),  (300, -90),  (560, -90) )

    OPTION_WIDTH = 200

    def __init__(self):
        self.running = True
        self.batch = pyglet.graphics.Batch()
        self.options = []   
 
        self.scoreboards = (HockeyScoreboard(),  
                            BasketballScoreboard(),
                            BasketballScoreboard(),  
                            FootballScoreboard(),
                            BasketballScoreboard(),  
                            BoxingScoreboard(),
                            BasketballScoreboard(),  
                            BasketballScoreboard(),
                            BasketballScoreboard())


        for i in range(0, len(ScoreboardPicker.TEXT_FONT_PAIRS)) :
            self.options.append(ScoreboardIcon(ScoreboardPicker.TEXT_FONT_PAIRS[i],
                                               ScoreboardPicker.POSITIONS[i],
                                               ScoreboardPicker.OPTION_WIDTH, self.batch, 
                                               self.scoreboards[i]  ) )
                                                 
                    
        self.options[0].setSelected(True)
        self.selectedOption = 0
        self.activeScoreboard = self.scoreboards[0]

 
    def selectNew(self, jump) :
        self.options[self.selectedOption].setSelected(False)
        self.selectedOption = (self.selectedOption + jump) % len(self.options)
        self.options[self.selectedOption].setSelected(True)

    def processSelection(self) :
        self.running = False
        self.activeScoreboard = self.scoreboards[self.selectedOption]
        self.activeScoreboard.execute()


    def draw(self) :
        if self.activeScoreboard.isRunning() :
            self.activeScoreboard.getBatch().draw()
        else :
            self.batch.draw()

    def update(self, dt) :
        x=1

    def isRunning(self) :
        return self.running
         
    def killScoreboard(self) :
        self.activeScoreboard.die()
        self.running = True

 
@window.event
def on_key_press(symbol, modifiers):
    if symbol == pyglet.window.key.D:
        if picker.isRunning() :
            picker.selectNew(1)  
        else :
            picker.activeScoreboard.handle_D(modifiers & pyglet.window.key.LSHIFT)
    elif symbol == pyglet.window.key.A:
        if picker.isRunning() :
            picker.selectNew(-1)
        else :
            picker.activeScoreboard.handle_A(modifiers & pyglet.window.key.LSHIFT)
    elif symbol == pyglet.window.key.S:
        if modifiers & pyglet.window.key.LSHIFT :
            picker.killScoreboard()
        elif picker.isRunning() :
            picker.processSelection()
        else :
            picker.activeScoreboard.handle_S()
    elif symbol == pyglet.window.key.Z:
        if not(picker.isRunning()) :
            picker.activeScoreboard.handle_Z(modifiers & pyglet.window.key.LSHIFT)
    elif symbol == pyglet.window.key.C:
        if not(picker.isRunning()) :
            picker.activeScoreboard.handle_C(modifiers & pyglet.window.key.LSHIFT)
    elif symbol == pyglet.window.key.X:
        if not(picker.isRunning()) :
            picker.activeScoreboard.handle_X(modifiers & pyglet.window.key.LSHIFT)
    elif symbol == pyglet.window.key.Q:
        if not(picker.isRunning()) :
            picker.activeScoreboard.handle_Q(modifiers & pyglet.window.key.LSHIFT)
    elif symbol == pyglet.window.key.E:
        if not(picker.isRunning()) :
            picker.activeScoreboard.handle_E(modifiers & pyglet.window.key.LSHIFT)



@window.event
def on_draw():
    window.clear()    
    picker.draw()


font.add_directory('.') 
font.add_file('sports.otf') 
#font.add_file('monofonto.otf')
picker = ScoreboardPicker()
pyglet.clock.schedule_interval(picker.update, 1/30.0)
pyglet.app.run()