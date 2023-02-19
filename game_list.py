import pyglet

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
 
        self.layout = pyglet.text.layout.IncrementalTextLayout(self.doc, GameList.WIDTH, GameList.HEIGHT,  
                                                                multiline=True, 
                                                                batch=self.batch, group=textGroup)
        self.layout.anchor_x = 'left'
        self.layout.y = GameList.BOTTOM
        self.layout.x = self.xPos
        self.layout.selection_color = GameList.HIGHLIGHT_COLOR
        self.layout.selection_background_color = (0,0,0,255)

        label_y = GameList.BOTTOM + GameList.HEIGHT + 20
  
        # title atop the list
        self.label = pyglet.text.Label(labelText, font_name='Built Titling', font_size=20, color=GameList.DEFAULT_COLOR,
                                        x=xPos, y=label_y, batch=batch, group=textGroup)

        self.border = pyglet.shapes.BorderedRectangle(xPos-GameList.SPACING, GameList.BOTTOM - GameList.SPACING, 
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
        
        d.set_style(0,len(d.text), dict(color=GameList.DEFAULT_COLOR))
        return d

    def zeroGames(self) :
        return len(self.gameList) == 0



    def highlightSelectedRow(self) :
        if not(self.zeroGames()) :
            j=0
            while j < len(self.doc.text) :
                end = self.doc.get_paragraph_end(j)
                text = self.doc.text[j:end-1] # subtract off newline character
                if text == self.gameList[self.selectedGameIndex][0] :
                    self.layout.set_selection(j, end-1)
                    break
                j = end
            #self.layout.ensure_line_visible(self.layout.get_line_from_position(j-2))
            if (self.selectedGameIndex > 4) :
                self.layout.view_y = self.selectedGameIndex * -10
            else :
                self.layout.view_y = 0

    # move the selected game up in the list by deleting and inserting
    def moveUp(self) :
        if (self.selectedGameIndex > 0) :
            g = self.gameList[self.selectedGameIndex]
            del self.gameList[self.selectedGameIndex]
            self.selectedGameIndex = self.selectedGameIndex - 1
            self.gameList.insert(self.selectedGameIndex, g)
            self.doc = self.createDocument()
            self.layout.document = self.doc
            self.highlightSelectedRow()

    # move the selected game down in the list by deleting and inserting
    def moveDown(self) : 
        if (self.selectedGameIndex < len(self.gameList) - 1) :
            g = self.gameList[self.selectedGameIndex]
            del self.gameList[self.selectedGameIndex]
            self.selectedGameIndex = self.selectedGameIndex + 1
            self.gameList.insert(self.selectedGameIndex, g)
            self.doc = self.createDocument()
            self.layout.document = self.doc
            self.highlightSelectedRow()

    def removeSelectedGame(self) :
        g = []
        if not(self.zeroGames()) :
            g = self.gameList[self.selectedGameIndex]
            del self.gameList[self.selectedGameIndex]
            self.doc = self.createDocument()
            self.layout.document = self.doc
            self.selectedGameIndex -= 1
  
            if not(self.zeroGames()) :
                if (self.selectedGameIndex < 0) :
                    self.selectedGameIndex = 0
                self.highlightSelectedRow()
            else :
                self.selectedGameIndex = GameList.EMPTY 
        return g

    def addGame(self, game) :
        self.gameList.insert(self.selectedGameIndex+1, game)
        self.selectedGameIndex += 1
        self.doc = self.createDocument()
        self.layout.document = self.doc
        self.highlightSelectedRow()


    def selectNext(self, direction) :
        if not(self.zeroGames()) :
            self.selectedGameIndex = (self.selectedGameIndex + direction) % len(self.gameList)
            self.highlightSelectedRow()


    def getGames(self) :
        return self.gameList