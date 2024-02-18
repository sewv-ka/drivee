from math import atan2, cos, radians, sin, sqrt
import random


def calculate_distance(coord1, coord2):
    # Радиус Земли в километрах
    radius = 6371.0
    
    # Конвертация градусов в радианы
    lat1 = radians(coord1[0])
    lon1 = radians(coord1[1])
    lat2 = radians(coord2[0])
    lon2 = radians(coord2[1])
    
    # Разница между координатами
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    
    # Вычисление расстояния с использованием формулы Haversine
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = radius * c
    
    return distance

# Координаты, которые ограничивают генерацию координат курьеров и заказов внутри центра якутска
yakutsk_sqr_coords = [(62.028875, 129.700389), (62.045542, 129.742564), (62.032347, 129.747391), (62.021842, 129.721376)]

def is_inside(coord, vertexes):
    # Проверка, находится ли координата внутри фигуры
    
    # Используем метод точки, чтобы проверить, лежит ли точка слева или справа от каждого отрезка
    # Фигура считается выпуклой и ограниченной отрезками между вершинами vertexes
    
    x, y = coord
    n = len(vertexes)
    inside = False
    
    for i in range(n):
        x1, y1 = vertexes[i]
        x2, y2 = vertexes[(i + 1) % n]
        
        if (y1 <= y < y2 or y2 <= y < y1) and x < (x2 - x1) * (y - y1) / (y2 - y1) + x1:
            inside = not inside
    
    return inside

def generate_random_coordinate(vertexes):
    # Генерация случайной координаты внутри фигуры
    
    min_x = min(vertex[0] for vertex in vertexes)
    max_x = max(vertex[0] for vertex in vertexes)
    min_y = min(vertex[1] for vertex in vertexes)
    max_y = max(vertex[1] for vertex in vertexes)
    
    while True:
        x = random.uniform(min_x, max_x)
        y = random.uniform(min_y, max_y)
        coord = (x, y)
        
        if is_inside(coord, vertexes):
            return coord


def generate_n_coords(num_coordinates: int) -> list[float]:
    # Генерация списка случайных координат
    random_coordinates = []

    for _ in range(num_coordinates):
        random_coord = generate_random_coordinate(yakutsk_sqr_coords)
        random_coordinates.append(random_coord)

    return random_coordinates
