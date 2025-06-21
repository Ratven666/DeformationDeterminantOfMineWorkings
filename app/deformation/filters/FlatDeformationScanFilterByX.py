from app.scan.filters.ScanFilterABC import ScanFilterABC


class FlatDeformationScanFilterByX(ScanFilterABC):
    def __init__(self, x_min, x_max):
        self.x_min = x_min
        self.x_max = x_max

    def filter(self, scan):
        points = []
        for point in scan:
            if self.x_min <= point.x < self.x_max:
                points.append(point)
        return points
