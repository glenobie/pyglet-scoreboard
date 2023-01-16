import pyglet
from die import Die
from dice_set import DiceSet 
from bordered_dice_set import BorderedDiceSet
from playing_cards import PlayingCardDeck
from playing_cards import CardDisplay
from functools import partial

from fac_set import FACSet
class MindenCricketSet(FACSet) :

    def __init__(self, loader) :
        FACSet.__init__(self, loader)
        self.createDice()
        self.createCards()

    def createDice(self) :
        d1 = Die(Die.D_DARK_GREEN, sides=6, text_color=Die.T_WHITE,batch=self.batch)
        d1.setInteriorSpacingPct(0.2)
        d2 = Die(Die.D_GRAY, sides=6, text_color=Die.T_WHITE,batch=self.batch)
        d2.setInteriorSpacingPct(0.2)

        self.dice = BorderedDiceSet([d1, d2], batch=self.batch)
        self.dice.setPosition(460, 320, 16)

    def createCards(self) :
        self.deck = PlayingCardDeck()
        self.cardDisplay = CardDisplay(140, self.deck, self.batch)
        self.cardDisplay.setPosition(80,420)

    def draw(self) :
        self.batch.draw()

    def handle_L(self) :
        self.dice.roll()
        self.deck.draw()

    def handle_K(self) :
        self.dice.roll()

    def handle_J(self):
        self.deck.shuffle()
