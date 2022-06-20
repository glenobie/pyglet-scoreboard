import pyglet
from pyglet import resource
from pyglet import shapes
import importlib
from key_handler import KeyHandler

#############################
# Ultimately this will become a sprite

class ScoreboardIcon:

    VERTICAL_SPACING = -24
    TEXT_FONT = 'Built Titling'
    SELECTED_COLOR = (255,255,255,255) #red
    DEFAULT_COLOR = (255,255,255,40) #white, opaque

    def __init__(self, dingbatChar, dingbatFont, titleText, batch):
        self.dingbat = pyglet.text.Label(text=dingbatChar, font_name=dingbatFont, font_size=80, color=ScoreboardIcon.DEFAULT_COLOR, batch=batch)
        self.title = pyglet.text.Label(text=titleText, font_name=ScoreboardIcon.TEXT_FONT, font_size=40, color=ScoreboardIcon.DEFAULT_COLOR, batch=batch)
 
    def setCenterTop(self, x, y) :
        self.dingbat.anchor_x = 'center'
        self.dingbat.anchor_y = 'top'
        self.dingbat.position = (x, y)

        self.title.anchor_x = 'center'
        self.title.anchor_y = 'top'
        self.title.position = (x, y - self.dingbat.content_height - ScoreboardIcon.VERTICAL_SPACING)

    def setSelected(self, isSelected) :
        self.isSelected = isSelected
        if self.isSelected :
            c = ScoreboardIcon.SELECTED_COLOR
        else :
            c = ScoreboardIcon.DEFAULT_COLOR
        self.dingbat.color = c
        self.title.color = c

######################################
class ConfigScreen(KeyHandler) :

    LINES_PER_GAME = 6
    END_OF_FILE = 'EOF'
    ALL_GAMES_FILE = 'games.txt'
    CHOSEN_GAMES_FILE = 'config.txt'

    def __init__(self, iconBatch) :
        self.batch = pyglet.graphics.Batch()
        self.scoreboards = []
        self.iconBatch = iconBatch

        # border will go in the background group, all others foreground
        self.bg = pyglet.graphics.OrderedGroup(0)
        self.fg = pyglet.graphics.OrderedGroup(1)


        allGames = self.processGamesFile(filename=ConfigScreen.ALL_GAMES_FILE)

        chosenGames = self.processGamesFile(filename=ConfigScreen.CHOSEN_GAMES_FILE)
        self.scoreboards = self.objectsFromGames(chosenGames)

        self.allGameLayout = self.layoutGames(allGames, self.batch, group=self.fg)
        self.allGameLayout.anchor_x = 'left'
        self.allGameLayout.anchor_y = 'bottom'
        self.allGameLayout.position = (100,100)
        
        self.leftBorder = shapes.BorderedRectangle(94, 94, 268, 308, color=(10,10,40), 
                                              border_color=(255,255,255), border=2, 
                                               batch=self.batch, group=self.bg)     
          

    def layoutGames(self, gameList, batch, group=None) :
        doc = pyglet.text.document.FormattedDocument('')
        for g in gameList :
            doc.insert_text(len(doc.text), g[0])
            doc.insert_text(len(doc.text), u'\u2029')

        doc.set_style(0, len(doc.text), dict(color=(255,255,255,255))) 
        layout = pyglet.text.layout.ScrollableTextLayout(doc, 260, 300, 
                                                         multiline=True, 
                                                         batch=batch, group=group)
        return layout

    # create objects from text descriptions in games
    # (game name, scoreboard, icon/sprite)
    def objectsFromGames(self, gameList) :
        objectList = []
        for g in gameList :    
            s = []
            s.append(g[0])   
            scoreboardClass = getattr(importlib.import_module(g[1]), g[2])
            s.append(scoreboardClass( ))
            s.append(ScoreboardIcon(g[3], g[4], g[5], self.iconBatch  ) )
            objectList.append(s)
        return objectList

    # (Menu Name in config screen, scoreboard module name, scoreboard class name, dingbat char, dingbat font, menu text )
    def processGamesFile(self, filename) :
        loader = resource.Loader()
        lines = loader.file(filename, mode='r').read().splitlines()
        games = []

        t = 0
        while not(lines[t] == ConfigScreen.END_OF_FILE):
            g = []
            for i in range(0, ConfigScreen.LINES_PER_GAME) :
                g.append(lines[t])
                t = t + 1
            games.append(g)
        return games


    def getBatch(self) :
        return self.batch

    def getScoreboards(self) :
        return self.scoreboards
    

    