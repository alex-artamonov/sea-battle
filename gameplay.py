# -*- coding: utf-8 -*-
import exceptions
import globals
from ship import Ship
from board import Board
from sys import exit
from itertools import zip_longest
from random import choice
from player import User, AI

# CLEAR = "\x1B[H\x1B[J"
def clear_screen():
    print("\x1B[H\x1B[J")


def to_lines_by_limit(string, limit):
    """Для форматирования: разбивает сплошной текст на строки с указанным
    лимитом знаков без переноса слов"""
    output = ""
    while len(string) >= limit:
        string = string.strip()
        n = min(string.find('\n'), string[:limit].rfind(' '))
        if n == -1:
            n = max(string.find('\n'), string[:limit].rfind(' '))
        if n > 0:  # если пробел есть и не в начале строки
            head = string[:n].strip()
            string = string[n:]
        elif n < 0:
            raise ValueError(f"The limit '{limit}' is too small: the text can't be split")
        else:  # если пробел в начале строки
            head = string[:limit]
            string = string[limit:]
        output += head + "\n"
    output += string.lstrip()
    return output


def print_side_by_side(str1, str2, divider="    |    "):
    """Для вывода рядом двух досок. Выводит попеременно строки из двух строковых переменных
    с указанным разделением между ними"""
    s1 = str1.split('\n')
    s2 = str2.split('\n')

    lst = [len(elem) for elem in s1]
    nbr_spaces = max(lst)  # ищем самую длинную строку, чтобы выровнять остальные
    clear_screen()
    for line1, line2 in zip_longest(s1, s2):
        line1, line2 = line1 or "", line2 or ""
        print(line1.ljust(nbr_spaces) + divider + line2)

HUMAN = "HUMAN_NAME"
gameplay_dict = {"COMPUTER_NAME": "computer", HUMAN: 'human'}


def greeting():
    print("Представьтесь, пожалуйста:")
    gameplay_dict["HUMAN_NAME"] = input(globals.INP_INVITE).upper()
    print("Привет,", gameplay_dict["HUMAN_NAME"])


def initialize_game():
    gameplay_dict["SIDE"] = 6
    msg = "Вспомним детство, поиграем в ""Морской бой""?\n"
    msg += "Играем на поле 6 * 6. При желании выйти из игры (и проиграть) можно ввести 'q' " \
           "вместо хода. В каждом флоте участвуют 7 кораблей:\n"
    msg += "- 1 корабль на 3 клетки\n- 2 корабля на 2 клетки\n- 4 корабля на 1 клетку\n"
    msg += "Итак, приступим. Для начала надо разместить корабли на поле боя. Для размещения вручную нажмите (1), " \
           "для автоматического - (2).\nИли введите 'q' для выхода из игры (и проигрыша).\n" \
           "Ходы обозначаются двумя цифрами подряд, например 12. Первая цифра - ряд, вторая - колонка.\n"
    print(to_lines_by_limit(msg, 60))
    while True:
        reply = input(globals.INP_INVITE)
        if reply in globals.QUIT:
            print(f"Жаль, {gameplay_dict[HUMAN]}, до следующего раза!")
            exit()
        if reply in ('1', '2'):
            print(reply)
            # call function to place the ships manually or automatically
            break
        else:
            print("Введите 1 или 2")
            continue

    brd_computer = Board(gameplay_dict["COMPUTER_NAME"], 4)
    brd_human = Board(gameplay_dict[HUMAN], 4)
    sh1 = Ship(3, choice(["H", "V"]))
    sh2 = Ship(2, choice(["H", "V"]))
    sh3 = Ship(2, choice(["H", "V"]))
    sh4 = Ship(1, choice(["H", "V"]))
    sh5 = Ship(1, choice(["H", "V"]))
    sh6 = Ship(1, choice(["H", "V"]))
    sh7 = Ship(1, choice(["H", "V"]))
    sh11 = Ship(3, choice(["H", "V"]))
    sh12 = Ship(2, choice(["H", "V"]))
    sh13 = Ship(2, choice(["H", "V"]))
    sh14 = Ship(1, choice(["H", "V"]))
    sh15 = Ship(1, choice(["H", "V"]))
    sh16 = Ship(1, choice(["H", "V"]))
    sh17 = Ship(1, choice(["H", "V"]))
    # ships = [sh1, sh2, sh3, sh4, sh5, sh6, sh7]
    ships = [sh1, sh7]
    # ships2 = [sh11, sh12, sh13, sh14, sh15, sh16, sh17]
    ships2 = [sh11, sh17]
    brd_computer.display_ships = False
    place_ships(brd_computer, ships)
    place_ships(brd_human, ships2)
    # brd_computer.place_ships(ships)
    # brd_human.place_ships(ships2)
    # print(brd_computer)
    # print_side_by_side(brd_computer.__repr__(), brd_human.__repr__(), divider="    |    ")
    print_side_by_side(str(brd_computer), str(brd_human))
    # move = input('Fire!')
    # move = (int(move[0]), int(move[1]))
    # brd_computer.fire(move)
    # print_side_by_side(str(brd_computer), str(brd_human))

    usr = User(brd_human, brd_computer, gameplay_dict[HUMAN])
    ai = AI(brd_computer, brd_human, gameplay_dict["COMPUTER_NAME"])

    current_player = usr
    next_player = ai
    move_number = 0
    while current_player.their_board.has_ships_afloat:
        try:
            move_number += 1
            current_player.move()
            while current_player.one_shot_kill and current_player.their_board.has_ships_afloat:
                print_side_by_side(str(brd_computer), str(brd_human))
                print(f"Отличный выстрел, {current_player.name}! За это полагается бонусный ход!")
                current_player.move()
        except (exceptions.PointHitAlready, IndexError, ValueError) as e:
            print(e, ' - try again!')
            continue
        else:
            current_player, next_player = next_player, current_player
            print("move_number:", move_number)
            if move_number % 2 == 0:
                print_side_by_side(str(brd_computer), str(brd_human))
    print(f"Победу одержал {current_player.name}")

def place_ships(board, ships):
    # (print(ship.front or 'Nothing') for ship in ships)
    number_of_attempts = 0
    while True:
        try:
            number_of_attempts += 1
            board.try_place_ships(ships)
        except (exceptions.FailedToPlaceAllShips, exceptions.NoVacantCells) as e:
            print(e)
            # print(board.cells)
            board.clear()
            # print(board.cells)
            # break
            continue
        except exceptions.PointUsedAlready as e:
            print(e)
        else:
            print(f"Все корабли на доске игрока '{board.player}' были успешно размещены "
                  f"случайным образом. Число попыток:", number_of_attempts)
            break


greeting()
initialize_game()
