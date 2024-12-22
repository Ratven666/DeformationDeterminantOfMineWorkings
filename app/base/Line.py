import numpy as np

from app.base.Point import Point


class Line:

    def __init__(self, start_point: Point, end_point: Point):
        self.s_point = start_point
        self.e_point = end_point
        self._start_line_point_np = np.array([self.s_point.x, self.s_point.y, self.s_point.z])
        self._line_direction_np = np.array([self.e_point.x, self.e_point.y, self.e_point.z])

    @property
    def horizontal_distance(self):
        dx = self.e_point.x - self.s_point.x
        dy = self.e_point.y - self.s_point.y
        distance = (dx ** 2 + dy ** 2) ** 0.5
        return distance

    @property
    def elevation(self):
        dz = self.e_point.z - self.s_point.z
        return dz

    @property
    def slope_distance(self):
        distance = (self.horizontal_distance ** 2 + self.elevation ** 2) ** 0.5
        return distance

    def distance_point_to_line_3d(self, point: Point):
        point = np.array([point.x, point.y, point.z])
        vector_p0q = point - self._start_line_point_np
        cross_product = np.cross(vector_p0q, self._line_direction_np)
        cross_product_length = np.linalg.norm(cross_product)
        line_direction_length = np.linalg.norm(self._line_direction_np)
        distance = cross_product_length / line_direction_length
        return float(distance)

    def closest_point_on_line_3d(self, point: Point):
        point = np.array([point.x, point.y, point.z])
        shifted_point = point - self._start_line_point_np
        shifted_line_direction = self._line_direction_np - self._start_line_point_np
        vector_p0q = shifted_point
        # Скалярное произведение вектора P0Q и направляющего вектора прямой
        t = np.dot(vector_p0q, shifted_line_direction) / np.dot(shifted_line_direction, shifted_line_direction)
        # Координаты ближайшей точки на прямой
        closest_point = self._start_line_point_np + t * shifted_line_direction
        closest_point = Point(*map(float, closest_point))
        return closest_point

    def is_point_on_line(self, point: Point):
        point = np.array([point.x, point.y, point.z])
        shifted_point = point - self._start_line_point_np
        shifted_end_point = self._line_direction_np - self._start_line_point_np
        vector_sp0ep = shifted_end_point
        vector_sp0p = shifted_point
        cross_product = np.cross(vector_sp0p, vector_sp0ep)
        if not np.allclose(cross_product, 0):
            return False
        t = np.dot(vector_sp0p, vector_sp0ep) / np.dot(vector_sp0ep, vector_sp0ep)
        return 0 <= t <= 1

    def point_on_line_at_distance(self, distance):
        direction_vector = self._line_direction_np - self._start_line_point_np
        length = np.linalg.norm(direction_vector)
        if distance > length:
            raise ValueError("Заданное расстояние превышает длину отрезка.")
        normalized_vector = direction_vector / length
        point = self._start_line_point_np + distance * normalized_vector
        point = Point(*map(float, point))
        return point

    def distance_from_start_point(self, point: Point):
        point = self.closest_point_on_line_3d(point)
        if self.is_point_on_line(point):
            point = np.array([point.x, point.y, point.z])
            direction_vector = self._line_direction_np - self._start_line_point_np
            vector_p0q = point - self._start_line_point_np
            # Вычисляем параметр t
            t = np.dot(vector_p0q, direction_vector) / np.dot(direction_vector, direction_vector)
            # Вычисляем расстояние от P1 до Q
            distance = t * np.linalg.norm(direction_vector)
            return distance
        else:
            raise ValueError("Точка Q не лежит на прямой.")

    def transform_to_new_coordinate_system(self, point):
        """
        Преобразует координаты точки Q в новую систему координат, где:
        - Начало координат совпадает с ближайшей точкой на прямой к точке Q.
        - Ось z совпадает с направлением прямой.
        - Ось x горизонтальна, ось y вертикальна.

        :param P1: Первая точка прямой (x1, y1, z1) в виде списка или массива.
        :param P2: Вторая точка прямой (x2, y2, z2) в виде списка или массива.
        :param Q: Точка для преобразования (x, y, z) в виде списка или массива.
        :return: Координаты точки Q в новой системе координат (x', y', z').
        """
        # Найдем ближайшую точку на прямой к точке Q
        point_on_line = self.closest_point_on_line_3d(point)
        point = np.array([point.x, point.y, point.z])
        point_on_line = np.array([point_on_line.x, point_on_line.y, point_on_line.z])
        # O_prime = closest_point_on_line(P1, P2, Q)

        # Вектор направления оси z (совпадает с направлением прямой)
        z_prime = self._line_direction_np - self._start_line_point_np
        z_prime = z_prime / np.linalg.norm(z_prime)  # Нормализуем

        # Выбираем ось x' горизонтальной (перпендикулярной z' и вертикали)
        if z_prime[0] != 0 or z_prime[1] != 0:
            x_prime = np.array([-z_prime[1], z_prime[0], 0])  # Перпендикулярный вектор
        else:
            x_prime = np.array([0, -z_prime[2], z_prime[1]])  # Перпендикулярный вектор
        x_prime = x_prime / np.linalg.norm(x_prime)  # Нормализуем

        # Вычисляем ось y' как векторное произведение z' и x'
        y_prime = np.cross(z_prime, x_prime)
        y_prime = y_prime / np.linalg.norm(y_prime)  # Нормализуем

        # Перемещаем точку Q так, чтобы начало координат совпало с O'
        point_shifted = point - point_on_line

        # Вычисляем координаты точки Q в новой системе координат
        x_new = np.dot(x_prime, point_shifted)
        y_new = np.dot(y_prime, point_shifted)
        z_new = np.dot(z_prime, point_shifted)
        point = Point(*map(float, [x_new, y_new, z_new]))

        return point

    def __str__(self):
        return f"Line ({self.s_point}-{self.e_point})"


if __name__ == "__main__":
    s_point = Point(400000, 12340, 5670)
    e_point = Point(400100, 12340, 5670)

    point = Point(400070, 12340, 5670)

    line = Line(start_point=s_point,
                end_point=e_point)

    # print(line)
    # print(line.horizontal_distance)
    # print(line.slope_distance)
    # print(line.elevation)
    #
    print(line.distance_point_to_line_3d(point))
    print(line.closest_point_on_line_3d(point))
    # print(line.is_point_on_line(line.closest_point_on_line_3d(point)))