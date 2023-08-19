from ship import Ship
from random import choice

s = Ship(3, front=(2, 3))
s2 = Ship(2, direction="V", front=(1, 3))


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
print(t.get_common())

class Player:
    memory = []
    def move(self, reply):
        # print(request)
        move = input('your move?\t')
        response = reply()
        self.memory.append((move, response))
    def get_memory(self):
        return self.memory


class Player:
    memory = {}
    def move(self):
        # print(request)
        move = input('your move?\t')
        self.memory[move] = None
        return move
    def write_response(self, move, response):
        self.memory[move] = response

    def get_memory(self):
        return self.memory



p = Player()

# question = input('Move?.\n')
def my_input(question=''):
    q = input(question)
    if q == 'q':
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
EMPTY = 'o'
lst = [g.HIT, g.BUFFER, g.BODY]
from random import choice, sample

side = 6
cells = [list(EMPTY * side) for _ in range(side)]
print(cells)
divider = '|'
output = ''
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
dct = {(x,y): 'o' for x in range(side) for y in range(side)}
print(dct)
output = ''
for x in range(side):
    inner = (dct[(x, y)] if dct[(x, y)] != g.BUFFER else EMPTY for y in range(side))
    inner = divider.join(inner) + divider
    output += str(x + 1).rjust(2) + " " + inner + "\n"
print(output)
# def to_lists(dct):
#     global side
#     output = []
#     for x in range(side):
#         output.append([dct[(x, y)] for y in range(side)])
#     return output

# lists = to_lists(dct)
# print(lists)