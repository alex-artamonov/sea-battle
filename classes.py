from random import choice
import exceptions

# EMPTY = 'О'
EMPTY = " "
BODY = '■'
DAGGER = '†'
HIT = "‡"
BUFFER = "B"
MISS = "T"


# =======================================
class Point:
    """Точка на игровой доске или корабле
    Аттрибуты:
        - coords: пара координат (x, y)
        - value: обстреляна (True/False)
    """
    def __init__(self, coord, value ):
        self.coord = coord
        self.value = value


# ======================================
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
    """
    #
    # def __init__(self, length, direction="H", front=(), board_size=6):
    #     self._front = front
    #     self.direction = direction
    #     self.board_size = board_size
    #     self._max_len = 4
    #     self.len = length
    #     # self.nbr_lives = len
    #     self._body = []
    #     self.body_dict = {}
    #     for _ in range(self._len):
    #         self._body.append(BODY)


    def __init__(self, length, direction="H", front=(), board_size=6):
        self.front = front
        self.direction = direction
        self.board_size = board_size
        self._max_len = 4
        self.len = length
        self.body_dict = {}
        # for _ in range(self._len):
        #     self._body.append(BODY)


    # @property
    # def body_dict(self):
    #     return self._body_dict
    #
    # @body_dict.setter
    # def body_dict(self, coord_value):
    #     key, value = coord_value
    #     if value not in [BODY, HIT]:
    #         raise ValueError(f"Значение должно быть <{BODY}> или <{HIT}>")
    #     self._body_dict[key] = value



    @property
    def len(self):
        return self._len

    @len.setter
    def len(self, value):
        if not (0 < value <= self._max_len):
            raise ValueError("Корабль слишком большой!")
        else:
            self._len = value

    # @property
    # def front(self):
    #     return self._front
    #
    # @front.setter
    # def front(self, val):
    #     self._front = val

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



    @property
    def nbr_lives(self):
        return list(self.body_dict.values()).count(BODY)
        # pass
    #
    # @property
    # def body(self):
    #     return self._body

    # @body.setter
    # def body(self, cell, val=DAGGER):
    #     self._body[cell] = val
    #     pass

    def __repr__(self):
        output = f"\nКорабль  {''.join(self.body)} :\n\t- Длина: {self.len}\n\t- Координаты: {self.coords_set}\n\t" \
                 f"- Жизней: {self.nbr_lives}/{self.len}"
        # print("self._body_dict.values()", "".join(self._body_dict.values()))
        return output

    def __str__(self):
        output = f"\nКорабль  {''.join(self.body_dict.values())} :\n\t- Длина: {self.len}\n\t- Координаты: {self.coords_set}\n\t" \
                 f"- Жизней: {self.nbr_lives}/{self.len}"
        # return ''.join(self._body_dict.values())
        return output

    @property
    def buffer_cells_set(self):
        """Возвращает сет буферной зоны вокруг корабля"""
        sb = self.coords_set
        print("hi from buffer_cells_set", sb)
        _set = set()
        for coord in sb:
            x, y = coord[0], coord[1]
            _set = _set | {
                (x - 1, y - 1), (x, y - 1), (x + 1, y - 1),
                (x - 1, y), (x + 1, y),
                (x - 1, y + 1), (x, y + 1), (x + 1, y + 1)
            }
        _set -= sb  # вычитаем массив координат корабля из массива координат буферной зону
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


    def __init__(self, player, side=6):
        if side < 6 or side > 99:
            raise ValueError(f"Размер поля должен быть в пределах от 6 до 99, указан '{side}'")
        self._cells = [list(EMPTY * side) for _ in range(side)]
        self._side = side
        self.player = player
        self.ships = []
        # self.ships = ships # что передавать на поле при инициализации?
        self.display_ships = True
        self._used_cells = []
        # for ship in self.ships:
        #     print("hi from Board.__init__: for ship in self. ships")
        #     for cell in ship:
        #         coords = (cell[0][0], cell[0][1])
        #         self.cells[coords[0]][coords[1]] = BODY if cell[1] else EMPTY

        # place_ships()

    @property
    def cells(self):
        return self._cells

    @cells.setter
    def cells(self, value):
        print("hi from @cells.setter")

    @property
    def used_cells(self):
        return self._used_cells

    @property
    def ship_sets(self):
        # for ship in ships:
        #     print(ship)
        # print(self.ships)
        # print("len(self.ships)", len(self.ships))
        return [ship.coords_set for ship in self.ships]

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
        lst = [(i, j) for i in range(self._side) for j in range(self._side)]
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
        """Размещает корабль на поле автоматически либо вручную
        """
        def do_place():
            bs = ship.buffer_cells_set
            cs = self.coords_set
            for i, coord in enumerate(ship.coords):
                x, y = coord
                # self.cells[coord[0]][coord[1]] = ship.body[i]
                self.cells[x][y], ship.body_dict[(x,y)] = BODY, BODY
                _set = cs & bs
                for coord in _set:
                    x, y = coord
                    self.cells[x][y] = BUFFER
            self.ships.append(ship)
            print("buffer:", [coord for coord in _set])
            print("def do_place():", ship)

        try:
            # если человек вручную пытаемся разместить корабль, непосредственно указав координата носа:
            if ship.front:
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
                    return False

            # если компьютер или человек выбирает автоматическое размещение,
            # делаем случайный выбор и пытаемся разместить корабль
            else:
                # создаем список свободных координат для экономии усилий
                vacant_coords = list(self.coords_set - self.occupied_set)
                if not vacant_coords:
                    # print("vacant coords:", vacant_coords or "no vacant coords")
                    raise exceptions.NoVacantCells()
                # else:
                # print("vacant coords:", vacant_coords)
                # print("occupied", self.occupied_set)
                max_attempts = 10
                i = 0
                while True:
                    ship.front = choice(vacant_coords)
                    i += 1
                    # print("i:", i)
                    if i > max_attempts:
                        raise exceptions.TooManyAttempts(i)
                    if (ship.coords_set.issubset(self.coords_set)) and not (ship.coords_set & self.occupied_set):
                        do_place()
                        iters = 'iteration' if i == 1 else 'iterations'
                        print(f"took {i} {iters} to place this ship ")
                        return True
                    else:
                        continue
        except exceptions.TooManyAttempts as e:
            print(e)
            return False
        except exceptions.OutOfBoard as e:
            print(e)
            return False
        except exceptions.PointUsedAlready as e:
            print(e)
            return False

    def place_ship_sets_(self, ship):
        # print("hi from place2")
        def do_place():
            bs = ship.buffer_cells_set
            cs = self.coords_set
            for i, coord in enumerate(ship.coords):
                self.cells[coord[0]][coord[1]] = ship.body[i]
                _set = cs & bs
                for coord in _set:
                    self.cells[coord[0]][coord[1]] = BUFFER
            print("buffer:", [coord for coord in _set])
            print("def do_place():", ship)

        # если человек вручную пытаемся разместить корабль, непосредственно указав координата носа:
        if ship.front:
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
        # если компьютер или человек выбирает автоматическое размещение,
        # делаем случайный выбор и пытаемся разместить корабль
        else:

            # print("hi from place2else")
            # создаем список свободных координат для экономии усилий
            vacant_coords = list(self.coords_set - self.occupied_set)
            if not vacant_coords:
                print("vacant coords:", vacant_coords or "no vacant coords")
                # raise ValueError("No vacant cells!")
            else:
                print("vacant coords:", vacant_coords)
                print("occupied", self.occupied_set)
            max_attempts = 10
            i = 0
            while True:
                # vacant_coords = list(self.coords_set - self.occupied_set)

                # ship.front = choice(self.coords)

                ship.front = choice(vacant_coords)
                i += 1
                # print("i:", i)
                if i > max_attempts:
                    print("too many iterations")
                    return False
                if (ship.coords_set.issubset(self.coords_set)) and not (ship.coords_set & self.occupied_set):
                    do_place()
                    iters = 'iteration' if i == 1 else 'iterations'
                    print(f"took {i} {iters} to place this ship ")
                    return True
                else:
                    continue
            return False

    def place_ships(self, ships):
        try:
            count = 0
            msg = ""
            for i, ship in enumerate(ships):
                if self.place_ship_sets2(ship):
                    count += 1
                    # ships.append(ship)
                    # print(ship)
                print("Ship No", i + 1)

            if count < len(ships):
                msg += ": попробуйте еще раз!"
                # print(f"{msg}: попробуйте еще раз!")
            else:
                # self.ships = ships
                msg += ": все корабли размещены успешно."
                self.ships = ships
                # print(f"{msg}: все корабли размещены успешно.")
                # print(self.ships)
        except exceptions.NoVacantCells as e:
            print(e)
        else:
            # msg = f"Размещено {count} из {len(ships)} кораблей"
            pass
        finally:
            msg = f"Размещено {count} из {len(ships)} кораблей"
            print(msg)

    @property
    def coords(self):
        """Возвращает список кортежей из пар координат"""
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
        """Возвращает сет кортежей из пар запрещенных для хода координат"""
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
                # inner = ((cell if cell != BUFFER else EMPTY) for cell in line)
                inner = ((cell if cell else EMPTY) for cell in line) # временно для теста
            else:
                inner = ((cell if cell != BODY and cell != BUFFER else EMPTY) for cell in line)

            inner = divider.join(inner)
            output += str(i).rjust(2) + '   ' + inner + "\n"  # временно для тестирования
        output = head + output
        return output


    def fire(self, cell):
        if cell in self.used_cells:
            raise exceptions.PointHitAlready(cell)
        self._used_cells.append((cell))
        print("hi from fire:", cell)
        x, y = cell
        # brd = Board("asdf")
        # if self.cells[x][y] == BODY:
        #     self.cells[x][y] = HIT
        #     print("hi from fire if")
        # else:
        #     self.cells[x][y] = MISS
        # board.cells[x][y] = HIT if board.cells[x][y] == BODY else MISS

        shot = {(x,y)}
        self.cells[x][y] = MISS #по умолчанию
        print("shot:", shot)
        for ship in self.ships:
            # print("for ship in self.ship_sets, ship.coords:", ship.coords_set)
            if shot & ship.coords_set:
                # ship.body[x][y] = HIT
                print("HIT!:", shot, ship.coords)
                self.cells[x][y], ship.body_dict[cell] = HIT, HIT
                print("ship.body_dict", ship.body_dict)
                # i = ship.coords.index((x,y))
                # print("ship.coords.index((x,y))", i )
                # ship.body[i] = HIT
                print(ship)
                break
                # for i, coord in ship.coords:
                #     if



            # if ship & shot:
            #     ship.coords[x],[y] = HIT
            #     print("HIT!:", ship, shot)

