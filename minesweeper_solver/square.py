from enum import IntEnum, auto


class State(IntEnum):
    NUMBER = auto()
    GRAY = auto()
    MINE = auto()
    WALL = auto()


class Color(IntEnum):
    WHITE = auto()
    GRAY = auto()
    BLACK = auto()


class Square(object):
    """マインスイーパのマスの表現用"""
    def __init__(self, x, y, num=None):
        self.x = x
        self.y = y
        self.number = num
        self.state = State.MINE if num == 9 else State.WALL if num == -1 else State.NUMBER if num is not None else State.GRAY
        self.color = Color.GRAY

    def __str__(self):
        if self.state == State.MINE:
            return '*'
        elif self.state == State.GRAY:
            return '?'
        elif self.state == State.WALL:
            return 'x'
        else:
            return str(self.number)

    def update_state(self):
        if self.number == 9:
            self.state = State.MINE
        elif self.number == -1:
            self.state = State.WALL
        elif self.number is not None:
            self.state = State.NUMBER
        else:
            self.state = State.GRAY



