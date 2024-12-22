# import numpy as np
#
#
# def is_point_on_segment(P1, P2, Q):
#     """
#     Проверяет, лежит ли точка Q на отрезке, заданном точками P1 и P2.
#
#     :param P1: Первая точка отрезка (x1, y1, z1) в виде списка или массива.
#     :param P2: Вторая точка отрезка (x2, y2, z2) в виде списка или массива.
#     :param Q: Точка для проверки (x, y, z) в виде списка или массива.
#     :return: True, если точка лежит на отрезке, иначе False.
#     """
#     # Преобразуем точки в numpy массивы
#     P1 = np.array(P1)
#     P2 = np.array(P2)
#     Q = np.array(Q)
#
#     # Вектор от P1 до P2
#     vector_P1P2 = P2 - P1
#
#     # Вектор от P1 до Q
#     vector_P1Q = Q - P1
#
#     # Нормализуем вектор P1P2 (чтобы избежать проблем с большими числами)
#     norm_P1P2 = np.linalg.norm(vector_P1P2)
#     if norm_P1P2 == 0:  # Если P1 и P2 совпадают
#         return np.allclose(P1, Q)  # Точка Q должна совпадать с P1
#
#     normalized_P1P2 = vector_P1P2 / norm_P1P2
#
#     # Проекция вектора P1Q на нормированный вектор P1P2
#     projection = np.dot(vector_P1Q, normalized_P1P2)
#
#     # Проверяем, лежит ли точка на прямой
#     if np.isclose(np.linalg.norm(vector_P1Q - projection * normalized_P1P2), 0):
#         # Проверяем, лежит ли точка в пределах отрезка
#         if 0 <= projection <= norm_P1P2:
#             return True
#     return False
#
# # line = Line(start_point=Point(x=42017.410,
# #                               y=54793.305,
# #                               z=116.218 + dz),
# #             end_point=Point(x=42015.508,
# #                             y=54801.223,
# #                             z=115.960 + dz))
# # (x=42019.093, y=54795.500, z=116.223)
# # Пример использования
# P1 = (42017.410, 54793.305, 116.218)
# P2 = (42015.508, 54801.223, 115.960)
# Q = (42019.093, 54795.500, 116.223)  # Точка на отрезке
#
#
# # # Пример использования
# # P1 = (1000000, 2000000, 3000000)
# # P2 = (4000000, 5000000, 6000000)
# # Q = (2500000, 3500000, 4500000)  # Точка на отрезке
#
# result = is_point_on_segment(P1, P2, Q)
# print(f"Точка {Q} лежит на отрезке [{P1}, {P2}]: {result}")

import numpy as np


def is_point_on_segment(P1, P2, Q):
    """
    Проверяет, лежит ли точка Q на отрезке, заданном точками P1 и P2.

    :param P1: Первая точка отрезка (x1, y1, z1) в виде списка или массива.
    :param P2: Вторая точка отрезка (x2, y2, z2) в виде списка или массива.
    :param Q: Точка для проверки (x, y, z) в виде списка или массива.
    :return: True, если точка лежит на отрезке, иначе False.
    """
    # Преобразуем точки в numpy массивы
    P1 = np.array(P1, dtype=float)
    P2 = np.array(P2, dtype=float)
    Q = np.array(Q, dtype=float)

    # Перемещаем все точки так, чтобы P1 стало началом координат
    Q_shifted = Q - P1
    P2_shifted = P2 - P1

    # Вектор от P1 до P2
    vector_P1P2 = P2_shifted

    # Вектор от P1 до Q
    vector_P1Q = Q_shifted

    # Проверяем, лежит ли точка на прямой
    # Векторное произведение должно быть близким к нулю
    cross_product = np.cross(vector_P1Q, vector_P1P2)
    if not np.allclose(cross_product, 0):
        return False

    # Проверяем, лежит ли точка в пределах отрезка
    # Вычисляем параметр t
    t = np.dot(vector_P1Q, vector_P1P2) / np.dot(vector_P1P2, vector_P1P2)

    # Если t лежит в диапазоне [0, 1], точка лежит на отрезке
    return 0 <= t <= 1


P1 = (42017.410, 54793.305, 116.218)
P2 = (42015.508, 54801.223, 115.960)
Q = (42019.093, 54795.500, 116.223)  # Точка на отрезке

result = is_point_on_segment(P1, P2, Q)
print(f"Точка {Q} лежит на отрезке [{P1}, {P2}]: {result}")