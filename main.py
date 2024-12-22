from app.deformation.DeformationScan import DeformationScan
from app.scan.Scan import Scan
from app.scan.filters.ScanFilterDelimiter import ScanFilterDelimiter

scan = Scan("Test")

scan.load_points_from_file(file_path="src/cl_1_cr_2.txt")
print(scan)
scan.filter_scan(filter_cls=ScanFilterDelimiter, delimiter=20)
print(scan)

def_scan = DeformationScan.create_def_scan_from_scan(scan=scan)
print(def_scan)

# def_scan.plot()