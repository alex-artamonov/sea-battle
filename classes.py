from random import choice
EMPTY = 'О'
# EMPTY = " "
BOX = '■'
DAGGER = '†'
HIT = "‡"


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

    def __init__(self, length, direction="H", board_size=6):
        self._front = ()
        self.direction = direction
        self.board_size = board_size
        self._max_len = 4
        self.len = length
        # self.nbr_lives = len
        self._body = []
        for _ in range(self._len):
            self._body.append(BOX)

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
        return self.body.count(BOX)
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

# ========================================================================
class Board:
    """Игровое поле
    Аттрибуты:
        - player: игрок (компьютер или человек). Корабли поля человека отображаются для него всегда
        - список кораблей
        - размерность: число - сторона квадрата, по умолчанию 6
        - points: двумерный массив состояний точек - море, корабль, буфер вокруг корабля, обстреляна
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
                self.cells[coords[0]][coords[1]] = BOX if cell[1] else EMPTY

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
        #lst = [(i, j) for i in range(self._side) for j in range(self._side)]
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
                return True

    def place_ship_sets(self, ship):
        """Возвращает True при успешной попытке размещения корабля
        и False при неудачной после превышения числа попыток"""
        max_attempts = 130
        # ship = Ship(4)
        #lst = [(i, j) for i in range(self._side) for j in range(self._side)]
        i = 0
        while True:
            i += 1
            print("i:", i)
            if i > max_attempts:
                print("too many iterations")
                return False
            ship.front = choice(self.coords)
            if  (ship.coords_set.issubset(self.coords_set)) and not (ship.coords_set & self.occupied_set()):
                for i, coord in enumerate(ship.coords):
                    print(coord, ship)
                    self.cells[coord[0]][coord[1]] = ship.body[i]
                return True
            else:
                continue
        return False


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
            target += [(e, i, j) for j, e in enumerate(elem) if e in (BOX, DAGGER, HIT)]
        return target

    def occupied_set(self):
        """Возвращает сет пар запрещенных для хода координат"""
        return {(x, y) for x, elem in enumerate(self.cells) for y, e in enumerate(elem) if e in (BOX, DAGGER, HIT)}


    # def add_ship(self, ship):
    #     for cell in ship:
    #         self.cells[cell[0]][cell[1]] = BOX

    # def place_ships(self):
    #     for ship in self.ships:
    #         for cell in ship:
    #             self.cells[cell[0]][cell[1]] = BOX

    def __repr__(self):
        """Формирует строку с изображением поля"""
        divider = " | "
        rng = range(1, self._side + 1)
        head = f"{self.player.center(25, '_')}\n    "
        head += "  ".join(str(i).rjust(2) for i in rng)
        head += "\n"
        output = ""
        for i, line in enumerate(self.cells):
            # out = ""
            for cell in line:
                inner = ((cell if self.display_ships or cell != BOX else EMPTY) for cell in line)
                inner = divider.join(inner)
            # s += str(i + 1) + "   " + divider.join(line) + "\n\n"
            # s += f"{str(i + 1)}   {divider.join(line)}\n" #   {' -- ' * 6}\n"
            output += str(i + 1).rjust(2) + '   ' + inner + "\n"

            # s += divider.join(line)
            # s += "\n\n"
        output = head + output
        return output
        
    def fire(self, cell):
        pass
