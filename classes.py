# EMPTY = 'О'
EMPTY = " "
BOX = '■'

class Board():
    def __init__(self, player, ships):
        self.cells = [list(EMPTY * 6) for _ in range(6)]
        self.player = player
        self.ships = ships
        for ship in self.ships:
            for cell in ship:
                coords = (cell[0][0], cell[0][1])
                self.cells[coords[0]][coords[1]] = BOX if cell[1] else EMPTY

        # place_ships()

    def add_ship(self, ship):
        for cell in ship:
            self.cells[cell[0]][cell[1]] = BOX
            
            
            
    def place_ships(self):
        for ship in self.ships:
            for cell in ship:
                self.cells[cell[0]][cell[1]] = BOX


    def __repr__(self):
        divider = " | "
        rng = range(1, 7)
        head = f"{self.player.center(25, '_')}\n    "
        head += "   ".join(str(i) for i in rng)
        head += "\n\n"
        s = ""
        for i, line in enumerate(self.cells):
            # s += str(i + 1) + "   " + divider.join(line) + "\n\n"
            s += f"{str(i + 1)}   {divider.join(line)}\n   {' -- ' * 6}\n"
            
            # s += divider.join(line)
            # s += "\n\n"
        s = head + s
        return s
        
    def fire(self, cell):
        pass

