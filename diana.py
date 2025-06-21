from copy import deepcopy

from app.base.Arc2D import Arc2D
from app.base.Line import Line
from app.base.Point import Point
from app.deformation.DeformationScan import DeformationScan
from app.deformation.FlatDeformationScan import FlatDeformationScan
from app.deformation.calculators.ChunkDeformationCalculatorBetweenTwoFlatDefScan import \
    ChunkDeformationCalculatorBetweenTwoFlatDefScan
from app.deformation.calculators.DeformationCalculatorBetweenTwoFlatDefScan import \
    DeformationCalculatorBetweenTwoFlatDefScan
from app.deformation.calculators.DeformationCalculatorByFlatDefScan import DeformationCalculatorByFlatDefScan
from app.deformation.calculators.MiningWorkingDeformationCalculator import MiningWorkingDeformationCalculator
from app.deformation.exporters.DeformationScaledColoredScanExporter import DeformationScaledColoredScanExporter
from app.deformation.filters.DeformationScanFilterByDeformationValue import DeformationScanFilterByDeformationValue
from app.deformation.parsers.DeformationScanParserFormTxt import DeformationScanParserFormTxt
from app.deformation.plotters.DeformationScanPlotterMPL import DeformationScanPlotterMPL
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

scan1 = Scan("Scan1")
scan1.load_points_from_file(file_path="src/diana/src/БДШ023 20_03_25сс.txt")
def_scan1 = DeformationScan.create_def_scan_from_scan(scan=scan1)
def_scan1.calculate_deformation(deformation_calculator=MiningWorkingDeformationCalculator,
                                mining_working=mw_vto)
def_scan1.export_points_from_file(file_path="src/diana/final/IL_БДШ023 20_03_25_VTO.txt",
                                  parser=DeformationScaledColoredScanExporter)

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


# def_scan1 = DeformationScan("БДШ023 20_03_25_BDH")
# def_scan2 = DeformationScan("БДШ023 16_04_25_BDH")
# def_scan3 = DeformationScan("БДШ023 20_03_25_VTO")
# def_scan4 = DeformationScan("БДШ023 16_04_25_VTO")
# # def_scan5 = DeformationScan("TOTAL_БДШ023 16_04_25_BDH")
# # def_scan6 = DeformationScan("TOTAL_БДШ023 20_03_25_BDH.txt")
# def_scan1.load_points_from_file(parser=DeformationScanParserFormTxt, file_path="src/diana/seismic_cmap/БДШ023 20_03_25_BDH.txt")
# def_scan2.load_points_from_file(parser=DeformationScanParserFormTxt, file_path="src/diana/seismic_cmap/БДШ023 16_04_25_BDH.txt")
# def_scan3.load_points_from_file(parser=DeformationScanParserFormTxt, file_path="src/diana/seismic_cmap/БДШ023 20_03_25_VTO.txt")
# def_scan4.load_points_from_file(parser=DeformationScanParserFormTxt, file_path="src/diana/seismic_cmap/БДШ023 16_04_25_VTO.txt")
# # print(def_scan1)
# # print(def_scan2)

# flat_ds1 = FlatDeformationScan("Flat_DS_БДШ023 20_03_25_BDH")
# flat_ds1.load_points_from_file(file_path="src/diana/Flat_DS_БДШ023 20_03_25_BDH.txt")
# flat_ds1.mining_working = mw_bdh
#
# flat_ds2 = FlatDeformationScan("Flat_DS_БДШ023 16_04_25_BDH")
# flat_ds2.load_points_from_file(file_path="src/diana/Flat_DS_БДШ023 16_04_25_BDH.txt")
# flat_ds2.mining_working = mw_bdh
#
# flat_ds2.calculate_deformation(deformation_calculator=ChunkDeformationCalculatorBetweenTwoFlatDefScan,
#                                base_scan=flat_ds1,
#                                chunk_length=0.5, chunk_offsets=0.2)
# print(flat_ds2)
# flat_ds2.export_points_from_file(f"DEF_{flat_ds2.name}.txt", parser=DeformationScaledColoredScanExporter)
# # flat_ds2.plot(plotter=DeformationScanPlotterMPL)

# flat_ds1 = FlatDeformationScan("Flat_DS_БДШ023 20_03_25_VTO")
# flat_ds1.load_points_from_file(file_path="src/diana/Flat_DS_БДШ023 20_03_25_VTO.txt")
# flat_ds1.mining_working = mw_vto
#
# flat_ds2 = FlatDeformationScan("Flat_DS_БДШ023 16_04_25_VTO")
# flat_ds2.load_points_from_file(file_path="src/diana/Flat_DS_БДШ023 16_04_25_VTO.txt")
# flat_ds2.mining_working = mw_vto
#
# flat_ds2.calculate_deformation(deformation_calculator=ChunkDeformationCalculatorBetweenTwoFlatDefScan,
#                                base_scan=flat_ds1,
#                                chunk_length=0.5, chunk_offsets=0.2)
# print(flat_ds2)
# flat_ds2.export_points_from_file(f"DEF_{flat_ds2.name}.txt", parser=DeformationScaledColoredScanExporter)
# # flat_ds2.plot(plotter=DeformationScanPlotterMPL)






# def_flat_vto = FlatDeformationScan("DEF_Flat_DS_БДШ023 20_03_25_VTO")
# def_flat_vto.load_points_from_file(file_path="src/diana/DEF_Flat_DS_БДШ023 16_04_25_VTO.txt")
# def_flat_vto.mining_working = mw_vto
#
# def_flat_bdh = FlatDeformationScan("DEF_Flat_DS_БДШ023 20_03_25_BDH")
# def_flat_bdh.load_points_from_file(file_path="src/diana/DEF_Flat_DS_БДШ023 16_04_25_BDH.txt")
# def_flat_bdh.mining_working = mw_bdh
#
# def_scan_bdh = DeformationScan("БДШ023 16_04_25_BDH")
# def_scan_vto = DeformationScan("БДШ023 16_04_25_VTO")
#
# def_scan_bdh.load_points_from_file(parser=DeformationScanParserFormTxt, file_path="src/diana/seismic_cmap/БДШ023 16_04_25_BDH.txt")
# def_scan_vto.load_points_from_file(parser=DeformationScanParserFormTxt, file_path="src/diana/seismic_cmap/БДШ023 16_04_25_VTO.txt")
#
# for point in def_scan_bdh:
#     point.deformation = -1000
#
# def_scan_bdh.calculate_deformation(deformation_calculator=DeformationCalculatorByFlatDefScan,
#                                    flat_def_scan=def_flat_bdh)
# def_scan_bdh.export_points_from_file(f"NEW_{def_scan_bdh.name}.txt", parser=DeformationScaledColoredScanExporter)
#
# for point in def_scan_vto:
#     point.deformation = -1000
#
# def_scan_vto.calculate_deformation(deformation_calculator=DeformationCalculatorByFlatDefScan,
#                                    flat_def_scan=def_flat_vto)
# def_scan_vto.export_points_from_file(f"NEW_{def_scan_vto.name}.txt", parser=DeformationScaledColoredScanExporter)

# def_scan_bdh = DeformationScan("БДШ023 16_04_25_BDH")
# def_scan_vto = DeformationScan("БДШ023 16_04_25_VTO")
#
# def_scan_bdh.load_points_from_file(parser=DeformationScanParserFormTxt, file_path="src/diana/final/NEW_БДШ023 16_04_25_BDH.txt")
# def_scan_vto.load_points_from_file(parser=DeformationScanParserFormTxt, file_path="src/diana/final/NEW_БДШ023 16_04_25_VTO.txt")
#
# total_def_scan = deepcopy(def_scan_bdh)
# total_def_scan.name = f"TOTAL_{total_def_scan.name}"
# for point in def_scan_vto:
#     total_def_scan.add_point(point)
# total_def_scan.refresh_def()
#
# print(total_def_scan)
#
# total_def_scan.filter_scan(filter_cls=DeformationScanFilterByDeformationValue, max_deformation=0.01)
# total_def_scan.refresh_def()
#
# total_def_scan.export_points_from_file(f"F_0.01_NEW_TOTAL_DEF_{total_def_scan.name}.txt",
#                                        parser=DeformationScaledColoredScanExporter)
# print(total_def_scan)





# def_scan_vto = def_flat_vto.calculate_def_scan_by_base_obj()
# def_scan_vto.refresh_def()
# def_scan_vto.export_points_from_file(f"F_{def_scan_vto.name}.txt", parser=DeformationScaledColoredScanExporter)
#
# def_scan_bdh = def_flat_bdh.calculate_def_scan_by_base_obj()
# def_scan_bdh.refresh_def()
# def_scan_bdh.export_points_from_file(f"F_{def_scan_bdh.name}.txt", parser=DeformationScaledColoredScanExporter)
#
# total_def_scan = deepcopy(def_scan_bdh)
# total_def_scan.name = f"TOTAL_{total_def_scan.name}"
# for point in def_scan_vto:
#     total_def_scan.add_point(point)
# total_def_scan.refresh_def()
# total_def_scan.export_points_from_file(f"TOTAL_DEF_{total_def_scan.name}.txt",
#                                        parser=DeformationScaledColoredScanExporter)




# def_scan1.export_points_from_file(f"{def_scan1.name}.txt", parser=DeformationScaledColoredScanExporter)
# def_scan2.export_points_from_file(f"{def_scan2.name}.txt", parser=DeformationScaledColoredScanExporter)
# def_scan3.export_points_from_file(f"{def_scan3.name}.txt", parser=DeformationScaledColoredScanExporter)
# def_scan4.export_points_from_file(f"{def_scan4.name}.txt", parser=DeformationScaledColoredScanExporter)

# flat_ds1 = FlatDeformationScan.create_flat_def_scan_from_mining_working_def_scan(def_scan=def_scan1,
#                                                                                  mining_working=mw_bdh,
#                                                                                  get_point_in_mw_cs=False)
# flat_ds2 = FlatDeformationScan.create_flat_def_scan_from_mining_working_def_scan(def_scan=def_scan2,
#                                                                                  mining_working=mw_bdh,
#                                                                                  get_point_in_mw_cs=False)
# flat_ds3 = FlatDeformationScan.create_flat_def_scan_from_mining_working_def_scan(def_scan=def_scan3,
#                                                                                  mining_working=mw_vto,
#                                                                                  get_point_in_mw_cs=False)
# flat_ds4 = FlatDeformationScan.create_flat_def_scan_from_mining_working_def_scan(def_scan=def_scan4,
#                                                                                  mining_working=mw_vto,
#                                                                                  get_point_in_mw_cs=False)

# flat_ds1.export_points_from_file(f"{flat_ds1.name}.txt", parser=DeformationScaledColoredScanExporter)
# flat_ds2.export_points_from_file(f"{flat_ds2.name}.txt", parser=DeformationScaledColoredScanExporter)
# flat_ds3.export_points_from_file(f"{flat_ds3.name}.txt", parser=DeformationScaledColoredScanExporter)
# flat_ds4.export_points_from_file(f"{flat_ds4.name}.txt", parser=DeformationScaledColoredScanExporter)



