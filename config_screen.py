import pyglet
from key_handler import KeyHandler
import os
import sys
import subprocess
from pathlib import Path
from game_list import GameList
from sprite import ScoreboardIconSprite

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
    

class ConfigScreen(KeyHandler) :

    LINES_PER_GAME = 6
    END_OF_FILE = 'EOF'
    ALL_GAMES_FILE = 'games.txt'
    CHOSEN_GAMES_FILE = 'config.txt'
    FIND_GIT_HUB_SCRIPT = 'git-test'
    GIT_PULL_SCRIPT = 'git-pull-scoreboard'

    def __init__(self, loader, iconBatch) :
        self.loader = loader

        self.batch = pyglet.graphics.Batch()
        self.scoreboards = []
        self.iconBatch = iconBatch

        # border will go in the background group, all others foreground
        self.bg = pyglet.graphics.OrderedGroup(0)
        self.fg = pyglet.graphics.OrderedGroup(1)


        self.createUserConfigFiles()

        allGames = self.processGamesFile(self.loader.file(ConfigScreen.ALL_GAMES_FILE, mode='r'))
        chosenGames = self.processGamesFile(open(self.configFilename, mode='r'))
        unchosenGames = listDifference(allGames,chosenGames)

        self.unchosenGameLayout = GameList('Other Games', unchosenGames, self.batch, self.fg, self.bg, 100)        
        self.chosenGameLayout = GameList('Chosen Games', chosenGames, self.batch, self.fg, self.bg, 450)

        self.scoreboards = self.objectsFromGames(self.chosenGameLayout.getGames())

        self.scriptHome = str(Path.home()) + '/'
        self.checkForGit()
        
    def checkForGit(self) :
        # run script to see if git-hub can be reached
        self.gitNotFound = subprocess.call(['sh',  self.scriptHome + ConfigScreen.FIND_GIT_HUB_SCRIPT])
        if (self.gitNotFound) :
            updateText = 'Not connected to internet.'
        else :
            updateText = 'Internet connection found. [MOD+F2] will update and restart.'

        self.msg = pyglet.text.Label(updateText, font_name='Arial', font_size=16, x=20, y=20, batch=self.batch, group=self.fg)

    def createUserConfigFiles(self) :
        # find user config directory or create it
        dir = pyglet.resource.get_settings_path('Scoreboard')
        if not os.path.exists(dir):
            os.makedirs(dir)
        # find chosen games file or create it
        self.configFilename = os.path.join(dir, ConfigScreen.CHOSEN_GAMES_FILE)
        if not (os.path.exists(self.configFilename)) :
            self.configFile = open(self.configFilename, 'wt')
            self.configFile.write(ConfigScreen.END_OF_FILE)
            self.configFile.close()

     # only scoreboards do autosave
    def autosave(self) :
        0

    def recordToFile(self, gameList) :
        self.configFile = open(self.configFilename, 'wt')
        print("writing")
        for g in gameList :
            for e in g :
                self.configFile.write(e)
                self.configFile.write('\n')    
        self.configFile.write(ConfigScreen.END_OF_FILE + '\n')
        self.configFile.close()

    def setIconBatch(self, batch) :
        self.iconBatch = batch

    # create objects from text descriptions in games
    # (game name, scoreboard module, scoreboard class, icon/sprite, fac module, fac class)
    def objectsFromGames(self, gameList) :
        print("generating")
        objectList = []
        for g in gameList :    
            s = []
            s.append(g[0])   
            s.append(g[1])
            s.append(g[2])
            s.append(ScoreboardIconSprite(self.loader.image(g[3]), self.iconBatch))
            s.append(g[4])
            s.append(g[5])
            objectList.append(s)
        return objectList

    # (Menu Name in config screen, scoreboard module name, scoreboard class name, dingbat char, dingbat font, menu text )
    def processGamesFile(self, file) :
        
        lines = file.read().splitlines()
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
    def handleExit(self, menuScreen) :   
        if (len(self.chosenGameLayout.getGames()) > 0) :
            self.recordToFile(self.chosenGameLayout.getGames())
            self.scoreboards = self.objectsFromGames(self.chosenGameLayout.getGames())
            menuScreen.createMenu()
            return 1
        return 0

    # keyboard handlers

    def handle_C(self, modified) :
        if modified :
            self.chosenGameLayout.moveDown()
        else :
            self.chosenGameLayout.selectNext(1)
                           
    def handle_E(self, modified) :
        if modified :
            self.chosenGameLayout.moveUp()
        else :
            self.chosenGameLayout.selectNext(-1)
 
    def handle_Q(self, modified) :
        if modified  and not(self.gitNotFound):
            # run github pull script
            subprocess.call(['sh', self.scriptHome + ConfigScreen.GIT_PULL_SCRIPT])
            # quit and restart
            os.execl(sys.executable, sys.executable, *sys.argv)
        else :
            self.unchosenGameLayout.selectNext(-1)
                           
    def handle_Z(self, modified) :
        self.unchosenGameLayout.selectNext(1)

    def handle_A(self, modified) :
        if modified and not(self.chosenGameLayout.zeroGames()) :
            g = self.chosenGameLayout.removeSelectedGame()
            self.unchosenGameLayout.addGame(g)

    def handle_D(self, modified) :
        if modified and not(self.unchosenGameLayout.zeroGames()) :
            g = self.unchosenGameLayout.removeSelectedGame()
            self.chosenGameLayout.addGame(g)
 


    