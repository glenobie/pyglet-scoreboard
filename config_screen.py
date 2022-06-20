import pyglet
import pyglet.resource
import importlib

from key_handler import KeyHandler
# use pyglet.resource.text to load text document

class ScoreboardIcon:
    VERTICAL_SPACING = 44
    TEXT_FONT = 'Built Titling'
    SELECTED_COLOR = (255,255,255,255) #red
    DEFAULT_COLOR = (255,255,255,40) #white, opaque

    def __init__(self, dingbatChar, dingbatFont, titleText,batch):
        
        # TODO compute height of dingbat

        self.dingbat = pyglet.text.Label(text=dingbatChar, font_name=dingbatFont, font_size=80, color=ScoreboardIcon.DEFAULT_COLOR, batch=batch)
        self.title = pyglet.text.Label(text=titleText, font_name=ScoreboardIcon.TEXT_FONT, font_size=40, color=ScoreboardIcon.DEFAULT_COLOR, batch=batch)
 
    def setCenterTop(self, x, y) :
        self.dingbat.anchor_x = 'center'
        self.dingbat.anchor_y = 'top'
        self.dingbat.position = (x, y)

        self.title.anchor_x = 'center'
        self.title.anchor_y = 'top'
        self.title.position = (x, y - self.dingbat.height + ScoreboardIcon.VERTICAL_SPACING)

    def setSelected(self, isSelected) :
        self.isSelected = isSelected
        if self.isSelected :
            c = ScoreboardIcon.SELECTED_COLOR
        else :
            c = ScoreboardIcon.DEFAULT_COLOR
        self.dingbat.color = c
        self.title.color = c


class ConfigScreen(KeyHandler) :

    LINES_PER_GAME = 6

    def __init__(self) :
        self.batch = pyglet.graphics.Batch()
        loader = pyglet.resource.Loader()
        lines = loader.file('config.txt', mode='r').readlines()
        games = []
        self.scoreboards = []

        # use file to create tuples of scoreboards (scoreboard class, ScoreboardIcon)
        # ultimately: (scoreboard class, sprite, FAC class)
        
        # (Menu Name in config screen, scoreboard module name, scoreboard class name, dingbat char, dingbat font, menu text )
        for t in lines :
            g = []
            for i in range(0, ConfigScreen.LINES_PER_GAME) :
                g.append(t)
            games.append(g)

        for g in games :    
            s = []    
            
            s.append(self.scoreboards.append( getattr(importlib.import_module(g[1]), g[2]) ))
            s.append(ScoreboardIcon(g[3], g[4], g[5], self.batch  ) )


            self.scoreboards.append(s)


#
#        d = pyglet.text.document.UnformattedDocument(games[0])
#        d.set_style(0, len(d.text), dict(color=(255,255,255,255)))
#        layout = pyglet.text.layout.TextLayout(d, width=100, height=100, batch=self.batch, multiline=True)
#        layout.position = (100,100)


    def getBatch(self) :
        return self.batch

    def getScoreboards(self) :
        return self.scoreboards
    

    