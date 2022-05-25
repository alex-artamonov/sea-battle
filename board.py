# from ship import Ship
from random import choice
import exceptions
EMPTY = " "
BODY = '■'
DAGGER = '†'
HIT = "‡"
BUFFER = "B"
MISS = "T"

# ========================================================================
class Board:
    """Игровое поле
    Аттрибуты:
        - player: игрок (компьютер или человек). Корабли поля человека отображаются для него всегда
        - список кораблей
        - размерность: число - сторона квадрата, по умолчанию 6
        - cells: двумерный массив состояний точек - море, корабль, буфер вокруг корабля, обстреляна
        - coords: массив координат"""

    def __init__(self, player, side=6):
        if side < 6 or side > 99:
            raise ValueError(f"Размер поля должен быть в пределах от 6 до 99, указан '{side}'")
        self.cells = [list(EMPTY * side) for _ in range(side)]
        self._side = side
        self.player = player
        self.ships = []
        # self.ships = ships # что передавать на поле при инициализации?
        self.display_ships = True
        self.used_cells = []


    @property
    def ship_sets(self):
        """Возвращает список множества кортежей из пар координат кораблей на поле"""
        return [ship.coords_set for ship in self.ships]

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

    def place_ship_(self, ship):
        """Размещает корабль на поле автоматически либо вручную
        """

        def do_place():
            bs = ship.buffer_cells_set
            cs = self.coords_set
            for i, coord in enumerate(ship.coords):
                x, y = coord
                # self.cells[coord[0]][coord[1]] = ship.body[i]
                self.cells[x][y], ship.body_dict[(x, y)] = BODY, BODY
                _set = cs & bs
                for coord in _set:
                    x, y = coord
                    self.cells[x][y] = BUFFER
            self.ships.append(ship)

        try:
            # если человек вручную пытаемся разместить корабль, непосредственно указав координата носа:
            if ship.front:
                intersection = ship.coords_set & self.occupied_set
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
                max_attempts = 20
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
                        print(f"*took {i} {iters} to place this ship*")
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

    def place_ship(self, ship):
        """Размещает корабль на поле автоматически либо вручную
        """

        def do_place():
            bs = ship.buffer_cells_set
            cs = self.coords_set
            for i, coord in enumerate(ship.coords):
                x, y = coord
                # self.cells[coord[0]][coord[1]] = ship.body[i]
                self.cells[x][y], ship.body_dict[(x, y)] = BODY, BODY
                _set = cs & bs
                for coord in _set:
                    x, y = coord
                    self.cells[x][y] = BUFFER
            self.ships.append(ship)

        # если человек вручную пытаемся разместить корабль, непосредственно указав координата носа:
        if ship.front:
            intersection = ship.coords_set & self.occupied_set
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
                    print(f"*took {i} {iters} to place this ship*")
                    return True
                else:
                    continue

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
            # print("buffer:", [coord for coord in _set])
            # print("def do_place():", ship)

        # если человек вручную пытаемся разместить корабль, непосредственно указав координата носа:
        if ship.front:
            intersection = ship.coords_set & self.occupied_set
            # print("hi from if ship.front", ship.front)
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
                    print(f"*took {i} {iters} to place this ship*")
                    return True
                else:
                    continue
            return False

    def try_place_ships(self, ships):
        count = 0
        for i, ship in enumerate(ships):
            # print(i, ship.len)
            if self.place_ship(ship):
                count += 1
            print(f"Корабль №{i + 1} длины {ship.len} прибывает в пункт назначения")

        if count < len(ships):
            raise exceptions.FailedToPlaceAllShips()
        else:
            self.ships = ships

    def place_ships_old(self, ships):
        try:
            count = 0
            msg = ""
            for i, ship in enumerate(ships):
                if self.place_ship(ship):
                    count += 1
                    # ships.append(ship)
                    # print(ship)
                print(f"Корабль №{i + 1} длины {ship.len}")

            if count < len(ships):
                # msg += ": попробуйте еще раз!"
                # print(f"{msg}: попробуйте еще раз!")
                raise exceptions.FailedToPlaceAllShips()
            else:
                # self.ships = ships
                msg += ": все корабли размещены успешно."
                self.ships = ships
                # print(f"{msg}: все корабли размещены успешно.")
                # print(self.ships)
        except exceptions.NoVacantCells as e:
            print(e)
        except exceptions.FailedToPlaceAllShips() as e:
            print(f"{msg}: попробуйте еще раз!")
        else:
            # msg = f"Размещено {count} из {len(ships)} кораблей"
            pass
        finally:
            msg = f"Размещено {count} из {len(ships)} кораблей"
            print(msg)


    @property
    def coords_set(self):
        """Возвращает сет кортежей из пар координат"""
        return {(i, j) for i, e in enumerate(self.cells) for j, _ in enumerate(e)}

    @property
    def occupied_set(self):
        """Возвращает сет кортежей из пар запрещенных для размещения корабля координат"""
        return {(x, y) for x, elem in enumerate(self.cells) for y, e in enumerate(elem) if
                e in (BODY, BUFFER, DAGGER, HIT)}

    def clear(self):
        for ship in self.ships:
            ship.clear() 
            # print("from self.clear:", ship)
            # ship.front = None
            # del ship # уходит в бесконечный цикл ошибки "Нет свободного места для размещения корабля!"
        # del self.ships
        # for line in self.cells:
        #     for cell in line:
        #         cell = EMPTY
        #     [print("from clear\n",line) in self.cells]
        self.cells = [list(EMPTY * self._side) for _ in range(self._side)]
        # print("from clear:\n", self.cells)



    def __repr__(self):
        """Формирует строку с изображением поля"""
        # shps = str(self.ships)
        shps = ' '.join(str(ship) for ship in self.ships)
        # divider = " | "
        divider = "|"
        rng = range(0, self._side)  # временно для тестирования
        # head = f"{self.player.center(25, '_')}\n    "
        head = f"\n{self.player.center(17, '_')}\n{shps}\n\n  "
        # head += "  ".join(str(i).rjust(2) for i in rng)
        head += "".join(str(i).rjust(2) for i in rng)
        head += f"\n"
        output = ""
        for i, line in enumerate(self.cells):
            if self.display_ships:
                inner = ((cell if cell != BUFFER else EMPTY) for cell in line)
                # inner = ((cell if cell else EMPTY) for cell in line)  # временно для теста
            else:
                inner = ((cell if cell != BODY and cell != BUFFER else EMPTY) for cell in line)

            inner = divider.join(inner)
            # output += str(i).rjust(2) + '   ' + inner + "\n"  # временно для тестирования
            output += str(i).rjust(2) + ' ' + inner + "\n"
        output = head + output
        return output

    def fire(self, cell):
        """устанавливает состояние поля и корабля по результату выстрела"""
        if cell in self.used_cells:
            raise exceptions.PointHitAlready(cell)
        self.used_cells.append(cell)
        x, y = cell
        shot = {(x, y)}
        self.cells[x][y] = MISS  # по умолчанию
        for ship in self.ships:
            # print("for ship in self.ship_sets, ship.coords:", ship.coords_set)
            if shot & ship.coords_set:
                self.cells[x][y], ship.body_dict[cell] = HIT, HIT
                break

