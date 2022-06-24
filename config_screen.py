from curses import start_color
from pydoc import doc
from re import L
from telnetlib import GA
from xmlrpc.server import DocXMLRPCRequestHandler
import pyglet
from pyglet import resource
from pyglet import shapes
import importlib
from key_handler import KeyHandler
import math


# helper function to subtract one list from another
def listDifference(list1, list2) :
    result = []
    i=0
    for e in list1 :
        game = e[0]
        if  not (game in (item for sublist in list2 for item in sublist)) :
            result.append(e)
        i = i + 1
    return result
    
class ScoreboardIconSprite :
    def __init__(self, dir, imageFile, batch):
        image = pyglet.image.load(dir + '/' + imageFile)
        self.icon = pyglet.sprite.Sprite(image, batch=batch)
        self.speed = 20
        self.scale_speed = 4
        
        self.moving = False

    def setPath(self, path) :
        self.path = path

    def getSprite(self) :
        return self.icon

    def moveTo(self, x, y, scale) :
        self.dest_x = x
        self.dest_y = y
        self.dest_scale = scale
        self.moving = True

    def update(self, dt) :
        if self.moving :
            x_d = self.dest_x - self.icon.x
            y_d = self.dest_y - self.icon.y
            scale_d = self.dest_scale - self.icon.scale

            angle = math.atan2(y_d, x_d)
            distance = math.sqrt((self.icon.x - self.dest_x) ** 2 + (self.icon.y - self.dest_y) ** 2)
            speed = min(self.speed, distance)
            change_x = math.cos(angle) * speed
            change_y = math.sin(angle) * speed
            change_scale =  scale_d / self.scale_speed
            self.icon.x += change_x
            self.icon.y += change_y
            self.icon.scale += change_scale
            distance = math.sqrt((self.icon.x - self.dest_x) ** 2 + (self.icon.y - self.dest_y) ** 2)

            # close enough?
            if distance <= self.speed:
                self.icon.x = self.dest_x
                self.icon.y = self.dest_y
                self.icon.scale = self.dest_scale
                self.moving= False


    


#############################
# Ultimately this will become a sprite
class ScoreboardIcon:

    VERTICAL_SPACING = -24
    TEXT_FONT = 'Built Titling'
    SELECTED_COLOR = (255,255,255,255) #white
    DEFAULT_COLOR = (255,255,255,40) #white, opaque
    DINGBAT_SIZE = 80
    TEXT_SIZE = 28

    def __init__(self, dingbatChar, dingbatFont, titleText, batch):
        self.dingbat = pyglet.text.Label(text=dingbatChar, font_name=dingbatFont, 
                        font_size=ScoreboardIcon.DINGBAT_SIZE, color=ScoreboardIcon.DEFAULT_COLOR, batch=batch)
        self.title = pyglet.text.Label(text=titleText, font_name=ScoreboardIcon.TEXT_FONT, 
                        font_size=ScoreboardIcon.TEXT_SIZE, color=ScoreboardIcon.DEFAULT_COLOR, batch=batch)
 
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

########################################
class GameList() :

    DEFAULT_COLOR = (255, 255, 255, 255) #white
    HIGHLIGHT_COLOR = (255, 0, 0, 255) #red
    WHITE = (255, 255, 255)
    GREY = (10,10,10)

    EMPTY = -1 # selected item if list is empty
    BOTTOM = 100
    WIDTH = 260
    HEIGHT = 300
    SPACING = 6
  

    def __init__(self, labelText, gameList, batch, textGroup, bgGroup, xPos) :
        self.gameList = gameList
        self.batch = batch
        self.textGroup = textGroup
        self.xPos = xPos

        #TODO handle empty list

        self.doc = self.createDocument()

        self.layout = self.makeLayout(0)

        label_y = GameList.BOTTOM + GameList.HEIGHT + 20
  
        # title atop the list
        self.label = pyglet.text.Label(labelText, font_name='Built Titling', font_size=20, color=GameList.DEFAULT_COLOR,
                                        x=xPos, y=label_y, batch=batch, group=textGroup)

        self.border = shapes.BorderedRectangle(xPos-GameList.SPACING, GameList.BOTTOM - GameList.SPACING, 
                                              GameList.WIDTH+GameList.SPACING*2, GameList.HEIGHT+GameList.SPACING * 2, 
                                              color=GameList.GREY, 
                                              border_color=GameList.WHITE, border=2, 
                                              batch=batch, group=bgGroup) 

        if self.zeroGames() :
            self.selectedGameIndex = GameList.EMPTY
        else :
            self.selectedGameIndex = 0
            self.highlightSelectedRow()

    def createDocument(self) :
        d = pyglet.text.document.FormattedDocument('')
        for g in self.gameList :
            d.insert_text(len(d.text), g[0])
            d.insert_text(len(d.text), u'\u2029') # denote a new paragraph
        return d

    def zeroGames(self) :
        return len(self.gameList) == 0


    def highlightSelectedRow(self) :
        if not(self.zeroGames()) :
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
            if (self.selectedGameIndex > 4) :
                scroll_y = self.selectedGameIndex * -10
            else :
                scroll_y = 0
            self.layout = self.makeLayout(scroll_y)

    # move the selected game up in the list by deleting and inserting
    def moveUp(self) :
        if (self.selectedGameIndex > 0) :
            g = self.gameList[self.selectedGameIndex]
            del self.gameList[self.selectedGameIndex]
            self.selectedGameIndex = self.selectedGameIndex - 1
            self.gameList.insert(self.selectedGameIndex, g)
            self.doc = self.createDocument()
            self.highlightSelectedRow()

    # move the selected game down in the list by deleting and inserting
    def moveDown(self) : 
        if (self.selectedGameIndex < len(self.gameList) - 1) :
            g = self.gameList[self.selectedGameIndex]
            del self.gameList[self.selectedGameIndex]
            self.selectedGameIndex = self.selectedGameIndex + 1
            self.gameList.insert(self.selectedGameIndex, g)
            self.doc = self.createDocument()
            self.highlightSelectedRow()

    def removeSelectedGame(self) :
        g = []
        if not(self.zeroGames()) :
            g = self.gameList[self.selectedGameIndex]
            del self.gameList[self.selectedGameIndex]
            self.doc = self.createDocument()
            self.selectedGameIndex -= 1
  
            if not(self.zeroGames()) :
                if (self.selectedGameIndex < 0) :
                    self.selectedGameIndex = 0
                self.highlightSelectedRow()
            else :
                self.layout.delete()
                self.selectedGameIndex = GameList.EMPTY
                self.layout = self.makeLayout(0)
        return g

    def addGame(self, game) :
        self.gameList.insert(self.selectedGameIndex+1, game)
        self.selectedGameIndex += 1
        self.doc = self.createDocument()
        self.highlightSelectedRow()

    # make/remake the layout after changes in  document
    # TODO: could use event listener??
    def makeLayout(self, scroll_y) :
        layout = pyglet.text.layout.ScrollableTextLayout(self.doc, GameList.WIDTH, GameList.HEIGHT,  
                                                         multiline=True, 
                                                         batch=self.batch, group=self.textGroup)
        layout.anchor_x = 'left'
        #layout.anchor_y = 'bottom'
        layout.y = GameList.BOTTOM
        layout.x = self.xPos
        layout.view_y = scroll_y
        return layout
        
    def selectNext(self, direction) :
        if not(self.zeroGames()) :
            self.selectedGameIndex = (self.selectedGameIndex + direction) % len(self.gameList)
            self.highlightSelectedRow()


    def getGames(self) :
        return self.gameList


######################################
class ConfigScreen(KeyHandler) :

    LINES_PER_GAME = 4
    END_OF_FILE = 'EOF'
    ALL_GAMES_FILE = 'games-w-icons.txt'
    CHOSEN_GAMES_FILE = 'config.txt'
    ICON_DIR = 'icons'

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

        self.unchosenGameLayout = GameList('Other Games', unchosenGames, self.batch, self.fg, self.bg, 100)        
        self.chosenGameLayout = GameList('Chosen Games', chosenGames, self.batch, self.fg, self.bg, 450)

        self.scoreboards = self.objectsFromGames(self.chosenGameLayout.getGames())

    def recordToFile(self, gameList) :
        f = open(ConfigScreen.CHOSEN_GAMES_FILE, 'w')
        for g in gameList :
            for e in g :
                f.write(e)
                f.write('\n')    
        f.write(ConfigScreen.END_OF_FILE + '\n')
        f.close()

    def setIconBatch(self, batch) :
        self.iconBatch = batch

    # create objects from text descriptions in games
    # (game name, scoreboard, icon/sprite)
    def objectsFromGames(self, gameList) :
        objectList = []
        for g in gameList :    
            s = []
            s.append(g[0])   
            scoreboardClass = getattr(importlib.import_module(g[1]), g[2])
            s.append(scoreboardClass())
            s.append(ScoreboardIconSprite(ConfigScreen.ICON_DIR, g[3], self.iconBatch))
            #s.append(ScoreboardIcon(g[3], g[4], g[5], self.iconBatch  ) )
            objectList.append(s)
        return objectList

    # (Menu Name in config screen, scoreboard module name, scoreboard class name, dingbat char, dingbat font, menu text )
    def processGamesFile(self, filename) :
        loader = resource.Loader()
        lines = loader.file(filename, mode='r').read().splitlines()
        games = []

        if len(lines) > 0 :
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

    # on exit, write to file and save scoraboards to list for picker
    def handleExit(self) :        
        self.recordToFile(self.chosenGameLayout.getGames())
        self.scoreboards = self.objectsFromGames(self.chosenGameLayout.getGames())

    # keyboard handlers

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
        self.unchosenGameLayout.selectNext(-1)
                           
    def handle_Z(self, modified) :
        self.unchosenGameLayout.selectNext(1)

    def handle_A(self, modified) :
        if (modified and not(self.chosenGameLayout.zeroGames())) :
            g = self.chosenGameLayout.removeSelectedGame()
            self.unchosenGameLayout.addGame(g)

    def handle_D(self, modified) :
        if (modified and not(self.unchosenGameLayout.zeroGames())) :
            g = self.unchosenGameLayout.removeSelectedGame()
            self.chosenGameLayout.addGame(g)
 


    