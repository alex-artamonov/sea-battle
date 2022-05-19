class PointHitAlready(Exception):
    """Raised when the point has been already hit
    Attributes:
        point - - input point which caused the error
        message - - explanation of the error"""

    def __init__(self, point, message="Эта точка уже обстрелена!"):
        self.message = f"Точка <{point}> уже обстрелена!"
        self.point = point
        super().__init__(self.message)


class PointUsedAlready(Exception):
    """Raised when the point has been already taken
    Attributes:
        point - - input point which caused the error
        message - - explanation of the error"""

    def __init__(self, point, message="Эта точка занята!"):
        self.message = f"Точка <{point}> уже занята!"
        self.point = point
        super().__init__(self.message)

class OutOfBoard(Exception):
    """Raised when the point is beyond the board
    Attributes:
        point - - input point which caused the error
        message - - explanation of the error"""

    def __init__(self, point, message="Эта точка занята!"):
        self.message = f"Точка <{point}> находится вне игрового поля!"
        self.point = point
        super().__init__(self.message)