from pieces import Piece
from utils import Square, Utils
from state import State
import random as rd

class Generator():
    """
    Generates starting states based on certain preconditions
    """
    def getPuzzle(self, n):
        while True:
            s0 = self.generate(n)
            if s0 is not None:
                return s0
            
    def generate(self, n):
        # Initializing the state info
        square = dict()
        qs = set()
        ps = set()
        caps = dict()

        # Adding the king
        k = Piece("K")
        s = Square(rd.choice([i for i in range(8)]), rd.choice([i for i in range(8)]))

        ps.add(k)
        qs.add(s)
        caps[k] = 2
        square[k] = s
        
        # debug
        # Utils.visualizeState(State(square))
        # print()


        for i in range(n-1):
            # starting with pieces with captures left
            pte = [p for p in ps if caps[p] > 0]
            
            # checking per piece whether expansion possible
            pte = {p: sqrs for p in pte if len(sqrs := self.getExpansions(p, square, qs)) > 0}
            
            # got stuck
            if len(pte) == 0: return None


            # choose a random piece from this list and a random reachable square
            p = rd.choice(list(pte.keys()))
            s = rd.choice(pte[p])

            # perform expansion with p, s
            self.expand(p, s, ps, qs, caps, square)

            # debug
            # Utils.visualizeState(State(square))
            # print()

        s0 = State(square, center = square[k])
        return s0

    def expand(self, p, s, ps, qs, caps, square):
        # make a new piece and place it on p's square
        p2 = Piece(rd.choice(["Q", "R", "B", "N", "P"]))
        caps[p2] = 2
        square[p2] = square[p]
        ps.add(p2)

        # move p square to s
        square[p] = s
        qs.add(s)
        caps[p] -= 1

    def getExpansions(self, p: Piece, square, qs):
        sqrs = Utils.possMovements(p, square[p], qs)
        return sqrs