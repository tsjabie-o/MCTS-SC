from utils import Square

class Piece():
    def __init__(self, s, c):
        self.square: Square = s
        self.caps = c

class Queen(Piece):
    def __init__(self, s, c):
        super().__init__(s, c)
        self.type = 1
        self.rank = 9

    def valCap(self, p: Piece):
        if self == p or p.type == 1 or self.caps <= 0:
            return False
        s1 = self.square
        s2 = p.square
        return s1.alignVer(s2) or s1.alignHor(s2) or s1.alignDia1(s2) or s1.alignDia2(s2)
        
class Rook(Piece):
    def __init__(self, s, c):
        super().__init__(s, c)
        self.type = 2
        self.rank = 5

    def valCap(self, p: Piece):
        if self == p or p.type == 1 or self.caps <= 0:
            return False
        s1 = self.square
        s2 = p.square
        return s1.alignVer(s2) or s1.alignHor(s2)
    
class Bischop(Piece):
    def __init__(self, s, c):
        super().__init__(s, c)
        self.type = 3
        self.rank = 5

    def valCap(self, p: Piece):
        if self == p or p.type == 1 or self.caps <= 0:
            return False
        s1 = self.square
        s2 = p.square
        return s1.alignDia1(s2) or s1.alignDia2(s2)

class Knight(Piece):
    def __init__(self, s, c):
        super().__init__(s, c)
        self.type = 4
        self.rank = 3


    def ValidCapture(self, p):
        if self == p or p.type == 1 or self.caps <= 0:
            return False

        s1 = self.Square
        s2 = p.Square
        if (abs(s2.x - s1.x) == 1 and abs(s2.y - s1.y) == 2) or (abs(s2.x - s1.x) == 2 and abs(s2.y - s1.y) == 1):
            return True

        return False
    
class Pawn(Piece):
    def __init__(self, s, c):
        super().__init__(s, c)
        self.type = 5
        self.rank = 1

    def valCap(self, p):
        if self == p or p.type == 1 or self.caps <= 0:
            return False
        s1 = self.Square
        s2 = p.Square
        if s2.x == s1.x - 1 and s2.y == s1.y - 1:
            return True
        elif s2.x == s1.x + 1 and s2.y == s1.y - 1:
            return True
        


class King(Piece):
    def __init__(self, s, c):
        super().__init__(s, c)
        self.type = 6
        self.rank = 99

    def valCap(self, p: Piece):
        if self == p or p.type == 1 or self.caps <= 0:
            return False

        return abs(self.square.x - p.square.x) <= 1 and abs(self.square.y - p.square.y) <= 1