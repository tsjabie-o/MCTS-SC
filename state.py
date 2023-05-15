from pieces import *

class State():
    def __init__(self, ps: set[Piece], square: dict, caps: dict):
        self.ps = ps
        self.square = square
        self.caps = caps

    def nextState(self, p1: Piece, p2: Piece):
        # p2 removed from set of pieces
        ps2 = self.ps.copy()
        ps2.remove(p2)

        # value of p1 takes over value of p2 in square, p2 removed
        square2 = self.square.copy()
        square2[p1] = square2[p2]
        square2.pop(p2)

        # value of p1 in caps decremented by one, p2 removed
        caps2 = self.caps.copy()
        caps2[p1] -= 1
        caps2.pop(p2)

        s2 = State(ps2, square2, caps2)
        return s2
