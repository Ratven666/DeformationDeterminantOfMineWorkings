import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Функция для линейной интерполяции между двумя точками
def linear_interpolation(p1, p2, t):
    """
    Линейная интерполяция между двумя точками p1 и p2.
    t — параметр интерполяции (от 0 до 1).
    """
    return (1 - t) * np.array(p1) + t * np.array(p2)

# Функция для построения поверхности по последовательным сечениям
def plot_3d_surface(sections, num_steps=10):
    """
    Построение замкнутой поверхности по последовательным трехмерным сечениям.
    sections — список сечений (каждое сечение — список точек).
    num_steps — количество шагов интерполяции между сечениями.
    """
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

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
    ax.plot_surface(X, Y, Z, cmap='viridis', edgecolor='none')

    # Настройка графика
    ax.set_title("Замкнутая поверхность по последовательным сечениям")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    plt.show()

section1 = [
    (0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0)  # Квадрат в плоскости Z=0
]
section2 = [
    (0, 0, 1), (1, 0, 1), (1, 1, 1), (0, 1, 1)  # Квадрат в плоскости Z=1
]
section3 = [
    (0, 0, 2), (1, 0, 2), (1, 1, 2), (0, 1, 2)  # Квадрат в плоскости Z=2
]

# Построение поверхности
plot_3d_surface([section1, section2, section3])