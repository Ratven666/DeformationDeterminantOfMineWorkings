

class Point:

    last_id = 0

    def __init__(self, x, y, z=0):
        self.x = x
        self.y = y
        self.z = z
        self.last_id += 1
        self.id_ = self.last_id

    def __hash__(self):
        return self.id_

    def __eq__(self, other):
        return self.x - other.x == 1e-5 and \
               self.y - other.y == 1e-5 and \
               self.z - other.z == 1e-5


    def __str__(self):
        return f"Point (id={self.id_} x={self.x:.3f}, y={self.y:.3f}, z={self.z:.3f})"

    def __repr__(self):
        return f"({self.x:.3f}, {self.y:.3f}, {self.z:.3f})"
