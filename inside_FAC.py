import random
import pyglet
from fac_set import FACSet

class FACField() :
    F_BLUE = (0, 255, 255)
    F_YELLOW = (255,255,150)
    F_GRAY = (180,180,180)
    F_WHITE = (240,240,240)
    F_GREEN = (102, 255, 102)
    B_BLACK = (0,0,0)


    FONT_SIZE = 18
    FONT_COLOR = (0, 0, 0, 255)
    LINE_SPACING = 8


    def __init__(self, font_size, bgColor, width, height, text='', bold=False,
                              batch=None, fgGroup = None, bgGroup = None) :
        self.border = pyglet.shapes.BorderedRectangle(0, 0, width, height, color = bgColor, border_color=FACField.B_BLACK,
                                                        batch = batch, group = bgGroup)
        self.doc = pyglet.text.document.FormattedDocument(text)

        self.doc.set_style(0, len(self.doc.text), dict(color=FACField.FONT_COLOR,
                                                       font_size=font_size,
                                                       font_name=FACSet.TEXT_FONT,
                                                       align='center',
                                                       bold=bold,
                                                       line_spacing=font_size+FACField.LINE_SPACING))
        self.layout = pyglet.text.layout.TextLayout(self.doc, multiline=True, width=width, batch=batch, group=fgGroup)
        self.layout.anchor_x = 'left'
        self.layout.anchor_y = 'bottom'
        #self.layout.content_valign = 'bottom'

    def setPosition(self, left, bottom) :
        self.left = left
        self.bottom = bottom
        self.border.position = (left, bottom)

        #center layout in border
        x = left #+ (self.border.width - self.layout.content_width) / 2
        y = bottom +  (self.border.height - self.layout.content_height + FACField.LINE_SPACING) // 2
        self.layout.position = (x, y)

    #replace all >= or <= in document text with underlined > or underline <
    def replaceComparators(self, comparator) :
       while (True) :
            pos = self.doc.text.find(comparator)
            if pos > 0  :
                self.doc.delete_text(pos+1, pos+2)
                self.doc.set_style(pos, pos+1, dict(baseline=1, underline=FACField.FONT_COLOR))
            else :
                break


    def setText(self, text) :
        # change <= and >=
        self.doc.text = text
        self.replaceComparators('<=')
        self.replaceComparators('>=')
        self.setPosition(self.left, self.bottom)


class InsideSportsSet(FACSet) :

    FIELD_WIDTH = 130
    FIELD_HEIGHT = 61
    SPACE = 3

    TEXT_FIELD_COLOR = FACField.F_GRAY

    # (color, width, title, index into list of card fields)
    COLUMNS = [ ( (FACField.F_GRAY, 1, 'PENALTY'), (FACField.F_GRAY, 1, 'LOOSE\nPUCK'),
                  (FACField.F_GRAY, 1, 'REBOUND'), (FACField.F_GRAY, 1, 'SHOTS'),
                  (FACField.F_BLUE, 3, 'FLIP'), (FACField.F_BLUE, 3, 'FLIP'),
                  (FACField.F_GRAY, 1, 'PASS TO')),
                ( (FACField.F_WHITE, 2, 'FLIP'), (FACField.F_WHITE, 2, 'FLIP'),
                  (FACField.F_YELLOW, 2, 'FLIP'), (FACField.F_GREEN, 2, 'FLIP'),
                  None, None, (FACField.F_BLUE, 1, 'FLIP')  ),
                ( None, None, None, None, None, None, (FACField.F_BLUE, 1, 'FLIP') ),
                ( (FACField.F_WHITE, 2, 'FLIP'), (FACField.F_WHITE, 2, 'FLIP'),
                    (FACField.F_YELLOW, 1, 'FLIP'), (FACField.F_GREEN, 3, 'FLIP'),
                    (FACField.F_WHITE, 1, 'FLIP'), (FACField.F_GRAY, 1, 'FO'),
                    (FACField.F_BLUE, 2, 'FLIP')),
                ( None, None, (FACField.F_GRAY, 1, 'SHOOTOUT'), None,
                 (FACField.F_WHITE, 1, 'FLIP'), (FACField.F_GRAY, 1, 'ASSIST'), None),
                ( (FACField.F_GRAY, 1, 'MAJOR\nMINOR'), (FACField.F_GRAY, 1, 'DUMP INS'),
                  (FACField.F_WHITE, 1, 'FLIP'), None, (FACField.F_WHITE, 1, 'FLIP'),
                  (FACField.F_GRAY, 1, 'BREAKAWAY'), (FACField.F_GRAY, 1, 'PASS TO')
                ) ]

    def __init__(self, loader) :
        FACSet.__init__(self, loader)
        self.paintBackground(FACSet.W_COLOR_WHITE)
        self.fg = pyglet.graphics.OrderedGroup(62)
        self.FACbg = pyglet.graphics.OrderedGroup(5)

        #self.deckIndex = 0
        #self.facs = self.readFACSFromFile('crease_FACs', 14)
        #random.shuffle(self.facs)

        self.positions = ['C', 'LW', 'RW', 'LD', 'RD']

        self.createLayout()


    def createLayout(self)  :
        self.textFields = []
        self.valueFields = []
        x = InsideSportsSet.SPACE
        for col in InsideSportsSet.COLUMNS :
            y = InsideSportsSet.SPACE
            for spot in col :
                if not(spot is None) :
                    if spot[0] == InsideSportsSet.TEXT_FIELD_COLOR :

                        f = FACField(16, spot[0], InsideSportsSet.FIELD_WIDTH * spot[1] + InsideSportsSet.SPACE * (spot[1] - 1),
                                    InsideSportsSet.FIELD_HEIGHT, spot[2], batch=self.batch, fgGroup=self.fg,
                                    bgGroup=self.FACbg, bold=True)

                        self.textFields.append(f)
                    else :
                        f = FACField(16, spot[0], InsideSportsSet.FIELD_WIDTH * spot[1] + InsideSportsSet.SPACE * (spot[1] - 1),
                                    InsideSportsSet.FIELD_HEIGHT, spot[2], batch=self.batch, fgGroup=self.fg,
                                    bgGroup=self.FACbg)
                        self.valueFields.append(f)
                    f.setPosition(x, y)

                y += InsideSportsSet.FIELD_HEIGHT + InsideSportsSet.SPACE
            x += InsideSportsSet.FIELD_WIDTH + InsideSportsSet.SPACE

    def readFACSFromFile(self, filename, numFACS) :
        facs = []
        f = self.loader.file(filename, mode='r')
        for j in range(0, numFACS) :
            list = f.readline().split(';')
            strings = []
            for s in list :
                strings.append(s.replace('\n', '').replace('$', '\n'))
            facs.append(strings)
        return facs

    def draw(self) :
        self.batch.draw()

    def flipForward(self) :
        self.deckIndex += 1
        if self.deckIndex >= len(self.facs) :
            random.shuffle(self.facs)
            self.deckIndex = 0

        for fieldIndex in range(8, 17) :
            self.valueFields[fieldIndex].setText(self.facs[self.deckIndex][fieldIndex].strip('\n'))
        for fieldIndex in range(0, 8) :
            self.valueFields[fieldIndex].setText(self.facs[self.deckIndex-1][fieldIndex].strip('\n'))

    def getPenaltyText(self) :
        pen = [ ' + OPP if PEN 5 or Higher',
                ' + OPP if PEN 4 or Higher',
                ' + OPP if PEN 3 or Higher',
                ' + OPP if PEN 2 or Higher',
                ' + OPP if Pen 1 or Higher',
                ' + OPP',
                ' + Highest OPP',
                ' + Highest OPP' ]
        penaltyNum = random.randint(1,40)
        if (penaltyNum >= 39) :
            return 'Goalie Penalty?'
        text = str(penaltyNum)
        s = random.randint(1,5)
        if s == 4 and penaltyNum >= 30 :
            text += ' Double Minor'
        elif s == 5 :
            text += str(pen[(penaltyNum-1) // 5])
        return text

    def getLoosePuck(self) :
        team = random.randint(1, 10)
        text = ''
        inj = 0
        if team <= 3 :
            text += 'Home '
            inj = random.randint(1, 6)
        elif team <= 6 :
            text += 'Visiting '
            inj = random.randint(1, 6)
        elif team <= 8 :
            text += 'Off '
        else :
            text += 'Def '

        pos = random.randint(0, 4)
        text += self.positions[pos]
        if inj == 1 :
            text = 'FO: INJ? ' + text

        return text

    def getRandomPenalty(self) :
        minor_odds = [2, 4, 6, 8, 10, 12, 13, 16, 18, 22, 26, 30, 36, 38, 46, 60, 78, 83,100, 122, 146, 200]
        minors = ['Diving', 'Charging', 'Delay of game', 'Close hand on puck', 'Clipping',
                    'Elbowing', 'Boarding (INJ?)', 'Boarding', 'Kneeing', 'Unsportsmanlike conduct',
                    'Goatender interference', 'Holding the stick', 'Cross-checking', 'Slashing (INJ?)', 'High Sticking',
                    'interference', 'Rouging (INJ?)', 'Tripping', 'Holding', 'Hooking']

        major_odds = [1, 2, 4, 5, 6, 7, 12, 17, 22, 27, 32, 37, 42, 47, 52, 200]
        majors = ['Charging (INJ?)', 'Elbowing (INJ?)', 'Boarding (INJ?)', 'Kneeing (INJ?)', 'Slashing (INJ?)',
                    'Spearing (INJ?)', 'Fighting (1)', 'Fighting (2)', 'Fighting (3)', 'Fighting (4)', 'Fighting (5)',
                    'Fighting (6)', 'Fighting (7)', 'Fighting (8)', 'Fighting (9)', 'Fighting']
        # Minors
        # diving - 2
        # charging - 2
        # delay of game - 2
        # close hand on puck - 2
        # Clipping - 2
        # Elbowing - 2
        # boarding - 4, 1 with INJ
        # kneeing - 2
        # unsportsmanlike conduct - 4
        # goaltender interference - 4
        # holding the stick - 4
        # cross-checking - 6
        # slashing - 10, 2 with INJ
        # high sticking - 14
        # interference - 18
        # roughing - 22, 5 with INJ
        # tripping - 22
        # holding - 24
        # hooking - 54

        # MAjors
        # charging - 1 (INJ?)
        # elbowing - 1 (INJ?)
        # boarding - 2 both with INJ
        # kneeing - 1 (INJ?)
        # slashging - 1 inj
        # spearing - 1(inj)
        # fighting ((1 - 9), 5 each (45 total)
        # fighting - 193 - 45




    def getAST(self) :
        p = random.randint(1, 200)
        odds = [6, 11, 15, 18, 20, 60, 95, 125, 150, 170, 185, 195, 200 ]
        asts = ['HIGH', '2nd High', '3rd High', '4th High', 'Lowest',
                'x (1)', 'x (2)', 'x (3)', 'x (4)', 'x (5)', 'x (6)', 'x (7)', 'x (8)']
        for a in range(0, len(odds)) :
            if p <= odds[a] :

                break
        text = asts[a]
        return text.replace('x', self.positions[random.randint(0,4)])


    def generateFAC(self) :
        random.shuffle(self.positions)
        self.valueFields[6].setText(self.positions[0])
        self.valueFields[7].setText('(' + self.positions[1] + ')')
        shotNum = str(random.randint(1, 100))
        if int(shotNum) <= 99 and int(shotNum) >= 90 :
            shotNum += (' (BRK)')
        self.valueFields[5].setText('# '+shotNum)
        self.valueFields[13].setText('# ' + str(random.randint(1,40)))
        self.valueFields[2].setText(self.getPenaltyText())
        self.valueFields[3].setText(self.getLoosePuck())
        self.valueFields[10].setText('# '+str(random.randint(1,40)))
        self.valueFields[14].setText(self.getAST())



    def handle_L(self) :
        #self.flipForward()
        self.generateFAC()


    def handle_K(self) :
        0
