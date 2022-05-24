# -*- coding: utf-8 -*-
import exceptions
from ship import Ship
from board import Board
from sys import exit
from itertools import zip_longest
from random import choice

INP_INVITE = "?--> "

sh = Ship(4, "H", (1, 1))


# print(sh)

def to_lines_by_limit(string, limit):
    """Разбивает сплошной текст на строки с указанным
    лимитом знаков без переноса слов"""
    output = ""
    while len(string) >= limit:
        temp = string[:limit]
        string = string[limit:]
        n = temp.rfind(' ')
        if n > 0: # если пробел есть и не в начале строки
            head = temp[:n].lstrip()
            tail = temp[n:]
            string = tail + string
        elif n <= 0:
            raise ValueError(f"The limit '{limit}' is too small: the text can't be split")
        else:  # если пробел в начале строки
            head = temp.lstrip()
            print("from else:", head)
        output += head + "\n"
    output += string.lstrip()
    return output


def print_side_by_side(str1, str2, divider="    |    "):
    """Выводит попеременно строки из двух строковых переменных
    с указанным разделением между ними"""
    s1 = str1.split('\n')
    s2 = str2.split('\n')

    lst = [len(elem) for elem in s1]
    nbr_spaced = max(lst)

    for line1, line2 in zip_longest(s1, s2):
        line1, line2 = line1 or "", line2 or ""
        print(line1.ljust(nbr_spaced) + divider + line2)


s1 = "Some people take the guideline “the shorter, the better” to an extreme and\
claim that all functions should be three or four lines of code at most. This is\
madness. For example, here’s the getPlayerMove() function from Chapter 14’s Tower\
of Hanoi game. The specifics of how this code works are unimportant. Just look at\
the function’s general structure:"
s2 = "Согласно пункту 2 Порядка выдачи разрешений на вывоз за пределы территории\
 РФ отдельных видов промышленной продукции по перечню согласно приложению № 3 к\
 постановлению № 312, заявление составляется на русском языке, оформляется на\
 бланке заявителя, подписывается заявителем (руководителем юридического лица,\
индивидуальным предпринимателем либо уполномоченным лицом с приложением\
доверенности, подписанной руководителем юридического лица или\
индивидуальным предпринимателем), заверяется печатью заявителя\
(при наличии), а также должно содержать дату и регистрационный (исходящий)\
номер. Дополнительных требований к доверенности не предусмотрено."


# s1, s2 = display_board("human:\n".center(25)), display_board("computer:\n".center(25))
HUMAN = "HUMAN_NAME"
gameplay_dict = {"COMPUTER_NAME": "computer", HUMAN: 'human'}

def greeting():
    print("Представьтесь, пожалуйста:")
    # gameplay_dict["HUMAN_NAME"] = input(INP_INVITE).upper()
    print("Привет,", gameplay_dict["HUMAN_NAME"])


def get_player_move():
    while True:
        response = input(INP_INVITE).upper().strip()
        if response == "QUIT":
            print("Спасибо за игру!")
            exit()

def initialize_game():
    gameplay_dict["SIDE"] = 6
    print("Вспомним детство, поиграем в ""Морской бой""?")
    print("По умолчанию играем на поле 6 * 6. При желании выйти из игры (и проиграть) можно ввести слово 'quit' "
    " вместо хода. В каждом флоте участвуют 6 кораблей:")
    print("- 1 корабль на 3 клетки\n- 2 корабля на 2 клетки\n- 4 корабля на 1 клетку")
    print("Итак, приступим. Для начала надо разместить корабли на поле боя. Для размещения вручную нажмите (1), "
            "для автоматического - (2). Или введите 'quit' для выхода из игры и проигрыша.")
    while True:
        reply = input(INP_INVITE).upper()
        if reply in ('QUIT', "ЙГШЕ"):
            print(f"Жаль, {gameplay_dict[HUMAN]}, до следующего раза!")
            exit()
        if reply in ('1', '2'):
            print(reply)
            # call function to place the ships manually or automatically
            break
        else:
            continue

    brd_computer = Board(gameplay_dict["COMPUTER_NAME"])
    brd_human = Board(gameplay_dict[HUMAN])
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
    ships = [sh1, sh2, sh3, sh4, sh5, sh6, sh7]
    ships2 = [sh11, sh12, sh13, sh14, sh15, sh16, sh17]
    brd_computer.display_ships = True
    place_ships(brd_computer, ships)
    place_ships(brd_human, ships2)
    # brd_computer.place_ships(ships)
    # brd_human.place_ships(ships2)
    # print(brd_computer)
    print_side_by_side(brd_computer.__repr__(), brd_human.__repr__(), divider="    |    ")

def place_ships(board, ships):
    while True:
        try:
            board.try_place_ships(ships)
        except exceptions.FailedToPlaceAllShips() as e:
            continue
        else:
            print("all ships have been successfully placed")
            break



# greeting()
# getPlayerMove()

# print(to_lines_by_limit(s1, 20))

# print(to_lines_by_limit(s1, 26))
# s2 = to_lines_by_limit(s2, 25)
# print(s2)
# print_side_by_side(to_lines_by_limit(s1, 26), to_lines_by_limit(s2, 26))

greeting()
initialize_game()