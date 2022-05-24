# -*- coding: utf-8 -*-
from ship import Ship
from board import Board
from sys import exit
from itertools import zip_longest

INP_INVITE = "?--> "

sh = Ship(4, "H", (1, 1))


# print(sh)

def to_lines_by_limit(string, limit):
    """Разбивает сплошной текст на строки с указанным
    лимитом знаков, не разбивая конечные слова"""
    # for word in string.split():
    #     if len(word) > limit:
    #         raise ValueError(f"The word '{word}' is too long for the specified limit '{limit}'")
    output = ""
    while len(string) >= limit:
        temp = string[:limit]
        string = string[limit:]
        n = temp.rfind(' ')
        if n > 0:
            # print("temp:", temp)
            # raise ValueError(f"the limit is too short for the word '{temp}' and limit '{limit}'")

            head = temp[:n].lstrip()
            tail = temp[n:]
            string = tail + string

        elif n <= 0:
            raise ValueError(f"The limit '{limit}' is too small: the text can't be split")
        else:  # если пробел в начале строки
            head = temp.lstrip()
            print("from else:", head)
        output += head + "\n"
        # print(head, "\t", len(head))
    # print(s.lstrip())
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


def greeting():
    s = "Представьтесь, пожалуйста:"
    name = input(INP_INVITE)
    print("Привет,", name)


def get_player_move():
    while True:
        response = input(INP_INVITE).upper().strip()
        if response == "QUIT":
            print("Спасибо за игру!")
            exit()


# greeting()
# getPlayerMove()

# print(to_lines_by_limit(s1, 20))

# print(to_lines_by_limit(s1, 26))
# s2 = to_lines_by_limit(s2, 25)
# print(s2)
print_side_by_side(to_lines_by_limit(s1, 26), to_lines_by_limit(s2, 26))
