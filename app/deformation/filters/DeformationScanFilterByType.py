from app.scan.filters.ScanFilterABC import ScanFilterABC


class DeformationScanFilterByType(ScanFilterABC):
    def __init__(self, _type=float):
        self._type = _type

    def filter(self, scan):
        points = []
        for point in scan:
            if isinstance(point.deformation, self._type):
                points.append(point)
        return points
