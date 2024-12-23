import math

from matplotlib import pyplot as plt

from app.base.Point import Point


class Arc2D:

    def __init__(self, center_point: Point, radius, start_angle, end_angle):
        self.center_point = center_point
        # self.center = (self.center_point.x, self.center_point.y)
        self.radius = radius
        self.start_angle = math.radians(start_angle)  # Преобразуем в радианы
        self.end_angle = math.radians(end_angle) # Преобразуем в радианы
        self.sweep_angle = math.radians(end_angle - start_angle)
        self.start_point = self.get_point_at_angle(start_angle)
        self.end_point = self.get_point_at_angle(end_angle)

    def get_point_at_angle(self, angle):
        """
        Возвращает координаты точки на дуге для заданного угла.

        :param angle: Угол в радианах.
        :return: Координаты точки (x, y).
        """
        angle = math.radians(angle)
        min_angle, max_angle = sorted([self.start_angle, self.end_angle])
        if min_angle <= angle <= max_angle:
            x = self.center_point.x + self.radius * math.cos(angle)
            y = self.center_point.y + self.radius * math.sin(angle)
            point = Point(x=x, y=y, z=self.center_point.z)
            return point
        raise ValueError(f"Угол {math.degrees(angle)} лежит вне дуги {self.__repr__()}")

    def is_point_on_arc(self, point: Point, tolerance=1e-4):
        r = ((point.x - self.center_point.x) ** 2 + (point.y - self.center_point.y) ** 2) ** 0.5
        if abs(self.radius - r) > tolerance:
            return False
        angle = math.atan2(point.y - self.center_point.y,
                           point.x - self.center_point.x)
        angle = angle if angle >= 0 else angle + math.tau
        min_angle, max_angle = sorted([self.start_angle, self.end_angle])
        return min_angle <= angle <= max_angle

    def get_distance_from_start_point_to_point(self, point: Point, tolerance=1e-4):
        if not self.is_point_on_arc(point, tolerance):
            raise ValueError(f"Точка {point} не лежит на дуге {repr(self)}")
        angle = math.atan2(point.y - self.center_point.y,
                           point.x - self.center_point.x)
        angle = angle if angle >= 0 else angle + math.tau
        sweep_angle = angle - self.start_angle
        return abs(sweep_angle * self.radius)

    def get_arc_length(self):
        return self.get_distance_from_start_point_to_point(self.end_point)

    def get_arc_points(self, num_points=100):
        """
        Возвращает список точек на дуге для визуализации.

        :param num_points: Количество точек для дискретизации дуги.
        :return: Список координат точек на дуге.
        """
        points = []
        for i in range(num_points + 1):
            angle = self.start_angle + (self.sweep_angle * i / num_points)
            angle = math.degrees(angle)
            points.append(self.get_point_at_angle(angle))
        return points

    @classmethod
    def create_arc_from_center_point_with_start_and_end_points(cls, center_point: Point,
                                                               start_point: Point,
                                                               end_point: Point,
                                                               tolerance=1e-4):
        r1 = ((start_point.x - center_point.x) ** 2 + (start_point.y - center_point.y) ** 2) ** 0.5
        r2 = ((end_point.x - center_point.x) ** 2 + (end_point.y - center_point.y) ** 2) ** 0.5
        if abs(r2 - r1) > tolerance:
            raise ValueError(f"Точки {start_point} и {end_point} не лежат на одной дуге - {r1} != {r2}")
        start_angle = math.degrees(math.atan2(start_point.y - center_point.y,
                                              start_point.x - center_point.x))
        start_angle = start_angle if start_angle >= 0 else start_angle + 360
        end_angle = math.degrees(math.atan2(end_point.y - center_point.y,
                                            end_point.x - center_point.x))
        end_angle = end_angle if end_angle >= 0 else end_angle + 360
        arc = cls(center_point=center_point, radius=r1, start_angle=start_angle, end_angle=end_angle)
        return arc

    def __str__(self):
        return (f"Arc2D (central_point={self.center_point}, "
                f"start_point={self.start_point}, "
                f"end_point={self.end_point}, "
                f"radius={self.radius}, "
                f"start_angle={math.degrees(self.start_angle):.3f}, "
                f"stop_angle={math.degrees(self.end_angle):.3f}")

    def __repr__(self):
        return (f"Arc2D (central_point={self.center_point}, "
                f"radius={self.radius}, "
                f"start_angle={math.degrees(self.start_angle):.3f}, "
                f"stop_angle={math.degrees(self.end_angle):.3f}")


if __name__ == "__main__":
    cp = Point(x=0, y=-0.806, z=0)
    sp = Point(x=0, y=2.1, z=0)
    ep = Point(x=1.7044, y=1.5477)
    arc = Arc2D.create_arc_from_center_point_with_start_and_end_points(center_point=cp,
                                                                       start_point=sp,
                                                                       end_point=ep)
    print(arc)
    point1 = arc.get_point_at_angle(60)
    # point2 = arc.get_point_at_angle(0)

    arc_points = arc.get_arc_points(10)
    print(arc_points)
    x, y = [], []
    for point in arc_points:
        print(arc.get_distance_from_start_point_to_point(point))
        x.append(point.x)
        y.append(point.y)

    fig, ax = plt.subplots()
    ax.scatter(x, y)
    ax.scatter(point1.x, point1.y)
    # ax.scatter(point2.x, point2.y)

    plt.axis('equal')
    plt.show()

    print(arc.is_point_on_arc(point1))
    print(arc.get_distance_from_start_point_to_point(point1))
    print(arc.get_arc_length())

