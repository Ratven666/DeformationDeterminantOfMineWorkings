import math

import numpy as np
from matplotlib import pyplot as plt

from CONFIG import DISTANCE_BTW_POINTS_ON_SECTION
from app.base.Arc2D import Arc2D
from app.base.Geometry import Geometry
from app.base.Line import Line
from app.base.Point import Point
from app.mine_workings.BASE_MCS import MCS
from app.mine_workings.MineCrossSection import MineCrossSection
from app.scan.Scan import Scan


class MiningSection:

    def __init__(self, base_line: Geometry, mine_cross_section=MCS,
                 distance_between_points_on_sections=DISTANCE_BTW_POINTS_ON_SECTION):
        self.base_line = base_line
        self.mcs = mine_cross_section
        self._vertical_mcs_points = self.__get_vertical_mcs_points(distance_between_points_on_sections)

    def __get_vertical_mcs_points(self, distance_between_points_on_sections):
        flat_points = self.mcs.get_points_on_mcs(distance_step=distance_between_points_on_sections)
        vert_points = []
        for point in flat_points:
            point = Point(x=point.x, y=point.z, z=point.y)
            vert_points.append(point)
        return vert_points

    def __get_next_point_on_base_line(self, point: Point, dl=1e-4):
        point_dist = self.base_line.get_distance_from_start_point_to_point(point)
        if (self.base_line.get_total_length() - point_dist) > dl:
            next_point = self.base_line.get_point_on_obj_at_distance(point_dist + dl)
        else:
            prev_point = self.base_line.get_point_on_obj_at_distance(point_dist - dl)
            dx = point.x - prev_point.x
            dy = point.y - prev_point.y
            dz = point.z - prev_point.z
            next_point = Point(x=point.x + dx,
                               y=point.y + dy,
                               z=point.z + dz)
        return next_point

    def transform_point_to_mcs_coord_system(self, point: Point):
        if isinstance(self.base_line, Arc2D):
            point_on_arc = self.base_line.get_closest_point_obj(point)
            next_point = self.__get_next_point_on_base_line(point_on_arc)
            line = Line(start_point=point_on_arc, end_point=next_point)
        else:
            line = self.base_line
        new_point = line.transform_point_coordinates_to_line_coordinate_system(point)
        return new_point

    def is_point_in_mining_section(self, point: Point):
        point = self.base_line.get_closest_point_obj(point)
        if point is None:
            return False
        return self.base_line.is_point_on_obj(point)

    def get_norm_distance_from_ms_to_point(self, point: Point):
        tr_point = self.transform_point_to_mcs_coord_system(point)
        distance = self.mcs.get_norm_distance_from_mcs_to_point(point=tr_point)
        return distance

    def _get_mcs_for_point_on_line(self, point: Point):
        next_point = self.__get_next_point_on_base_line(point)
        line = Line(start_point=point, end_point=next_point)
        azimuth = line.azimuth + math.pi / 2
        mcs_points = []
        for vert_mcs_point in self._vertical_mcs_points:
            new_x = point.x + vert_mcs_point.x * math.cos(azimuth) - vert_mcs_point.y * math.sin(azimuth)
            new_y = point.y + vert_mcs_point.x * math.sin(azimuth) + vert_mcs_point.y * math.cos(azimuth)
            new_z = point.z + vert_mcs_point.z
            mcs_points.append(Point(x=new_x, y=new_y, z=new_z))
        return mcs_points

    def get_sections_points_on_base_line(self, num_of_section=5):
        base_points = self.base_line.get_points_on_obj(num_of_section)
        sections = []
        for base_point in base_points:
            section_points = self._get_mcs_for_point_on_line(base_point)
            sections.append(section_points)
        return sections

    def plot(self, num_of_section=5, num_steps=2, fig_ax=None, is_show=True):
        """
            Построение замкнутой поверхности по последовательным трехмерным сечениям.
            sections — список сечений (каждое сечение — список точек).
            num_steps — количество шагов интерполяции между сечениями.
            """

        def linear_interpolation(p1, p2, t):
            """
            Линейная интерполяция между двумя точками p1 и p2.
            t — параметр интерполяции (от 0 до 1).
            """
            return (1 - t) * np.array([p1.x, p1.y, p1.z]) + t * np.array([p2.x, p2.y, p2.z])
        if fig_ax is None:
            fig = plt.figure(figsize=(10, 8))
            ax = fig.add_subplot(111, projection='3d')
        else:
            fig, ax = fig_ax
        sections = self.get_sections_points_on_base_line(num_of_section)
        # Создаем массивы для хранения координат точек поверхности
        X, Y, Z = [], [], []
        # Проходим по всем парам последовательных сечений
        for i in range(len(sections) - 1):
            current_section = sections[i]
            next_section = sections[i + 1]

            # Проходим по всем парам соответствующих точек в сечениях
            for j in range(len(current_section)):
                p1 = current_section[j]
                p2 = next_section[j]

                # Интерполяция между точками
                for t in np.linspace(0, 1, num_steps):
                    interpolated_point = linear_interpolation(p1, p2, t)
                    X.append(interpolated_point[0])
                    Y.append(interpolated_point[1])
                    Z.append(interpolated_point[2])

        # Создаем сетку для визуализации поверхности
        X = np.array(X).reshape(-1, num_steps)
        Y = np.array(Y).reshape(-1, num_steps)
        Z = np.array(Z).reshape(-1, num_steps)

        # Визуализация поверхности
        # ax.plot_surface(X, Y, Z, cmap='ocean', edgecolor='none', alpha=0.5)
        ax.plot_surface(X, Y, Z, edgecolor='none', alpha=0.5)

        # Настройка графика
        ax.set_title("Замкнутая поверхность по последовательным сечениям")
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")
        if is_show:
            plt.axis('equal')
            plt.show()
        return fig, ax

    def __str__(self):
        return f"{self.__class__.__name__} (base_line={repr(self.base_line)}, msc={self.mcs}"


if __name__ == "__main__":
    dz = 4.4 / 2
    line = Line(start_point=Point(x=42017.410,
                                  y=54793.305,
                                  z=116.218 - dz),
                end_point=Point(x=42015.508,
                                y=54801.223,
                                z=115.960 - dz))

    ms = MiningSection(base_line=line)

    cp = Point(x=0, y=-0.806, z=0)
    sp = Point(x=0, y=2.1, z=0)
    ep = Point(x=1.7044, y=1.5477)
    arc = Arc2D.create_arc_from_center_point_with_start_and_end_points(center_point=cp,
                                                                       start_point=ep,
                                                                       end_point=sp)

    ms = MiningSection(base_line=arc, distance_between_points_on_sections=0.25)

    ms.plot(num_of_section=2)

    sections = ms.get_sections_points_on_base_line(num_of_section=10)
    scan = Scan("!")
    for section in sections:
        for point in section:
            scan.add_point(point)
    fig, ax = scan.plot(is_show=False)
    # # ax.plot([line.start_point.x, line.end_point.x], [line.start_point.y, line.end_point.y],
    # #         [line.start_point.z, line.end_point.z])
    plt.axis('equal')

    plt.show()



