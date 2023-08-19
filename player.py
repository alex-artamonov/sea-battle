from board import Board
import globals
import exceptions
from random import choice, choices
from globals import MOVE_DICT
from globals import ai_to_user
from ship import Ship


class Player:
    """родитель для классов User и AI
    Аттрибуты:
        - name: имя игрока
        - my_board: "своя доска"
        - their_board: доска противника
    Методы:
        - ask: запрос хода от игрока - заглушка для реализации метода потомком
        - move: вызов self.ask, their_board.fire
    """

    def __init__(self, my_board: Board, their_board: Board, name="human"):
        self.name = name
        self.my_board = my_board
        self.their_board = their_board
        side = their_board.side
        self.allowed_moves = {(i, j) for i in range(side) for j in range(side)}
        self.fired_at = set()
        self.just_killed_a_ship = False
        self.recent_hit = None
        self.message = ""
        self.hits = []
        self.probable_hits = set()
        self.buffer_cells = set()

    def move(self):
        """Вызываем метод ask, делаем выстрел по вражеской доске
        (метод Board.fire), отлавливаем исключения, и если они есть,
        пытаемся повторить ход. Метод должен возвращать True,
        если этому игроку нужен повторный ход (например если он выстрелом подбил корабль)"""

        while True:
            msg = "Попробуйте еще раз."
            self.just_killed_a_ship = False
            try:
                mv = self.ask()
                self.fired_at.add(mv)
                result, ship_len = self.their_board.take_fire(mv)

                # ship_len = self.their_board.take_fire(mv)[1] # !! Lessson learned - double call lead to infinite cycle
                if result == globals.SUNKEN:
                    self.just_killed_a_ship = True
                    self.hits.append(mv)
                    self.add_buffer_diagonals(mv)
                    self.add_buffer_endcells()
                    self.recent_hit, self.hits = None, []

                if result == globals.HIT:
                    self.recent_hit = mv
                    self.hits.append(mv)
                    self.add_buffer_diagonals(mv)
                    # self.probable_hits = self.predict_set()

                self.message = f"Игрок {self.name}, ход '{ai_to_user(mv)}': {MOVE_DICT[result]}{ship_len}!"
                return
                # return
            except exceptions.PointHitAlready as e:
                print(e, msg)
                continue
            except IndexError as e:
                print("Координаты за пределами поля.", msg, "move: ", mv)
                print(e)
                continue
            except ValueError as e:
                print("Введано неверное значение координат.", msg)
                print(e)
                continue

    def add_buffer_diagonals(self, cell):
        self.buffer_cells = self.buffer_cells | (
            {
                (cell[0] - 1, cell[1] - 1),
                (cell[0] - 1, cell[1] + 1),
                (cell[0] + 1, cell[1] - 1),
                (cell[0] + 1, cell[1] + 1),
            }
            & self.allowed_moves
        )

    def add_buffer_endcells(self):
        self.buffer_cells = self.buffer_cells | (
            self.predict_set() & self.allowed_moves
        )

    def predict_set(self):
        # output = []
        # coords = ship.coords
        # print(coords)

        coords = sorted(self.hits)
        if len(coords) == 1:
            output = {
                (coords[0][0] - 1, coords[0][1]),
                (coords[0][0] + 1, coords[0][1]),
                (coords[0][0], coords[0][1] - 1),
                (coords[0][0], coords[0][1] + 1),
            }
        elif coords[0][0] == coords[-1][0]:
            output = {
                (coords[0][0], coords[0][1] - 1),
                (coords[-1][0], coords[-1][1] + 1),
            }
        else:
            output = {
                (coords[0][0] - 1, coords[0][1]),
                (coords[-1][0] + 1, coords[-1][1]),
            }
        # output = set(output)
        return output

    def ask(self):
        return NotImplemented


class User(Player):
    def ask(self):
        """реализация родительского метода-заглушки в классе User"""
        move = input(f"{self.name}! Огонь!{globals.INP_INVITE}\t")
        if move in globals.QUIT:
            print(f"Спасибо за игру, {self.name}!")
            exit()
        side = (
            self.their_board.side + 1
        )  # отображаемая на доске нумерация начинается с 1
        lst_moves = [str(i) + str(j) for i in range(1, side) for j in range(1, side)]
        if move not in lst_moves:
            raise ValueError
        else:
            move = (int(move[0]) - 1, int(move[1]) - 1)
            return move


class AI(Player):
    def __init__(self, my_board: Board, their_board: Board, name="human"):
        super().__init__(my_board, their_board, name)
        # self.memory = dict(their_ships = [], my_moves = [])
        ships = their_board.ship_list
        for ship in ships:
            print(f"{len(ship)=}, {ship.coords=}, {ship.front=}, {ship.body_dict=},{ship.direction=}")
        print('ship lengths:')
        [print(len(ship)) for ship in ships]
        self.memory = dict(their_ships = ships)
        print('my memory:', self.memory)
        self.cheat_move = self.cheat()

    def ask(self):
        # n = choice((1,2))
        # if n == 1:
        #     print('odd')
        #     move = self.smart_move()
        # else:
        #     print('even')
        #     move = self.cheating()
        #
        fun = choices((self.smart_move, self.cheating), weights=(1, 9),k=1)[0]
        move = fun()
        print(f"hi from ask. The move should be {move}")
        return move

    def smart_move(self):
        """реализация родительского метода-заглушки в классе AI"""
        # self.hits = []
        print("Computer, огонь!")
        print("smart move")
        # move = next(self.cheat_moves())
        # print(move)
        # print('my next move would be:', next(self.cheat_move))
        # side = self.their_board.side
        self.allowed_moves = self.allowed_moves - self.fired_at

        if self.recent_hit:
            self.probable_hits = self.predict_set() - self.buffer_cells
            # print(f"{self.recent_hit=}, {self.hits=}")
            # print(f"{self.predict_set()=}")
            # print(f"{self.buffer_cells=}")
            self.probable_hits = self.probable_hits & self.allowed_moves
            print(f"calculated moves:{self.probable_hits=}")
            return choice(list(self.probable_hits))
        else:
            print(f"random move minus {self.buffer_cells=}")
            return choice(list(self.allowed_moves - self.buffer_cells))

    def cheating(self):
        print("I'm cheating!")
        # print(self.their_board.ship_sets)
        move = next(self.cheat_move)
        while move in self.fired_at:
            move = next(self.cheat_move)
        return move

    def cheat(self):
        print("hi from cheat mode")
        # print(self.their_board.ship_sets)
        # print(self.their_board.ships)
        return (
            cell for cells 
            in sorted(self.their_board.ship_sets, key=len, reverse=True)
            for cell in cells
        )

    # @property
    # def memory(self):
    #     n = 'asdf'