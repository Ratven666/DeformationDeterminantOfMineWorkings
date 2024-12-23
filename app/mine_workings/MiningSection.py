import numpy as np

from app.base.Geometry import Geometry
from app.mine_workings.BASE_MCS import MCS


class MiningSection:

    def __init__(self, base_line: Geometry, mine_cross_section=MCS):
        self.base_line = base_line
        self.mcs = mine_cross_section

    # def transform_points_to_obj_coordinate_system(self, distance, points):
    #     """
    #     Преобразует координаты точек в новую систему координат, где:
    #     - Начало координат совпадает с точкой P1.
    #     - Ось z' направлена вдоль прямой P1P2.
    #
    #     :param P1: Первая точка прямой (x1, y1, z1) в виде списка или массива.
    #     :param P2: Вторая точка прямой (x2, y2, z2) в виде списка или массива.
    #     :param points: Список точек для преобразования (каждая точка - список или массив).
    #     :return: Список точек в новой системе координат.
    #     """
    #     # Преобразуем точки в numpy массивы
    #     P1 = np.array([self.base_line.start_point.x,
    #                    self.base_line.start_point.y,
    #                    self.base_line.start_point.z], dtype=float)
    #     P2 = np.array([self.base_line.end_point.x,
    #                    self.base_line.end_point.y,
    #                    self.base_line.end_point.z], dtype=float)
    #     points = [np.array([point.x, point.y, point.z], dtype=float) for point in points]
    #
    #     # Вектор направления оси z' (P1P2)
    #     z_prime = P2 - P1
    #     z_prime = z_prime / np.linalg.norm(z_prime)  # Нормализуем
    #
    #     # Выбираем произвольный вектор, перпендикулярный z'
    #     if z_prime[0] != 0 or z_prime[1] != 0:
    #         x_prime = np.array([-z_prime[1], z_prime[0], 0])

