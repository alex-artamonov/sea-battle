from classes import Ship, Board
from random import choice

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



# ships = [[(0, 0, True), (1, 0, True), (2, 0, True)], [(3,2, False), (3,3, False)], [(0,3, False), (1,3, False)], [(1,5, False)], [(5,0, False)]]

# ships = [[[(0,1), True], [(1,1), True], [(2,1), True] ]]

brd1 = Board("computer", ships)
# brd1.display_ships = False
#
brd1.cells[0][2] = MISS
brd1.cells[0][1] = HIT
brd1.cells[4][3] = HIT
# brd1.add_ship([(0, 0), (1, 0), (2, 0)])
# print(brd1.to_str())
# brd1.add_ship([(3,2), (3,3)])
# print(brd1)
# [print(cell) for cell in brd1.cells]
lst = ((i, j) for i in range(6) for j in range(6))
point = tuple("fd t".split())
# print(point in lst)
# print(brd1)
# print(brd1.cells)


#
sh = Ship(4, choice(["V", "H"]))
sh1 = Ship(4, choice(["V", "H"]))
# sh.front = (2,3)
# print(sh)
# sh.body[1] = HIT
# sh.body[2] = HIT
# sh.body[0] = HIT
# print(sh)
# print(dir(sh))
# print(brd1)
print("brd1.place_ship(sh)", brd1.place_ship_sets(sh))
print(brd1.cells, brd1.coords, brd1.coords_set )
print(brd1)
print("brd1.occupied:\t\t", brd1.occupied)
print("brd1.occupied_set:\t", brd1.occupied_set())
#==================
# ls = ["s g a d".split(), "s g d".split(), "a b c d".split(), "b a c a".split()]
# print(ls)
# ls =  brd1.cells
# set1 = {(4, 1), (3, 15)}
# set2 = brd1.coords_set
# print("set1 & set2:", set1 & set2)
print("brd1.place_ship(sh1)", brd1.place_ship_sets(sh1))
print(brd1.cells, brd1.coords, brd1.coords_set )
print(brd1)
print("brd1.occupied:\t\t", brd1.occupied)
print("brd1.occupied_set:\t", brd1.occupied_set())
# target = []
# for i, elem in enumerate(ls):
#     target += [(e, i, j) for j, e in enumerate(elem) if e in ('‡', '-')]
# print(target)