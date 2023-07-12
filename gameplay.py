import exceptions
import globals
from globals import to_lines_by_limit
from globals import print_side_by_side
from globals import INP_INVITE
from ship import Ship
from board import Board
from random import choice
from player import User, AI
from os import system


# CLEAR = "\x1B[H\x1B[J"

COMPUTER = "COMPUTER_NAME"
HUMAN = "HUMAN_NAME"
FIELD_SIZE = "FIELD_SIZE"
fleet_dict = {3: 1, 2: 3, 1: 3} #type of ship: ship count
ship_count = sum(fleet_dict.values())

gameplay_dict = {COMPUTER: "A.I. Computer", HUMAN: "human", FIELD_SIZE: 6}


def greeting():

    border = 20 * "="
    ship_list = ""
    for e in fleet_dict:
        ship_list += f"\n- {e} * {fleet_dict[e]}-палубных"
    ship_list = f"{border}\n{ship_list}\n{border}"
    print("Перед началом игры, представьтесь, пожалуйста:")
    gameplay_dict["HUMAN_NAME"] = input(INP_INVITE).capitalize()
    msg = (
        f"Привет, {gameplay_dict[HUMAN]}. Я - плод нескольких дней мучений "
        f"студента школы Skillfactory Александра Артамонова, "
        f"скрипт на Питоне, {gameplay_dict['COMPUTER_NAME']}"
    )
    print(to_lines_by_limit(msg))

    msg = "Вспомним детство, поиграем в " "Морской бой" "?\n"
    msg += (
        f"Играем на поле {gameplay_dict[FIELD_SIZE]} * {gameplay_dict[FIELD_SIZE]}. При желании выйти из игры (и проиграть) можно ввести 'q' "
        f"вместо хода. В каждом флоте участвуют {ship_count} кораблей:\n"
    )
    msg += f"{ship_list}\n"
    msg += "Итак, приступим. Для начала разместим корабли на поле боя. Поехали!\n"
    print(to_lines_by_limit(msg))


def populate_fleet(lst):
    for ele in fleet_dict:
        for i in range(fleet_dict[ele]):
            lst.append(Ship(ele, choice(["H", "V"])))


def gameplay():
    """Движок игры. Реализован в виде функции, а не класса, так как
    'simple is better than complex'"""

    brd_computer = Board(gameplay_dict[COMPUTER], gameplay_dict[FIELD_SIZE])
    brd_human = Board(gameplay_dict[HUMAN], gameplay_dict[FIELD_SIZE])
    ships_computer = []
    populate_fleet(ships_computer)
    ships_human = []
    populate_fleet(ships_human)

    try:
        place_ships(brd_computer, ships_computer)
        place_ships(brd_human, ships_human)
    except Exception as e:
        print(
            to_lines_by_limit(
                "Возникла непредвиденная ситуация: видимо, "
                "не удалось расставить корабли. Игра завершается."
            )
        )
        print(e)
        exit()
        # ships =
        # ships2 =

    # устанавливаем режим видимости кораблей
    brd_computer.display_ships = False
    brd_human.display_ships = True

    # выводим доски рядом
    print_side_by_side(str(brd_computer), str(brd_human))
    usr = User(brd_human, brd_computer, gameplay_dict[HUMAN])
    ai = AI(brd_computer, brd_human, gameplay_dict["COMPUTER_NAME"])

    msg = (
        "Чтобы определить, кто первый ходит, бросим жребий. "
        "Решка - 1, Орел - 2. Для выхода нажмите 'q'"
    )
    print(to_lines_by_limit(msg))
    ALLOWED_BETS = ("1", "2")
    while True:
        bet = input(INP_INVITE)
        if bet in ALLOWED_BETS:
            break
        elif bet in globals.QUIT:
            print(f"До следующего раза, {usr.name}")
            exit()
        else:
            print("Попробуйте еще")

    flip_coin = choice(ALLOWED_BETS)
    if bet == flip_coin:
        msg = "Угадали! Первый ход - ваш."
        current_player, next_player = usr, ai
    else:
        msg = "Не повезло. Первый ход - мой."
        current_player, next_player = ai, usr

    msg += "\nХоды обозначаются двумя цифрами подряд, например 12. Первая цифра - ряд, вторая - колонка.\n"
    print(to_lines_by_limit(msg))

    def get_message():
        return f"Ход №{move_number}\n{next_player.message}\n{current_player.message}"
    # обработка и смена ходов
    move_number = 0
    while current_player.their_board.has_ships_afloat:
        try:
            move_number += 1
            current_player.move()
            msg = get_message()
            # print(msg)
            while (
                current_player.just_killed_a_ship
                and current_player.their_board.has_ships_afloat
            ):
                system("clear")
                print_side_by_side(str(brd_computer), str(brd_human))
                print(msg)
                print(
                    f"Отличный выстрел, {current_player.name}! За это полагается бонусный ход!"
                )
                current_player.move()
                msg = get_message()
        except (exceptions.PointHitAlready, IndexError, ValueError) as e:
            print(e, " - try again!")
            continue
        except Exception as e:
            # При непредвиденной ошибке
            print(e)
            exit()
        else:
            current_player, next_player = next_player, current_player
            system("clear")
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
            msg = (
                f"Все корабли на доске игрока '{board.player}' "
                f"были успешно размещены случайным образом. Число попыток: {number_of_attempts}"
            )
            print(to_lines_by_limit(msg))
            break


def get_possible_coords():
    pass


def start_game():
    greeting()
    gameplay()
