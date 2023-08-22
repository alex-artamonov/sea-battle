# from ship import Ship
from random import choice
import exceptions
import globals as g
from ship import Ship

# BUFFER = g.BUFFER


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

    def __init__(self, player, side=6, sample:dict = None):
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
        if not sample:
            self.cells = {(x, y): g.UNKNOWN for x in range(side) for y in range(side)}
        else:
            self.cells = sample.copy()

    # def copy(self, sample):
    #     side = sample.side
    #     player = sample.player
    #     ships = sample.ships
    #     used_cells = sample.used_cells
    #     board = Board(side=side, player=player)
    #     self.cells.copy(sample.cells)

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
        return {
            cell
            for cell in self.cells.keys()
            if self.cells[cell] in (g.BODY, g.HIDDEN_BUFFER, g.HIT)
        }

    @property
    def has_ships_afloat(self):
        """Возвращает True, если не все корабли на доске подбиты"""
        return any(ship.is_afloat for ship in self.ships)

    def place_ship(self, ship):
        """Размещает корабль на поле случайным образом"""

        def do_place():
            bs = ship.buffer_cells_set
            cs = self.coords_set
            for coord in ship.coords:
                self.cells[coord], ship.body_dict[(coord)] = g.BODY, g.BODY
                _set = cs & bs
                # отрисовка невидимой буферной зоны по контуру корабля
                for buffer_coord in _set:
                    self.cells[buffer_coord] = g.HIDDEN_BUFFER
            self.ships.append(ship)

        # создаем список свободных координат для экономии усилий
        vacant_coords = list(self.coords_set - self.occupied_set)
        if not vacant_coords:
            raise exceptions.NoVacantCells()
        max_attempts = 100
        i = 0
        directons = ['']
        while True:

            ship.front = choice(vacant_coords)
            # if g.ANCOR in ship.body_dict.values():
            #     raise exceptions.ValueError('ancored!!!')
            i += 1
            if i == max_attempts:
                print('Before toomanyattempts:', len(ship))
                raise exceptions.TooManyAttempts(i)
            if (ship.coords_set.issubset(self.coords_set)) and not (
                ship.coords_set & self.occupied_set
            ):
                do_place()
                # iters = "iteration" if i == 1 else "iterations"
                # print(f"*took {i} {iters} to place this ship*: {ship.coords_set=}") # для отладки
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
                print('try_place_ships:before exception:\n', self.cells)
                raise exceptions.NoVacantCells(
                    f"Нет свободного места для размещения корабля №{i + 1}!"
                )

        self.ships = ships
    
    def place_ships(self, ships, show=False):
        if show:
            print('hi from place ships:\n', self)
        number_of_attempts = 0
        while True:
            try:
                number_of_attempts += 1
                self.try_place_ships(ships)
            except (exceptions.FailedToPlaceAllShips, exceptions.NoVacantCells) as e:
                print('!!!!!!!!!!!!!!!!The board was cleared!!!!!!!!')
                print(e)
                self.clear()
                continue
            except exceptions.PointUsedAlready as e:
                print(e)
                continue
            else:
                return True

    def clear(self):
        """Очистка игрового поля и кораблей"""
        for ship in self.ships:
            ship.clear()
        for cell in self.cells:
            self.cells[cell] = g.EMPTY


    def __repr__(self):
        """Формирует строку с изображением поля"""
        shps = " ".join(str(ship) for ship in self.ships)
        shps = g.to_lines_by_limit(shps, 24)
        divider = "|"
        rng = range(1, self.side + 1)  # нумеруем с единицы
        head = f"\n{self.player.center(17, '_')}\n{shps}\n\n  "
        head += "".join(str(i).rjust(2) for i in rng)
        head += f"\n"
        output = ""
        for x in range(self.side):
            if self.display_ships:
                inner = (
                    self.cells[(x, y)] if self.cells[(x, y)] != g.HIDDEN_BUFFER else g.EMPTY
                    for y in range(self.side)
                )
            else:
                inner = (
                    (
                        self.cells[(x, y)]
                        if self.cells[(x, y)] not in [g.BODY, g.HIDDEN_BUFFER]
                        else g.EMPTY
                    )
                    for y in range(self.side)
                )
            inner = (self.cells[(x, y)] for y in range(self.side)) #temporary hack!
            inner = divider.join(inner) + divider
            output += str(x + 1).rjust(2) + " " + inner + "\n"  # нумеруем строки с 1
        output = head + output
        return output

    def take_fire(self, cell) -> tuple():
        """Устанавливает состояние поля и корабля по результату выстрела и
        возвращает состояние ячейки, а если корабль "убит", то g.SUNKEN"""
        if cell in self.used_cells:
            raise exceptions.PointHitAlready(g.ai_to_user(cell))
        self.used_cells.append(cell)
        shot = {cell}
        self.cells[cell] = g.MISS  # по умолчанию
        for ship in self.ships:
            if shot & ship.coords_set:
                self.cells[cell], ship.body_dict[cell] = g.HIT, g.HIT
                if not ship.is_afloat:
                    self.display_kill(ship)
                    self.display_buffer(ship)
                    # возвращаем вызывавшей функции о подбитии корабля и его длине
                    return g.SUNKEN, len(ship)
                else:
                    return g.HIT, ""
        #  возвращаем вызвавшей функции непосредственное  состояние обстрелянной точки
        return (
            self.cells[cell],
            "",
        )  # длину сообщаем только в случае подбитого корабля

    def display_kill(self, ship):
        for s in ship.coords:
            self.cells[s] = g.SUNKEN

    def display_buffer(self, ship):
        st = ship.buffer_cells_set & self.coords_set
        for cell in st:
            if cell not in self.used_cells:
                self.cells[cell] = g.BUFFER
