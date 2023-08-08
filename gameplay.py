import exceptions
import globals as g
from ship import Ship
from board import Board
from random import choice
from player import User, AI
from os import system
import getpass as gp


# CLEAR = "\x1B[H\x1B[J"
score = {}
COMPUTER = "COMPUTER_NAME"
HUMAN = "HUMAN_NAME"
FIELD_SIZE = "FIELD_SIZE"
fleet_dict = {3: 1, 2: 3, 1: 3}  # type of ship: ship count
fleet_dict = {2: 1, 1: 2}  # type of ship: ship count
ship_count = sum(fleet_dict.values())
last_time_began = None
gameplay_dict = {COMPUTER: "Computer", HUMAN: "human", FIELD_SIZE: 4}


def greeting():

    border = 20 * "="
    ship_list = ""
    for e in fleet_dict:
        ship_list += f"\n- {e} * {fleet_dict[e]}-палубных"
    ship_list = f"{border}\n{ship_list}\n{border}"
    # print("Перед началом игры, представьтесь, пожалуйста:")
    # gameplay_dict["HUMAN_NAME"] = input(g.INP_INVITE).capitalize()
    gameplay_dict[HUMAN] = gp.getuser().capitalize()
    msg = (
        f"Привет, {gameplay_dict[HUMAN]}. Я - плод нескольких дней мучений "
        f"студента школы Skillfactory Александра Артамонова, "
        f"скрипт на Питоне, {gameplay_dict['COMPUTER_NAME']}"
    )
    print(g.to_lines_by_limit(msg))

    msg = "Вспомним детство, поиграем в " "Морской бой" "?\n"
    msg += (
        f"Играем на поле {gameplay_dict[FIELD_SIZE]} * {gameplay_dict[FIELD_SIZE]}. При желании выйти из игры (и проиграть) можно ввести 'q' "
        f"вместо хода. В каждом флоте участвуют {ship_count} кораблей:\n"
    )
    msg += f"{ship_list}\n"
    msg += "Итак, приступим. Для начала разместим корабли на поле боя. Поехали!\n"
    print(g.to_lines_by_limit(msg))


def populate_fleet(lst):
    for ele in fleet_dict:
        for i in range(fleet_dict[ele]):
            lst.append(Ship(ele, choice(["H", "V"])))


def who_first(usr, ai):
    # if sum(score.values()) == 0:
    global last_time_began
    if not last_time_began:
        print("First round!")
        msg = (
            "Чтобы определить, кто первый ходит, бросим жребий. "
            "Решка - 1, Орел - 2. Для выхода нажмите 'q'"
        )
        print(g.to_lines_by_limit(msg))
        ALLOWED_BETS = ("1", "2")
        flip_coin = choice(ALLOWED_BETS)
        while True:
            bet = input(g.INP_INVITE)
            if bet in ALLOWED_BETS:
                break
            elif bet in g.QUIT:
                print(f"До следующего раза, {usr.name}")
                exit()
            else:
                print("Попробуйте еще")
        if bet == flip_coin:
            last_time_began = usr
            msg = "Угадали! Первый ход - ваш."
            return usr, ai, msg
        else:
            last_time_began = ai
            msg = "Не повезло. Первый ход - мой."
            return ai, usr, msg
    else:
        print(f"Next round! Last time began {last_time_began.name}")
        print(f"This time should begin the other player")
        if last_time_began.name == gameplay_dict[COMPUTER]:
            last_time_began = usr
            return usr, ai, f"Теперь ваша очередь делать первый ход, {usr.name}."
        else:
            last_time_began = ai
            return ai, usr, f"На этот раз первый ход мой."


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
            g.to_lines_by_limit(
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
    
    g.print_side_by_side(str(brd_computer), str(brd_human))
    # usr = User(brd_human, brd_computer, gameplay_dict[HUMAN])
    usr = User(brd_human, brd_computer, gameplay_dict[HUMAN])
    ai = AI(brd_computer, brd_human, gameplay_dict["COMPUTER_NAME"])

    current_player, next_player, msg = who_first(usr, ai)

    msg += "\nХоды обозначаются двумя цифрами подряд, например 12. Первая цифра - ряд, вторая - колонка.\n"
    print(g.to_lines_by_limit(msg))

    def get_message():
        return f"Ход №{move_number}\n{next_player.message}\n{current_player.message}"

    # обработка и смена ходов
    move_number = 0
    endgame = False
    while current_player.their_board.has_ships_afloat:
        if endgame:
            current_player = next_player
            break
        try:
            move_number += 1
            current_player.move()
            msg = get_message()
            # print(msg)
            while (
                current_player.just_killed_a_ship
                # and current_player.their_board.has_ships_afloat
            ):
                if not current_player.their_board.has_ships_afloat:
                    # print('supposed to be the end of game')
                    # endgame = True
                    # break
                    print(f"Победу одержал {current_player.name}:")
                    g.print_side_by_side(str(brd_computer), str(brd_human))
                    update_score(current_player.name)
                    print_score()
                    # exit()
                    return
                # system("clear")
                g.print_side_by_side(str(brd_computer), str(brd_human))
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
            # system("clear")
            g.print_side_by_side(str(brd_computer), str(brd_human))
            print(msg)
    # print(f"Победу одержал {current_player.name}")


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
            print(g.to_lines_by_limit(msg))
            break


# def get_possible_coords():
#     pass


def create_score():
    """Creates the score"""
    
    global gameplay_dict
    global score
    score[gameplay_dict[HUMAN]], score[gameplay_dict[COMPUTER]] = 0, 0


def update_score(winner: str):
    """Updates the score"""
    global score
    score[winner] += 1


def shift_right(text, n=2):
    s = ""
    ls = text.splitlines(True)
    for line in ls:
        s += " " * n + str(line)
    return s


def print_score():
    """Prints the score"""

    computer_name = gameplay_dict[COMPUTER]
    human_name = gameplay_dict[HUMAN]
    max_len = max(len(computer_name), len(human_name))
    fillnbr = 4
    computer_name, human_name = computer_name.center(max_len), human_name.center(
        max_len
    )
    head = (
        "|"
        + computer_name.center(max_len + fillnbr)
        + "|"
        + human_name.center(max_len + fillnbr)
        + "|"
    )
    s_border = "=" * len(head)
    numbers = "|" + str(score[gameplay_dict[COMPUTER]]).center(max_len + fillnbr)
    numbers += "|" + str(score[gameplay_dict[HUMAN]]).center(max_len + fillnbr) + "|"
    lst = [s_border, head, numbers, s_border]
    s = "\n".join(lst)
    s = shift_right(s, 5)
    print(s)


def play_again_or_leave():
    """Gives a choice to the user to continue or quit."""
    human_name = gameplay_dict[HUMAN]
    print("Сыграем еще? (Y/n)")
    reply = input(g.INP_INVITE).upper().strip()
    yes = reply in ("Y", "")
    if yes:
        print("Отлично, следующая игра!")
        gameplay()
    else:
        print(f"Ну ладно, пока, {human_name}!")
        exit()


def start_game():
    system("clear")
    greeting()
    create_score()
    print_score()
    gameplay()
    while True:
        play_again_or_leave()
