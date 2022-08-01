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
    COLUMNS = [ ( (InsideFACField.F_GRAY, 2, 'REBOUND'), (InsideFACField.F_GRAY, 2, 'F(2) ?\nWHO?'),
                  (InsideFACField.F_GRAY, 2, 'ASSIST TO'), 
                  (InsideFACField.F_YELLOW, 6, 'FLIP'), (InsideFACField.F_GRAY, 1, 'SHOT'),
                  (InsideFACField.F_BLUE, 7, 'FLIP'), (InsideFACField.F_BLUE, 7, 'FLIP'),
                  (InsideFACField.F_GRAY, 1, 'PASS\nTO')),
                (None, None, None, None, (InsideFACField.F_YELLOW, 5, 'FLIP'),
                                    None,None,(InsideFACField.F_BLUE, 2, 'FLIP')),
                ( (InsideFACField.F_GREEN, 4, 'FLIP'), (InsideFACField.F_WHITE, 4, 'FLIP'),
                                    (InsideFACField.F_BLUE, 2, 'FLIP'), None, None, None, None, None ),
                ( None, None, None, None, None, None, None, (InsideFACField.F_BLUE, 2, 'FLIP')),
                ( None, None, (InsideFACField.F_BLUE, 2, 'FLIP'), None, None, None, None, None),
                (None,None,None,None,None,None,None,(InsideFACField.F_BLUE, 2, 'FLIP') ),
                ( (InsideFACField.F_GREEN, 3, 'Offensive Rebound\nFLIP'), (InsideFACField.F_WHITE, 3, 'FLIP'),
                    (InsideFACField.F_GRAY, 3, 'Regular\nASSIST LOOKUP'), (InsideFACField.F_YELLOW, 6, 'FLIP'),
                    (InsideFACField.F_YELLOW, 5, 'FLIP'), None,
                    None, None),
                (None,None,None,None,None,(InsideFACField.F_WHITE, 3, 'FLIP'),(InsideFACField.F_GRAY, 3, 'FASTBREAK #'),(InsideFACField.F_BLUE, 4, 'FLIP')),
                (None, None, None,None,None,None,None,None),
                 ( (InsideFACField.F_GREEN, 3, 'Fastbreak\nFLIP'), (InsideFACField.F_WHITE, 3, 'FLIP'),
                (InsideFACField.F_GRAY, 3, 'Fastbreak/Alternate\nASSIST LOOKUP'), None,None,None,None,None),
                ( None, None, None,  None, None, 
                        (InsideFACField.F_WHITE, 2, 'FLIP'),(InsideFACField.F_GRAY, 2, 'JUMP'), None),
                (None,None,None,None,(InsideFACField.F_GRAY, 1, 'SHOT'), None,None,(InsideFACField.F_GRAY, 1, 'PASS\nTO')) ]


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

    def draw(self) :
        self.batch.draw()

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
            texts[1] = self.positions[1] + ' (' + str(11 - value % 10) + ')'
            if value >= 17 :
                texts[2] = 'Any ' + str(random.randint(21, 30) )


        return texts
        # 20 for each position
        # each position (1-20), with (1-12) asterisked
 
        # function -> second number = (11 - first % 10 )
        # if first >= 17, third elemnt is 'Any ' + a random 21-30

    def generateFAC(self) :
        random.shuffle(self.positions)
        self.valueFields[16].setText('# '+str(random.randint(1,40)))
        self.valueFields[15].setText('# '+str(random.randint(1,40)))
        self.valueFields[11].setText('Offensive Rebound\n# '+str(random.randint(1,40)))
        passes = self.getPassTo()
        self.valueFields[4].setText(passes[0])
        self.valueFields[8].setText(passes[1])
        self.valueFields[10].setText(passes[2])

    

    def handle_L(self) :
        self.generateFAC()


    def handle_K(self) :
        0
