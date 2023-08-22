import globals as g
div = '|'
inner =  []
side = 3
dct = {(x, y): g.UNKNOWN for x in range(side) for y in range(side)}
# print(dct)
dct = {(0, 0): '?', (0, 1): '?', (0, 2): '?', 
       (1, 0): '?', (2, 1): '?', (1, 2): '?', 
       (2, 0): '?', (1, 1): '?', (2, 2): '?'}


i = 0
for cell in sorted(dct.keys()):
    # print(cell, i)
    # inner.append(dct[cell])
    # print(cell[0] )
    if cell[0] == i:
        # print(cell[0], i)
        inner.append(dct[cell])
    else:
        print(i, div.join(inner))
        i += 1
        inner = [dct[cell]]

print(i, div.join(inner))
