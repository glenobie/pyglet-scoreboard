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
                    (InsideFACField.F_YELLOW, 4, 'FLIP'), None,
                    None, None),
                ( None,None,None,None,None,(InsideFACField.F_WHITE, 3, 'FLIP'),(InsideFACField.F_GRAY, 3, 'FASTBREAK #'),(InsideFACField.F_BLUE, 4, 'FLIP')),
                ( None, None, None,None,None,None,None,None),
                 ( (InsideFACField.F_GREEN, 3, 'Fastbreak\nFLIP'), (InsideFACField.F_WHITE, 3, 'FLIP'),
                (InsideFACField.F_GRAY, 3, 'Fastbreak/Alternate\nASSIST LOOKUP'), None,None,None,None,None),
                ( None, None, None,  None, (InsideFACField.F_YELLOW, 1, 'G'), 
                        (InsideFACField.F_WHITE, 2, 'FLIP'),(InsideFACField.F_GRAY, 2, 'JUMP'), None),
                ( None,None,None,None,(InsideFACField.F_GRAY, 1, 'SHOT'), None,None,(InsideFACField.F_GRAY, 1, 'PASS\nTO')) ]


    jump_odds = [10, 20, 110, 128, 137, 146, 155, 164, 173, 182, 191, 200]
    jump_texts = ['OB: HOME', 'OB: AWAY', 'x', '+1 x', '+1 x', '+2 x', '+3 x', '+4 x', '+5 x', '+6 x', '+7 x', '+8 x', '+9 x']

    defense_odds = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 
                    120, 125, 130, 135, 140, 145, 150, 200]
    defense_texts = [ ['Steal if x STL >= 2','No Steal if x is SAFE'], ['Steal if x STL >= 4',''], ['Steal if x STL >= 6',''], ['Steal if x STL >= 8',''],
                      ['F(1) if x CF >= 20','No Foul if x in SAFE'], ['F(1) if x CF >= 40',''], ['F(1) if x CF >= 60',''], ['F(1) if x CF >= 80',''], 
                      ['Steal if Defender STL >= 1','No Steal if Defender in SAFE'], ['Steal if Defender STL >= 3',''], ['Steal if Defender STL >= 5',''], 
                      ['Steal if Defender STL >= 7',''], ['Steal if Defender STL >= 9','Steal if Defense in PRESS'], ['Steal if Defender STL >= 10','Steal if Defense in PRESS'], 
                      ['F(1) if Defender CF >= 10','No Foul if Defender in SAFE'], ['F(1) if Defender CF >= 30',''], ['F(1) if Defender CF >= 50',''],
                      ['F(1) if Defender CF >= 70',''], ['F(1) if Defender CF >= 90','F(1) if Defense in PRESS'], ['F(1) if Defender CF >= 100','F(1) if Defense in PRESS'],
                      ['TO if Opposing Team TO >= 1',''], ['TO if Opposing Team TO >= 2',''], ['TO if Opposing Team TO >= 3',''], ['TO if Opposing Team TO >= 4',''],
                      ['TO if Opposing Team TO >= 5',''], ['TO if Opposing Team TO >= 6',''], ['TO if Opposing Team TO >= 7',''], ['TO if Opposing Team TO >= 8',''] ,
                      ['TO if Opposing Team TO >= 9',''], ['TO if Opposing Team TO >= 10', ''] , ['','TO if opposing team in PRESS'],
                      ['', 'AST if Defense in PRESS and x AST >= 4'], ['', 'AST if Defense in PRESS and x AST >= 8'], ['', 'AST if Defense in PRESS and x AST >= 12'], 
                      ['', 'AST if Defense in PRESS and x AST >= 16'], ['', 'AST if Defense in PRESS and x AST >= 20'],['', 'AST if Defense in PRESS and x AST >= 24'],
                      
                      
                      ['','']]
    defs = [1,1,1,1,2,2,2,2,4,4,4,4,5,5,5,5,6,6,6,6,7,7,7,7,8,8,8,8,9,9,9,9,10,10,10,10,11,11,11,11,12,12,12,12,12]
    rebound_odds = [24, 44, 57, 67, 77, 88, 99, 106, 111, 116, 137, 151, 161, 166, 170, 178, 183, 190, 195, 200]
    rebound_texts = [['Def C (x) or Off', 36], ['Def PF (x) or Off', 35], ['Def F (x) or Off', 25],
                    ['Def SG (x) or Off', 19], ['Def PG (x) or Off', 19], ['Off C (x) or Def', 21],
                    ['Off PF (x) or Def', 21], ['Off F (x) or Def', 13], ['Off SG (x) or Def', 9], 
                    ['Off PG (x) or Def', 9], ['Def C (x) or Def', 36], ['Def PF (x) or Def', 27],
                    ['Def F (x) or Def', 19], ['Def SG (x) or Def', 9], ['Def PG (x) or Def', 7],
                    ['Loose Ball Foul',0], ['OFF OB',0], ['DEF OB',0], ['Jump',0], ['HOME y',0]]


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
        self.valueFields[21].setFont(FACSet.DINGBAT_FONT, InsideFACField.FONT_RED, 44)
        self.valueFields[21].setBaseline(-12)

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
        p = random.randint(1,200)
        text1 = ''
        text2 = ''
        mom = ''
        if p <= 60 :
            text1 = 'Missed Shot if\n'
            if p <= 15 :
                text1 += random.choice(self.positions) + ' DEF >= ' + str(3*random.randint(1,3))
            else :                
                value = random.choice(InsidePaintSet.defs)
                if value >= 11 :
                    text2 = 'Missed Shot if Shooter is DOUBLED'
                elif value <= 2 :
                    text2 = 'Not Missed if Shot Defender is\nSAFE or DOUBLING'

                text1 += 'Defender DEF >= ' + str(value)
                

        elif p <= 117 :
            text1 = 'Blocked Shot if\n'
            if p <= 75 :
                value = random.randint(1,3)
                if value <= 2 :
                    text2 = 'No Block if Shot Defender is SAFE'
                text1 += 'Defender BLK >= ' + str(value)
                mom = 'G'
            elif p <= 92 :
                text1 += 'C BLK >= ' + str(random.randint(4,20))
            elif p <= 104 :
                text1 += 'PF BLK >= ' + str(random.randint(4,16))
            elif p <= 111 :
                text1 += 'F BLK >= ' + str(random.randint(4,10))
            elif p <= 114 :
                text1 += 'SG BLK >= ' + str(random.randint(4,6))
            else :
                text1 += 'PG BLK >= ' + str(random.randint(4,6))
            
        elif p <= 147 :
            q = random.randint(1,30)
            text = 'Shooting Foul if\n Shooter FD >= ' + str(q)
            if q // 4 == 0 :
                text += ' (3pt) '
        return [mom, text1, text2]

    def getPassDefense(self) :
        data = self.getTextViaOdds(random.randint(1,200), InsidePaintSet.defense_odds, InsidePaintSet.defense_texts)
        pos = random.choice(self.positions)
        text1 = data[0].replace('x', pos )
        text2 = data[1].replace('x', pos )
        return [ text1, text2 ]


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
            text = '# 1 if team Momentum >= +' + str(((101-p)//5 +1 ))
        return [mom,num, text]

    def getFastBreak(self) :
        pos = random.choice(self.positions)
        text = 'Fastbreak\n'
        text += pos + ' (' + str(random.randint(1,20)) + ')'
        if random.random() < 0.5 :
            text += ' STL only'
        return text

    def getAssistLookup(self) :
        text = 'TODO'
        p = random.randint(1,200)
        if p <= 100 :
            text = random.choice(self.positions) + ' (' + str(random.randint(1,10)) + ')'
        elif p <= 125 :
            text = random.choice(self.positions) + ' (' + str(random.randint(11,15)) + ')'
        elif p <= 145 :
            subset = ['PF','PG','SG','F']
            text = random.choice(subset) + ' (' + str(random.randint(16,20)) + ')'
        elif p <= 165 :
            anys = [26, 26, 27,27, 28, 28, 29, 29, 30, 30, 31, 31, 32, 32, 32, 33, 34, 34, 35, 35]
            text = 'Any ('+ str(random.choice(anys)) + ')'
        elif p <= 175 : 
            subset = ['C or PF', 'F or G']
            text = random.choice(subset) + ' (' + str(random.randint(11,15)) + ')'
        elif p <= 185 :
            subset = ['PF or C', 'G or PG']
            text = random.choice(subset) + ' (' + str(random.randint(16,20)) + ')'
        else : 
            leftovers = ['PF or F (17)', 'PG (11)', 'PG (12)', 'PG (13)', 'PG (14)', 'PG (15)', 
                        'PG (21)', 'PG (21)', 'PG (22)', 'PG (22)', 'PG (23)', 'PG (23)', 'PG (24)', 
                        'PG (25)', 'PG (25)']
            text = random.choice(leftovers)
        return text

    def getFouler(self) :
        return 'TODO'

    def getRebound(self) :
        result = self.getTextViaOdds(random.randint(1,200), InsidePaintSet.rebound_odds, InsidePaintSet.rebound_texts)
        text = result[0]
        if result[1] > 0 :
            text = text.replace('x', str(random.randint(1, result[1])))
        return text + ' TODO'
    




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
        self.valueFields[22].setText(self.getJump())   
        self.valueFields[19].setText(self.getFastBreak()) 
        passDefs = self.getPassDefense()
        self.valueFields[1].setText(passDefs[1])
        self.valueFields[2].setText(passDefs[0])
        shotDefs = self.getShotDefense()
        self.valueFields[16].setText(shotDefs[1])
        self.valueFields[15].setText(shotDefs[2])
        self.valueFields[21].setText(shotDefs[0])
        self.valueFields[6].setText(self.getRebound())
        self.valueFields[7].setText(self.getFouler())
        self.valueFields[14].setText(self.getAssistLookup())
        self.valueFields[20].setText(self.getAssistLookup())

    def handle_L(self) :
        self.generateFAC()


    def handle_K(self) :
        0
