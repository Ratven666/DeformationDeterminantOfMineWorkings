from app.base.Line import Line
from app.base.Point import Point
from app.deformation.DeformationCalculatorBetweenTwoFlatDefScan import DeformationCalculatorBetweenTwoFlatDefScan
from app.deformation.DeformationScan import DeformationScan
from app.deformation.filters.DeformationScanFilterByDeformationValue import DeformationScanFilterByDeformationValue
from app.deformation.FlatDeformationScan import FlatDeformationScan
from app.deformation.MiningWorkingDeformationCalculator import MiningWorkingDeformationCalculator
from app.mine_workings.MineWorking import MineWorking
from app.scan.Scan import Scan
from app.deformation.exporters.DeformationScaledColoredScanExporter import DeformationScaledColoredScanExporter
from app.scan.filters.ScanFilterByLineDistance import ScanFilterByLineDistance
from app.scan.filters.ScanFilterDelimiter import ScanFilterDelimiter

scan1 = Scan("Scan1")
scan2 = Scan("Scan2")
scan1.load_points_from_file(file_path="src/base_src/Облако 160724.xyz")
scan2.load_points_from_file(file_path="src/base_src/Облако 160824.xyz")

# scan1.load_points_from_file(file_path="src/2_1607flt.xyz")
# scan2.load_points_from_file(file_path="src/2_1608flt.xyz")
print(scan1)
print(scan2)

scan1.filter_scan(filter_cls=ScanFilterDelimiter, delimiter=5)
scan2.filter_scan(filter_cls=ScanFilterDelimiter, delimiter=5)
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
# def_scan1.plot(plotter=DeformationScanPlotterMPL, base_obj=mw)
#
def_scan1.filter_scan(filter_cls=DeformationScanFilterByDeformationValue, max_deformation=3)
def_scan2.filter_scan(filter_cls=DeformationScanFilterByDeformationValue, max_deformation=3)

filter_line = Line(start_point=points[0], end_point=points[-1])
def_scan1.filter_scan(filter_cls=ScanFilterByLineDistance, line=filter_line, max_distance=5)
def_scan2.filter_scan(filter_cls=ScanFilterByLineDistance, line=filter_line, max_distance=5)
print(def_scan1)
print(def_scan2)
# def_scan2.plot(plotter=DeformationScanPlotterMPL, base_obj=mw)

# def_scan1.export_points_from_file(file_path="def_scan1.txt", parser=DeformationScaledColoredScanExporter)
# def_scan2.export_points_from_file(file_path="def_scan2.txt", parser=DeformationScaledColoredScanExporter)

flat_ds1 = FlatDeformationScan.create_flat_def_scan_from_mining_working_def_scan(def_scan=def_scan1,
                                                                                 mining_working=mw,
                                                                                 get_point_in_mw_cs=False)
flat_ds2 = FlatDeformationScan.create_flat_def_scan_from_mining_working_def_scan(def_scan=def_scan2,
                                                                                 mining_working=mw,
                                                                                 get_point_in_mw_cs=False)
# flat_ds1.plot(plotter=DeformationScanPlotterMPL)
print(flat_ds1)
print(flat_ds2)

# flat_ds1.export_points_from_file(file_path="flat_def_scan1.txt", parser=DeformationScaledColoredScanExporter)
# flat_ds2.export_points_from_file(file_path="flat_def_scan2.txt", parser=DeformationScaledColoredScanExporter)

# flat_ds1.plot(plotter=DeformationScanPlotterMPL)
# flat_ds2.plot(plotter=DeformationScanPlotterMPL)

flat_ds2.calculate_deformation(deformation_calculator=DeformationCalculatorBetweenTwoFlatDefScan,
                               base_scan=flat_ds1)

# flat_ds2.filter_scan(filter_cls=DeformationScanFilterByDeformationValue, max_deformation=0.2)
flat_ds2.refresh_def()
print(flat_ds1)
print(flat_ds2)
flat_ds2.export_points_from_file(file_path="flat_def_result.txt", parser=DeformationScaledColoredScanExporter)

# flat_ds2.plot(plotter=DeformationScanPlotterMPL)

def_scan3 = flat_ds2.calculate_def_scan_by_base_obj()

print(def_scan3)
# def_scan3.filter_scan(filter_cls=DeformationScanFilterByDeformationValue, max_deformation=0.3)
# def_scan3.refresh_def()
# print(def_scan3)
def_scan3.export_points_from_file("res_def_scan_mw.txt", parser=DeformationScaledColoredScanExporter)
# def_scan3.plot(plotter=DeformationScanPlotterMPL)
