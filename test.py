

EMPTY = 'О'
BOX = '■'
HIT = "‡"
MISS = "-"

# log(INFO, "I am in the weird function and a is", a, "and b is", b, "but I got a null C — using default", default_c)

def display_board(player):
    divider = " | "
    rng = range(1, 7)
    head = f"{player}\n    "
    head += "   ".join(str(i) for i in rng)
    head += "\n\n"
    # print()
    s = ""
    for j in rng:
        # s += str(j) + divider + divider.join(EMPTY * 6) + "\n\n"
        s += f"{str(j)}   {divider.join(EMPTY * 6)}\n\n"
    return head + s.strip()




# print(display_board())


s1 = """
fdsfds

sdf
hk
fds
"""

s2 = """
kl;'

fdsasdf

dsfsda;
fds
"""

# print(s1,s2)

def print_side_by_side(str1, str2, divider = "    |    "):
    s1 = str1.split('\n')
    s2 = str2.split('\n')

    lst = [len(elem) for elem in s1]
    nbr_spaced = max(lst)


    for line1, line2 in zip(s1, s2):
        print(line1.ljust(nbr_spaced) + divider + line2)

s1, s2 = display_board("human:\n".center(25)), display_board("computer:\n".center(25))

# print_side_by_side(s1, s2)

s = "asdfdsa"
# print(s.center(25))


# class Ship(lst):
#     def __init__(self):
#         self.body = lst

#
# fld = [list(EMPTY * 6) for _ in range(6)]
# [print(line) for line in fld]

from classes import Board

# ships = [[(0, 0, True), (1, 0, True), (2, 0, True)], [(3,2, False), (3,3, False)], [(0,3, False), (1,3, False)], [(1,5, False)], [(5,0, False)]]

ships = [[[(0,1), True], [(1,1), True]]]

brd1 = Board("computer", ships)
# brd1.display_ships = False
#
brd1.cells[0][2] = MISS
brd1.cells[0][1] = HIT
# brd1.add_ship([(0, 0), (1, 0), (2, 0)])
# print(brd1.to_str())
# brd1.add_ship([(3,2), (3,3)])
# print(brd1)
# [print(cell) for cell in brd1.cells]
print(brd1)