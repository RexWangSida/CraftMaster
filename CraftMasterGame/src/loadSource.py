import os,math

from block import Block
from pyglet.gl import *

# the icon of the window
ICON = pyglet.image.load(os.path.join("source","icon.png"))
# the music played when any blocks are built
BUILDSOUND = pyglet.media.load(os.path.join("source",'build.wav'),streaming=False)
# the music played when any blocks are distroied
DESTROYSOUND = pyglet.media.load(os.path.join("source",'destroy.wav'),streaming=False)
# the background music played whenever the game is started
BACKGROUNDMUSIC = pyglet.media.load(os.path.join("source",'bgmusic.wav'))

# blocks of the game
BRICK = Block("BRICK",(0, 0), (0, 0), (0, 0), 1, os.path.join("texture","Brick.png"),destroyable = True)
GRASS = Block("GRASS",(0, 0), (0, 1), (1, 1), 2, os.path.join("texture","Grass.png"),destroyable = True)
STONE = Block("STONE",(0, 0), (0, 0), (0, 0), 1, os.path.join("texture","Stone.png"),destroyable = True)
MARBLE = Block("MARBLE",(0, 0), (0, 0), (0, 0), 1, os.path.join("texture","Marble.png"),destroyable = False)

#list of all types of blocks in the game
ALLBLOCKS = [BRICK,GRASS,STONE,MARBLE]
# list of all types of destroyable blocks of the game
PLACEBLOCKS = [BRICK,GRASS,STONE]
