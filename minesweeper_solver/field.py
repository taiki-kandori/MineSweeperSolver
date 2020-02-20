from minesweeper_solver.square import Square

class Field(object):
    """NxMマスのフィールドを表現する"""
    def __init__(self, n, m):
        self.field = [[Square(j, i) for i in range(n)] for j in range(m)]

    def __getitem__(self, i):
        return self.field[i]

    def __str__(self):
        line = ["".join(map(str, i)) for i in self.field]
        return '\n'.join(map(str, line))

