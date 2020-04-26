from pyglet.graphics import TextureGroup
from pyglet import image
##  Documentation for Block.
#   @brief Module for creating Block object.

class Block(object):
##  @brief Block module
#   @details Creat a block instance with name, coordinates, texture and specify whether it's destroyable

    def __init__(self,name, top, bottom, side, size, texturePath,destroyable = True):
        ##  @brief Initializer
        #   @param top,bottom,side: the coordinates of the left corner for each side on the texture image
        #   @param size: the size of the image
        self.name = name
        self.coordinates = self._tex_coords(top, bottom, side, size)
        self.texture = TextureGroup(image.load(texturePath).get_texture())
        self.destroyable = destroyable


    def __eq__(self, other):
        ##  @brief To decide whether the name of this block equals another
        #   @return True for equals and False for not
        return self.name == other.name

    def _tex_coords(self, top, bottom, side, size):
        ##  @brief collect coordinates on texture image for the top, bottom and side of each block
        #   @return List of the texture squares for the top, bottom and side
        top = self._tex_coord(*top,n = size)
        bottom = self._tex_coord(*bottom, n = size)
        side = self._tex_coord(*side, n = size)
        result = []
        result.extend(top)
        result.extend(bottom)
        result.extend(side * 4)
        return result

    def _tex_coord(self, x, y, n):
        ##  @brief convert the size to coordinates in texture image
        #   @return the bounding vertices of the texture square
        m = 1.0 / n
        dx = x * m
        dy = y * m
        return dx, dy, dx + m, dy, dx + m, dy + m, dx, dy + m
