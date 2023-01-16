import random
import pyglet
from fac_set import FACSet

class PlayingCardDeck() :
    CARD_FONT = 'Playing Cards'

    def __init__(self) :
        self.deck = []
        self.drawnCardListeners = []
        self.drawnCardIndex = -1

        # Add capital and lowercase letters to array
        for c in range(65, 91) : 
            self.deck.append(c)
        for c in range(97, 123) :
            self.deck.append(c)

        random.shuffle(self.deck)

        # for c in deck :
        #    print(chr(c)) 
        
    def addDrawnCardListener(self, listener) :
        self.drawnCardListeners.append(listener)

    def draw(self) :
        self.drawnCardIndex += 1
        if (self.drawnCardIndex < len(self.deck)) :
            for l in self.drawnCardListeners :
                l.cardDrawn(self.deck[self.drawnCardIndex])

    def shuffle(self) :
        self.drawnCardIndex = -1
        random.shuffle(self.deck)
        if (self.drawnCardIndex < len(self.deck)) :
            for l in self.drawnCardListeners :
                l.cardDrawn(ord('?'))

class CardDisplay() :

    THREES = [67, 80, 99, 112]
    JACKS = [75, 88, 107, 120]
    COURT = [74, 75, 76, 77, 87, 88, 89, 90, 106, 107, 108, 109, 119, 120, 121, 122]

    BLACK = (0,0,0,255)
    RED = (255,0,0,255)

    def __init__(self, font_size, deck, batch) :
        self.font_size = font_size
        self.deck = deck
        self.batch = batch
        self.fg = pyglet.graphics.OrderedGroup(2)
        self.bg = pyglet.graphics.OrderedGroup(1)
        deck.addDrawnCardListener(self)

        self.cardDoc = pyglet.text.document.UnformattedDocument('?')
        self.cardDoc.set_style(0, len(self.cardDoc.text),  dict(font_name = PlayingCardDeck.CARD_FONT,
                                                                  font_size = self.font_size,
                                                                  color=CardDisplay.BLACK))
        self.cardLayout = pyglet.text.layout.TextLayout(self.cardDoc, batch=self.batch, group=self.fg)
        self.cardLayout.anchor_y = 'top'
        self.cardLayout.anchor_x = 'left'

        self.cardBack = pyglet.shapes.Rectangle(0, 0, 164, 220, color=(255,255,255), batch=self.batch, group = self.bg)

        self.labelDoc = pyglet.text.document.UnformattedDocument('test')
        self.labelDoc.set_style(0, len(self.labelDoc.text),  dict(font_name = FACSet.TEXT_FONT,
                                                                       font_size = 20,
                                                                       color=(255,255,255,255)))
        self.labelLayout = pyglet.text.layout.TextLayout(self.labelDoc, batch=batch, group = self.fg)
        self.labelLayout.anchor_y = 'center'
        self.labelLayout.anchor_x = 'center'
        
    def cardDrawn(self, card) :
        # print(chr(card))
        self.cardDoc.text = chr(card)
        c = CardDisplay.BLACK if card > ord('Z') else CardDisplay.RED
        self.cardDoc.set_style(0, len(self.cardDoc.text), dict(color=c))
        self.rewriteLabel(card)
    
    def setPosition(self, x, y) :
        #TODO remove constants for computations
        self.cardLayout.position = (x,y)
        self.cardBack.position = (x + 19, y - 220)
        self.labelLayout.position = (x+106, y-260)

    def rewriteLabel(self, card) :
        text = ''
        if card in CardDisplay.THREES :
            text = 'Extras?'
        elif card in CardDisplay.JACKS :
            text = 'Extras? / Dismissal?'
        elif card in CardDisplay.COURT :
            text = 'Dismissal?'
        self.labelDoc.text = text