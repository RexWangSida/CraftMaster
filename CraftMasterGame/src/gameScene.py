import sys,time

from pyglet.gl import *
from pyglet.window import key, mouse

from screen import Screen
from loadSource import *
from shape import Shape3D

if sys.version_info[0] >= 3:
    xrange = range
    if sys.version_info[0] * 10 + sys.version_info[1] >= 38:
        time.clock = time.process_time

class  GameScene(Screen):
    def __init__(self,game,placeBlocks):
        super(GameScene,self).__init__(game,True)
        self.label = pyglet.text.Label('', font_name='Arial', font_size=18,
            x=10, y=self.game.height - 10, anchor_x='left', anchor_y='top',
            color=(255,255,255, 255))
        ##Initialize crosshairs and add it to the batch
        self.reticle = None
        # A list of Block.name the player can place. Hit num keys to cycle.
        self.inventory = [block.name for block in placeBlocks]
        # The current block the user can place. Hit num keys to cycle.
        self.block = self.inventory[0]
        # Convenience list of num keys.
        self.num_keys = [
            key._1, key._2, key._3, key._4, key._5,
            key._6, key._7, key._8, key._9, key._0]

    def mouseClick(self, x, y, button, modifiers):
        """called when players move their mouses
        """
        vector = self.game.player.get_sight_vector()
        curPos, prePos = self.game.world.hit_test(self.game.player.position, vector)
        if (button == mouse.RIGHT) or \
            ((button == mouse.LEFT) and (modifiers & key.MOD_CTRL)):
            # ON OSX, control + left click = right click.
            if prePos:
                self.game.world.add_block(prePos, self.block)
                BUILDSOUND.play()
        elif button == pyglet.window.mouse.LEFT and curPos:
            block = self.game.world.world[curPos]
            if block in self.inventory:
                self.game.world.remove_block(curPos)
                DESTROYSOUND.play()


    def mouseMove(self, x, y, dx, dy):
        """called when player click the mouse"""
        #the sentivility of the mouse
        m = 0.15
        x, y = self.game.player.rotation
        x, y = x + dx * m, y + dy * m
        self.game.player.rotate(x,y)

    def keyPressed(self, symbol, modifiers):
        """called when player press any key"""
        if symbol == key.W:
            self.game.player.move("FORWARD")
        elif symbol == key.S:
            self.game.player.move("BACKWARD")
        elif symbol == key.A:
            self.game.player.move("LEFT")
        elif symbol == key.D:
            self.game.player.move("RIGHT")
        elif symbol == key.SPACE:
            if self.game.player.dy == 0:
                self.game.player.jump(self.game.world.gravity)
        elif symbol == key.ESCAPE:
            self.game.changeScene('set')
        elif symbol == key.TAB:
            self.game.player.switchFlyState()
        elif symbol in self.num_keys:
            index = (symbol - self.num_keys[0]) % len(self.inventory)
            self.block = self.inventory[index]


    def keyRelease(self, symbol, modifiers):
        """called when player release any key"""
        if symbol == key.W:
            self.game.player.stopMove("FORWARD")
        elif symbol == key.S:
            self.game.player.stopMove("BACKWARD")
        elif symbol == key.A:
            self.game.player.stopMove("LEFT")
        elif symbol == key.D:
            self.game.player.stopMove("RIGHT")


    def screenResize(self, width, height):
        """ Called when the window is resized to a new `width` and `height`.
        """
        # label
        self.label.y = height - 10
        # reticle
        if self.reticle:
            self.reticle.delete()
        x, y = self.game.width // 2, self.game.height // 2
        n = 10
        self.reticle = pyglet.graphics.vertex_list(4,
            ('v2i', (x - n, y, x + n, y, x, y - n, x, y + n))
        )

    def update(self, dt):
        """scheduled to be called repeatedly by the game"""
        self.game.world.updateWorld(1.0/self.game.refreshRate,self.game.player)
        m = 8
        dt = min(dt, 0.2)
        for _ in xrange(m):
            self.game.player.update(dt/m,self.game.world)


    def draw(self):
        """called by game to draw the current gamming scene"""
        ##set up the sky color
        self._setBGColor(*self.game.world.skyColor())
        self._setup_glbasic()
        self._setup_fog(*self.game.world.skyColor(),20.0,60.0)
        self._setup_3d(self.game.player.rotation, self.game.player.position)
        glColor3d(1, 1, 1)
        self.game.world.batch.draw()
        self._drawFocusedBlock()
        self._setup_2d()
        self._draw_label()
        self._draw_reticle()

    def _draw_label(self):
        """ Draw the label in the top left of the screen.
        """
        x, y, z = self.game.player.position
        self.label.text = '%02d (%.2f, %.2f, %.2f) %d / %d' % (
            pyglet.clock.get_fps(), x, y, z,
            len(self.game.world._shown), len(self.game.world.world))
        self.label.draw()

    def _draw_reticle(self):
        """ Draw the crosshairs in the center of the screen.
        """
        glColor3d(0, 0, 0)
        self.reticle.draw(GL_LINES)

    def _drawFocusedBlock(self):
        """ Draw black edges around the block that is currently under the
        crosshairs.

        """
        vector = self.game.player.get_sight_vector()
        block = self.game.world.hit_test(self.game.player.position, vector)[0]
        if block:
            x, y, z = block
            vertex_data = Shape3D.cube_vertices(x, y, z, 0.51)
            glColor3d(0, 0, 0)
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
            pyglet.graphics.draw(24, GL_QUADS, ('v3f/static', vertex_data))
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
