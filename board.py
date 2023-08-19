# from ship import Ship
from random import choice
import exceptions
import globals as g

BUFFER = "B"
LOWER_LIMIT = 2
UPPER_LIMIT = 20

# ========================================================================
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
            raise ValueError(
                f"Размер поля должен быть в пределах от {LOWER_LIMIT} "
                f"до {UPPER_LIMIT}, указан '{side}'"
            )
        self.side = side
        self.player = player
        self.ships = []
        self.display_ships = True
        self.used_cells = []
        self.hit = ()
        self.cells = {(x,y): g.UNKNOWN for x in range(side) for y in range(side) }


    @property
    def ship_sets(self):
        """Возвращает список множеств кортежей из пар координат кораблей на поле"""
        return [ship.coords_set for ship in self.ships]

    @property
    def coords_set(self):
        """Возвращает сет кортежей из пар координат"""
        return set(self.cells.keys())
    @property
    def occupied_set(self):
        """Возвращает сет кортежей из пар запрещенных для размещения корабля координат"""
        return {cell for cell in self.cells.keys() 
                if self.cells[cell] in (g.BODY, BUFFER, g.HIT)}

    @property
    def has_ships_afloat(self):
        """Возвращает True, если не все корабли на доске подбиты"""
        return any(ship.is_afloat for ship in self.ships)

    def place_ship(self, ship):
        """Размещает корабль на поле случайным образом"""

        def do_place():
            bs = ship.buffer_cells_set
            cs = self.coords_set
            for i, coord in enumerate(ship.coords):
                x, y = coord
                self.cells[(x,y)], ship.body_dict[(x, y)] = g.BODY, g.BODY
                _set = cs & bs
                # отрисовка буферной зоны по контуру корабля
                for buffer_coord in _set:
                    x, y = buffer_coord
                    self.cells[(x,y)] = BUFFER
            self.ships.append(ship)

        # создаем список свободных координат для экономии усилий
        vacant_coords = list(self.coords_set - self.occupied_set)
        if not vacant_coords:
            raise exceptions.NoVacantCells()
        max_attempts = 300
        i = 0
        while True:
            ship.front = choice(vacant_coords)
            i += 1
            if i == max_attempts:
                raise exceptions.TooManyAttempts(i)
            if (ship.coords_set.issubset(self.coords_set)) and not (
                ship.coords_set & self.occupied_set
            ):
                do_place()
                # iters = "iteration" if i == 1 else "iterations"
                # print(f"*took {i} {iters} to place this ship*") # для отладки
                return True
            else:
                continue

    def try_place_ships(self, ships):
        """размещает все корабли на поле"""
        self.ship_list = ships
        count = 0
        for i, ship in enumerate(ships):
            if self.place_ship(ship):
                count += 1
            else:
                raise exceptions.NoVacantCells(
                    f"Нет свободного места для размещения корабля №{i + 1}!"
                )

        self.ships = ships

    def clear(self):
        """Очистка игрового поля и кораблей"""
        for ship in self.ships:
            ship.clear()
        self.cells = {(x, y): g.EMPTY for x in range(self.side)
                           for y in range(self.side)}

    def to_list(self):
        """Returns list of lists (rows) from self.cells"""
        output = []
        for x in range(self.side):
            output.append([self.cells[(x, y)] for y in range(self.side)])
        return output

    def __repr__(self):
        """Формирует строку с изображением поля"""
        shps = " ".join(str(ship) for ship in self.ships)
        shps = g.to_lines_by_limit(shps, 24)
        divider = "|"
        rng = range(1, self.side + 1)  # нумеруем с единицы
        head = f"\n{self.player.center(17, '_')}\n{shps}\n\n  "
        head += "".join(str(i).rjust(2) for i in rng)
        head += f"\n"
        # cells_list = self.to_list()
        output = ""        
        for x in range(self.side):
            if self.display_ships:
                inner = (
                    self.cells[(x, y)] 
                    if self.cells[(x, y)] != BUFFER 
                    else g.EMPTY for y in range(self.side)
                )
            else:
                inner = (
                    (self.cells[(x, y)] 
                        if self.cells[(x, y)] not in [g.BODY, BUFFER]
                        else g.EMPTY) for y in range(self.side)
                )
            inner = divider.join(inner) + divider
            output += str(x + 1).rjust(2) + " " + inner + "\n"  # нумеруем строки с 1      
        output = head + output
        return output

    def take_fire(self, cell) -> tuple():
        """Устанавливает состояние поля и корабля по результату выстрела и
        возвращает состояние ячейки, а если корабль "убит", то g.SUNKEN"""
        if cell in self.used_cells:
            x, y = cell
            raise exceptions.PointHitAlready(g.ai_to_user(cell))
        self.used_cells.append(cell)
        x, y = cell
        shot = {(x, y)}
        self.cells[(x,y)] = g.MISS # по умолчанию
        for ship in self.ships:
            if shot & ship.coords_set:
                self.cells[(x, y)], ship.body_dict[cell] = g.HIT, g.HIT
                if not ship.is_afloat:
                    self.display_kill(ship)
                    self.display_buffer(ship)
                    # возвращаем вызывавшей функции о подбитии корабля и его длине
                    return g.SUNKEN, len(ship)
                else:
                    return g.HIT, ""
        #  возвращаем вызвавшей функции непосредственное  состояние обстрелянной точки
        return self.cells[(x,y)], ""  # длину сообщаем только в случае подбитого корабля


    def display_kill(self, ship):
        for s in ship.coords:
            self.cells[s] = g.SUNKEN

    def display_buffer(self, ship):
        st = ship.buffer_cells_set & self.coords_set
        for cell in st:
            if cell not in self.used_cells:
                self.cells[cell] = g.BUFFER
