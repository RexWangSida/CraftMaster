import math
from pyglet.gl import *


class Screen(object):
    def __init__(self,game, exclusive):
        self.game = game
        # Whether or not the window exclusively captures the mouse.
        self.mouseExclusive = exclusive

    def mouseClick(self, x, y, button, modifiers):
        pass

    def update(self, dt):
        pass

    def mouseMove(self,x, y, dx, dy):
        pass

    def keyPressed(self,symbol, modifiers):
        pass

    def keyRelease(self,symbol, modifiers):
        pass

    def screenResize(self,width, height):
        pass

    def draw(self):
        pass

    def _setBGColor(self,R,G,B,A):
        if R<0 or R>1 or G<0 or G>1 or B<0 or B>1 or A<0 or A>1:
            raise ValueError("The value of RGBA should be between 0 and 1")
        glClearColor(R, G, B, A)

    def _setup_fog(self, R, G, B, A,start,end):
        """ Configure the OpenGL fog properties.

        """
        if R<0 or R>1 or G<0 or G>1 or B<0 or B>1 or A<0 or A>1:
            raise ValueError("The value of RGBA should be between 0 and 1")
        # Enable fog. Fog "blends a fog color with each rasterized pixel fragment's
        # post-texturing color."
        glEnable(GL_FOG)
        # Set the fog color.
        glFogfv(GL_FOG_COLOR, (GLfloat * 4)(R, G, B, A))
        # Say we have no preference between rendering speed and quality.
        glHint(GL_FOG_HINT, GL_DONT_CARE)
        # Specify the equation used to compute the blending factor.
        glFogi(GL_FOG_MODE, GL_LINEAR)
        # How close and far away fog starts and ends. The closer the start and end,
        # the denser the fog in the fog range.
        glFogf(GL_FOG_START, start)
        glFogf(GL_FOG_END, end)

    def _setup_glbasic(self):
        """ Basic OpenGL configuration.
        """
        # Enable culling (not rendering) of back-facing facets -- facets that aren't
        # visible to you.
        glEnable(GL_CULL_FACE)
        # Set the texture minification/magnification function to GL_NEAREST (nearest
        # in Manhattan distance) to the specified texture coordinates. GL_NEAREST
        # "is generally faster than GL_LINEAR, but it can produce textured images
        # with sharper edges because the transition between texture elements is not
        # as smooth."
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

    def _setup_2d(self):
        """ Configure OpenGL to draw in 2d.

        """
        width, height = self.game.get_size()
        glDisable(GL_DEPTH_TEST)
        viewport = self.game.get_viewport_size()
        glViewport(0, 0, max(1, viewport[0]), max(1, viewport[1]))
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, max(1, width), 0, max(1, height), -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def _setup_3d(self,rotation,position):
        """ Configure OpenGL to draw in 3d.
            @param rotation tuple of (x,y) representing the the rotation angle in  the z-axis down and the ground up
            @param position tuple of (x,y,z) representing the position of the view
        """
        width, height = self.game.get_size()
        glEnable(GL_DEPTH_TEST)
        viewport = self.game.get_viewport_size()
        glViewport(0, 0, max(1, viewport[0]), max(1, viewport[1]))
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(65.0, width / float(height), 0.1, 60.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        x, y = rotation
        glRotatef(x, 0, 1, 0)
        glRotatef(-y, math.cos(math.radians(x)), 0, math.sin(math.radians(x)))
        x, y, z = position
        glTranslatef(-x, -y, -z)
