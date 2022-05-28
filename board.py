# from ship import Ship
from random import choice
import exceptions

# EMPTY = " "
# BODY = '■'
# DAGGER = '†'
# HIT = "‡"
BUFFER = "B"
# MISS = "О"


# ========================================================================
import globals
LOWER_LIMIT = 3
UPPER_LIMIT = 20
class Board:
    """Игровое поле
    Аттрибуты:
        - player: игрок (компьютер или человек). Корабли поля человека отображаются для него всегда
        - список кораблей
        - размерность: число - сторона квадрата, по умолчанию 6
        - cells: двумерный массив состояний точек - море, корабль, буфер вокруг корабля, обстреляна
        - coords_set(: массив координат"""

    def __init__(self, player, side=6):
        if side < LOWER_LIMIT or side > UPPER_LIMIT:
            raise ValueError(f"Размер поля должен быть в пределах от {LOWER_LIMIT} "
                             f"до {UPPER_LIMIT}, указан '{side}'")
        self.cells = [list(globals.EMPTY * side) for _ in range(side)]
        self.side = side
        self.player = player
        self.ships = []
        # self.ships = ships # что передавать на поле при инициализации?
        self.display_ships = True
        self.used_cells = []

    @property
    def ship_sets(self):
        """Возвращает список множеств кортежей из пар координат кораблей на поле"""
        return [ship.coords_set for ship in self.ships]

    @property
    def coords_set(self):
        """Возвращает сет кортежей из пар координат"""
        return {(i, j) for i, e in enumerate(self.cells) for j, _ in enumerate(e)}

    @property
    def occupied_set(self):
        """Возвращает сет кортежей из пар запрещенных для размещения корабля координат"""
        return {(x, y) for x, elem in enumerate(self.cells) for y, e in enumerate(elem) if
                e in (globals.BODY, BUFFER, globals.DAGGER, globals.HIT)}

    @property
    def has_ships_afloat(self):
        """Возвращает True, если все корабли на доске подбиты"""
        return any(ship.is_afloat for ship in self.ships)

    def place_ship(self, ship):
        """Размещает корабль на поле автоматически либо вручную
        """
        def do_place():
            bs = ship.buffer_cells_set
            cs = self.coords_set
            for i, coord in enumerate(ship.coords):
                x, y = coord
                # self.cells[coord[0]][coord[1]] = ship.body[i]
                self.cells[x][y], ship.body_dict[(x, y)] = globals.BODY, globals.BODY
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


    def clear(self):
        for ship in self.ships:
            ship.clear()
        self.cells = [list(globals.EMPTY * self.side) for _ in range(self.side)]

    def __repr__(self):
        """Формирует строку с изображением поля"""
        shps = ' '.join(str(ship) for ship in self.ships)
        # divider = " | "
        divider = "|"
        # rng = range(0, self.side)  # временно для тестирования
        rng = range(0 + 1, self.side + 1)  # нумеруем с единицы
        # head = f"{self.player.center(25, '_')}\n    "
        head = f"\n{self.player.center(17, '_')}\n{shps}\n\n  "
        head += "".join(str(i).rjust(2) for i in rng)
        head += f"\n"
        output = ""
        for i, line in enumerate(self.cells):
            if self.display_ships:
                inner = ((cell if cell != BUFFER else globals.EMPTY) for cell in line)
                # inner = ((cell if cell else EMPTY) for cell in line)  # временно для теста
            else:
                inner = ((cell if cell != globals.BODY and cell != BUFFER else globals.EMPTY) for cell in line)

            inner = divider.join(inner)
            # output += str(i).rjust(2) + '   ' + inner + "\n"  # временно для тестирования
            output += str(i + 1).rjust(2) + ' ' + inner + "\n" # нумеруем строки с 1
        output = head + output
        return output

    def take_fire(self, cell):
        """Устанавливает состояние поля и корабля по результату выстрела
        возвращает True если корабль убит одним выстрелом и false в остальных случаях"""
        if cell in self.used_cells:
            raise exceptions.PointHitAlready(cell)
        self.used_cells.append(cell)
        x, y = cell
        shot = {(x, y)}
        self.cells[x][y] = globals.MISS  # по умолчанию
        for ship in self.ships:
            # print("for ship in self.ship_sets, ship.coords:", ship.coords_set)
            if shot & ship.coords_set:
                self.cells[x][y], ship.body_dict[cell] = globals.HIT, globals.HIT
                if ship.len == 1:
                    print("killed at on shot!")
                    return True
                return False
        return False

