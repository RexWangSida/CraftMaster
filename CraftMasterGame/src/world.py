import sys,random,time

from pyglet.gl import *

from processQueue import ProcessQueue
from shape import Shape3D
from loadSource import *

if sys.version_info[0] >= 3:
    xrange = range
    if sys.version_info[0] * 10 + sys.version_info[1] >= 38:
        time.clock = time.process_time


class World(object):
    def __init__(self, allBlocks, sectorSize = 16, gravity = 20):

        # A Batch is a collection of vertex lists for batched rendering.
        self.batch = pyglet.graphics.Batch()

        # A mapping from position to the texture of the block at that position.
        # This defines all the blocks that are currently in the world.
        self.world = {}

        # Same mapping as `world` but only contains blocks that are shown.
        self.shown = {}

        # Mapping from position to a pyglet `VertextList` for all shown blocks.
        self._shown = {}

        # Mapping from sector to a list of positions inside that sector.
        self.sectors = {}
        self.sectorSize = sectorSize
        # Simple function queue implementation. The queue is populated with
        # __show_block() and __hide_block() calls The queue contains calls to
        #  __show_block() and __hide_block() so this method should be called if
        #  add_block() or remove_block() was called with immediate=False
        self.processQueue = ProcessQueue()
        #the gravity of the World
        self.gravity = gravity
        # Which sector the player is currently in.
        self.sector = None
        self.mode = "day"

        self.blocks = {}
        for block in allBlocks:
            self.blocks[block.name] = block

    def skyColor(self):
        """get the current skyColor
        return
        ----
        tuple of rgba representing the color of the current sky
        """
        if self.mode == "day":
            return(0.5, 0.69, 1.0, 1)
        elif self.mode == "night":
            return(0.05, 0, 0.15, 1)

    def changeMode(self,mode):
        """ change the mode of the World
            Parameters
            ----------
            mode: string
                wither day or night
        """
        if mode == "day" or mode == "night":
            self.mode = mode
        else:
            raise ValueError("The mode should be either 'day' or ' night'")

    def updateWorld(self,freshPeriod,player):
        """Update the world, called by gameScene every frame
            Parameters
            ----------
            freshPeriod : float
                The max time that this function can cost to update the World

            player : instance of Player
                the player that world update itself based on

        """
        self.processQueue.process_queue(1.0 / freshPeriod)
        sector = self._sectorize(player.position)
        if sector != self.sector:
            self._change_sectors(self.sector, sector)
            if self.sector is None:
                self.processQueue.process_entire_queue()
            self.sector = sector

    def clearWorld(self):
        """Clear the world"""
        self.batch = pyglet.graphics.Batch()
        self.world = {}
        self.shown = {}
        self._shown = {}
        self.sectors = {}
        self.processQueue = ProcessQueue()
        self.sector = None

    def changeWorld(self,world):
        """ change the world to
            Parameters
            ----------
            world : dict of {position : block Name}
                The dictionary that store the the block type for each positions

        """
        for i in world.keys():
            if len(i) != 3: raise ValueError("The world contains unreadable position")
            if world[i] not in self.blocks: raise ValueError("The given world contains block type that cannot be recognized")
            self.add_block(i,world[i],immediate = False)

    def setupWorld(self):
        """ Initialize the world by placing all the blocks.
        """
        n = 80  # 1/2 width and height of world
        s = 1  # step size
        y = 0  # initial y height
        for x in xrange(-n, n + 1, s):
            for z in xrange(-n, n + 1, s):
                # create a layer MARBLE.coordinates an GRASS.coordinates everywhere.
                self.add_block((x, y - 2, z), GRASS.name, immediate=False)
                self.add_block((x, y - 3, z), MARBLE.name, immediate=False)
                if x in (-n, n) or z in (-n, n):
                    # create outer walls.
                    for dy in xrange(-2, 3):
                        self.add_block((x, y + dy, z), MARBLE.name, immediate=False)

        # generate the hills randomly
        o = n - 10
        for _ in xrange(120):
            a = random.randint(-o, o)  # x position of the hill
            b = random.randint(-o, o)  # z position of the hill
            c = -1  # base of the hill
            h = random.randint(1, 6)  # height of the hill
            s = random.randint(4, 8)  # 2 * s is the side length of the hill
            d = 1  # how quickly to taper off the hills
            t = random.choice([GRASS, STONE, BRICK])
            for y in xrange(c, c + h):
                for x in xrange(a - s, a + s + 1):
                    for z in xrange(b - s, b + s + 1):
                        if (x - a) ** 2 + (z - b) ** 2 > (s + 1) ** 2:
                            continue
                        if (x - 0) ** 2 + (z - 0) ** 2 < 5 ** 2:
                            continue
                        self.add_block((x, y, z), t.name, immediate=False)
                s -= d  # decrement side lenth so hills taper off

    def collide(self, position, creature):
        """ Checks to see if the player at the given `position` and `height`
        is colliding with any blocks in the world.

        Parameters
        ----------
        position : tuple of len 3
            The (x, y, z) position to check for collisions at.
        creature : instance of subclasses of creature
            Player.

        Returns
        -------
        position : tuple of len 3
            The new position of the player taking into account collisions.

        """
        # How much overlap with a dimension of a surrounding block you need to
        # have to count as a collision. If 0, touching terrain at all counts as
        # a collision. If .49, you sink into the ground, as if walking through
        # tall GRASS.coordinates. If >= .5, you'll fall through the ground.
        pad = 0.25
        p = list(position)
        np = self._normalize(position)
        for face in [( 0, 1, 0),( 0,-1, 0),(-1, 0, 0),( 1, 0, 0),( 0, 0, 1),( 0, 0,-1)]:  # check all surrounding blocks
            for i in xrange(3):  # check each dimension independently
                if not face[i]:
                    continue
                # How much overlap you have with this dimension.
                d = (p[i] - np[i]) * face[i]
                if d < pad:
                    continue
                for dy in xrange(creature.height):  # check each height
                    op = list(np)
                    op[1] -= dy
                    op[i] += face[i]
                    if tuple(op) not in self.world:
                        continue
                    p[i] -= (d - pad) * face[i]
                    if face == (0, -1, 0) or face == (0, 1, 0):
                        # You are colliding with the ground or ceiling, so stop
                        # falling / rising.
                        creature.dy = 0
                    break
        return tuple(p)

    def hit_test(self, position, vector, max_distance=8):
        """ Line of sight search from current position. If a block is
        intersected it is returned, along with the block previously in the line
        of sight. If no block is found, return None, None.

        Parameters
        ----------
        position : tuple of len 3
            The (x, y, z) position to check visibility from.
        vector : tuple of len 3
            The line of sight vector.
        max_distance : int
            How many blocks away to search for a hit.
        @return the position of the block that is intersected with the sight and the previous position(for adding blocks)
        """
        m = 8
        x, y, z = position
        dx, dy, dz = vector
        previous = None
        for _ in xrange(max_distance * m):
            key = self._normalize((x, y, z))
            if key != previous and key in self.world:
                return key, previous
            previous = key
            x, y, z = x + dx / m, y + dy / m, z + dz / m
        return None, None

    def add_block(self, position, block, immediate=True):
        """ Add a block with the given `texture` and `position` to the world.

        Parameters
        ----------
        position : tuple of len 3
            The (x, y, z) position of the block to add.
        texture : list of len 3
            The coordinates of the texture squares. Use `tex_coords()` to
            generate.
        immediate : bool
            Whether or not to draw the block immediately.

        """
        if block not in self.blocks:
            raise ValueError("The block cannot be recognized in this world.")
        if position in self.world:
            self.remove_block(position, immediate)
        self.world[position] = block
        self.sectors.setdefault(self._sectorize(position), []).append(position)
        if immediate:
            if self._exposed(position):
                self._show_block(position)
            self._check_neighbors(position)

    def remove_block(self, position, immediate=True):
        """ Remove the block at the given `position`.

        Parameters
        ----------
        position : tuple of len 3
            The (x, y, z) position of the block to remove.
        immediate : bool
            Whether or not to immediately remove block from canvas.

        """
        if position not in self.world:
            raise ValueError("There is not block at the given position")
        del self.world[position]
        self.sectors[self._sectorize(position)].remove(position)
        if immediate:
            if position in self.shown:
                self._hide_block(position)
            self._check_neighbors(position)

    def _check_neighbors(self, position):
        """ Check all blocks surrounding `position` and ensure their visual
        state is current. This means hiding blocks that are not _exposed and
        ensuring that all _exposed blocks are shown. Usually used after a block
        is added or removed.

        """
        x, y, z = position
        for dx, dy, dz in [( 0, 1, 0),( 0,-1, 0),(-1, 0, 0),( 1, 0, 0),( 0, 0, 1),( 0, 0,-1)]:
            key = (x + dx, y + dy, z + dz)
            if key not in self.world:
                continue
            if self._exposed(key):
                if key not in self.shown:
                    self._show_block(key)
            else:
                if key in self.shown:
                    self._hide_block(key)

    def _exposed(self, position):
        """ Returns False is given `position` is surrounded on all 6 sides by
        blocks, True otherwise.

        """
        x, y, z = position
        for dx, dy, dz in [( 0, 1, 0),( 0,-1, 0),(-1, 0, 0),( 1, 0, 0),( 0, 0, 1),( 0, 0,-1)]:
            if (x + dx, y + dy, z + dz) not in self.world:
                return True
        return False

    def _show_block(self, position, immediate=True):
        """ Show the block at the given `position`. This method assumes the
        block has already been added with add_block()

        Parameters
        ----------
        position : tuple of len 3
            The (x, y, z) position of the block to show.
        immediate : bool
            Whether or not to show the block immediately.

        """
        if immediate:
            if position not in self.world:
                raise IndexError("There is no block at the given position in the current world")
            if self.world[position] not in self.blocks:
                raise ValueError("The stored block cannot be found in the block inventory.")
            block = self.blocks[self.world[position]]
            self.shown[position] = block
            x, y, z = position
            vertex_data = Shape3D.cube_vertices(x, y, z, 0.5)
            texture_data = list(block.coordinates)
            # create vertex list
            # FIXME Maybe `add_indexed()` should be used instead
            self._shown[position] = self.batch.add(24, GL_QUADS, block.texture,
                ('v3f/static', vertex_data),
                ('t2f/static', texture_data))
        else:
            self.processQueue.enqueue(self._show_block, position, True)

    def _hide_block(self, position, immediate=True):
        """ Hide the block at the given `position`. Hiding does not remove the
        block from the world.

        Parameters
        ----------
        position : tuple of len 3
            The (x, y, z) position of the block to hide.
        immediate : bool
            Whether or not to immediately remove the block from the canvas.

        """
        if immediate:
            if position not in self.shown:
                raise IndexError("There is no block at the given position that was shown")
            self.shown.pop(position)
            self._shown.pop(position).delete()
        else:
            self.processQueue.enqueue(self._hide_block, position, True)

    def _show_sector(self, sector):
        """ Ensure all blocks in the given sector that should be shown are
        drawn to the canvas.

        """
        for position in self.sectors.get(sector, []):
            if position not in self.shown and self._exposed(position):
                self._show_block(position, False)

    def _hide_sector(self, sector):
        """ Ensure all blocks in the given sector that should be hidden are
        removed from the canvas.

        """
        for position in self.sectors.get(sector, []):
            if position in self.shown:
                self._hide_block(position, False)

    def _change_sectors(self, before, after):
        """ Move from sector `before` to sector `after`. A sector is a
        contiguous x, y sub-region of world. Sectors are used to speed up
        world rendering.

        """
        before_set = set()
        after_set = set()
        pad = 4
        for dx in xrange(-pad, pad + 1):
            for dy in [0]:  # xrange(-pad, pad + 1):
                for dz in xrange(-pad, pad + 1):
                    if dx ** 2 + dy ** 2 + dz ** 2 > (pad + 1) ** 2:
                        continue
                    if before:
                        x, y, z = before
                        before_set.add((x + dx, y + dy, z + dz))
                    if after:
                        x, y, z = after
                        after_set.add((x + dx, y + dy, z + dz))
        show = after_set - before_set
        hide = before_set - after_set
        for sector in show:
            self._show_sector(sector)
        for sector in hide:
            self._hide_sector(sector)

    def _sectorize(self,position):
        """ Returns a tuple representing the sector for the given `position`.

        Parameters
        ----------
        position : tuple of len 3

        Returns
        -------
        sector : tuple of len 3

        """
        x, y, z = self._normalize(position)
        x, y, z = x // self.sectorSize, y // self.sectorSize, z // self.sectorSize
        return (x, 0, z)

    def _normalize(self,position):
        """ Accepts `position` of arbitrary precision and returns the block
        containing that position.

        Parameters
        ----------
        position : tuple of len 3

        Returns
        -------
        block_position : tuple of ints of len 3

        """
        x, y, z = position
        x, y, z = (int(round(x)), int(round(y)), int(round(z)))
        return (x, y, z)
