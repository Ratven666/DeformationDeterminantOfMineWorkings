import math
import numpy as np

from app.base.Point import Point


class Arc3D:
    def __init__(self, center_point: Point, start_point: Point, end_point: Point):
        self.center_point = center_point
        self.start_point = start_point
        self.end_point = end_point

        self.center_np = np.array([center_point.x, center_point.y, center_point.z])
        self.start_point_np = np.array([start_point.x, start_point.y, start_point.z])
        self.end_point_np = np.array([end_point.x, end_point.y, end_point.z])

        self.normal = self.__calculate_normal()
        self.radius = self.__calculate_radius()
        self.start_angle, self.end_angle = self.__calculate_angles()

    def __calculate_normal(self):
        """
        Вычисляет нормаль к плоскости дуги как векторное произведение векторов
        из центра к точкам начала и конца.

        :return: Нормаль к плоскости дуги (единичный вектор).
        """
        vector_start = self.start_point_np - self.center_np
        vector_end = self.end_point_np - self.center_np
        normal = np.cross(vector_start, vector_end)  # Векторное произведение
        return normal / np.linalg.norm(normal)  # Нормализуем вектор

    def __calculate_radius(self):
        """
        Вычисляет радиус дуги как расстояние от центра до точки начала.

        :return: Радиус дуги.
        """
        return np.linalg.norm(self.start_point_np - self.center_np)

    def __calculate_angles(self):
        """
        Вычисляет углы начала и конца дуги в плоскости дуги.

        :return: Кортеж с углами начала и конца (в градусах).
        """
        # Находим векторы от центра к началу и концу
        vector_start = self.start_point_np - self.center_np
        vector_end = self.end_point_np - self.center_np

        # Находим базисные векторы в плоскости дуги
        basis_x = vector_start / np.linalg.norm(vector_start)  # Ось X в плоскости дуги
        basis_y = np.cross(self.normal, basis_x)  # Ось Y в плоскости дуги

        # Проекции векторов на базисные векторы
        start_x = np.dot(vector_start, basis_x)
        start_y = np.dot(vector_start, basis_y)
        end_x = np.dot(vector_end, basis_x)
        end_y = np.dot(vector_end, basis_y)

        # Вычисляем углы
        start_angle = math.degrees(math.atan2(start_y, start_x))
        end_angle = math.degrees(math.atan2(end_y, end_x))

        # Нормализуем углы в диапазоне [0, 360)
        start_angle = start_angle if start_angle >= 0 else start_angle + 360
        end_angle = end_angle if end_angle >= 0 else end_angle + 360

        return start_angle, end_angle

    def get_length(self):
        """
        Вычисляет длину дуги.

        :return: Длина дуги.
        """
        angle_difference = self.end_angle - self.start_angle
        if angle_difference < 0:
            angle_difference += 360  # Угол должен быть положительным
        angle_difference_rad = math.radians(angle_difference)
        return self.radius * angle_difference_rad

    def get_direction(self):
        """
        Определяет направление дуги (по часовой стрелке или против).

        :return: Строка "clockwise" или "counterclockwise".
        """
        angle_difference = self.end_angle - self.start_angle
        if angle_difference >= 0:
            return "counterclockwise"
        else:
            return "clockwise"

    def __str__(self):
        """
        Возвращает строковое представление дуги.

        :return: Строка с описанием дуги.
        """
        return (f"Arc3D(center={self.center_point}, start_point={self.start_point}, end_point={self.end_point}, "
                f"normal={self.normal}, radius={self.radius}, start_angle={self.start_angle}°, "
                f"end_angle={self.end_angle}°, direction={self.get_direction()})")


# Пример использования
if __name__ == "__main__":
    center = Point(0, 0, 0)
    start_point = Point(5, 0, 0)
    end_point = Point(0, 5, 0)
    end_point = Point(0, 3, 0)

    arc = Arc3D(center, start_point, end_point)
    print(arc)
    print(f"Длина дуги: {arc.get_length()}")
    print(f"Направление дуги: {arc.get_direction()}")

    point = Point(x=5 * math.cos(math.radians(45)),
                  y=1115 * math.sin(math.radians(45)),
                  z=0)
