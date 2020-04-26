import math
from creature import Creature
class Player(Creature):
    def __init__(self,position):
        super(Player,self).__init__(position = position, height = 2, health = 100)
        self.energy = 100

    def get_sight_vector(self):
        """ Returns the current line of sight vector indicating the direction
        the Player is looking.
        """
        x, y = self.rotation
        # y ranges from -90 to 90, or -pi/2 to pi/2, so m ranges from 0 to 1 and
        # is 1 when looking ahead parallel to the ground and 0 when looking
        # straight up or down.
        m = math.cos(math.radians(y))
        # dy ranges from -1 to 1 and is -1 when looking straight down and 1 when
        # looking straight up.
        dy = math.sin(math.radians(y))
        dx = math.cos(math.radians(x - 90)) * m
        dz = math.sin(math.radians(x - 90)) * m
        return (dx, dy, dz)

    def switchFlyState(self):
        """switch the flying state of player"""
        self.flying = not self.flying
