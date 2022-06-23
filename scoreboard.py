import pyglet

from functools import partial
from element import ScoreboardElement
from element import HorizontalElement
from element import ClockElement
from key_handler import KeyHandler

class Scoreboard(KeyHandler) :

    # THree main columns top scorebaord screen
    LEFT_CENTER = 140
    RIGHT_CENTER = 660
    CENTER = 400

    # font sizes
    SCORE_SIZE = 76
    CLOCK_SIZE = 84
    MEDIUM_DIGIT_SIZE = 64
    SMALL_DIGIT_SIZE = 44
    VERY_SMALL_DIGIT_SIZE = 36

    LARGE_TEXT_SIZE = 50
    MEDIUM_TEXT_SIZE = 40
    SMALL_TEXT_SIZE = 30
    VERY_SMALL_TEXT_SIZE = 22

    WHITE = (255,255,255,255)
    RED = (255, 10, 10, 255)
    GREEN = (10, 255, 10, 255)
    YELLOW = (255, 255, 40, 255)
    BLUE = (0, 0, 255, 255)

    DIGIT_FONT = 'Digital-7 Mono'
    TEXT_FONT = 'Built Titling'

    def __init__(self) :
        #self.x = 0
        self.batch = pyglet.graphics.Batch()
        self.elements = []
        self.state = None

    def getBatch(self) :
        return self.batch

    def updateElements(self) :
        for e in self.elements :
            e.update()

    # convenience method to add guest and home scores
    def addScores(self, maxDigits, height,  leftLabel='GUEST', rightLabel='HOME') :
        self.addLargeElement(maxDigits, Scoreboard.LEFT_CENTER, height, leftLabel, partial(self.state.getScore, 0), Scoreboard.RED)
        self.addLargeElement(maxDigits, Scoreboard.RIGHT_CENTER, height, rightLabel, partial(self.state.getScore, 1), Scoreboard.RED)

    def addLargeElement(self, maxDigits, x, y, text, func, color) :
        e = ScoreboardElement(text=text, textFont=Scoreboard.TEXT_FONT, textSize=Scoreboard.LARGE_TEXT_SIZE, textColor=Scoreboard.WHITE,
                              updateFunc=func, digitFont=Scoreboard.DIGIT_FONT,
                              digitSize=Scoreboard.SCORE_SIZE, digitColor=color, maxDigits=maxDigits,  
                              batch=self.batch)
        e.setCenterTop(x,y)
        self.elements.append(e)

    def addMediumElement(self, maxDigits, x, y, text, func, color) :
        e = ScoreboardElement(text=text, textFont=Scoreboard.TEXT_FONT, textSize=Scoreboard.MEDIUM_TEXT_SIZE, textColor=Scoreboard.WHITE,
                              updateFunc=func, digitFont=Scoreboard.DIGIT_FONT,
                              digitSize=Scoreboard.MEDIUM_DIGIT_SIZE, digitColor=color, maxDigits=maxDigits,  
                              batch=self.batch)
        e.setCenterTop(x,y)
        self.elements.append(e)

    def addHorizontalElement(self, maxDigits, x, y, text, func, color) :
        e = HorizontalElement(text=text, textFont=Scoreboard.TEXT_FONT, textSize=Scoreboard.MEDIUM_TEXT_SIZE, textColor=Scoreboard.WHITE,
                              updateFunc=func, digitFont=Scoreboard.DIGIT_FONT,
                              digitSize=Scoreboard.MEDIUM_DIGIT_SIZE, digitColor=color, maxDigits=maxDigits,  
                              batch=self.batch)
        e.setCenterTop(x,y)
        self.elements.append(e)


    def addClock(self, height) :
        e = ClockElement(text=None, textFont=Scoreboard.TEXT_FONT, textSize=0, textColor=Scoreboard.WHITE, 
                              updateFunc=self.state.getSeconds, digitFont=Scoreboard.DIGIT_FONT,
                              digitSize=Scoreboard.CLOCK_SIZE, digitColor=Scoreboard.GREEN, maxDigits=2, batch=self.batch)
        e.setCenterTop(Scoreboard.CENTER, height)
        self.elements.append(e)

    def addPeriod(self, height, horizontal=False, maxDigits=1) :
        text = self.state.getTimeDivisionName()
        func = ScoreboardElement
        if horizontal :
            text = text + ':'
            func = HorizontalElement
        e = func(text=text, textFont=Scoreboard.TEXT_FONT, 
                                  textSize=Scoreboard.MEDIUM_TEXT_SIZE, textColor=Scoreboard.WHITE, 
                                  updateFunc=self.state.getPeriod, digitFont=Scoreboard.DIGIT_FONT,
                                  digitSize=Scoreboard.MEDIUM_DIGIT_SIZE, digitColor=Scoreboard.GREEN, maxDigits=maxDigits, 
                                  displayLeadingZeroes=False, batch=self.batch)
        e.setCenterTop(Scoreboard.CENTER, height)
        self.elements.append(e)

    def handleExit(self):
        0

    # handle keys

    def handle_Z(self, modified=False) :
        self.state.modifyGuestScore(modified)
        self.updateElements()

    def handle_C(self, modified=False) :
        self.state.modifyHomeScore(modified)
        self.updateElements()

    def handle_X(self, modified=False) :
        self.state.modifyTime(modified)
        self.updateElements()
    
    def handle_S(self, modified=False) :
        self.state.modifyPeriod()
        self.updateElements()

