from minesweeper_solver.square import Square
from collections import namedtuple

Size = namedtuple('Size', 'x, y')
class Field(object):
    """NxMマスのフィールドを表現する"""
    def __init__(self, n, m):
        self.size_x = n
        self.size_y = m
        self.field = [[Square(j, i) for i in range(n)] for j in range(m)]

    def __getitem__(self, i):
        return self.field[i]

    def __str__(self):
        line = ["".join(map(str, i)) for i in self.field]
        return '\n'.join(map(str, line))

    def get_size(self):
        return Size(self.size_x, self.size_y)

    def get_around(self, x, y):
        return Around(x, y, self.get_size(), self.field)


Center = namedtuple("Center", 'x y')
class Around(object):
    def __init__(self, x, y, size, field):
        self.center = Center(x, y)
        self.field = list(map(lambda li: li[max(0, x-1):min(x+2, size.x)], field[max(0, y-1):min(y+2, size.y)]))

    def __getitem__(self, i):
        return self.field[i]

    def __str__(self):
        line = ["".join(map(str, i)) for i in self.field]
        return '\n'.join(map(str, line))
