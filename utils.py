from math import sqrt

class Square():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f"{self.x}, {self.y}"
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    def __hash__(self) -> int:
        # prime factorisation so unique
        return hash(2**(self.x) * 3**(self.y))
    
class Utils():
    """Class with some classmethods for long but trivial computations and checks

    These methods are mostly about implementing rules of chess and movement patterns for pieces.
    That requires long and boring code, which is why it's hidden away in this class.
    """
    @classmethod
    def visualizeState(cls, s):
        """Visualizes the game board in a simple grid on the terminal
        
        Agrs:
            s: the state to visualize
        """
        board = [["-" for i in range(8)] for i in range(8)]
        for p in s.square:
            q = s.square[p]
            board[q.y][q.x] = p

        # matter of perspective
        board.reverse()
        for row in board:
            for square in row:
                print(square, end=' ')
            print()
        
    
    @classmethod
    def distance(cls, q1, q2):
        """Returns euclidiean distance between two squares
        """
        return sqrt((q1.x - q2.x)**2 + (q1.y - q2.y)**2)

    @classmethod
    def alignVer(cls, q1, q2, qs):
        """Checks whether two squares are vertically aligned
        
        Two squares are aligned vertically if they occupy the same column AND if there is no occupied square in between them.
        To check the latter, qs is used.

        Args:
            s1: square 1
            s2: square 2
            qs: set of occupied squares

        Returns:
            A bool
        """
        # check if same x coordinate
        if q1.x != q2.x:
            return False

        # check if any piece in between
        y_low = min(q1.y, q2.y)
        y_high = max(q1.y, q2.y)
        for q in qs:
            if q.x == q1.x:
                if y_low < q.y < y_high:
                    return False
        return True

    @classmethod
    def alignHor(cls, q1, q2, qs):
        """Checks whether two squares are horizontally aligned
        
        Two squares are aligned horizontally if they occupy the same row AND if there is no occupied square in between them.
        To check the latter, qs is used.

        Args:
            s1: square 1
            s2: square 2
            qs: set of occupied squares

        Returns:
            A bool
        """
        # check if same y coordinate
        if q1.y != q2.y:
            return False

        # check if any piece in between
        x_low = min(q1.x, q2.x)
        x_high = max(q1.x, q2.x)
        for q in qs:
            if q.y == q1.y:
                if x_low < q.x < x_high:
                    return False
        return True

    @classmethod
    def alignDia(cls, q1, q2, qs):
        """Checks whether two squares are diagonally aligned
        
        Two squares can be aligned dianogally in two ways: from left-down to right-up or from right-down to left-up.
        In the first case, the sum of the x and y coordinates of each square will be equal.
        In the second case, this same thing applies but with the difference of x and y.

        Args:
            s1: square 1
            s2: square 2
            qs: set of occupied squares

        Returns:
            A bool
        """
        x_low = min(q1.x, q2.x)
        x_high = max(q1.x, q2.x)

        # check alignment 1 (left-up to right-down)
        align1 = q1.x + q1.y == q2.x + q2.y

        # check alignment 2 (left-down to right-up)
        align2 = q1.x - q1.y == q2.x - q2.y

        # check if any piece in between p1 and p2 on the diagonal
        if align1 or align2:
            for q in qs:
                if (align1 and q.x + q.y == q2.x + q2.y) or (align2 and q.x - q.y == q2.x - q2.y):
                    if x_low < q.x < x_high:
                        # piece in between
                        return False
            return True

        # they are not on the same diagonal
        return False
    
    @classmethod
    def canReach(cls, p, q1, q2, qs):
        """Checks whether piece p on square q can reach square q2
        
        This method uses the rules of chess and knowledge of occupied squares.

        Args:
            p: the piece making the move
            q1: the square the piece is currently occupying
            q2: the square the piece has to move to
            qs: set of occupied squares

        Returns:
            Bool
        """
        ver = Utils.alignVer(q1, q2, qs)
        hor = Utils.alignHor(q1, q2, qs)
        dia = Utils.alignDia(q1, q2, qs)
        
        match p.type:
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
                if abs(q2.x - q1.x) == 1 and abs(q2.y - q1.y) == 2:
                    return True
                elif abs(q2.x - q1.x) == 2 and abs(q2.y - q1.y) == 1:
                    return True
            case 5:
                # Pawn
                if q2.x == q1.x - 1 and q2.y == q1.y + 1:
                    return True
                elif q2.x == q1.x + 1 and q2.y == q1.y + 1:
                    return True
                return False
            case 6:
                # King
                return abs(q1.x - q2.x) <= 1 and abs(q1.y - q2.y) <= 1

    @classmethod
    def possMovements(cls, p, q, qs):
        """Returns list of squares a piece can move to (not capture)
        
        Uses the rules of chess to determine possible squares a piece can move to.
        This method assumes an 8x8 board and also checks for whether a square is inside board bounds,
        not occupied and is not blocked by another piece.

        Args:
            p: the piece for which to compute possible movements
            q: the square p occupies
            qs: the set of occupied squares

        Returns:
            a list of squares the piece can reach.
        """
        sqrs = []
        match p.type:
            case 1:
                # Queen
                dirs = [(i,j) for i in [-1,0,1] for j in [-1,0,1] if not i == 0 == j]
                sqrs = [Square(q.x + a*i, q.y + a*j) for (i,j) in dirs for a in range(1,9)]
            case 2:
                # Rook
                dirs = [(i,j) for i in [-1,0,1] for j in [-1,0,1] if (i == 0) != (j == 0)]
                sqrs = [Square(q.x + a*i, q.y + a*j) for (i,j) in dirs for a in range(1,9)]
            case 3:
                # Bischop
                dirs = [(i,j) for i in [-1,1] for j in [-1,1]]
                sqrs = [Square(q.x + a*i, q.y + a*j) for (i,j) in dirs for a in range(1,9)]
            case 4:
                # Knight
                steps = [-2, -1, 1, 2]
                sqrs = [Square(q.x + i, q.y + j) for i in steps for j in steps if abs(i) != abs(j)]
            case 5:
                # Pawn
                sqrs = [Square(q.x + i, q.y - 1) for i in [-1,1]]
            case 6:
                # King
                sqrs = [Square(q.x + i, q.y + j) for i in [-1,0,1] for j in [-1,0,1] if not i == 0 == j]

        # remove squares outside board
        sqrs = [q2 for q2 in sqrs if 0 <= q2.x <= 7 and 0 <= q2.y <= 7]

        # remove occupied squares
        sqrs = [q2 for q2 in sqrs if q2 not in qs]

        # remove squares that are blocked by another piece
        match p.type:
            case 1:
                # Queen
                sqrs = [q2 for q2 in sqrs if cls.alignDia(q2, q, qs) or cls.alignHor(q2, q, qs) or cls.alignVer(q2, q, qs)]
            case 2:
                # Rook
                sqrs = [q2 for q2 in sqrs if cls.alignHor(q2, q, qs) or cls.alignVer(q2, q, qs)]
            case 3:
                # Bischop
                sqrs = [q2 for q2 in sqrs if cls.alignDia(q2, q, qs)]
            case other:
                sqrs = sqrs

        return sqrs