import socket
import pyglet
from game_picker import MainWindow

################
# start me up! #
################

isPi = socket.gethostname() == "raspberrypi"
window = MainWindow(800, 1100, isPi)
window.activate() # should work on Linux, won't on windows
pyglet.clock.schedule_interval(window.update, 1/60.0)
pyglet.app.run()


