from utils import Square

class Piece():
    def __init__(self, t):
        match t:
            case "Q":
                # Queen
                self.type = 1
                self.rank = 9
            case "R":
                # Rook
                self.type = 2
                self.rank = 5
            case "B":
                # Bischop
                self.type = 3
                self.rank = 5
            case "N":
                # kNight
                self.type = 4
                self.rank = 3
            case "P":
                # Pawn
                self.type = 5
                self.rank = 1
            case "K":
                # King
                self.type = 6
                self.rank = 99