from pieces import Piece
from utils import Square, Utils
from state import State
import random as rd


class Generator():
    """Generates starting states based on certain preconditions
    """
    def getPuzzle(self, n):
        """Interface for other parts of code
        
        Uses internal methods to generate a puzzle starting state. Basically checks if generation has
        succesfully ended, as it might end up stuck.
        
        Args:
            n: the number of pieces
            s: seed for random
        Returns:
            A starting state corresponding to a level n+1 puzzle of Solo Chess
        """
        while True:
            s0 = self.generate(n)
            if s0 is not None:
                return s0
            
    def generate(self, n):
        """Performs the actual generation of a starting state
        
        Starts with a king on the board. Calls a method to collect all the expendable pieces and the squares they can be expanded to.
        Chooses a random piece and square to expand to and calls method to expand that.

        Args:
            n: the amount of pieces that need to be on the board

        Returns:
            a starting state
        """
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

        s0 = State(square)
        return s0

    def expand(self, p, q, ps, qs, caps, square):
        """Performs the expansion part of the generation.
        
        Picks a random piece (except King) and places it on the square of the expanded piece.
        Expanded piece is moved to new square. All internal data is updated to reflect this change
        
        Args:
            p: the piece being expanded
            q: the square p is being expanded to
            ps: list of pieces on the board
            qs: list of occupied squares
            caps: dictionary from piece to amount of captures left
            square: dictionary from piece to square
        """
        # make a new piece and place it on p's square
        p2 = Piece(rd.choice(["Q", "R", "B", "N", "P"]))
        caps[p2] = 2
        square[p2] = square[p]
        ps.add(p2)

        # move p square to s
        square[p] = q
        qs.add(q)
        caps[p] -= 1

    def getExpansions(self, p: Piece, square, qs):
        """Gets the sqaure a piece can expand to
        
        Uses the Utils.possMovements method. Made it a seperate method here for clarity.
        
        Args:
            p: piece for which to check squares it can expand to.
            square: dictionary from piece to square
            qs: list of occupied squares
        
        Returns:
            list of squares piece p could move to its original square from
        """
        sqrs = Utils.possMovements(p, square[p], qs)
        return sqrs