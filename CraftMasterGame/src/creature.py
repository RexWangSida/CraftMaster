import math

class Creature(object):
    def __init__(self, position, health,dy = 0, walkSpeed = 5, flying = False, flySpeed = 10, height = 1, jumpHeight = 1.0):
        # Current (x, y, z) position in the world, specified with floats. Note
        # that, perhaps unlike in math class, the y-axis is the vertical axis.
        self.position = position
        # First element is rotation of the player in the x-z plane (ground
        # plane) measured from the z-axis down. The second is the rotation
        # angle from the ground plane up. Rotation is in degrees.
        #
        # The vertical plane rotation ranges from -90 (looking straight down) to
        # 90 (looking straight up). The horizontal rotation range is unbounded.
        self.rotation = (0, 0)
        # Strafing is moving lateral to the direction you are facing,
        # e.g. moving to the left or right while continuing to face forward.
        #
        # First element is -1 when moving forward, 1 when moving back, and 0
        # otherwise. The second element is -1 when moving left, 1 when moving
        # right, and 0 otherwise.
        self.strafe = [0, 0]
        # Velocity in the y (upward) direction.
        self.dy = dy
        #
        self.walkSpeed = walkSpeed
        #the height that creature can reach by jumping (default : About the height of a block)
        self.JumpHeight = jumpHeight
        #max falling velocity
        self.terminalVelocity = 50
        #weather creature are flying
        self.flying = flying
        #how fast could the creature fly
        self.flySpeed = flySpeed
        #the height of the creature
        self.height = height
        #the health of the creatures
        self.health = health

    def rotate(self,x,y):
    ##  @brie frotate the player
        y = max(-90, min(90, y))
        self.rotation = (x, y)

    def move(self,direction):
    ##  @brief move the creature in the current position
        if direction == "FORWARD":
            self.strafe[0] -= 1
        elif direction == "BACKWARD":
            self.strafe[0] += 1
        elif direction == "LEFT":
            self.strafe[1] -= 1
        elif direction == "RIGHT":
            self.strafe[1] += 1
        else:
            raise ValueError("The direction has to be forward, backward, left or right.")

    def stopMove(self,direction):
    ##  @brief stop move the creature in the current position
        if direction == "FORWARD":
            self.strafe[0] += 1
        elif direction == "BACKWARD":
            self.strafe[0] -= 1
        elif direction == "LEFT":
            self.strafe[1] += 1
        elif direction == "RIGHT":
            self.strafe[1] -= 1
        else:
            raise ValueError("The direction has to be forward, backward, left or right.")

    def jump(self,gravity):
    # To derive the formula for calculating jump speed, first solve
    #    v_t = v_0 + a * t
    # for the time at which you achieve maximum height, where a is the acceleration
    # due to gravity and v_t = 0. This gives:
    #    t = - v_0 / a
    # Use t and the desired MAX_JUMP_HEIGHT to solve for v_0 (jump speed) in
    #    s = s_0 + v_0 * t + (a * t^2) / 2
        self.dy = math.sqrt(2 * gravity * self.JumpHeight)

    def update(self,dt,world):
    ##  @brief Private implementation of the `update()` method. This is where most
    #       of the motion logic lives, along with gravity and collision detection.
    #   @param dt : float The change in time since the last call.
        # walking
        speed = self.walkSpeed
        d = dt * speed # distance covered this tick.
        dx, dy, dz = self.get_motion_vector()
        # New position in space, before accounting for gravity.
        dx, dy, dz = dx * d, dy * d, dz * d
        # gravity
        if not self.flying:
            # Update your vertical speed: if you are falling, speed up until you
            # hit terminal velocity; if you are jumping, slow down until you
            # start falling.
            self.dy -= dt * world.gravity
            self.dy = max(self.dy, - self.terminalVelocity)
            dy += self.dy * dt
        # collisions
        x, y, z = self.position
        x, y, z = world.collide((x + dx, y + dy, z + dz), self)
        self.position = (x, y, z)

    def get_motion_vector(self):
    ##  @brief returns the current motion vector indicating the velocity of the creature.
    #   @return vector : tuple of len 3 Tuple containing the velocity in x, y, and z respectively.
        if any(self.strafe):
            x, y = self.rotation
            strafe = math.degrees(math.atan2(*self.strafe))
            y_angle = math.radians(y)
            x_angle = math.radians(x + strafe)
            if self.flying:
                m = math.cos(y_angle)
                dy = math.sin(y_angle)
                if self.strafe[1]:
                    # Moving left or right.
                    dy = 0.0
                    m = 1
                if self.strafe[0] > 0:
                    # Moving backwards.
                    dy *= -1
                # When you are flying up or down, you have less left and right
                # motion.
                dx = math.cos(x_angle) * m
                dz = math.sin(x_angle) * m
            else:
                dy = 0.0
                dx = math.cos(x_angle)
                dz = math.sin(x_angle)
        else:
            dy = 0.0
            dx = 0.0
            dz = 0.0
        return (dx, dy, dz)
