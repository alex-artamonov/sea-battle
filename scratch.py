from ship import Ship

s = Ship(3,front=(2,3))
s2 = Ship(2, direction='V', front=(1,3))


def predict_set(ship: Ship):
    # output = []
    coords = ship.coords
    # print(coords)
    if ship.len == 1:
        output = {(coords[0][1] - 1,coords[0][1]), 
                       (coords[0][1] + 1,coords[0][1]),
                       (coords[0][1], coords[0][1] - 1),
                       (coords[0][1], coords[0][1] + 1)}
    elif get_direction(ship) == "H":
        output = {
                (coords[0][0], coords[0][1] - 1),
                (coords[-1][0], coords[-1][1] + 1)
                    }
    elif get_direction(ship) == "V":
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
    

s3 = Ship(1,front=(2,2))


print(s.coords, s.direction)
print(get_direction(s))
print(predict_set(s))
print(s2.coords, s2.direction)
print(get_direction(s2))
print(predict_set(s2))
print(s3.coords, s3.direction)
print(get_direction(s3))
print(predict_set(s3))