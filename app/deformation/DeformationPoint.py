from app.base.Point import Point
from app.scan.ScanPoint import ScanPoint


class DeformationPoint(ScanPoint):

    def __init__(self, x, y, z, color=(0, 0, 0)):
        super().__init__(x, y, z, color)
        self.deformation = None

    @classmethod
    def create_def_point_from_point(cls, point: ScanPoint):
        if isinstance(point, ScanPoint):
            return cls(x=point.x, y=point.y, z=point.z, color=point.color)
        elif isinstance(point, Point):
            return cls(x=point.x, y=point.y, z=point.z)
        else:
            raise ValueError(f"Должен быть объект класса Point, передан {point.__class__}")

    def __str__(self):
        deformation = round(self.deformation, 4) if self.deformation is not None else "Not Calculated"
        return (f"DeformationPoint (x={self.x}, y={self.y}, z={self.z}, "
                f"deformation={deformation}, "
                f"color={self.color})")
