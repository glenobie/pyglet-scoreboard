import socket
import pyglet
from game_picker import GamePicker


##################################################
# start me up!

isPi = socket.gethostname() == "raspberrypi"
picker = GamePicker(800, 480, isPi)
picker.activate() # should work on Linux, won't on windows
pyglet.clock.schedule_interval(picker.update, 1/30.0)
pyglet.app.run()
