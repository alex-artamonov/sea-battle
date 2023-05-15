# import exceptions
# from board import BODY
BODY = "■"
# =======================================


class Ship:
    """Корабль
    Аттрибуты:
        - len: длина (количество клеток)
        - front: координаты носа
        - direction: направление: горизонтальное (H) или вертикальное (V)
        - side: размер поля (сторона квадрата)
        - lives: количество жизней
        - body: строковый массив состояний точек корабля
        - buffer_cells_set: сет кортежей из пар координат буферной зоны
        - is_afloat: True если на плаву. False если подбит
    """

    def __init__(self, length, direction="H", front=(), max_len=4):
        self.front = front
        self.direction = direction
        # self.board_size = board_size
        self._max_len = max_len
        self.len = length
        self.body_dict = {}

    @property
    def len(self):
        return self._len

    @len.setter
    def len(self, value):
        if not (0 < value <= self._max_len):
            raise ValueError(f"Корабль длины {value} слишком большой!")
        else:
            self._len = value

    @property
    def coords(self):
        lst = []
        for i, cell in enumerate(range(self._len)):
            if self.direction == "H":
                lst.append((self.front[0], self.front[1] + i))
            elif self.direction == "V":
                lst.append((self.front[0] + i, self.front[1]))
            else:
                raise ValueError("Введено неправильное направление корабля!")
        return lst

    @property
    def coords_set(self):
        if self.direction == "H":
            return {
                (self.front[0], self.front[1] + i)
                for i, cell in enumerate(range(self._len))
            }
        elif self.direction == "V":
            return {
                (self.front[0] + i, self.front[1])
                for i, cell in enumerate(range(self._len))
            }
        else:
            raise ValueError("Введено неправильное направление корабля!")

    @property
    def nbr_lives(self):
        return list(self.body_dict.values()).count(BODY)
        # pass

    @property
    def is_afloat(self):
        return self.nbr_lives > 0

    def __str__(self):
        return str(self.len) + ":" + chr(160) + "".join(self.body_dict.values())

    def __repr__(self):
        return str(self.len) + ":" + chr(160) + "".join(self.body_dict.values())

    @property
    def buffer_cells_set(self):
        """Возвращает сет кортежей координат буферной зоны вокруг корабля"""
        sb = self.coords_set
        _set = set()
        for coord in sb:
            x, y = coord[0], coord[1]
            _set = _set | {
                (x - 1, y - 1),
                (x, y - 1),
                (x + 1, y - 1),
                (x - 1, y),
                (x + 1, y),
                (x - 1, y + 1),
                (x, y + 1),
                (x + 1, y + 1),
            }
        _set -= (
            sb  # вычитаем массив координат корабля из массива координат буферной зону
        )
        return _set

    def clear(self):
        self.front = ()
        self.body_dict = {}
