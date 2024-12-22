

class Point:

    def __init__(self, x, y, z=0):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return f"Point (x={self.x:.3f}, y={self.y:.3f}, z={self.z:.3f})"

    def __repr__(self):
        return f"({self.x:.3f}, {self.y:.3f}, {self.z:.3f})"
