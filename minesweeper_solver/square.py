from enum import IntEnum, auto

class State(IntEnum):
    WHITE = auto()
    GRAY = auto()
    BLACK = auto()

class Square(object):
    """マインスイーパのマスの表現用"""
    def __init__(self, x, y, num=None):
        self.x = x
        self.y = y
        self.number = num
        self.state = State.BLACK if num == 9 else State.WHITE if num in [0, 1, 2, 3, 4, 5, 6, 7, 8] else State.GRAY

    def __str__(self):
        if self.state == State.BLACK:
            return '*'
        elif self.state == State.GRAY:
            return 'x'
        else:
            return str(self.number)

    def update_state(self):
        if self.number == 9:
            self.state = State.BLACK
        elif self.number in [0, 1, 2, 3, 4, 5, 6, 7, 8]:
            self.state = State.WHITE
        else:
            self.state = State.GRAY



