from pieces import Piece
from utils import Square
import random as rd

class Generator():
    """
    Generates starting states based on certain preconditions
    """
    def __init__(self) -> None:
        pass

    def generate(self, n, c):
        # Initializing the state info
        square = dict()
        ps = set()
        caps = dict()

        # Adding the king
        k = Piece("K")
        ps.add(k)
        caps[k] = c
        square[k] = Square(rd.choice([i for i in range(9)]), rd.choice(i for i in range(9)))

        for i in range(n-1):
            # starting with pieces with captures left
            pte = [p for p in ps if caps[p] > 0]
            if len(pte) == 0: return False
            
            # checking per piece whether expansion possible
            pte = {p: sqrs for p in pte if len(sqrs := self.getExpansions(p, square)) > 0}

            # choose a random piece from this list and a random reachable square
            p = rd.choice(list(pte.keys()))
            s = rd.choice(pte[p])

            # perform expansion with p, s
            self.expand(p, s)



    def expand(self, p, s):
        pass

    def getExpansions(self, p: Piece, square, ps):
        sqrs = list()
        # piece-type specific moves
        x = square[p].x
        y = square[p].y
        match p.type:
            case 1:
                # Queen
                dirs = [(i,j) for i in [-1,0,1] for j in [-1,0,1] if not i == 0 == j]
                sqrs = [Square(x + a*i, y + a*j) for (i,j) in dirs for a in range(1,9)]
            case 2:
                # Rook
                dirs = [(i,j) for i in [-1,0,1] for j in [-1,0,1] if (i == 0) != (j == 0)]
                sqrs = [Square(x + a*i, y + a*j) for (i,j) in dirs for a in range(1,9)]
            case 3:
                # Bischop
                dirs = [(i,j) for i in [-1,1] for j in [-1,1]]
                sqrs = [Square(x + a*i, y + a*j) for (i,j) in dirs for a in range(1,9)]
            case 4:
                # Knight
                steps = [-2, -1, 1, 2]
                sqrs = [Square(x + i, y + j) for i in steps for j in steps if abs(i) != abs(j)]
            case 5:
                # Pawn
                sqrs = [Square(x + i, y + 1) for i in [-1,1]]
            case 6:
                # King
                sqrs = [Square(x + i, y + j) for i in [-1,0,1] for j in [-1,0,1] if not i == 0 == j]
        
        # remove squares outside board
        sqrs = [s for s in sqrs if 0 <= s.x <= 8 and 0 <= s.y <= 8]

        # remove occupied sqaures
        sqrs = [s for s in sqrs if square[p] != s for p in ps]
        return sqrs