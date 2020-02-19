class Field(object):
    """NxMマスのフィールドを表現する"""
    def __init__(self, n, m):
        self.field = [[Square(j, i) for i in range(n)] for j in range(m)]

