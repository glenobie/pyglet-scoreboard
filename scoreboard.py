import pyglet

from element import ScoreboardElement
from element import HorizontalElement

class Scoreboard():

    LEFT_CENTER = 140
    RIGHT_CENTER = 660
    CENTER = 400

    SCORE_SIZE = 76
    CLOCK_SIZE = 84
    MEDIUM_DIGIT_SIZE = 64
    SMALL_DIGIT_SIZE = 44

    LARGE_TEXT_SIZE = 50
    MEDIUM_TEXT_SIZE = 40
    SMALL_TEXT_SIZE = 30

    WHITE = (255,255,255,255)
    RED = (255, 0, 0, 255)
    GREEN = (0, 255, 0, 255)

    DIGIT_FONT = 'Digital-7 Mono'
    TEXT_FONT = 'Built Titling'

    def __init__(self) :
        self.x = 0
        self.batch = pyglet.graphics.Batch()
        self.elements = []

        self.running = False
        self.state = None

    def getBatch(self) :
        return self.batch

    def isRunning(self) :
        return self.running

    def execute(self) :
        self.running = True

    def die(self) :
        self.running = False

    def updateElements(self) :
        for e in self.elements :
            e.update()

    def addScores(self, maxDigits, leftLabel='GUEST', rightLabel='HOME') :
        e = ScoreboardElement(text=leftLabel, textFont=Scoreboard.TEXT_FONT, textSize=Scoreboard.LARGE_TEXT_SIZE, textColor=Scoreboard.WHITE,
                              updateFunc=self.state.getGuestScore, digitFont=Scoreboard.DIGIT_FONT,
                              digitSize=Scoreboard.SCORE_SIZE, digitColor=Scoreboard.RED, maxDigits=maxDigits, 
                              batch=self.batch)
        e.setCenterTop(Scoreboard.LEFT_CENTER,460)
        self.elements.append(e)

        e = ScoreboardElement(text=rightLabel, textFont=Scoreboard.TEXT_FONT, textSize=Scoreboard.LARGE_TEXT_SIZE, textColor=Scoreboard.WHITE,
                              updateFunc=self.state.getHomeScore, digitFont=Scoreboard.DIGIT_FONT,
                              digitSize=Scoreboard.SCORE_SIZE, digitColor=Scoreboard.RED, maxDigits=maxDigits,  
                              batch=self.batch)
        e.setCenterTop(Scoreboard.RIGHT_CENTER,460)
        self.elements.append(e)

    def addClock(self, height) :
        self.clockColon = pyglet.text.Label(':', font_name=Scoreboard.DIGIT_FONT,  
                                        font_size=Scoreboard.CLOCK_SIZE, color=Scoreboard.WHITE, 
                                        batch=self.batch)
        self.clockColon.anchor_x = 'center'
        self.clockColon.anchor_y = 'top'
        self.clockColon.position = (Scoreboard.CENTER, height)


        e = ScoreboardElement(text=None, textFont=Scoreboard.TEXT_FONT, textSize=0, 
                              updateFunc=self.state.getMinutes, digitFont=Scoreboard.DIGIT_FONT,
                              digitSize=Scoreboard.CLOCK_SIZE, digitColor=Scoreboard.GREEN, maxDigits=2, batch=self.batch)
        e.setRightTop(Scoreboard.CENTER - 20, height)
        self.elements.append(e)

        e = ScoreboardElement(text=None, textFont=Scoreboard.TEXT_FONT, textSize=0, 
                              updateFunc=self.state.getSeconds, digitFont=Scoreboard.DIGIT_FONT,
                              digitSize=Scoreboard.CLOCK_SIZE, digitColor=Scoreboard.GREEN, maxDigits=2, 
                              displayLeadingZeroes=True, batch=self.batch)
        e.setLeftTop(Scoreboard.CENTER+20, height)
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
    
    def handle_S(self) :
        self.state.modifyPeriod()
        self.updateElements()

