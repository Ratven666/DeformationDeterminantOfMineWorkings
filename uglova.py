from app.base.Line import Line
from app.base.Point import Point
from app.deformation.DeformationScan import DeformationScan
from app.deformation.DeformationScanFilterByDeformationValue import DeformationScanFilterByDeformationValue
from app.deformation.DeformationScanPlotterMPL import DeformationScanPlotterMPL
from app.deformation.FlatDeformationScan import FlatDeformationScan
from app.deformation.MiningWorkingDeformationCalculator import MiningWorkingDeformationCalculator
from app.mine_workings.MineWorking import MineWorking
from app.scan.Scan import Scan
from app.scan.filters.ScanFilterByLineDistance import ScanFilterByLineDistance
from app.scan.filters.ScanFilterDelimiter import ScanFilterDelimiter

scan = Scan("Scan1")
scan.load_points_from_file(file_path="src/base_src/Облако 160724.xyz")
print(scan)
#
scan.filter_scan(filter_cls=ScanFilterDelimiter, delimiter=100)

print(scan)
# scan.plot()
def_scan = DeformationScan.create_def_scan_from_scan(scan=scan)
print(def_scan)
#
points = []
with open("src/Узлы проект КВГ 110.txt", "rt") as file:
    for line in file:
        line = [float(xyz) for xyz in line.strip().split()]
        point = Point(*line)
        points.append(point)

lines = []
for idx in range(len(points)-1):
    line = Line(start_point=points[idx], end_point=points[idx+1])
    lines.append(line)

mw = MineWorking(*lines)

# mw.plot()

def_scan.calculate_deformation(deformation_calculator=MiningWorkingDeformationCalculator,
                               mining_working=mw)

print(def_scan)
# def_scan.plot(plotter=DeformationScanPlotterMPL, base_obj=mw)
#
def_scan.filter_scan(filter_cls=DeformationScanFilterByDeformationValue, max_deformation=2)

filter_line = Line(start_point=points[0], end_point=points[-1])
def_scan.filter_scan(filter_cls=ScanFilterByLineDistance, line=filter_line, max_distance=5)
#
print(def_scan)
# def_scan.plot(plotter=DeformationScanPlotterMPL, base_obj=mw)

flat_ds = FlatDeformationScan.create_flat_def_scan_from_mining_working_def_scan(def_scan=def_scan,
                                                                                mining_working=mw,
                                                                                get_point_in_mw_cs=True)

flat_ds.plot(plotter=DeformationScanPlotterMPL)
print(flat_ds)