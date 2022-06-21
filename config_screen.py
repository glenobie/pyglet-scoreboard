from curses import start_color
from pydoc import doc
from telnetlib import GA
import pyglet
from pyglet import resource
from pyglet import shapes
import importlib
from key_handler import KeyHandler

#############################
# Ultimately this will become a sprite
def listDifference(list1, list2) :
    result = []
    i=0
    for e in list1 :
        game = e[0]
        if  not (game in (item for sublist in list2 for item in sublist)) :
            result.append(e)
        i = i + 1
    return result
    
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

class GameList() :

    DEFAULT_COLOR = (255, 255, 255, 255)
    HIGHLIGHT_COLOR = (255, 0, 0, 255)
    WHITE = (255, 255, 255)
    GREY = (10,10,10)

    def __init__(self, gameList, batch, textGroup, bgGroup, xPos) :
        self.gameList = gameList
        self.batch = batch
        self.textGroup = textGroup
        self.xPos = xPos

        self.doc = self.createDocument()

        self.layout = self.makeLayout()

        self.border = shapes.BorderedRectangle(xPos-6, 94, 268, 308, color=GameList.GREY, 
                                              border_color=GameList.WHITE, border=2, 
                                               batch=batch, group=bgGroup) 

        self.selectedGameIndex = 0
        self.highlightSelectedRow()

    def createDocument(self) :
        d = pyglet.text.document.FormattedDocument('')
        for g in self.gameList :
            d.insert_text(len(d.text), g[0])
            d.insert_text(len(d.text), u'\u2029')

        d.set_style(0, len(d.text), dict(color=GameList.DEFAULT_COLOR)) 
        return d


    def highlightSelectedRow(self) :
        self.layout.delete()
        j=0
        while j < len(self.doc.text) :
            end = self.doc.get_paragraph_end(j)
            text = self.doc.text[j:end-1] # subtract off newline character
            if text == self.gameList[self.selectedGameIndex][0] :
                self.doc.set_style(j, end, dict(color=GameList.HIGHLIGHT_COLOR))
            else :
                self.doc.set_style(j, end, dict(color=GameList.DEFAULT_COLOR))
            j = end
        self.layout = self.makeLayout()

    def moveUp(self) :
        if (self.selectedGameIndex > 0) :
            g = self.gameList[self.selectedGameIndex]
            del self.gameList[self.selectedGameIndex]
            self.selectedGameIndex = self.selectedGameIndex - 1
            self.gameList.insert(self.selectedGameIndex, g)
            self.doc = self.createDocument()
            self.highlightSelectedRow()

    def moveDown(self) : 
        if (self.selectedGameIndex < len(self.gameList) - 1) :
            g = self.gameList[self.selectedGameIndex]
            del self.gameList[self.selectedGameIndex]
            self.selectedGameIndex = self.selectedGameIndex + 1
            self.gameList.insert(self.selectedGameIndex, g)
            self.doc = self.createDocument()
            self.highlightSelectedRow()

    def removeSelectedGame(self) :
        return 0

    def addGame(self, game) :
        0

    def makeLayout(self) :
        layout = pyglet.text.layout.ScrollableTextLayout(self.doc, 260, 300,  
                                                         multiline=True, 
                                                         batch=self.batch, group=self.textGroup)
        layout.anchor_x = 'left'
        layout.anchor_y = 'bottom'
        layout.y = 100
        layout.x = self.xPos
        return layout
        

    def selectNext(self, direction) :
         self.selectedGameIndex = (self.selectedGameIndex + direction) % len(self.gameList)
         self.highlightSelectedRow()

    def addGame(self, game) :
        0
    
    def deleteGame(self, game) :
        0



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
        unchosenGames = listDifference(allGames,chosenGames)

        self.scoreboards = self.objectsFromGames(chosenGames)

        self.unchosenGameLayout = GameList(unchosenGames, self.batch, self.fg, self.bg, 100)
        
        self.chosenGameLayout = GameList(chosenGames, self.batch, self.fg, self.bg, 450)

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

    def handle_C(self, modified) :
        if (modified) :
            self.chosenGameLayout.moveDown()
        else :
            self.chosenGameLayout.selectNext(1)
                           
    def handle_E(self, modified) :
        if (modified) :
            self.chosenGameLayout.moveUp()
        else :
            self.chosenGameLayout.selectNext(-1)
 
    def handle_Q(self, modified) :
        self.unchosenGameLayout.selectNext(1)
                           
    def handle_Z(self, modified) :
        self.unchosenGameLayout.selectNext(-1)

    def handle_A(self, modified) :
        if (modified) :
            g = self.chosenGameLayout.removeSelectedGame()
            self.unchosenGameLayout.addGame(g)

    def handle_D(self, modified) :
        if (modified) :
            g = self.unchosenGameLayout.removeSelectedGame()
            self.chosenGameLayout.addGame(g)
 


    