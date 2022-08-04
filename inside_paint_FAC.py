import random
import pyglet
from inside_FAC_field import InsideFACField
from fac_set import FACSet

########################################################################
class InsidePaintSet(FACSet) :

    FIELD_WIDTH = 63
    FIELD_HEIGHT = 56
    SPACE = 3

    TEXT_FIELD_COLOR = InsideFACField.F_GRAY

    # (color, width, title, index into list of card fields)
    COLUMNS = [ ( (InsideFACField.F_GRAY, 2, 'REBOUND'), (InsideFACField.F_GRAY, 2, 'F(2)?\nWHO?'),
                  (InsideFACField.F_GRAY, 1, 'AST\nTO'), 
                  (InsideFACField.F_YELLOW, 6, 'FLIP'), (InsideFACField.F_GRAY, 1, 'SHOT'),
                  (InsideFACField.F_BLUE, 7, 'FLIP'), (InsideFACField.F_BLUE, 7, 'FLIP'),
                  (InsideFACField.F_GRAY, 1, 'PASS\nTO')),
                ( None, None, (InsideFACField.F_BLUE, 1, 't'), None, (InsideFACField.F_YELLOW, 1, 'G'),
                                    None,None,(InsideFACField.F_BLUE, 2, 'FLIP')),
                ( (InsideFACField.F_GREEN, 4, 'FLIP'), (InsideFACField.F_WHITE, 4, 'FLIP'),
                                    (InsideFACField.F_BLUE, 2, 'FLIP'), None, (InsideFACField.F_YELLOW, 4, 'FLIP'), None, None, None ),
                ( None, None, None, None, None, None, None, (InsideFACField.F_BLUE, 2, 'FLIP')),
                ( None, None, (InsideFACField.F_BLUE, 2, 'FLIP or\nFLIP'), None, None, None, None, None),
                ( None,None,None,None,None,None,None,(InsideFACField.F_BLUE, 2, 'FLIP') ),
                ( (InsideFACField.F_GREEN, 3, 'Offensive Rebound\nFLIP'), (InsideFACField.F_WHITE, 3, 'FLIP'),
                    (InsideFACField.F_GRAY, 3, 'Regular\nASSIST LOOKUP'), (InsideFACField.F_YELLOW, 6, 'FLIP'),
                    (InsideFACField.F_YELLOW, 5, 'FLIP'), None,
                    None, None),
                ( None,None,None,None,None,(InsideFACField.F_WHITE, 3, 'FLIP'),(InsideFACField.F_GRAY, 3, 'FASTBREAK #'),(InsideFACField.F_BLUE, 4, 'FLIP')),
                ( None, None, None,None,None,None,None,None),
                 ( (InsideFACField.F_GREEN, 3, 'Fastbreak\nFLIP'), (InsideFACField.F_WHITE, 3, 'FLIP'),
                (InsideFACField.F_GRAY, 3, 'Fastbreak/Alternate\nASSIST LOOKUP'), None,None,None,None,None),
                ( None, None, None,  None, None, 
                        (InsideFACField.F_WHITE, 2, 'FLIP'),(InsideFACField.F_GRAY, 2, 'JUMP'), None),
                ( None,None,None,None,(InsideFACField.F_GRAY, 1, 'SHOT'), None,None,(InsideFACField.F_GRAY, 1, 'PASS\nTO')) ]


    jump_odds = [10, 20, 110, 128, 137, 146, 155, 164, 173, 182, 191, 200]
    jump_texts = ['OB: HOME', 'OB: AWAY', 'x', '+1 x', '+1 x', '+2 x', '+3 x', '+4 x', '+5 x', '+6 x', '+7 x', '+8 x', '+9 x']

    defense_odds = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 200]
    defense_texts = ['Steal if x STL >= 2', 'Steal if x STL >= 4','Steal if x STL >= 6','Steal if x STL >= 8',
                     'F(1) if x CF >= 20', 'F(1) if x CF >= 40', 'F(1) if x CF >= 60', 'F(1) if x CF >= 80', 
                      'Steal if Defender STL >= 1', 'Steal if Defender STL >= 3', 'Steal if Defender STL >= 5', 
                      'Steal if Defender STL >= 7', 'Steal if Defender STL >= 9', 'Steal if Defender STL >= 10', 
                      'F(1) if Defender CF >= 10', 'F(1) if Defender CF >= 30','F(1) if Defender CF >= 50',
                      'F(1) if Defender CF >= 70','F(1) if Defender CF >= 90','F(1) if Defender CF >= 100',
                      'TO if Opposing Team TO >= 1', 'TO if Opposing Team TO >= 2', 'TO if Opposing Team TO >= 3', 'TO if Opposing Team TO >= 4', 
                      'TO if Opposing Team TO >= 5', 'TO if Opposing Team TO >= 6', 'TO if Opposing Team TO >= 7', 'TO if Opposing Team TO >= 8', 
                      'TO if Opposing Team TO >= 9', 'TO if Opposing Team TO >= 10', '']

    def __init__(self, loader) :
        FACSet.__init__(self, loader)
        self.paintBackground(FACSet.W_COLOR_WHITE)
        self.positions = ['C', 'PF', 'F', 'SG', 'PG']
        self.fg = pyglet.graphics.OrderedGroup(62)
        self.FACbg = pyglet.graphics.OrderedGroup(5)
        self.createLayout()


    def createLayout(self)  :
        self.textFields = []
        self.valueFields = []
        x = InsidePaintSet.SPACE
        for col in InsidePaintSet.COLUMNS :
            y = InsidePaintSet.SPACE
            for spot in col :
                if not(spot is None) :
                    if spot[0] == InsidePaintSet.TEXT_FIELD_COLOR :

                        f = InsideFACField(16, spot[0], InsidePaintSet.FIELD_WIDTH * spot[1] + InsidePaintSet.SPACE * (spot[1] - 1),
                                    InsidePaintSet.FIELD_HEIGHT, spot[2], batch=self.batch, fgGroup=self.fg,
                                    bgGroup=self.FACbg, bold=True)

                        self.textFields.append(f)
                    else :
                        f = InsideFACField(16, spot[0], InsidePaintSet.FIELD_WIDTH * spot[1] + InsidePaintSet.SPACE * (spot[1] - 1),
                                    InsidePaintSet.FIELD_HEIGHT, spot[2], batch=self.batch, fgGroup=self.fg,
                                    bgGroup=self.FACbg)
                        self.valueFields.append(f)
                    f.setPosition(x, y)

                y += InsidePaintSet.FIELD_HEIGHT + InsidePaintSet.SPACE
            x += InsidePaintSet.FIELD_WIDTH + InsidePaintSet.SPACE

        self.valueFields[3].setFont(FACSet.DINGBAT_FONT, InsideFACField.FONT_RED, 44)
        self.valueFields[3].setBaseline(-12)
        self.valueFields[4].setFont(FACSet.DINGBAT_FONT, InsideFACField.FONT_RED, 44)
        self.valueFields[4].setBaseline(-12)

    def draw(self) :
        self.batch.draw()

    def getTextViaOdds(self, value, odds, texts) :
        for a in range(0, len(odds)) :
            if value <= odds[a] :
                break
        return texts[a]

    # returns a list of 3 pass To values
    def getPassTo(self) :
        texts = ['','','']
        p = random.random()
        random.shuffle(self.positions)
        texts[0] = self.positions[0]

        if (p > 0.5) :
            texts[0] += ' '
            value = random.randint(1,20)
            if value <= 12 :
                texts[0] += '*'
            texts[0] += '(' + str(value) + ')'
            texts[1] = self.positions[1] + ' (' + ('1' if value == 20 else str(11 - value % 10) ) + ')'
            if value >= 17 :
                texts[2] = 'Any ' + str(random.randint(21, 30) )
        return texts

    def getJump(self) :
        text = self.getTextViaOdds(random.randint(1,200), InsidePaintSet.jump_odds, InsidePaintSet.jump_texts)
        text = text.replace('x', random.choice(self.positions))
        return text

    def getAssists(self) :
        random.shuffle(self.positions)
        t1 = self.positions[0]
        mom = ''
        t2 = 'y or\nx'
        if (random.random() < 0.5) :
            mom = 'G'
        else :
            t1 += ' ('
            t1 += str(random.randint(1,20))
            t1 += ')'
        
        if random.random() < 0.45 :
            x = random.randint(6,10)
            y = 11 - x
        else :
            x = random.randint(1,5)
            y = 6 - x
        t2 = self.positions[1] + ' (' +str(x)+ ') or\n' + self.positions[2] + ' (' +str(y) + ')'
        #90 add up to 11, 110 add up to 6

        return [mom,t1,t2]

    def getShotDefense(self) :
        return ''
        # missed if [pos] def >= (3, 6, 9) -> 15
        # missed if defender def >= (1, 2, 4, 5, 6, 7, 8, 9, 10, 11) 4 each, (12) 5 -> 45
        # blocked if defender BLK >= (1, 2, 3), 5 each -> 15
        # blocked if center BLK >= (4-20) -> 17
        # " " PF >= (4-16) -> 12
        # forward .+ (4-10) -> 7
        #, g, pg, (4, 5, 6) -> 6
        # total blocked = 57
        # F(2) WHO : (1-30) with + (3pt) if divisble by 4: -> 30
        # total = 60 + 57 + 30 = 147


    def getDefense(self) :
        text = self.getTextViaOdds(random.randint(1,200), InsidePaintSet.defense_odds, InsidePaintSet.defense_texts)
        return text.replace('x', random.choice(self.positions))


    def getShotNumber(self) :
        p = random.randint(1, 100)
        mom = ''
        num = '# ' + str(p)
        text = ''
        if p <= 20 :
            mom = 'G'
        if p <= 8 and random.random() < 0.5 :
            text = '# 100 if AWAY and HRF >= ' + str(p)
        elif p <= 25 :
            text = '# 100 if team Momentum <= ' + str(-((p-1)//5 +1 ))
        elif p >= 93 and random.random() < 0.5 :
            text = '# 1 if HOME and HRF >= ' + str(101-p)
        elif p >= 76 :
            text = '# 100 if team Momentum >= +' + str(((101-p)//5 +1 ))
        return [mom,num, text]

    def getFastBreak(self) :
        pos = random.choice(self.positions)
        text = 'Fastbreak\n'
        text += pos + ' (' + str(random.randint(1,20)) + ')'
        if random.random() < 0.5 :
            text += ' STL only'
        return text

    def generateFAC(self) :
        random.shuffle(self.positions)
        shot = self.getShotNumber()
        self.valueFields[4].setText(shot[0])
        self.valueFields[9].setText(shot[1])
        self.valueFields[0].setText(shot[2])
        self.valueFields[18].setText('# '+str(random.randint(1,40)))
        self.valueFields[17].setText('# '+str(random.randint(1,40)))
        self.valueFields[13].setText('Offensive Rebound\n# '+str(random.randint(1,40)))
        passes = self.getPassTo()
        self.valueFields[5].setText(passes[0])
        self.valueFields[10].setText(passes[1])
        self.valueFields[12].setText(passes[2])
        assists = self.getAssists()
        self.valueFields[3].setText(assists[0])
        self.valueFields[8].setText(assists[1])
        self.valueFields[11].setText(assists[2])
        self.valueFields[21].setText(self.getJump())   
        self.valueFields[19].setText(self.getFastBreak()) 
        self.valueFields[2].setText(self.getDefense())

    def handle_L(self) :
        self.generateFAC()


    def handle_K(self) :
        0
