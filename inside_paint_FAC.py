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
        t1 = random.choice(self.positions)
        mom = ''
        t2 = 'y or\nx'
        if (random.random() < 0.5) :
            mom = 'G'
        else :
            t1 += ' (x)'
        return [mom,t1,t2]

    def getShotNumber(self) :
        p = random.randint(1, 100)
        mom = ''
        num = '# ' + str(p)
        if p <= 20 :
            mom = 'G'
        return [mom,num]


    def generateFAC(self) :
        random.shuffle(self.positions)
        shot = self.getShotNumber()
        self.valueFields[4].setText(shot[0])
        self.valueFields[9].setText(shot[1])
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

    def handle_L(self) :
        self.generateFAC()


    def handle_K(self) :
        0
