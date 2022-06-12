import exceptions
import globals
from globals import to_lines_by_limit
from globals import print_side_by_side
from globals import INP_INVITE
from ship import Ship
from board import Board
from random import choice
from player import User, AI


# CLEAR = "\x1B[H\x1B[J"


HUMAN = "HUMAN_NAME"
gameplay_dict = {"COMPUTER_NAME": "A.I. Computer",
                 HUMAN: 'human',
                 "SIDE": 6}


def greeting():
    print("Представьтесь, пожалуйста:")
    gameplay_dict["HUMAN_NAME"] = input(INP_INVITE).capitalize()
    msg = f"Привет, {gameplay_dict['HUMAN_NAME']}. Я - плод нескольких дней мучений " \
        f"студента школы Skillfactory Александра Артамонова, " \
        f"скрипт на Питоне, {gameplay_dict['COMPUTER_NAME']}"
    print(to_lines_by_limit(msg))

    msg = "Вспомним детство, поиграем в ""Морской бой""?\n"
    msg += "Играем на поле 6 * 6. При желании выйти из игры (и проиграть) можно ввести 'q' " \
           "вместо хода. В каждом флоте участвуют 7 кораблей:\n"
    msg += "- 1 корабль на 3 клетки\n- 2 корабля на 2 клетки\n- 4 корабля на 1 клетку\n"
    msg += "Итак, приступим. Для начала разместим корабли на поле боя. Поехали!\n"
    print(to_lines_by_limit(msg))


def gameplay():
    """Движок игры. Реализовал в виде функции, а не класса, так как
    'simple is better than complex'  """

    brd_computer = Board(gameplay_dict["COMPUTER_NAME"])
    brd_human = Board(gameplay_dict[HUMAN])
    try:
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
    except Exception as e:
        print(to_lines_by_limit("Возникла непредвиденная ситуация: видимо, "
                                "не удалось расставить корабли. Игра завершается."))
        print(e)
        exit()
    else:
        # ships =
        # ships2 =
        place_ships(brd_computer, [sh1, sh2, sh3, sh4, sh5, sh6, sh7])
        place_ships(brd_human, [sh11, sh12, sh13, sh14, sh15, sh16, sh17])

    # устанавливаем режим видимости кораблей
    brd_computer.display_ships = False
    brd_human.display_ships = True

    # выводим доски рядом
    print_side_by_side(str(brd_computer), str(brd_human))
    usr = User(brd_human, brd_computer, gameplay_dict[HUMAN])
    ai = AI(brd_computer, brd_human, gameplay_dict["COMPUTER_NAME"])

    msg = "Чтобы определить, кто первый ходит, бросим жребий. " \
          "Решка - 1, Орел - 2. Для выхода нажмите 'q'"
    print(to_lines_by_limit(msg))
    while True:
        bet = input(INP_INVITE)
        if bet in ('1', '2'):
            break
        elif bet in globals.QUIT:
            print(f"До следующего раза, {usr.name}")
            exit()
        else:
            print("Попробуйте еще")

    flip_coin = choice(('1', '2'))
    if bet == flip_coin:
        msg = "Угадали! Первый ход - ваш."
        current_player, next_player = usr, ai
    else:
        msg = "Не повезло. Первый ход - мой."
        current_player, next_player = ai, usr

    msg += "\nХоды обозначаются двумя цифрами подряд, например 12. Первая цифра - ряд, вторая - колонка.\n"
    print(to_lines_by_limit(msg))

    # обработка и смена ходов
    move_number = 0
    while current_player.their_board.has_ships_afloat:
        try:
            move_number += 1
            msg = current_player.move()
            # print(msg)
            while current_player.just_killed_a_ship and current_player.their_board.has_ships_afloat:
                print_side_by_side(str(brd_computer), str(brd_human))
                print(msg)
                print(f"Отличный выстрел, {current_player.name}! За это полагается бонусный ход!")
                msg = current_player.move()
        except (exceptions.PointHitAlready, IndexError, ValueError) as e:
            print(e, ' - try again!')
            continue
        except Exception as e:
            # При непредвиденной ошибке
            print(e)
            exit()
        else:
            current_player, next_player = next_player, current_player
            print_side_by_side(str(brd_computer), str(brd_human))
            print(msg)
    print(f"Победу одержал {current_player.name}")


def place_ships(board, ships):
    """Обертка для размещения кораблей на игровом поле"""

    number_of_attempts = 0
    while True:
        try:
            number_of_attempts += 1
            board.try_place_ships(ships)
        except (exceptions.FailedToPlaceAllShips, exceptions.NoVacantCells) as e:
            print(e)
            board.clear()
            continue
        except exceptions.PointUsedAlready as e:
            print(e)
            continue
        except Exception as e:
            print("Возникла неожиданная ситуация. Игра завершается")
            print(e)
            exit()
        else:
            msg = f"Все корабли на доске игрока '{board.player}' " \
                  f"были успешно размещены случайным образом. Число попыток: {number_of_attempts}"
            print(to_lines_by_limit(msg))
            break


def start_game():
    greeting()
    gameplay()
