from utils import calculate_distance


class Order:
    """
    Класс, содержащий информацию о заказе
    """
    def __init__(self, start, end, price) -> None:
        self.start: list[float, float] = start
        self.end: list[float, float] = end
        self.distance: float = calculate_distance(self.start, self.end)
        self.price: float = price
        # self.nearest_driver_distance: list[Driver, float]|None = None
        
    def __str__(self) -> str:
        return f"Заказ:\nОткуда: {self.start}\nКуда: {self.end}\nЦена: {self.price}"
    

    

class Driver:
    """Класс, содержащий информацию о водителе
    """
    def __init__(self, start_coords) -> None:
        self.nearest_order_distance: list[Order, float]|None = None
        self.start_coords: list[float, float] = start_coords
        self.current_coords = start_coords
        self.trip = 0
        self.orders = []
        self.balance = 0
        
    def add_order(self, order: Order, distance: float) -> None:
        """Функция добавляет заказ к списку заказов курьера

        Args:
            order (Order): Заказ, который будет добавлен курьеру
            distance (float): Расстояние от водителя до заказа
        """
        self.orders.append(order)
        self.current_coords = order.end
        self.trip += distance + order.distance
        self.balance += order.price
    
    def __str__(self):
        return f"Водитель:\nНачальные коордианты: {self.start_coords}\nТекущие координаты: {self.current_coords}\nПроделанный путь: {self.trip}\nЗаказов выполнено на сумму: {self.balance}"
    
    def print_route(self):
        print(f'{self}\nЗаказы выполнены курьером в этом порядке:')
        
        for order in self.orders:
            print(order)