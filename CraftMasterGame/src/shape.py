class Shape3D(object):
    def cube_vertices(x, y, z, n):
        """ Return the vertices of the cube at position x, y, z with size 2*n.

        """
        if(n <= 0): raise ValueError("size n should be positive")
        return [
            x-n,y+n,z-n, x-n,y+n,z+n, x+n,y+n,z+n, x+n,y+n,z-n,  # top
            x-n,y-n,z-n, x+n,y-n,z-n, x+n,y-n,z+n, x-n,y-n,z+n,  # bottom
            x-n,y-n,z-n, x-n,y-n,z+n, x-n,y+n,z+n, x-n,y+n,z-n,  # left
            x+n,y-n,z+n, x+n,y-n,z-n, x+n,y+n,z-n, x+n,y+n,z+n,  # right
            x-n,y-n,z+n, x+n,y-n,z+n, x+n,y+n,z+n, x-n,y+n,z+n,  # front
            x+n,y-n,z-n, x-n,y-n,z-n, x-n,y+n,z-n, x+n,y+n,z-n,  # back
        ]

class Shape2D(object):
    """ Return the vertices of the rect at position x, y with the width w and height h.

    """
    def quad_vertices(x, y, w, h):
        if (w <= 0 or h <= 0): raise ValueError("width and height should be positive")
        return [
            x,y,    x+w,y,
            x+w,y+h,  x,y+h,]
