from ship import Ship

s = Ship(3,front=(2,3))
s2 = Ship(2, direction='V', front=(1,3))


def predict_set(coords):
    # output = []
    # coords = ship.coords
    # print(coords)
        # coords = self.hits
    if len(coords) == 1:
        output = {(coords[0][0] - 1,coords[0][1]), 
                    (coords[0][0] + 1,coords[0][1]),
                    (coords[0][0], coords[0][1] - 1),
                    (coords[0][0], coords[0][1] + 1)}
    elif coords[0][0] == coords[-1][0]:
        output = {
                (coords[0][0], coords[0][1] - 1),
                (coords[-1][0], coords[-1][1] + 1)
                    }
    else:
        output = {
                (coords[0][0] - 1, coords[0][1]),
                (coords[-1][0] + 1, coords[-1][1])
                    }
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
    buffer_list.extend([
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
            (ship[0][0], ship[0][1] +1),
            (ship[0][0] - 1, ship[0][1]),
            (ship[0][0] + 1, ship[0][1]),
        }
        print(buffer_set)
        return
    
   

s3 = Ship(1,front=(2,2))

t1, t2, t3 = [(1,3), (1,2)], [(4,2), (3,2)], [(4,4)]
print(t1, predict_set(t1))
print(t2, predict_set(t2))
print(t3, predict_set(t3))

# print(s.coords, s.direction)
# # print(get_direction(s))
# print(predict_set(s.coords))
# print(s2.coords, s2.direction)
# # print(get_direction(s2))
# print(predict_set(s2.coords))
# print(s3.coords, s3.direction)
# # print(get_direction(s3))
# print(predict_set(s3.coords))
buffer = []
cell = (3,3)
add_buffer_diagonal(buffer, cell)
print(buffer)
buffer_set = set()
print(buffer_set)
add_buffer_endcells(buffer_set, t3)

print(t3, buffer_set)