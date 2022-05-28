from board import Board
import globals
import exceptions
from random import choice

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
        self.one_shot_kill = False


    def move(self):
        """Вызываем метод ask, делаем выстрел по вражеской доске
        (метод Board.fire), отлавливаем исключения, и если они есть,
        пытаемся повторить ход. Метод должен возвращать True,
        если этому игроку нужен повторный ход (например если он выстрелом подбил корабль)"""

        while True:
            msg = "Попробуйте еще раз."
            try:
                mv = self.ask()
                if self.their_board.take_fire(mv):
                    self.one_shot_kill = True
                else:
                    self.one_shot_kill = False
                self.fired_at.add(mv)
                break
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
        move = input(f'{self.name}! Fire!{globals.INP_INVITE}\t')
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

    def ask(self):
        side = self.their_board.side
        lst_moves = list({(i, j) for i in range(side) for j in range(side)} - self.fired_at)
        mv = choice(lst_moves)
        return mv


