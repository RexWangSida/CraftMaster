from pyglet.gl import *

from game import Game
from loadSource import *

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

def main():
    game = Game(width=WINDOW_WIDTH, height=WINDOW_HEIGHT,caption='CraftMaster', resizable=True, refreshRate = 100)
    game.set_fullscreen()
    game.set_icon(ICON)
    BACKGROUNDMUSIC.play()
    pyglet.app.run()

if __name__ == '__main__':
    main()
