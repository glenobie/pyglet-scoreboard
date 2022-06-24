from pyglet import *
from pyglet.gl import *

key = pyglet.window.key
# Indented oddly on purpose to show the pattern:
UP    = 0b0001
DOWN  = 0b0010
LEFT  = 0b0100
RIGHT = 0b1000

class heart(pyglet.sprite.Sprite):
    def __init__(self, parent, image='ball.png', x=0, y=0):
        self.texture = pyglet.image.load(image)
        pyglet.sprite.Sprite.__init__(self, self.texture, x=x, y=y)

        self.parent = parent
        self.direction = UP | RIGHT # Starting direction

    def update(self):
        # We can use the pattern above with bitwise operations.
        # That way, one direction can be merged with another without collision.
        if self.direction & UP:
            self.y += 1
        if self.direction & DOWN:
            self.y -= 1
        if self.direction & LEFT:
            self.x -= 1
        if self.direction & RIGHT:
            self.x += 1

        if self.x+self.width > self.parent.width:
            self.direction = self.direction ^ RIGHT # Remove the RIGHT indicator
            self.direction = self.direction ^ LEFT # Start moving to the LEFT
        if self.y+self.height > self.parent.height:
            self.direction = self.direction ^ UP # Remove the UP indicator
            self.direction = self.direction ^ DOWN # Start moving DOWN
        if self.y < 0:
            self.direction = self.direction ^ DOWN
            self.direction = self.direction ^ UP
        if self.x < 0:
            self.direction = self.direction ^ LEFT
            self.direction = self.direction ^ RIGHT

    def render(self):
        self.draw()

# This class just sets up the window,
# self.heart <-- The important bit
class main(pyglet.window.Window):
    def __init__ (self, width=800, height=600, fps=False, *args, **kwargs):
        super(main, self).__init__(width, height, *args, **kwargs)
        self.x, self.y = 0, 0

        self.heart = heart(self, x=100, y=100)

        self.alive = 1

    def on_draw(self):
        self.render()

    def on_close(self):
        self.alive = 0

    def on_key_press(self, symbol, modifiers):
        if symbol == key.ESCAPE: # [ESC]
            self.alive = 0

    def render(self):
        self.clear()

        self.heart.update()
        self.heart.render()
        ## Add stuff you want to render here.
        ## Preferably in the form of a batch.

        self.flip()

    def run(self):
        while self.alive == 1:
            self.render()

            # -----------> This is key <----------
            # This is what replaces pyglet.app.run()
            # but is required for the GUI to not freeze
            #
            event = self.dispatch_events()

if __name__ == '__main__':
    x = main()
    x.run()