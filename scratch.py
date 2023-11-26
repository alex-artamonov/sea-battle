from ship import Ship
from random import choice
import globals as g

s = Ship(3, front=(2, 3))
s2 = Ship(2, direction=g.VERT, front=(1, 3))


def predict_set(coords):
    # output = []
    # coords = ship.coords
    # print(coords)
    # coords = self.hits
    if len(coords) == 1:
        output = {
            (coords[0][0] - 1, coords[0][1]),
            (coords[0][0] + 1, coords[0][1]),
            (coords[0][0], coords[0][1] - 1),
            (coords[0][0], coords[0][1] + 1),
        }
    elif coords[0][0] == coords[-1][0]:
        output = {(coords[0][0], coords[0][1] - 1), (coords[-1][0], coords[-1][1] + 1)}
    else:
        output = {(coords[0][0] - 1, coords[0][1]), (coords[-1][0] + 1, coords[-1][1])}
    # output = set(output)
    return output


def get_direction(ship: Ship):
    coords = ship.coords
    # print(coords)
    if coords[0][0] == coords[-1][0]:
        return "H"
    else:
        return "V"


def add_buffer_diagonal(buffer_list, cell):
    buffer_list.extend(
        [
            (cell[0] - 1, cell[1] - 1),
            (cell[0] - 1, cell[1] + 1),
            (cell[0] + 1, cell[1] - 1),
            (cell[0] + 1, cell[1] + 1),
        ]
    )


def add_buffer_endcells(buffer_set, ship: list):
    if len(ship) == 1:
        buffer_set = buffer_set | {
            (ship[0][0], ship[0][1] - 1),
            (ship[0][0], ship[0][1] + 1),
            (ship[0][0] - 1, ship[0][1]),
            (ship[0][0] + 1, ship[0][1]),
        }
        print(buffer_set)
        return


s3 = Ship(1, front=(2, 2))

t1, t2, t3 = [(1, 3), (1, 2)], [(4, 2), (3, 2)], [(4, 4)]
# print(t1, predict_set(t1))
# print(t2, predict_set(t2))
# print(t3, predict_set(t3))

# print(s.coords, s.direction)
# # print(get_direction(s))
# print(predict_set(s.coords))
# print(s2.coords, s2.direction)
# # print(get_direction(s2))
# print(predict_set(s2.coords))
# print(s3.coords, s3.direction)
# # print(get_direction(s3))
# print(predict_set(s3.coords))
# buffer = []
# cell = (3, 3)
# add_buffer_diagonal(buffer, cell)
# print(buffer)
# buffer_set = set()
# print(buffer_set)
# add_buffer_endcells(buffer_set, t3)

# print(t3, buffer_set)


class Test_cheat:
    def __init__(self) -> None:
        self.cheat_move = self.cheat()

    def cheat(self):
        return (x for x in range(10))

    def cheating(self):
        print("cheating")
        return str(next(self.cheat_move))

    def no_cheat(self):
        # print('no cheat')
        return "no cheat"

    def rand_move(self):
        n = choice((1, 2))
        if n == 1:
            return self.cheating()
        else:
            return self.no_cheat()


tst = Test_cheat()
# tst.cheating()
# tst.cheating()
# tst.cheating()
# tst.no_cheat()
# for i in range(8):
#     print(tst.rand_move())


def one():
    return "first"


def two():
    return "second"


def rand():
    # result = choice((one, two))
    lst = [one, two]
    result = choice(lst)
    print(result())
    # print(two())


# rand()


class Test:
    common = 1

    def get_common(self):
        return self.common


t = Test()
# print(t.get_common())


class Player:
    memory = []

    def move(self, reply):
        # print(request)
        move = input("your move?\t")
        response = reply()
        self.memory.append((move, response))

    def get_memory(self):
        return self.memory


class Player:
    memory = {}

    def move(self):
        # print(request)
        move = input("your move?\t")
        self.memory[move] = None
        return move

    def write_response(self, move, response):
        self.memory[move] = response

    def get_memory(self):
        return self.memory


p = Player()

# question = input('Move?.\n')
def my_input(question=""):
    q = input(question)
    if q == "q":
        exit()
    return q


# while True:
#     res = p.move(my_input)
#     print('res:', res)
#     mem = p.get_memory()
#     print(mem)

#     if mem[-1][1] == 'q':
#         break
# while True:
#     move = p.move()
#     reply = input('Result?\t')
#     if reply == 'q':
#         break
#     p.write_response(move, reply)
# print(p.get_memory())


import globals as g

EMPTY = "o"
lst = [g.HIT, g.BUFFER, g.BODY]
from random import choice, sample

side = 6
cells = [list(EMPTY * side) for _ in range(side)]
# print(cells)
divider = "|"
output = ""
display_ships = True
for i, line in enumerate(cells):
    if display_ships:
        inner = ((cell if cell != g.BUFFER else EMPTY) for cell in line)
    else:
        inner = (
            (cell if cell != globals.BODY and cell != g.BUFFER else EMPTY)
            for cell in line
        )

    inner = divider.join(inner) + divider
    output += str(i + 1).rjust(2) + " " + inner + "\n"  # нумеруем строки с 1
# print(output)

# for i, line in enumerate(cells):
#     ln = '|'.join(line)
#     print(ln)
# for line in inner:
#     for ele in line:
#         print(ele)
side = 3
dct = {(x, y): g.UNKNOWN for x in range(side) for y in range(side)}
# print(dct)
dct = {(0, 0): 'B', (0, 1): '?', (0, 2): '?', 
       (1, 0): 'B', (2, 1): '?', (1, 2): '?', 
       (2, 0): '?', (1, 1): 'B', (2, 2): '?'}
# print(dct)
output = ""
# for x in range(side):
#     inner = (dct[(x, y)] if dct[(x, y)] != g.BUFFER else EMPTY for y in range(side))
#     inner = divider.join(inner) + divider
#     output += str(x + 1).rjust(2) + " " + inner + "\n"
# print(output)
# print(list(dct.keys()))
output = ''
i = 0
inner = []
even = []
odd = []
div = '|'
output = ''

# print(dct)

for cell in sorted(dct.keys()):
    # print(cell, i)
    # inner.append(dct[cell])
    # print(cell[0] )
    if cell[0] == i:
        inner.append(dct[cell]) 
    else:      
        # print(i, div.join(inner))
        # print(inner)
        inner = [dct[cell]]
        i +=1


# print(i, div.join(inner))
        
# print(odd)
        

# def to_lists(dct):
#     global side
#     output = []
#     for x in range(side):
#         output.append([dct[(x, y)] for y in range(side)])
#     return output

# lists = to_lists(dct)
# print(lists)
h,v = 'h', 'v'
from random import shuffle
lst = [h,v]
# print(lst)
# shuffle(lst)
# print(lst)
cells_list = sorted([key for key in dct.keys()])
# print(cells_list)
directions = ( g.VERT,)
# # for i in range(side):
# lines = {g.HORIZ:[], g.VERT: []}
# i = 0
# lst = []
# for cell in cells_list:
#     if cell[0] == i:
#         lst.append(cell)
#     else:
#         lines[g.HORIZ].append(lst)
#         i += 1
#         lst = [cell]
# lines[g.HORIZ].append(lst)
# # print(lines)

# j = 0
# lst = []
# for cell in cells_list:
#     if cell[1] == j:
#         lst.append(cell)
#     else:
#         lines[g.VERT].append(lst)
#         j += 1
#         lst = [cell]
# lines[g.VERT].append(lst)
# print(lines)
# lst = []

# for i, direction in enumerate(directions):
#     print(i, direction)
#     j = 0
#     lst = []
#     for cell in cells_list:
#         print(cell, cell[1])
#         if cell[1] == j:
#             lst.append(cell)
#         else:
#             lines[direction].append(lst)
#             j += 1
#             lst = [cell]
#     lines[direction].append(lst)
def build_lines_dict(side: int):
    '''buils a dictionary with matrices of coordinates of a square of a given side'''
    lines_dict = {g.HORIZ:[], g.VERT:[]}
    i, j = 0, 0
    lines = []
    for i in range(side):
        horiz = []
        vert = []
        for j in range(side):
            horiz.append((i,j))
            vert.append((j,i))
        lines.append(horiz)
        lines.append(vert)
        lines_dict[g.HORIZ].append(horiz)
        lines_dict[g.VERT].append(vert)
    return lines_dict
# lines[g.HORIZ] = horiz
# lines[g.VERT] = vert
# print(lines_dict)


def is_adjacent(cell1, cell2, direction):
    if direction == g.HORIZ:
        return cell1[0] == cell2[0] and abs(cell1[1] - cell2[1]) == 1 
    if direction == g.VERT:
        return cell1[1] == cell2[1] and abs(cell1[0] - cell2[0]) == 1 
    
    
# print(is_adjacent((1,0),(3,0) ))
# print(lines)
# # print(horiz)
# # print(vert)
# # print(lines)
# # print(dct)
# target = 3
# # print(dct)
dct = {(0, 0): 'V', (0, 1): '?', (0, 2): '?', (0, 3): '?',
       (1, 0): 'V', (1, 1): '?', (1, 2): '?', (1, 3): '?',
       (2, 0): '?', (2, 1): 'V', (2, 2): '?', (2, 3): '?',
       (3, 0): '?', (3, 1): '?', (3, 2): '?', (3, 3): '?',
       
       }
spaces = []
# for key in lines_dict:
    # print(lines_dict[key])
# print(dct)

lines_dict = build_lines_dict(4)
# print(lines_dict)

def is_line_continuous(line):
    '''determines if the list of cells has no gaps'''
    test = sorted(line.copy())
    # print(test)
    prev_cell = test[0]
    for i, cell in enumerate(test[1:]):
        # print(i, prev_cell, cell)
        if not (prev_cell[0] == cell[0] and abs(prev_cell[1] - cell[1]) == 1) \
        and \
        not (prev_cell[1] == cell[1] and abs(prev_cell[0] - cell[0]) == 1):
            return False
        prev_cell = cell
    return True
        


def find_spaces(dct, lines_dict, direction):
    ''''''
    spaces = []
    for lst in lines_dict[direction]:
        space = []
        prev_cell = lst[0]
        for cell in lst[1:]:
            if dct[prev_cell] != 'V' and \
                    dct[cell] != 'V' and \
                    is_adjacent(cell, prev_cell, direction):
                space.append(prev_cell)
                space.append(cell)
            prev_cell = cell
        if dct[prev_cell] != 'V' and \
                    dct[cell] != 'V' and \
                    is_adjacent(cell, prev_cell, direction):
            space.append(prev_cell)
            space.append(cell)
        spaces.append(list(set(space)))
    return spaces

length = 3






spaces = find_spaces(dct, lines_dict, g.HORIZ)

for i, lst in enumerate(spaces):
    spaces[i] = sorted(lst)
# print(spaces)
# [print(space) for space in spaces if len(space) >= length]
# print(spaces)
# spaces = find_spaces(dct, lines_dict, g.VERT)
# print(spaces)
# # print([(cell, dct[cell]) for line in lines_dict[g.HORIZ] for cell in line])

# [print(space) for space in spaces if len(space) == length]
target = 3
# spaces = [space in spaces if len(space) >= target else pass]
# print(spaces)
exact_spaces = []
# for space in spaces:
#     lst = []
#     if len(space) >= target:
#         for cell in range(target):
# line = [i for i in range(5)]
# print(line)
line = [(3, 0), (3, 1), (3, 2), (3, 3)]
for i, ele in enumerate(line):
    space = line[i:i + target]
    # print(space)
    if len(space) == target:
        exact_spaces.append(space)
           
# print(exact_spaces)
# for space in exact_spaces:
#     print(is_line_continuous(space))
    

side = 3
dct = build_lines_dict(side)
# print(dct)
# for direction in dct:
#     print(dct[direction])

from board import Board

brd = Board('xxxx', 4)
print(brd.rows)
print(brd.columns)
