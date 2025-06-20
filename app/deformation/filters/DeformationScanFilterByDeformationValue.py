from app.scan.filters.ScanFilterABC import ScanFilterABC


class DeformationScanFilterByDeformationValue(ScanFilterABC):
    def __init__(self, max_deformation):
        self.max_deformation = max_deformation

    def filter(self, scan):
        points = []
        for point in scan:
            if abs(point.deformation) <= self.max_deformation:
                points.append(point)
        return points
