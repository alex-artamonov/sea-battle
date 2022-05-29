from board import Board
import globals
import exceptions
from random import choice
from globals import MOVE_DICT
from globals import ai_to_user

class Player:
    """ родитель для классов User и AI
    Аттрибуты:
        - name: имя игрока
        - my_board: "своя доска"
        - their_board: доска противника
    Методы:
        - ask: запрос хода от игрока - заглушка для реализации метода потомком
        - move: вызов self.ask, their_board.fire
    """
    def __init__(self, my_board: Board, their_board: Board, name='human'):
        self.name = name
        self.my_board = my_board
        self.their_board = their_board
        self.fired_at = set()
        self.just_killed_a_ship = False

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
                return (f"Игрок {self.name}, ход '{ai_to_user(mv)}': {MOVE_DICT[result]}{ship_len}!")
                # return
            except exceptions.PointHitAlready as e:
                print(e, msg)
                continue
            except IndexError:
                print("Координаты за пределами поля.", msg)
                continue
            except ValueError:
                print("Введано неверное значение координат.", msg)
                continue

    def ask(self):
        return NotImplemented

class User(Player):
    def ask(self):
        move = input(f'{self.name}! Огонь!{globals.INP_INVITE}\t')
        if move in globals.QUIT:
            print(f"Спасибо за игру, {self.name}!")
            exit()
        side = self.their_board.side + 1 # отображаемая на доске нумерация начинается с 1
        lst_moves = [str(i) + str(j) for i in range(1,side) for j in range(1, side)]
        if move not in lst_moves:
            raise ValueError
        else:
            move = (int(move[0]) - 1, int(move[1]) - 1)
            return move

class AI(Player):
    """реализация родительского метода-заглушки"""
    def ask(self):
        side = self.their_board.side
        # чтобы совсем не палить случайноым образом, ограничиваем до возможных ходов:
        lst_moves = list({(i, j) for i in range(side) for j in range(side)} - self.fired_at)
        mv = choice(lst_moves)
        return mv


