from minesweeper_solver.square import Square
from minesweeper_solver.square import State
from minesweeper_solver.square import Pos
from collections import namedtuple

Size = namedtuple('Size', 'x, y')
class Field(object):
    """NxMマスのフィールドを表現する"""
    def __init__(self, n, m):
        self.size_x = n
        self.size_y = m
        self.field = [[Square(i, j) for i in range(n)] for j in range(m)]

    def __getitem__(self, i):
        return self.field[i]

    def __str__(self):
        line = ["".join(map(str, i)) for i in self.field]
        return '\n'.join(map(str, line))

    def get_size(self):
        return Size(self.size_x, self.size_y)

    def get_around(self, pos):
        return Around(pos, self.get_size(), self.field)


class Around(object):
    def __init__(self, pos, size, field):
        self.center = pos
        self.field = list(map(lambda li: li[max(0, pos.x-1):min(pos.x+2, size.x)], field[max(0, pos.y-1):min(pos.y+2, size.y)]))
        self.number_count = self.count(State.NUMBER)
        self.gray_count = self.count(State.GRAY)
        self.mine_count = self.count(State.MINE)

    def __getitem__(self, i):
        return self.field[i]

    def __str__(self):
        line = ["".join(map(str, i)) for i in self.field]
        return '\n'.join(map(str, line))

    def count(self, state):
        cnt = 0
        for line in self.field:
            for square in line:
                if square.pos == self.center:
                    continue

                if square.state == state:
                    cnt += 1
        return cnt

    def get_square_pos(self, state):
        squares = []
        for line in self.field:
            for square in line:
                if square.pos == self.center:
                    continue

                if square.state == state:
                    squares.append(square.pos)

        return squares
