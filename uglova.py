from app.base.Line import Line
from app.base.Point import Point
from app.deformation.DeformationCalculatorBetweenTwoFlatDefScan import DeformationCalculatorBetweenTwoFlatDefScan
from app.deformation.DeformationScan import DeformationScan
from app.deformation.DeformationScanFilterByDeformationValue import DeformationScanFilterByDeformationValue
from app.deformation.DeformationScanPlotterMPL import DeformationScanPlotterMPL
from app.deformation.FlatDeformationScan import FlatDeformationScan
from app.deformation.MiningWorkingDeformationCalculator import MiningWorkingDeformationCalculator
from app.mine_workings.MineWorking import MineWorking
from app.scan.Scan import Scan
from app.scan.filters.ScanFilterByLineDistance import ScanFilterByLineDistance
from app.scan.filters.ScanFilterDelimiter import ScanFilterDelimiter

scan1 = Scan("Scan1")
scan2 = Scan("Scan2")
scan1.load_points_from_file(file_path="src/base_src/Облако 160724.xyz")
scan2.load_points_from_file(file_path="src/base_src/Облако 160824.xyz")
print(scan1)
print(scan2)

scan1.filter_scan(filter_cls=ScanFilterDelimiter, delimiter=100)
scan2.filter_scan(filter_cls=ScanFilterDelimiter, delimiter=100)
print(scan1)
print(scan2)

def_scan1 = DeformationScan.create_def_scan_from_scan(scan=scan1)
def_scan2 = DeformationScan.create_def_scan_from_scan(scan=scan2)
print(def_scan1)
print(def_scan2)
points = []
# with open("src/Узлы проект КВГ 110.txt", "rt") as file:
with open("src/2_Узлы ФАКТ КВГ 110.txt", "rt") as file:
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

def_scan1.calculate_deformation(deformation_calculator=MiningWorkingDeformationCalculator,
                                mining_working=mw)
def_scan2.calculate_deformation(deformation_calculator=MiningWorkingDeformationCalculator,
                                mining_working=mw)

print(def_scan1)
print(def_scan2)
print()
# def_scan.plot(plotter=DeformationScanPlotterMPL, base_obj=mw)
#
def_scan1.filter_scan(filter_cls=DeformationScanFilterByDeformationValue, max_deformation=2)
def_scan2.filter_scan(filter_cls=DeformationScanFilterByDeformationValue, max_deformation=2)

filter_line = Line(start_point=points[0], end_point=points[-1])
def_scan1.filter_scan(filter_cls=ScanFilterByLineDistance, line=filter_line, max_distance=5)
def_scan2.filter_scan(filter_cls=ScanFilterByLineDistance, line=filter_line, max_distance=5)
print(def_scan1)
print(def_scan2)
# def_scan.plot(plotter=DeformationScanPlotterMPL, base_obj=mw)

flat_ds1 = FlatDeformationScan.create_flat_def_scan_from_mining_working_def_scan(def_scan=def_scan1,
                                                                                 mining_working=mw,
                                                                                 get_point_in_mw_cs=True)
flat_ds2 = FlatDeformationScan.create_flat_def_scan_from_mining_working_def_scan(def_scan=def_scan2,
                                                                                 mining_working=mw,
                                                                                 get_point_in_mw_cs=True)
# flat_ds.plot(plotter=DeformationScanPlotterMPL)
print(flat_ds1)
print(flat_ds2)

flat_ds2.calculate_deformation(deformation_calculator=DeformationCalculatorBetweenTwoFlatDefScan,
                               base_scan=flat_ds1)

flat_ds2.plot(plotter=DeformationScanPlotterMPL)
print(flat_ds1)
print(flat_ds2)