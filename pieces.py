class Piece():
    """A class wich represents a piece of chess
    
    Attributes:
        type: the numerical representation of the type of piece (King, Queen, etc.)
        rank: the rank of the piece, dependent on its type and used in the Rank heuristic by Verlaan
    """

    toType = {
            1: "Q",
            2: "R",
            3: "B",
            4: "N",
            5: "P",
            6: "K"
    }

    def __init__(self, t):
        """Initialises a Piece object
        
        Args:
            t: the numerical representation of the type of piece
        """
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

    def __repr__(self) -> str:
        """The string representation of a Piece object
        
        Returns:
            A string containing information about the type and rank of the piece
        """
        return f"{Piece.toType[self.type]}"

    def __lt__(self, other):
        return self.type < other.type