from random import choice
import exceptions

# EMPTY = 'О'
EMPTY = " "
BODY = '■'
DAGGER = '†'
HIT = "‡"
BUFFER = "B"

# =======================================
class Point:
    """Точка на игровой доске
    Аттрибуты:
        - coords: пара координат (x, y)
        - hit: обстреляна (True/False)
    """
    pass


# ======================================
class Ship:
    """Корабль
    Аттрибуты:
        - длина (количество клеток)
        - координаты носа
        - направление: горизонтальное (H) или вертикальное (V)
        - размер поля (сторона квадрата)
        - количество жизней
        - массив точек (body)
    """

    def __init__(self, length, direction="H", front=(), board_size=6):
        self._front = front
        self.direction = direction
        self.board_size = board_size
        self._max_len = 4
        self.len = length
        # self.nbr_lives = len
        self._body = []
        for _ in range(self._len):
            self._body.append(BODY)

    @property
    def len(self):
        return self._len

    @property
    def front(self):
        return self._front

    @front.setter
    def front(self, val):
        self._front = val

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
            return {(self.front[0], self.front[1] + i) for i, cell in enumerate(range(self._len))}
        elif self.direction == "V":
            return {(self.front[0] + i, self.front[1]) for i, cell in enumerate(range(self._len))}
        else:
            raise ValueError("Введено неправильное направление корабля!")

    @len.setter
    def len(self, value):
        if not (0 < value <= self._max_len):
            raise ValueError("Корабль слишком большой!")
        else:
            self._len = value

    @property
    def nbr_lives(self):
        return self.body.count(BODY)
        # pass

    @property
    def body(self):
        return self._body

    @body.setter
    def body(self, cell, val=DAGGER):
        self._body[cell] = val
        pass

    def __repr__(self):
        output = f"Корабль  {' '.join(self.body)} :\n\t- Длина: {self.len}\n\t- Координаты: {self.coords}\n\t" \
                 f"- Жизней: {self.nbr_lives}/{self.len}"
        return output

    @property
    def buffer_cells_set(self):
        """Возвращает сет буферной зоны вокруг корабля"""
        sb = self.coords_set
        print(sb)
        _set = set()
        for coord in sb:
            x, y = coord[0], coord[1]
            _set = _set | {
                (x - 1, y - 1), (x, y - 1), (x + 1, y - 1),
                (x - 1, y), (x + 1, y),
                (x - 1, y + 1), (x, y + 1), (x + 1, y + 1)
            }
        _set -= sb # вычитаем массив координат корабля из массива координат буферной зону
        return _set


# ========================================================================
class Board:
    """Игровое поле
    Аттрибуты:
        - player: игрок (компьютер или человек). Корабли поля человека отображаются для него всегда
        - список кораблей
        - размерность: число - сторона квадрата, по умолчанию 6
        - cells: двумерный массив состояний точек - море, корабль, буфер вокруг корабля, обстреляна
        - coords: массив координат

    """

    def __init__(self, player, ships, side=6):
        if side < 6 or side > 99:
            raise ValueError(f"Размер поля должен быть в пределах от 6 до 99, указан '{side}'")
        self.cells = [list(EMPTY * side) for _ in range(side)]
        self._side = side
        self.player = player
        self.ships = ships
        self.display_ships = True
        for ship in self.ships:
            for cell in ship:
                coords = (cell[0][0], cell[0][1])
                self.cells[coords[0]][coords[1]] = BODY if cell[1] else EMPTY

        # place_ships()

    def place_ship1(self, ship):
        # ship = Ship(4)
        lst = [(i, j) for i in range(self._side) for j in range(self._side)]
        while True:
            try:
                ship.front = choice(lst)
                for i, coord in enumerate(ship.coords):
                    self.cells[coord[0]][coord[1]] = ship.body[i]
                    print(coord, ship.body[i])
                return True
            except IndexError:
                print("from Except IndexError:", ship.coords[-1])
                # ship.front = []
                continue

    def place_ship(self, ship):
        """Возвращает True при успешной попытке размещения корабля
        и False при неудачной после превышения числа попыток"""
        max_attempts = 3
        # ship = Ship(4)
        # lst = [(i, j) for i in range(self._side) for j in range(self._side)]
        i = 0
        while True:
            i += 1
            print("i:", i)
            if i > max_attempts:
                print("too many iterations")
                return False
            ship.front = choice(lst)
            if not ship.coords[-1] in self.coords:
                continue
            else:
                for i, coord in enumerate(ship.coords):
                    self.cells[coord[0]][coord[1]] = ship.body[i]
                    print(coord, ship.body[i])
                # for i, coord in enumerate(ship.buffer_cells_set):
                #     self.cells
                return True

    def place_ship_sets(self, ship):
        """Возвращает True при успешной попытке размещения корабля
        и False при неудачной после превышения числа попыток"""
        max_attempts = 300
        i = 0
        while True:
            i += 1
            # print("i:", i)
            if i > max_attempts:
                print("too many iterations")
                return False
            ship.front = choice(self.coords)
            if (ship.coords_set.issubset(self.coords_set)) and not (ship.coords_set & self.occupied_set):
                for i, coord in enumerate(ship.coords):
                    # print(coord, ship)
                    self.cells[coord[0]][coord[1]] = ship.body[i]
                    _set = self.coords_set & ship.buffer_cells_set
                    print("buffer:", [coord for coord in _set])
                    for coord in _set:
                        self.cells[coord[0]][coord[1]] = BUFFER
                return True
            else:
                continue
        return False

    def place_ship_sets2(self, ship):
        print("hi from place2")
        def do_place():
            for i, coord in enumerate(ship.coords):
                print("def do_place():", coord, ship)
                self.cells[coord[0]][coord[1]] = ship.body[i]
                _set = self.coords_set & ship.buffer_cells_set
                print("buffer:", [coord for coord in _set])
                for coord in _set:
                    self.cells[coord[0]][coord[1]] = BUFFER

        if ship.front: # если человек (заранее указана координата носа), пытаемся разместить корабль
            intersection = ship.coords_set & self.occupied_set
            print("hi from if ship.front", ship.front)
            if (ship.coords_set.issubset(self.coords_set)) and not intersection:
                do_place()
                return True
            elif not ship.coords_set.issubset(self.coords_set):
                raise exceptions.OutOfBoard(ship.front, ship.len)
            elif intersection:
                raise exceptions.PointUsedAlready(intersection)
            else:
                print("Something strange happened")
            # try_to_place
        else: # если компьютер, делаем случайный выбор и пытаемся разместить корабль
            print("hi from place2else")
            max_attempts = 5000
            i = 0
            while True:
                ship.front = choice(self.coords)
                i += 1
                # print("i:", i)
                if i > max_attempts:
                    print("too many iterations")
                    return False
                if (ship.coords_set.issubset(self.coords_set)) and not (ship.coords_set & self.occupied_set):
                    do_place()
                    return True
                else:
                    continue
            return False

    def place_ships(self, ships):
        count = 0
        for i, ship in enumerate(ships):
            if self.place_ship_sets2(ship):
                count += 1
            print("Ship No", i + 1)
        print(f"Успешно размещено {count} из {len(ships)} кораблей!")

    @property
    def coords(self):
        """Возвращает список пар координат"""
        output = []
        for i, elem in enumerate(self.cells):
            output += [(i, j) for j, e in enumerate(elem)]
        return output

    @property
    def coords_set(self):
        """Возвращает сет пар координат"""
        return {(i, j) for i, e in enumerate(self.cells) for j, _ in enumerate(e)}

    @property
    def occupied(self):
        target = []
        for i, elem in enumerate(self.cells):
            target += [(e, i, j) for j, e in enumerate(elem) if e in (BODY, DAGGER, HIT)]
        return target
    @property
    def occupied_set(self):
        """Возвращает сет пар запрещенных для хода координат"""
        return {(x, y) for x, elem in enumerate(self.cells) for y, e in enumerate(elem) if
                e in (BODY, BUFFER, DAGGER, HIT)}

    # def add_ship(self, ship):
    #     for cell in ship:
    #         self.cells[cell[0]][cell[1]] = BODY

    # def place_ships(self):
    #     for ship in self.ships:
    #         for cell in ship:
    #             self.cells[cell[0]][cell[1]] = BODY

    def __repr__(self):
        """Формирует строку с изображением поля"""
        divider = " | "
        rng = range(0, self._side)  # временно для тестирования
        head = f"{self.player.center(25, '_')}\n    "
        head += "  ".join(str(i).rjust(2) for i in rng)
        head += "\n"
        output = ""
        for i, line in enumerate(self.cells):
            if self.display_ships:
                inner = ((cell if cell != BUFFER else EMPTY) for cell in line)
            else:
                inner = ((cell if cell != BODY and cell != BUFFER else EMPTY) for cell in line)

            inner = divider.join(inner)
            output += str(i).rjust(2) + '   ' + inner + "\n"  # временно для тестирования
        output = head + output
        return output

    def fire(self, cell):
        pass
