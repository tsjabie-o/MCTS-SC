from pieces import *

class State():
    def __init__(self, ps: set[Piece], square: dict, caps: dict):
        self.ps = ps
        self.square = square
        self.caps = caps

    def getActions(self):
        actions = []
        for p1 in self.ps:
            for p2 in self.ps:
                if self.valCap(p1, p2):
                    actions.append((p1, p2))

    def transition(self):
        actions = self.getActions()
        nexts = [self.nextState(p1, p2) for (p1, p2) in actions]
        return nexts

    def nextState(self, p1: Piece, p2: Piece):
        """
        Generates a next state from this state based on a capture (p, p')
        """
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
    
    def isGoal(self) -> bool:
        """
        Checks whether this state is a goal state
        """
        if len(self.ps) == 1:
            for p in self.ps:
                return p.type == 6
        return False
    
    def alignVer(self, p1, p2):
        s1 = self.square[p1]
        s2 = self.square[p2]

        # check if same x coordinate
        if s1.x != s2.x:
            return False

        # check if any piece in between
        y_low = min(s1.y, s2.y)
        y_high = max(s1.y, s2.y)
        for p in self.ps:
            if self.square[p].x == s1.x:
                if y_low < self.square[p].y < y_high:
                    return False
        return True

    def alignHor(self, p1, p2):
        s1 = self.square[p1]
        s2 = self.square[p2]
        
        # check if same y coordinate
        if s1.y != s2.y:
            return False

        # check if any piece in between
        x_low = min(s1.x, s2.x)
        x_high = max(s1.x, s2.x)
        for p in self.ps:
            if self.square[p].y == s1.y:
                if x_low < self.square[p].x < x_high:
                    return False
        return True

    def alignDia(self, p1, p2):
        s1 = self.square[p1]
        s2 = self.square[p2]
        x_low = min(s1.x, s2.x)
        x_high = max(s1.x, s2.x)

        # check alignment 1 (left-up to right-down)
        align1 = s1.x + s1.y == s2.x + s2.y

        # check alignment 2 (left-down to right-up)
        align2 = s1.x - s1.y == s2.x - s2.y

        # check if any piece in between p1 and p2 on the diagonal
        if align1 or align2:
            for p in self.ps:
                s = self.square[p]
                if (align1 and s.x + s.y == s2.x + s2.y) or (align2 and s.x - s.y == s2.x - s2.y):
                    if x_low < s.x < x_high:
                        # piece in between
                        return False
            return True

        # they are not on the same diagonal
        return False

    def valCap(self, p1, p2):
        # Independent of piece type:
            # cannot capture itself, king or when no captures left
        if p1 == p2 or p2.type == 6 or self.caps[p1] <= 0:
            return False
        
        ver = self.alignVer(p1, p2)
        hor = self.alignHor(p1, p2)
        dia = self.alignDia(p1, p2)
        
        match p1.type:
            case 1:
                # Queen
                return ver or hor or dia
            case 2:
                # Rook
                return ver or hor
            case 3:
                # Bischop
                return dia
            case 4:
                # Knight
                if abs(self.square[p2].x - self.square[p1].x) == 1 and abs(self.square[p2].y - self.square[p1].y) == 2:
                    return True
                elif abs(self.square[p2].x - self.square[p1].x) == 2 and abs(self.square[p2].y - self.square[p1].y) == 1:
                    return True
            case 5:
                # Pawn
                if self.square[p2].x == self.square[p1].x - 1 and self.square[p2].y == self.square[p1].y - 1:
                    return True
                elif self.square[p2].x == self.square[p1].x + 1 and self.square[p2].y == self.square[p1].y - 1:
                    return True
                return False
            case 6:
                # King
                return abs(self.square[p1].x - self.square[p2].x) <= 1 and abs(self.square[p1].y - self.square[p2].y) <= 1

if __name__ == "__main__":
    p1 = Pawn()
    p2 = King()
    p3 = Queen()
    square = {p1: Square(3, 1), p2: Square(1, 3), p3: Square(4, 4)}
    caps = {p1: 2, p2: 2, p3: 2}
    s1 = State({p1, p2, p3}, square, caps)
    
    res = s1.alignDia(p1, p2)
    print(res)