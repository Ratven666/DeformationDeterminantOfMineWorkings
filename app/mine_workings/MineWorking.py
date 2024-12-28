from matplotlib import pyplot as plt

from app.base.Arc2D import Arc2D
from app.base.Geometry import Geometry
from app.base.Line import Line
from app.base.Point import Point
from app.mine_workings.BASE_MCS import MCS
from app.mine_workings.MiningSection import MiningSection


class MineWorking:

    def __init__(self, *base_lines: Geometry, mine_cross_section=MCS):
        self.mining_sections = [MiningSection(base_line=base_line, mine_cross_section=mine_cross_section)
                                for base_line in base_lines]
        self._base_lines = base_lines
        self.mcs = mine_cross_section

    def get_mining_section_to_point(self, point: Point):
        for ms in self.mining_sections:
            if ms.is_point_in_mining_section(point):
                return ms

    def get_distance_from_start_point_to_point(self, point: Point):
        distance = 0
        for ms in self.mining_sections:
            if ms.is_point_in_mining_section(point):
                distance += ms.base_line.get_distance_from_start_point_to_point(point)
                return distance
            distance += ms.base_line.get_total_length()
        return -1
        # raise ValueError(f"Точка {point} не принадлежит выработке {self}!")

    def get_ms_elm_for_distance(self, distance):
        current_dist = 0
        distance_left = distance
        for ms in self.mining_sections:
            current_dist += ms.base_line.get_total_length()
            if distance <= current_dist:
                return ms, distance_left
            distance_left = distance - current_dist

    def get_norm_distance_from_mw_to_point(self, point: Point):
        ms = self.get_mining_section_to_point(point)
        if ms is None:
            return 0
        distance = ms.get_norm_distance_from_ms_to_point(point=point)
        return distance

    def plot(self, fig_ax=None, is_show=True):
        if fig_ax is None:
            fig = plt.figure(figsize=(10, 8))
            ax = fig.add_subplot(111, projection='3d')
        else:
            fig, ax = fig_ax
        for mining_section in self.mining_sections:
            mining_section.plot(num_of_section=5,
                                num_steps=2,
                                fig_ax=(fig, ax),
                                is_show=False)
        if is_show:
            plt.axis('equal')
            plt.show()
        return fig, ax


if __name__ == "__main__":

    spl1 = Point(x=100, y=100, z=-25)
    epl1 = Point(x=150, y=100)
    line1 = Line(start_point=spl1, end_point=epl1)

    spa1 = epl1
    cpa1 = Point(x=150, y=125)
    epa1 = Point(x=175, y=125)
    # arc1 = Arc2D.create_arc_from_center_point_with_start_and_end_points(center_point=cpa1,
    #                                                                     start_point=epa1,
    #                                                                     end_point=spa1)
    arc1 = Arc2D(center_point=cpa1, start_angle=270, end_angle=359.999999999, radius=25)

    line2 = Line(start_point=epa1,
                 end_point=Point(x=175, y=175))

    print(line1)
    print(arc1)

    arc2 = Arc2D(center_point=Point(200, 175),
                 radius=25,
                 start_angle=180,
                 end_angle=90)

    line3 = Line(start_point=Point(200, 200),
                 end_point=Point(250, 200, z=25))

    mw = MineWorking(line1, arc1, line2, arc2, line3)

    mw.plot()
    p = Point(x=151, y=122)

    dist = mw.get_norm_distance_from_mw_to_point(p)
    print(dist)