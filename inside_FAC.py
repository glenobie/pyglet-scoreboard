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
    LINE_SPACING = 10

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

########################################################################
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
                ( (FACField.F_GRAY, 1, 'MINOR\nMAJOR'), (FACField.F_GRAY, 1, 'DUMP INS'),
                  (FACField.F_WHITE, 1, 'FLIP'), None, (FACField.F_WHITE, 1, 'FLIP'),
                  (FACField.F_GRAY, 1, 'BREAKAWAY'), (FACField.F_GRAY, 1, 'PASS TO')
                ) ]

    minor_odds = [2, 4, 6, 8, 10, 12, 13, 16, 18, 22, 26, 30, 36, 38, 46, 60, 78, 83, 100, 122, 146, 200]
    minors = ['Diving', 'Charging', 'Delay of game', 'Close hand on puck', 'Clipping',
                'Elbowing', 'Boarding (INJ?)', 'Boarding', 'Kneeing', 'Unsportsmanlike conduct',
                'Goatender interference', 'Holding the stick', 'Cross-checking', 'Slashing (INJ?)', 'Slashing', 'High Sticking',
                'Interference', 'Rouging (INJ?)', 'Roughing', 'Tripping', 'Holding', 'Hooking']

    major_odds = [1, 2, 4, 5, 6, 7, 12, 17, 22, 27, 32, 37, 42, 47, 52, 200]
    majors = ['Charging (INJ?)', 'Elbowing (INJ?)', 'Boarding (INJ?)', 'Kneeing (INJ?)', 'Slashing (INJ?)',
                'Spearing (INJ?)', 'Fighting (1)', 'Fighting (2)', 'Fighting (3)', 'Fighting (4)', 'Fighting (5)',
                'Fighting (6)', 'Fighting (7)', 'Fighting (8)', 'Fighting (9)', 'Fighting']

    assist_odds = [6, 11, 15, 18, 20, 60, 95, 125, 150, 170, 185, 195, 200 ]
    assists = ['Highest', '2nd Highest', '3rd Highest', '4th Highest', 'Lowest',
            'x (1)', 'x (2)', 'x (3)', 'x (4)', 'x (5)', 'x (6)', 'x (7)', 'x (8)']

    blk_texts = ['\nNo block if Defense FC = 3', '\nNo block if Defense FC = 3', '','','','',
                 '\nBlocked if Defense FC = 0','\nBlocked if Defense FC = 0',
                 '\nBlocked if Defense FC = 0 or 1', '\nBlocked if Defense FC = 0 or 1' ]
    wide_texts = ['\nOn target if Defense FC = 3','\nOn target if Defense FC = 3','','','','',
                  '\nWide shot if Defense FC = 0', '\nWide shot if Defense FC = 0',
                  '\nWide shot if Defense FC = 0 or 1','\nWide shot if Defense FC = 0 or 1']
    brk_texts = ['\nNot if FC = 0', '\nNot if FC <= 1','','','','','','','',
                '\nOr if FC = 3']
    dump_texts = ['Use Pass # if Defense FC = 3','','','','','','Forced Dump In if Defense FC = 0','Forced Dump In if Defense FC = 0 or 1']
    take_texts = ['Use Pass # if Defense FC = 0 or 1','Use Pass # if Defense FC = 0','','','','AST if Offense FC = 3 and PASS','',
                'Takeaway if Defense FC = 3']
    loose_texts = ['No hit if Defense PHY = LOW', 'No hit if Defense PHY = LOW', '','','','AST if Offense FC = 3 and PASS',
                    'Loose Puck if Defense PHY = HIGH', 'Loose Puck if Defense PHY = HIGH'] 
    interception_texts = ['','No AST if Offense FC = 0 or 1','No AST if Offense FC = 0', 'No AST if Offense FC = 0',
                        'No AST if Offense FC = 0 or 1','No AST if Offense FC = 0',
                        'No AST if Offense FC = 0','No AST if Offense FC = 0']
    penalty_texts = ['No penalty if Defense PHY = LOW', '','','','','AST if Offense FC = 3 and PASS',
                    'Penalty check if Defense PHY = HIGH']
    dump_in_odds = [30, 54, 64, 104, 144, 184, 188, 194, 200]
    dump_in_text = ['Goalie recovers,\nleaves for x', 'Defense x\nchases down puck', 'Goalie covers (faceoff)',
                'Puck battle:\nOff. Cq vs. Def. Cz', 'Puck battle:\nOff. LWq vs. Def. RDz', 'Puck battle:\nOff. RWq vs. Def. LDz',
                'Puck battle:\nVisiting C vs. Home C', 'Puck battle:\nVisiting LW vs. Home RDz', 'Puck battle:\nVisiting RW vs. Home LDz']
    fo_odds = [90, 108, 117, 126, 135, 144, 153, 162, 171, 180, 184, 186, 194, 195, 200]
    fo_texts = ['x, (y)','+1 x, (y)', '+2 x, (y)', '+3 x, (y)', '+4 x, (y)', '+5 x, (y)', 
               '+6 x, (y)', '+7 x, (y)', '+8 x, (y)', '+9 x, (y)', 'KO: Low', 'KO: High', 
               'KO: Visitor', 'KO: Both', 'KO: Home']

    def __init__(self, loader) :
        FACSet.__init__(self, loader)
        self.paintBackground(FACSet.W_COLOR_WHITE)
        self.fg = pyglet.graphics.OrderedGroup(62)
        self.FACbg = pyglet.graphics.OrderedGroup(5)

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

    def draw(self) :
        self.batch.draw()


    def getPenaltyID(self) :
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

    def getTextViaOdds(self, value, odds, texts) :
        for a in range(0, len(odds)) :
            if value <= odds[a] :

                break
        return texts[a]

    def getRandomPenalty(self) :
        minorText = self.getTextViaOdds(random.randint(1, 200), InsideSportsSet.minor_odds, InsideSportsSet.minors)
        majorText = self.getTextViaOdds(random.randint(1, 200), InsideSportsSet.major_odds, InsideSportsSet.majors)

        return minorText +'\n' + majorText


    def getAST(self) :
        text = self.getTextViaOdds(random.randint(1, 200), InsideSportsSet.assist_odds, InsideSportsSet.assists)
        return text.replace('x', random.choice(self.positions))

    def getShotNumber(self) :
        shotNum = str(random.randint(1, 100))
        if int(shotNum) <= 99 and int(shotNum) >= 90 :
            shotNum += (' (BRK)')
        return '# ' + shotNum

    def getRebound(self) :
        rebound_odds =  [45, 65, 85, 115]
        rebounds = ['Def x', 'Off x', 'Visiting x', 'Home x']
        p = random.randint(1,200)
        if p <= 115 :
            text = self.getTextViaOdds(115, rebound_odds, rebounds)
            text = text.replace('x', random.choice(self.positions))
        elif p <= 165 :
            adj = [ ['', ''],[' +1', ''],[' +2', ''],[' +3', ''],['', ' +1'],['', ' +2'],
                    ['', ' +3'],['', ' +4'],['', ' +5'],['', ' +6']]
            q = random.choice(adj)
            text = 'Off ' + random.choice(self.positions) + q[0] + ' vs. '
            text += 'Def ' + random.choice(self.positions)  + q[1]
        elif p <= 195 :
            adj = ['Def LD', 'Def LD +1', 'Def LD +2', 'Def LD +3',
                    'Def RD', 'Def RD +1', 'Def RD +2', 'Def RD +3']
            defense = []
            text = 'Off ' + random.choice(self.positions) + ' vs. ' + random.choice(adj)
        else :
            leftovers = ['Off LW vs. Def RD',
                         'Off RD vs. Def R',
                         'Off RW vs. Def LD',
                         'Off LD vs. Def RW',
                         'Off RD vs. Def LW']
            text = random.choice(leftovers)
        return text

    def getShootout(self) :
        odds = [41, 69, 75, 87, 95, 98, 99, 100]
        shots = ['\nWrist', '\nBackhand','\nSlap', '\nSnap', 'Wide of net', 'Goalpost', 'Over the net', 'Crossbar']
        p = random.randint(1,100)
        text = self.getTextViaOdds(p, odds, shots)
        if p <= 87 :
            text = '# ' + str(p) + ' ' + text
        return text

    def getBlockText(self) :
        p = random.randint(1,4)
        if p >= 3 :
            return ''
        else :
            value = random.randint(1,10)
            text = 'if ' + random.choice(self.positions) + ' DEF >= ' + str(value)
            if p == 1 :
                text = 'Blocked ' + text + InsideSportsSet.blk_texts[value-1]
            elif p == 2 :
                text = 'Wide shot ' + text + InsideSportsSet.wide_texts[value-1]
            return text

    def getBreakaway(self) :
        p = random.random()
        forwards = ['C', 'RW','LW']
        if p <= 0.4 :
            text = 'None for ' + random.choice(forwards)
            penalty = random.random()
            if penalty < 0.0375 :
                text += '\nPen. Shot?'
        else :
            value = random.randint(1,10)
            text = random.choice(forwards) + ' BRK >= ' + str(value) + InsideSportsSet.brk_texts[value-1]
        return text

    def getFaceOff(self) :
        text = self.getTextViaOdds(random.randint(1, 200), InsideSportsSet.fo_odds, InsideSportsSet.fo_texts)
        text = text.replace('y', 'H' if random.random() < 0.58 else 'V')
        return text.replace('x', random.choice(self.positions))

    def getDumpIn(self) :
        p = random.randint(1,200)
        text = self.getTextViaOdds(p, InsideSportsSet.dump_in_odds, InsideSportsSet.dump_in_text)
        if p <= 54 :
            defense = ['LD', 'RD']
            text = text.replace('x', random.choice(defense))
        elif p <= 184:
            adjPairs = [['',''], ['',' +1'], ['',' +2'], ['',' +3'],['',' +4'],['',' +5'],['',' +6'],
                    [' +1',''],[' +2',''],[' +3','']]
            adj = random.choice(adjPairs)
            text = text.replace('q', adj[0])
            text = text.replace('z', adj[1])
        else:
            home_adv = ['',' +1', ' +2']
            text= text.replace('z', random.choice(home_adv))
        return text

    def getDefenseText(self) :
        p = random.randint(1,5)
        text2 = ''
        if p == 1 :
            value = random.randint(1,8)
            text1 = 'Forced Dump In if ' + random.choice(self.positions) + ' DEF >= ' + str(value)
            text2 = InsideSportsSet.dump_texts[value-1]
        elif p == 2 :
            value = random.randint(1,8)
            text1 = 'Loose Puck if ' + random.choice(self.positions) + ' HIT >= ' + str(value)
            text2 = InsideSportsSet.loose_texts[value-1]
        elif p == 3 :
            value = random.randint(1,8)
            text1 = 'Takeaway if ' + random.choice(self.positions) + ' TAKE >= ' + str(value)
            text2 = InsideSportsSet.take_texts[value-1]
        elif p == 4 :
            value = random.randint(1,8)
            pos = random.choice(self.positions)
            if value >= 8 :
                v = [8,12,16,20,25]
                value = random.choice(v)
                pos = 'any defender'
            else :
                text2 = InsideSportsSet.penalty_texts[value-1]
            text1 = 'Penalty if ' + pos + ' PEN >= ' + str(value)
            
        else :
            value = random.randint(5,12)
            combos = ['LD+RD', 'LW+LD', 'RW+RD', 'C+LW', 'C+RW']
            text1 = 'Interception if ' + random.choice(combos) + ' DEF >= ' + str(value)
            text2 = InsideSportsSet.interception_texts[value-5]
        return (text1, text2)

    def generateFAC(self) :
        random.shuffle(self.positions)
        defense = self.getDefenseText()
        self.valueFields[0].setText(defense[1])
        self.valueFields[1].setText(defense[0])
        self.valueFields[2].setText(self.getPenaltyID())
        self.valueFields[3].setText(self.getLoosePuck())
        self.valueFields[4].setText(self.getRebound())
        self.valueFields[5].setText(self.getShotNumber())
        self.valueFields[6].setText(self.positions[0])
        self.valueFields[7].setText('(' + self.positions[1] + ')')
        self.valueFields[8].setText(self.getRandomPenalty())
        self.valueFields[9].setText(self.getDumpIn())
        self.valueFields[10].setText('# '+str(random.randint(1,40)))
        self.valueFields[11].setText(self.getBlockText())
        self.valueFields[12].setText(self.getFaceOff())
        self.valueFields[13].setText('# ' + str(random.randint(1,40)))
        self.valueFields[14].setText(self.getAST())
        self.valueFields[15].setText(self.getShootout())
        self.valueFields[16].setText(self.getBreakaway())


    def handle_L(self) :
        self.generateFAC()


    def handle_K(self) :
        0
