from matplotlib import pyplot as plt

from app.base.Line import Line
from app.base.Point import Point
from app.deformation.DeformationScan import DeformationScan
from app.scan.Scan import Scan
from app.scan.filters.ScanFilerByLineClosing import ScanFilerByLineClosing
from app.scan.filters.ScanFilterDelimiter import ScanFilterDelimiter

scan = Scan("Test")

scan.load_points_from_file(file_path="src/cl_1_cr_2.txt")
print(scan)
scan.filter_scan(filter_cls=ScanFilterDelimiter, delimiter=100)
print(scan)

def_scan = DeformationScan.create_def_scan_from_scan(scan=scan)
print(def_scan)

dz = 4.4 / 2
line = Line(start_point=Point(x=42017.410,
                              y=54793.305,
                              z=116.218 - dz),
            end_point=Point(x=42015.508,
                            y=54801.223,
                            z=115.960 - dz))
sp_new = line.point_on_line_at_distance(1)
ep_new = line.point_on_line_at_distance(3)
line = Line(start_point=sp_new, end_point=ep_new)


def_scan.filter_scan(filter_cls=ScanFilerByLineClosing, line=line)
print(def_scan)

# points = []
# scan = Scan("Test2")
# for point in def_scan:
#     scan.add_point(line.closest_point_on_line_3d(point))
#
# print(scan)
# fig_ax = scan.plot(is_show=False)
# fig, ax = def_scan.plot(fig_ax=fig_ax, is_show=False)
#
# for point in def_scan:
#     c_point = line.closest_point_on_line_3d(point)
#     ax.plot([point.x, c_point.x], [point.y, c_point.y], [point.z, c_point.z])
#
# ax.plot([line.s_point.x, line.e_point.x], [line.s_point.y, line.e_point.y], [line.s_point.z, line.e_point.z])
# plt.axis('equal')
#
# plt.show()


scan = Scan("Test3")

for point in def_scan:
    distance = line.distance_from_start_point(point)
    point = line.transform_to_new_coordinate_system(point)
    point.z = distance
    scan.add_point(point)

scan.plot()