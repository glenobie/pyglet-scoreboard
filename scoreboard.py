import pyglet

from element import ScoreboardElement
from element import HorizontalElement
from element import ClockElement
from key_handler import KeyHandler

class Scoreboard(KeyHandler) :

    LEFT_CENTER = 140
    RIGHT_CENTER = 660
    CENTER = 400

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

    def addScores(self, maxDigits, height,  leftLabel='GUEST', rightLabel='HOME') :
        e = ScoreboardElement(text=leftLabel, textFont=Scoreboard.TEXT_FONT, textSize=Scoreboard.LARGE_TEXT_SIZE, textColor=Scoreboard.WHITE,
                              updateFunc=self.state.getGuestScore, digitFont=Scoreboard.DIGIT_FONT,
                              digitSize=Scoreboard.SCORE_SIZE, digitColor=Scoreboard.RED, maxDigits=maxDigits, 
                              batch=self.batch)
        e.setCenterTop(Scoreboard.LEFT_CENTER, height)
        self.elements.append(e)

        e = ScoreboardElement(text=rightLabel, textFont=Scoreboard.TEXT_FONT, textSize=Scoreboard.LARGE_TEXT_SIZE, textColor=Scoreboard.WHITE,
                              updateFunc=self.state.getHomeScore, digitFont=Scoreboard.DIGIT_FONT,
                              digitSize=Scoreboard.SCORE_SIZE, digitColor=Scoreboard.RED, maxDigits=maxDigits,  
                              batch=self.batch)
        e.setCenterTop(Scoreboard.RIGHT_CENTER, height)
        self.elements.append(e)

    def addClock(self, height) :
        e = ClockElement(text=None, textFont=Scoreboard.TEXT_FONT, textSize=0, textColor=Scoreboard.WHITE, 
                              updateFunc=self.state.getSeconds, digitFont=Scoreboard.DIGIT_FONT,
                              digitSize=Scoreboard.CLOCK_SIZE, digitColor=Scoreboard.GREEN, maxDigits=2, batch=self.batch)
        e.setCenterTop(Scoreboard.CENTER, height)
        self.elements.append(e)

    def addPeriod(self, height, horizontal=False, maxDigits=1) :
        text = self.state.getTimeDivisionName()
        if horizontal :
            text = text + ':'
            e = HorizontalElement(text=text, textFont=Scoreboard.TEXT_FONT, 
                                  textSize=Scoreboard.MEDIUM_TEXT_SIZE, textColor=Scoreboard.WHITE, 
                                  updateFunc=self.state.getPeriod, digitFont=Scoreboard.DIGIT_FONT,
                                  digitSize=Scoreboard.MEDIUM_DIGIT_SIZE, digitColor=Scoreboard.GREEN, maxDigits=maxDigits, 
                                  displayLeadingZeroes=False, batch=self.batch)
        else :           
            e = ScoreboardElement(text=text, textFont=Scoreboard.TEXT_FONT, 
                                textSize=Scoreboard.MEDIUM_TEXT_SIZE, textColor=Scoreboard.WHITE, 
                                updateFunc=self.state.getPeriod, digitFont=Scoreboard.DIGIT_FONT,
                                digitSize=Scoreboard.MEDIUM_DIGIT_SIZE, digitColor=Scoreboard.GREEN, maxDigits=maxDigits, 
                                displayLeadingZeroes=False, batch=self.batch)

        e.setCenterTop(Scoreboard.CENTER, height)
        self.elements.append(e)

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

    def handleExit(self):
        0

