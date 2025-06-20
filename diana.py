from copy import deepcopy

from app.base.Arc2D import Arc2D
from app.base.Line import Line
from app.base.Point import Point
from app.deformation.DeformationCalculatorBetweenTwoFlatDefScan import DeformationCalculatorBetweenTwoFlatDefScan
from app.deformation.DeformationScan import DeformationScan
from app.deformation.DeformationScanPlotterMPL import DeformationScanPlotterMPL
from app.deformation.FlatDeformationScan import FlatDeformationScan
from app.deformation.MiningWorkingDeformationCalculator import MiningWorkingDeformationCalculator
from app.deformation.exporters.DeformationScaledColoredScanExporter import DeformationScaledColoredScanExporter
from app.deformation.filters.DeformationScanSeparatorByMW import DeformationScanSeparatorByMW
from app.deformation.parsers.DeformationScanParserFormTxt import DeformationScanParserFormTxt
from app.mine_workings.MineCrossSection import MineCrossSection
from app.mine_workings.MineWorking import MineWorking
from app.scan.Scan import Scan
from app.scan.filters.ScanFilterDelimiter import ScanFilterDelimiter

points_bdh = [Point(x=44749.300, y=27681.158, z=434.127),
              Point(x=44759.493, y=27675.814, z=434.118),
              Point(x=44770.242, y=27670.178, z=432.210),
              Point(x=44781.184, y=27664.442, z=431.701),
              ]

points_vto = [Point(x=44744.656, y=27672.297, z=434.921),
              Point(x=44753.012, y=27688.239, z=433.492),
              ]

lines_bdh = []
for idx in range(len(points_bdh) - 1):
    line = Line(start_point=points_bdh[idx], end_point=points_bdh[idx + 1])
    lines_bdh.append(line)

lines_vto = []
for idx in range(len(points_vto) - 1):
    line = Line(start_point=points_vto[idx], end_point=points_vto[idx + 1])
    lines_vto.append(line)

cs_bdh = MineCrossSection(Point(0, 0, 0),
                          Line(start_point=Point(x=2.3, y=0),
                               end_point=Point(x=2.3, y=0.001)),
                          Arc2D.create_arc_from_center_point_with_start_and_end_points(center_point=Point(x=0,
                                                                                                          y=-0.3225),
                                                                                       start_point=Point(x=2.3,
                                                                                                         y=0.001),
                                                                                       end_point=Point(x=-2.3,
                                                                                                       y=0.001)),
                          Line(start_point=Point(x=-2.3, y=0.001),
                               end_point=Point(x=-2.3, y=-2)),
                          Line(start_point=Point(x=-2.3, y=-2),
                               end_point=Point(x=2.3, y=-2)),
                          Line(start_point=Point(x=2.3, y=-2),
                               end_point=Point(x=2.3, y=0)))

cs_vto = MineCrossSection(Point(0, 0, 0),
                          Arc2D.create_arc_from_center_point_with_start_and_end_points(center_point=Point(x=0,
                                                                                                          y=-0.561),
                                                                                       start_point=Point(x=2.55, y=0),
                                                                                       end_point=Point(x=-2.55, y=0)),
                          Line(start_point=Point(x=-2.55, y=0),
                               end_point=Point(x=-2.55, y=-2)),
                          Line(start_point=Point(x=-2.55, y=-2),
                               end_point=Point(x=2.55, y=-2)),
                          Line(start_point=Point(x=2.55, y=-2),
                               end_point=Point(x=2.55, y=0)))

mw_bdh = MineWorking(*lines_bdh, mine_cross_section=cs_bdh, name="BDH", offsets=0.25)
mw_vto = MineWorking(*lines_vto, mine_cross_section=cs_vto, name="VTO")

# mw_bdh.plot()
# fig_ax = mw_bdh.plot(is_show=False)
# mw_vto.plot(fig_ax=fig_ax)

def_scan1 = DeformationScan("БДШ023 20_03_25_BDH")
def_scan2 = DeformationScan("БДШ023 16_04_25_BDH")
def_scan1.load_points_from_file(parser=DeformationScanParserFormTxt, file_path="src/diana/БДШ023 20_03_25_BDH.txt")
def_scan2.load_points_from_file(parser=DeformationScanParserFormTxt, file_path="src/diana/БДШ023 16_04_25_BDH.txt")
print(def_scan1)
print(def_scan2)

def_scan1.filter_scan(filter_cls=ScanFilterDelimiter, delimiter=100)
def_scan2.filter_scan(filter_cls=ScanFilterDelimiter, delimiter=100)
print(def_scan1)
print(def_scan2)

# def_scan1.plot(plotter=DeformationScanPlotterMPL, base_obj=mw_bdh)

flat_ds1 = FlatDeformationScan.create_flat_def_scan_from_mining_working_def_scan(def_scan=def_scan1,
                                                                                 mining_working=mw_bdh,
                                                                                 get_point_in_mw_cs=False)
flat_ds2 = FlatDeformationScan.create_flat_def_scan_from_mining_working_def_scan(def_scan=def_scan2,
                                                                                 mining_working=mw_bdh,
                                                                                 get_point_in_mw_cs=False)
print(flat_ds1)
print(flat_ds2)

# flat_ds1.plot(plotter=DeformationScanPlotterMPL)

flat_ds2.calculate_deformation(deformation_calculator=DeformationCalculatorBetweenTwoFlatDefScan,
                               base_scan=flat_ds1)

# flat_ds2.filter_scan(filter_cls=DeformationScanFilterByDeformationValue, max_deformation=0.2)
flat_ds2.refresh_def()
print(flat_ds1)
print(flat_ds2)
# flat_ds2.export_points_from_file(file_path="flat_def_result.txt", parser=DeformationScaledColoredScanExporter)

# flat_ds2.plot(plotter=DeformationScanPlotterMPL)

def_scan3 = flat_ds2.calculate_def_scan_by_base_obj()
def_scan3.refresh_def()
print(def_scan3)

def_scan3.plot(plotter=DeformationScanPlotterMPL)




# ###### Разделение скана по выработкам ######
#
# df_scan_sep_by_mw = DeformationScanSeparatorByMW(scan=scan2, mining_workings=(mw_bdh, mw_vto))
# df_scans = df_scan_sep_by_mw.separate_scan_by_mw()
# print(*df_scans)
#
# for scan in df_scans:
#     scan.export_points_from_file(f"{scan.name}.txt", parser=DeformationScaledColoredScanExporter)
#
# total_def_scan = deepcopy(df_scans[0])
# total_def_scan.name = f"TOTAL_{total_def_scan.name}"
# for point in df_scans[1]:
#     total_def_scan.add_point(point)
# total_def_scan.refresh_def()
# total_def_scan.export_points_from_file(f"{total_def_scan.name}.txt", parser=DeformationScaledColoredScanExporter)
