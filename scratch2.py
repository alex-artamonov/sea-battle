import globals as g
from board import Board

div = '|'
inner =  []
side = 3
dct = {(x, y): g.UNKNOWN for x in range(side) for y in range(side)}
# print(dct)
dct = {(0, 0): '?', (0, 1): '?', (0, 2): '?', 
       (1, 0): '?', (2, 1): 'X', (1, 2): '?', 
       (2, 0): '?', (1, 1): '?', (2, 2): '?'}


i = 0
# for cell in sorted(dct.keys()):
#     # print(cell, i)
#     # inner.append(dct[cell])
#     # print(cell[0] )
#     if cell[0] == i:
#         # print(cell[0], i)
#         inner.append(dct[cell])
#     else:
#         print(i, div.join(inner))
#         i += 1
#         inner = [dct[cell]]

# print(i, div.join(inner))

def options(dct: dict, n: int):
    output = []
    lst = sorted(dct.keys())
    if n > len(lst):
        return output
    for i in range(len(lst) - n + 1):
        output.append(lst[i:n + i])
    return output

# print(options('abcde', 1))


dct = {(0, 0): '?', (0, 1): '?', (0, 2): '?', 
       (1, 0): '?', (2, 1): 'X', (1, 2): '?', 
       (2, 0): '?', (1, 1): '?', (2, 2): '?'}
print(sorted(dct))

dct2 = {i:dct[i] for i in sorted(dct)}
# print(dct2)
brd = Board('xxx', sample=dct2)
print(brd)
# print(len(dct2))
# for line in brd.rows:
#     print([c for c in line.values()])
# # print(brd.columns)
# for line in brd.columns:
#     print([c for c in line.values()])

ship = 'X?'

lines_list = brd.rows + brd.columns
# print(lines_list)
output = []
for ele in lines_list:
#     s = ''.join(s for s in ele.values())
    lines = options(ele, len(ship))
    for line in lines:
        s = ''.join(ele[cell] for cell in line)
        # print(s, line)        
        if ship in s:
            output.append(line)

print(ship, len(output))
print(output)
# print(len(output))
# for ele in brd.rows:
#     print(options(ele, 4))