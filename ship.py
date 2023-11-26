# import exceptions
# from board import BODY
import globals as g

BODY = "■"
# =======================================
class Ship:
    """Корабль
    Аттрибуты:
        - len: длина (количество клеток)
        - front: координаты носа
        - direction: направление: горизонтальное (H) или вертикальное (V)
        - lives: количество жизней
        - body: строковый массив состояний точек корабля
        - buffer_cells_set: сет кортежей из пар координат буферной зоны
        - is_afloat: True если на плаву. False если подбит
    """

    def __init__(self, length, direction='', front=(), max_len=4):
        self.front = front
        self.direction = direction
        # self.board_size = board_size
        self._max_len = max_len
        self._len = length
        self.body_dict = {}
        self.coords = []

    def __len__(self):
        return self._len

    # @property
    # def coords(self):
    #     lst = []
    #     for i, cell in enumerate(range(self._len)):
    #         if self.direction == g.HORIZ:
    #             lst.append((self.front[0], self.front[1] + i))
    #         elif self.direction == g.VERT:
    #             lst.append((self.front[0] + i, self.front[1]))
    #         else:
    #             raise ValueError("Введено неправильное направление корабля!")
    #     return lst

    @property
    def coords_set(self):
        return set(self.coords)
    #     if self.direction == g.HORIZ:
    #         return {
    #             (self.front[0], self.front[1] + i)
    #             for i, cell in enumerate(range(self._len))
    #         }
    #     elif self.direction == g.VERT:
    #         return {
    #             (self.front[0] + i, self.front[1])
    #             for i, cell in enumerate(range(self._len))
    #         }
    #     else:
    #         raise ValueError("Введено неправильное направление корабля!")

    @property
    def nbr_lives(self):
        return list(self.body_dict.values()).count(BODY)
        # pass

    @property
    def is_afloat(self):
        return self.nbr_lives > 0

    def __str__(self):
        s = "".join(self.body_dict.values())
        if not self.body_dict:
            s = g.UNKNOWN * len(self)
        # s = g.SUNKEN * self._len
        # print('__str__:', s)
        if not all((ele == g.HIT for ele in self.body_dict.values())):
            print('hi from Ship.__str__')
            s = BODY * self._len
        # return str(self._len) + ":" + chr(160) + s
        return s

    def __repr__(self):
        return str(self._len) + ":" + chr(160) + "".join(self.body_dict.values())

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
