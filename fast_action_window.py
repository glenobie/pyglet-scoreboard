import pyglet
from fac_set import FACSet, ChoiceFAC
from die import Die
from random import seed
import time

####################################################################
class FastActionWindow() :

    def __init__(self) :
        
        seed(time.time_ns())
        self.fac = ChoiceFAC()

    def draw(self) :
        self.fac.draw()
 
    def setFACSet(self, fac):
        self.fac = fac

    def handle_L(self) :
        self.fac.handle_L()

    def handle_K(self) :
        self.fac.handle_K()

    def handle_J(self) :
        self.fac.handle_J()

    def clearFACSet(self) :
        self.fac = ChoiceFAC()


