from globals import ai_to_user
class PointHitAlready(Exception):
    """Raised when the point has been already hit
    Attributes:
        point - - input point which caused the error
        message - - explanation of the error"""

    def __init__(self, point):
        self.message = f"Точка {point} уже обстрелена!"
        self.point = point
        super().__init__(self.message)

class NoVacantCells(Exception):
    """Raised when there are no vacant cells to place a ship
        Attributes:
            message - - explanation of the error"""
    def __init__(self, msg="Нет свободного места для размещения следующего корабля!"):
        self.message = msg
        super().__init__(self.message)
class TooManyAttempts(Exception):
    """Raised when there have been too many attampts to place a ship
        Attributes:
            message - - explanation of the error"""
    def __init__(self, attempts, message=f"Превышено количество попыток для размещения корабля"):
        self.message = message + f": ({attempts})"
        super().__init__(self.message)

class FailedToPlaceAllShips(Exception):
    """Raised when some ships have been left unplaced
    Attributes:
        message - - explanation of the error"""

    def __init__(self, message="Не удалось разместить все корабли"):
        self.message = message
        super().__init__(self.message)



class PointUsedAlready(Exception):
    """Raised when the point has been already taken
    Attributes:
        point - - input point which caused the error
        message - - explanation of the error"""

    def __init__(self, points, message="Эта точка занята!"):
        self.message = f"Координаты {ai_to_user(points)} уже заняты!"
        super().__init__(self.message)

class OutOfBoard(Exception):
    """Raised when the point is beyond the board
    Attributes:
        point - - input point which caused the error
        message - - explanation of the error"""

    def __init__(self, point, length):
        self.message = f"Координаты {point} выводят корабль длины {length} из игрового поля!"
        super().__init__(self.message)