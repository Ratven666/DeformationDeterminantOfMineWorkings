import math

from matplotlib import pyplot as plt

from app.base.Arc2D import Arc2D
from app.base.Geometry import Geometry
from app.base.Line import Line
from app.base.Point import Point
from app.scan.Scan import Scan


class MineCrossSection:

    def __init__(self, center_point: Point, *geometry_elements: Geometry):
        self.center_point = center_point
        self.elements_dict = self.__init_elements_dict(geometry_elements)

    def _get_angle_to_point(self, point: Point):
        angle = math.atan2(point.y - self.center_point.y,
                           point.x - self.center_point.x)
        angle = angle if angle >= 0 else angle + math.tau
        return angle

    def __init_elements_dict(self, geometry_elements):
        elements_dict = {}
        for element in geometry_elements:
            start_angle = self._get_angle_to_point(element.start_point)
            end_angle = self._get_angle_to_point(element.end_point)
            elements_dict[(start_angle, end_angle)] = element
        return elements_dict

    def get_element_by_angle(self, angle_rad):
        if angle_rad == 0:
            angle_rad += 1e-10
        for key, element in self.elements_dict.items():
            if key[0] < angle_rad <= key[1]:
                return element

    def get_points_on_mcs(self, num_of_points_on_element=10):
        points = []
        for element in self.elements_dict.values():
            points.extend(element.get_points_on_obj(num_of_points_on_element))
        return points

    def plot(self, color=(0, 0, 0), line_width=2):
        fig, ax = plt.subplots()
        for element in self.elements_dict.values():
            if isinstance(element, Line):
                ax.plot([element.start_point.x, element.end_point.x],
                        [element.start_point.y, element.end_point.y], c=color, linewidth=line_width)
            if isinstance(element, Arc2D):
                points = element.get_points_on_obj(num_points=10)
                x, y = [], []
                for point in points:
                    x.append(point.x)
                    y.append(point.y)
                ax.plot(x, y, c=color, linewidth=line_width)
                ax.scatter(element.center_point.x, element.center_point.y, c=color)
                ax.plot([element.start_point.x,
                         element.center_point.x,
                         element.end_point.x],
                        [element.start_point.y,
                         element.center_point.y,
                         element.end_point.y], c=color, linestyle="--")
            ax.plot([element.start_point.x,
                     self.center_point.x,
                     element.end_point.x],
                    [element.start_point.y,
                     self.center_point.y,
                     element.end_point.y], c="r", linestyle="--")
        plt.axis('equal')
        plt.show()

    def __str__(self):
        return f"{self.__class__.__name__} ({self.elements_dict})"


if __name__ == "__main__":
    mcs = MineCrossSection(Point(0, 0, 0),
                           Line(start_point=Point(x=2.1, y=0, z=0),
                                end_point=Point(x=2.1, y=0.7, z=0)),
                           Arc2D.create_arc_from_center_point_with_start_and_end_points(center_point=Point(x=1.004,
                                                                                                           y=0.7),
                                                                                        start_point=Point(x=2.1, y=0.7, z=0),
                                                                                        end_point=Point(x=1.7044, y=1.5477, z=0)),
                           Arc2D.create_arc_from_center_point_with_start_and_end_points(center_point=Point(x=0, y=-0.806, z=0),
                                                                                        start_point=Point(x=1.7044, y=1.5477, z=0),
                                                                                        end_point=Point(x=0, y=2.1)),
                           Arc2D.create_arc_from_center_point_with_start_and_end_points(center_point=Point(x=0, y=-0.806, z=0),
                                                                                        start_point=Point(x=0, y=2.1),
                                                                                        end_point=Point(x=-1.7044, y=1.5477, z=0)),
                           Arc2D.create_arc_from_center_point_with_start_and_end_points(center_point=Point(x=-1.004,
                                                                                                           y=0.7),
                                                                                        start_point=Point(x=-1.7044, y=1.5477, z=0),
                                                                                        end_point=Point(x=-2.1, y=0.7)),
                           Line(start_point=Point(x=-2.1, y=0.7),
                                end_point=Point(x=-2.1, y=-2.1)),
                           Line(start_point=Point(x=-2.1, y=-2.1),
                                end_point=Point(x=2.1, y=-2.1)),
                           Line(start_point=Point(x=2.1, y=-2.1),
                                end_point=Point(x=2.1, y=0)))
    mcs.plot()
    print(mcs)

    print(mcs.get_element_by_angle(math.radians(0)))
    scan = Scan("!")
    for point in mcs.get_points_on_mcs():
        scan.add_point(point)
    scan.plot()