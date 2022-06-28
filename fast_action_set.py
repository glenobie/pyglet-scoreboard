import pyglet
from die import Die, DiceSet, SortedDiceSet

class FastActionSet :
    def __init__(self, batch) :
        self.batch = batch

    def handle_L(self, modified = False) :
        for d in self.dice :
            d.roll()
        
class HistoryMakerGolfSet(FastActionSet) :

    def __init__(self, batch) :
        FastActionSet.__init__(self, batch)
        
        dice = []

        self.white = Die((255,255,255), sides=6, batch=self.batch)
        dice.append(self.white)
        self.green = Die((40,200,40), sides=6, text_color=(255,255,255,255),batch=self.batch)
        dice.append(self.green)
        self.black = Die((0,0,0), sides=6, text_color=(255,255,255,255),batch=self.batch)
        dice.append(self.black)
        self.gray = Die((100,100,100), sides=6, text_color=(255,255,255,255),batch=self.batch)
        dice.append(self.gray)

        for d in dice :
            d.scale(0.8)

        self.allDice = DiceSet(dice)
        self.allDice.setPosition(100, 100, 30)

        d = []
        d.append(self.gray.makeClone())
        d.append(self.black.makeClone())
        self.holeSet = SortedDiceSet(d)
        self.holeSet.setPosition(100,300,30)




    def handle_L(self, modified) :
        self.allDice.roll()
