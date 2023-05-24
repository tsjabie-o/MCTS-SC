from pieces import Piece

class State():
    """A class which represents a state in a Solo Chess game.
    
    A state object holds all the information about a state such as decribed in the mathematical model of Solo Chess in the paper.
    
    Attributes:
        ps: the set of pieces in this state
        qs: the set of occupied squares
        square: a dictionary which maps a piece to a square
        caps: a dictionary which maps a piece to the amount of captures it has left
    """

    def __init__(self, square: dict, caps = None):
        """Initialises a State object

        Args:
            square: a dictionary which maps a piece to a square.
            caps = None: a dictionary which maps a piece to the amount of captures it has left
        """
        self.square = square
        
        # the set of pieces self.ps and set of squares self.qs can be inferred from self.square
        self.ps = {p for p in self.square}
        self.qs = {self.square[p] for p in self.square}

        if caps is not None:
            self.caps = caps
        else:
            self.caps = {p: 2 for p in self.ps}

    def set_square(self, square):
        """Changes self.square and updates other attributes
        
        For debug and testing purposes, should never actually be used during normal algorithm

        Args:
            square: the new dictionary which maps a piece to a square
        """
        self.square = square
        # the set of pieces self.ps and set of squares self.qs can be inferred from self.square
        self.ps = {p for p in self.square}
        self.qs = {self.square[p] for p in self.square}


    def getActions(self) -> list:
        """Creates a list of actions which can be taken in this state
        
        An action consists of a capture by p1 of p2.
        This function doubly iterates through self.ps, and adds each (p1, p2) combination to the returned list
        if self.valCap(p1, p2) returns True.

        Returns:
            A list of (p1, p2) tuples representing the captures that can be taken.
            p1 is the piece doing the capturing
            p2 is the piece being captured
        """
        actions = []
        for p1 in self.ps:
            for p2 in self.ps:
                if self.valCap(p1, p2):
                    actions.append((p1, p2))
        return actions

    def transition(self) -> dict:
        """Returns a list of states which can be reached from this state
        
        Uses self.getActions() to retreive a list of possible captures. 
        Each capture is then given to self.nextState() and the resulting states are stored in a dictionary.

        Returns:
            A dictionary mapping captures of the form (p1: Piece, p2: Piece) to states as determined by self.nextState()
        """
        actions = self.getActions()
        nexts = {(p1, p2): self.nextState(p1, p2) for (p1, p2) in actions}
        return nexts

    def nextState(self, p1: Piece, p2: Piece):
        """Generates a next state from this state based on a capture (p1, p2)

        Analogous to the set operations performed in the state transition function as described in the paper.
        However, since self.ps and self.qs can be inferred from the self.square function, only this function and self.caps are altered for brevity.

        ! This function assumes validity of the capture and does not check this.

        Args:
            p1: The piece doing the capture
            p2: The piece being captures

        Returns:
            A State object which represents the state resulting from this action.
        """

        # value of p1 takes over value of p2 in square, p2 removed
        square2 = self.square.copy()
        square2[p1] = square2[p2]
        square2.pop(p2)

        # value of p1 in caps decremented by one, p2 removed
        caps2 = self.caps.copy()
        caps2[p1] -= 1
        caps2.pop(p2)

        s2 = State(square2, caps2)
        return s2
    
    def isGoal(self) -> bool:
        """Checks whether this state is a goal state

        Uses the rules of Solo Chess to determine whether this state is a winning (goal) state.
        The amount of pieces has to equal one and the type of this piece must be a King.

        Returns:
            A bool
        """
        if len(self.ps) == 1:
            for p in self.ps:
                return p.type == 6
        return False
    
    def alignVer(self, p1: Piece, p2: Piece) -> bool:
        """Checks whether two pieces are vertically aligned in this state
        
        Two pieces are aligned vertically if they occupy the same column AND if there is no piece in between them.
        To check the latter, the coordinate of each piece in the state is checked.

        Args:
            p1: A piece
            p2: Another piece

        Returns:
            A bool
        """
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

    def alignHor(self, p1: Piece, p2: Piece) -> bool:
        """Checks whether two pieces are horizontally aligned in this state
        
        Two pieces are aligned horizontally if they occupy the same row AND if there is no piece in between them.
        To check the latter, the coordinate of each other piece in the state is checked.

        Args:
            p1: A piece
            p2: Another piece

        Returns:
            A bool
        """
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

    def alignDia(self, p1: Piece, p2: Piece) -> bool:
        """Checks whether two pieces are diagonally aligned in this state
        
        Two pieces can be aligned dianogally in two ways: from left-down to right-up or from right-down to left-up.
        In the first case, the sum of the x and y coordinates of each piece will be equal.
        In the second case, this applies to the difference.

        To check whether there is a piece in between, the coordinate of each piece in the state is checked in much the same way.

        Args:
            p1: A piece
            p2: Another piece

        Returns:
            A bool
        """
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

    def valCap(self, p1: Piece, p2: Piece) -> bool:
        """Determines whether a certain capture is valid in this state
        
        This method checks the validity of a capture using both the information in this state and the rules of chess.
        First, piece-type independent conditions are checked: a piece cannot capture itself or a King and can only capture if it has captures left.

        Afterwards, the type of the piece is determined and we check whether this piece can indeed move to the other.

        Args:
            p1: The piece doing the capturing
            p2: The piece being captured

        Returns:
            A bool
        """
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
                if self.square[p2].x == self.square[p1].x - 1 and self.square[p2].y == self.square[p1].y + 1:
                    return True
                elif self.square[p2].x == self.square[p1].x + 1 and self.square[p2].y == self.square[p1].y + 1:
                    return True
                return False
            case 6:
                # King
                return abs(self.square[p1].x - self.square[p2].x) <= 1 and abs(self.square[p1].y - self.square[p2].y) <= 1
    
    def __repr__(self) -> str:
        """The representation of an object of class State
        
        Implements a readable and informative string to represent a State object.

        Returns:
            A string representation
        """
        repr = ""
        for p in self.ps:
            repr += f"{p} at square {self.square[p]}, with {self.caps[p]} captures left\n"
        return repr