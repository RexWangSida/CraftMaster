from __future__ import division

import json,os
from sys import platform

from pyglet.gl import *

from player import Player
from world import World

from gameScene import GameScene
from mainScene import MainScene
from settingScene import SettingScene
from loadSource import ALLBLOCKS,PLACEBLOCKS

class Game(pyglet.window.Window):
##  @brief Game module
    def __init__(self, refreshRate = 60,*args, **kwargs):
        super(Game, self).__init__(*args, **kwargs)
        #Initialize the player at the position (0,0,0)
        self.player = Player((0,0,0))
        # Instance of the world that handles the world.
        self.world = World(ALLBLOCKS)
        #TICKS_PER_SEC
        self.refreshRate = refreshRate
        # This call schedules the `update()` method to be called
        # TICKS_PER_SEC. This is the main game event loop.
        pyglet.clock.schedule_interval(self.update, 1.0 / self.refreshRate)

        self.setScene = SettingScene(self)
        self.gameScene = GameScene(self,PLACEBLOCKS)
        self.mainScene = MainScene(self)
        #self.setScene = SetScene(self)
        #Initialize the first scene of the give
        self.lastScene = None
        self.currentScene  = None
        self.changeScene("main")
        # https://stackoverflow.com/questions/62116953/mouse-not-drawing-in-pyglet
        if platform == "linux" or platform == "linux2":
            # linux
            self.game_cursor = pyglet.image.load(os.path.join("texture", "mouse-small.png"))
            self.cursor = pyglet.window.ImageMouseCursor(self.game_cursor, 0, 0)
            self.set_mouse_cursor(self.cursor)


    def loadGame(self,file):
    ##  @brief read player position and world from the file
        if not os.path.exists(file):
            raise ValueError("The file cannot be found on the given path")
        with open(file, 'r') as f:
            data = json.load(f)
            self.player.position = data["position"]
            world = {}
            for block in data["world"]:
                for pos in data["world"][block]:
                    world[tuple(pos)] = block
            self.world.changeWorld(world)

    def saveGame(self,file):
    ##  @brief save the player position and world into the file
        world = {}
        for block in ALLBLOCKS:
            world[block.name] = []
        for i in self.world.world:
            world[self.world.world[i]].append(i)
        data = {"position":self.player.position,"world":world}
        with open(file,"w") as f:
              json.dump(data,f)

    def goBack(self):
    ##  @brief go back to the previous scene
        if (self.lastScene == None): return
        self.currentScene = self.lastScene
        self.set_exclusive_mouse(self.currentScene.mouseExclusive)

    def StartNewGame(self):
    ##  @brief clear the current game state and start a new game
        self.player.position = (0,0,0)
        self.world.clearWorld()
        self.world.setupWorld()
        self.changeScene("game")

    def changeScene(self,scene):
    ##  @brief change scene between gameScene, mainScene, and settingScene
        if scene == self.currentScene:
            return
        self.lastScene = self.currentScene
        if scene == "main":
            self.currentScene = self.mainScene
        elif scene == "game":
            self.currentScene = self.gameScene
        elif scene == "set":
            self.currentScene = self.setScene
        else:
            raise ValueError("The Game doesn't has the scene: "+ scene)
        self.set_exclusive_mouse(self.currentScene.mouseExclusive)

    def update(self,dt):
    ##  @brief This method is scheduled to be called repeatedly by the pyglet clock.
    #   @param dt : float The change in time since the last call.
        self.currentScene.update(dt)

    def on_mouse_press(self, x, y, button, modifiers):
    ##  @brief Called when a mouse button is pressed. See pyglet docs for button amd modifier mappings.
    #   @param x, y : int The coordinates of the mouse click. Always center of the screen if the mouse is captured.
    #   @param button : int Number representing mouse button that was clicked. 1 = left button, 4 = right button.
    #   @param modifiers : int Number representing any modifying keys that were pressed when the mouse button was clicked.
        self.currentScene.mouseClick(x, y, button, modifiers)

    def on_mouse_motion(self, x, y, dx, dy):
    ##  @brief Called when the player moves the mouse.
    #   @param x, y : int The coordinates of the mouse click. Always center of the screen if the mouse is captured.
    #   @param dx, dy : float The movement of the mouse.
        self.currentScene.mouseMove(x, y, dx, dy)

    def on_key_press(self, symbol, modifiers):
    ##  @brief Called when the player presses a key. See pyglet docs for key mappings.
    #   @param symbol : int Number representing the key that was pressed.
    #   @param modifiers : int Number representing any modifying keys that were pressed.
        self.currentScene.keyPressed(symbol, modifiers)

    def on_key_release(self, symbol, modifiers):
    ##  @brief Called when the player releases a key. See pyglet docs for key mappings.
    #   @param symbol : int Number representing the key that was pressed.
    #   @param modifiers : int Number representing any modifying keys that were pressed.
        self.currentScene.keyRelease(symbol, modifiers)

    def on_resize(self, width, height):
    ##  @brief Called when the window is resized to a new `width` and `height`.
        self.mainScene.screenResize(width,height)
        self.gameScene.screenResize(width,height)
        self.setScene.screenResize(width,height)

    def on_draw(self):
        ##  @brief Called by pyglet to draw the canvas.
        self.clear()
        self.currentScene.draw()
