from schemas import Driver, Order
from utils import calculate_distance, generate_n_coords
from random import randint

# Вводные данные заказов из примера
orders = [
    {'start': (62.03353600191244, 129.71739238052666), 'end': (62.035482092433334, 129.7411106520348), 'price': 450}, 
    {'start': (62.037277184844626, 129.72747818840008), 'end': (62.02397487412333, 129.7232159703657), 'price': 400},
    {'start': (62.04112222676953, 129.74020446313853), 'end': (62.034563952117814, 129.72517562668028), 'price': 350},
    {'start': (62.0342834992526, 129.73328983449997), 'end': (62.0355448631261, 129.7363134241373), 'price': 250},
    ]

# Вводные данные курьеров из примера
drivers = [
    {'location': (62.03340846842955, 129.71510618738895)},
    {'location': (62.02499740639912, 129.71659642041098)}
]

def get_first_order(orders: list[Order], drivers: list[Driver]):
    """
        Распределяет курьеров по ближайшим заказам к ним

    Args:
        orders (list[Order]): список заказов
        drivers (list[Driver]): список курьеров
    """
    for driver in drivers:
        # Сохраняем ближайший заказ к курьеру и расстояние до него
        min_distance: list[Order|None, float] = [None, float('inf')]
        for order in orders:
            distance = calculate_distance(order.start, driver.start_coords)
            if distance < min_distance[1]:
                min_distance[0] = order
                min_distance[1] = distance
        orders.remove(min_distance[0])
        driver.add_order(order=min_distance[0], distance=min_distance[1])
        

def split_orders(orders: list[Order], drivers: list[Driver]):
    """
        Распределяет оставшиеся заказы по ближайшим курьерам с учетом их проделанного пути

    Args:
        orders (list[Order]): список заказов
        drivers (list[Driver]): список курьеров
    """
    for i in range(len(orders)): 
        # Сохраняем ближайшего к заказу курьера, его путь проделанный им и путь от курьера до заказа
        min_distance: list[Driver|None, list[float, float]] = [None, [float('inf'), float('inf')]]
        for driver in drivers:
            distance = calculate_distance(orders[0].start, driver.current_coords)
            if distance + driver.trip <= min_distance[1][1]:
                min_distance[0] = driver
                min_distance[1][0] = distance
                min_distance[1][1] = distance + driver.trip
        min_distance[0].add_order(orders[0], distance=min_distance[1][0])
        orders.remove(orders[0])
        

        

        
def main(orders: list[Order], drivers: list[Driver]):
    get_first_order(orders, drivers)
    split_orders(orders=orders, drivers=drivers)

    

if __name__ == '__main__':
    n = input(f'Сгенерировать заказы и курьеров? \nДа - введите через пробел два числа, количество заказов и курьеров (5 3)\nНет, пустая строка (enter)\n')
    if n == '':
        print('Вводите список заказов (коордианата1 координата2 стоимость (итого 5 чисел)), каждый заказ с новой строки, если хотите закончить - оставьте строку пустой')
        order = ' '
        orders = []
        while order != '':
            order = input()
            try:
                coord1, coord2, coord3, coord4, price = order.split(' ')
                coord1, coord2, coord3, coord4, price = float(coord1), float(coord2), float(coord3), float(coord4), float(price)
                orders.append(Order((coord1, coord2), (coord3, coord4), price))
                order = ' '
            except ValueError:
                if order != '':
                    print('Введите 5 чисел, широту и долготу начала заказа, широту и долготу конца заказа и стоимость')
                    exit(1)
            if len(orders) == 0:
                print('Нужно ввести хотябы один заказ')
                exit(1)
        print('Вводите список курьеров (коордианата1 координата2 (итого 2 числа)), каждый заказ с новой строки, если хотите закончить - оставьте строку пустой')
        driver = ' '
        drivers = []
        while driver != '':
            driver = input()
            try:
                coord1, coord2 = driver.split(' ')
                coord1, coord2 = float(coord1), float(coord2)
                orders.append(Driver((coord1, coord2)))
                driver = ' '
            except ValueError:
                if driver != '':
                    print('Введите 2 числа, широту и долготу начальной точки курьера')
                    exit(1)
            if len(orders) == 0:
                print('Нужно ввести хотябы одного курьера')
                exit(1)

    else:
        try:
            orders_cnt, drivers_cnt = n.split(' ')
            orders_cnt = int(orders_cnt)
            drivers_cnt = int(drivers_cnt)
        except ValueError:
            print("Нужно ввести всего два числа через пробел (5 3)")
            exit(1)
        print(f'Генерирую {orders_cnt} заказов')
        orders_coords = generate_n_coords(orders_cnt*2)
        orders = []
        for i in range(0, orders_cnt*2, 2):
            orders.append(Order(start=orders_coords[i], end=orders_coords[i+1], price=randint(100, 1000)))
        print(f'Генерирую {drivers_cnt} водителей')
        drivers_coords = generate_n_coords(drivers_cnt)
        drivers = []
        for coord in drivers_coords:
            drivers.append(Driver(coord))
    for order in orders:
            print(order)
            print('-'*5)
    for driver in drivers:
        print(driver)
        print('-'*5)   
    print('Начинаю распределение заказов между курьерами\n')
    main(orders, drivers)
    for driver in drivers:
        driver.print_route()
        print('-'*10)
    
        