from app.base.Line import Line
from app.scan.filters.ScanFilterABC import ScanFilterABC


class ScanFilterByLineDistance(ScanFilterABC):
    def __init__(self, line: Line, max_distance):
        self.line = line
        self.max_distance = max_distance

    def filter(self, scan):
        points = []
        for point in scan:
            distance = self.line.get_distance_from_obj_to_point(point)
            try:
                if distance <= self.max_distance:
                    points.append(point)
            except TypeError:
                continue
        return points
