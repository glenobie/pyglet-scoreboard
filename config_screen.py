import pyglet

from key_handler import KeyHandler


class ConfigScreen(KeyHandler) :
    
    def __init__(self) :
        self.batch = pyglet.graphics.Batch()

    def getBatch(self) :
        return self.batch

    

    