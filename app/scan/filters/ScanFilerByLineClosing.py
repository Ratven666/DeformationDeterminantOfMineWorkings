from app.base.Line import Line
from app.scan.filters.ScanFilterABC import ScanFilterABC


class ScanFilerByLineClosing(ScanFilterABC):

    def __init__(self, line: Line):
        self.line = line

    def filter(self, scan):
        point_lst = []
        for point in scan:
            if self.line.is_point_on_line(self.line.closest_point_on_line_3d(point)):
                point_lst.append(point)
        return point_lst
