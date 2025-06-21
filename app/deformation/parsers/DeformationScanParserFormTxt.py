from app.deformation.calculators.DeformationPoint import DeformationPoint
from app.deformation.DeformationScan import DeformationScan
from app.scan.Scan import Scan
from app.scan.parsers.ScanParserABC import ScanParserABC


class DeformationScanParserFormTxt(ScanParserABC):
    def parse(self, scan):
        if not isinstance(scan, DeformationScan):
            if isinstance(scan, Scan):
                scan = DeformationScan.create_def_scan_from_scan(scan)
            else:
                raise ValueError("Неправильный тип данных!")
        with open(self.file_path, "rt", encoding="UTF-8") as file:
            for line in file:
                line = line.strip().split()
                xyz = [float(xyz_) for xyz_ in line[:3]]
                rgb = list(map(int, line[3:6]))
                deformation = float(line[6])
                point = DeformationPoint(x=xyz[0], y=xyz[1], z=xyz[2], color=rgb)
                point.deformation = deformation
                scan.add_point(point)
        scan.refresh_def()
