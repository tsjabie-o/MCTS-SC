from pieces import Piece
from utils import Utils

class State():
    """A class which represents a state in a Solo Chess game.
    
    A state object holds all the information about a state such as decribed in the mathematical model of Solo Chess in the paper.
    
    Attributes:
        ps: the set of pieces in this state
        qs: the set of occupied squares
        square: a dictionary which maps a piece to a square
        caps: a dictionary which maps a piece to the amount of captures it has left
    """

    def __init__(self, square: dict, caps = None, center = None):
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
        
        self.center = center

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
        s2.center = self.center
        return s2
    
    def isGoal(self) -> bool:
        """Checks whether this state is a goal state

        Uses the rules of Solo Chess to determine whether this state is a winning (goal) state.
        The state has to be terminl and the type of the only piece must be a King.

        Returns:
            A bool
        """
        if self.isTerminal():
            return all([p.type == 6 for p in self.ps])
        return False
    
    def isTerminal(self):
        """Checks whether state is a terminal state
        
        Returns:
            A bool indicating whether this is a terminal state, i.e. no more actions can be taken
        """
        return len(self.ps) == 1 or len(self.getActions()) == 0

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
        
        return Utils.canReach(p1, self.square[p1], self.square[p2], self.qs)
    
    def heuristic(self, h, p1, p2):
        """Implementation of the Heuristics
        
        Rank: Favours low-ranked pieces capturing low-ranked pieces.
        Center: Favours pieces moving towards the center and pieces capturing far away pieces.

        Args:
            p1: the piece doing the capturing
            p2: the piece being captured
        
        Returns:
            heuristic value of the capture
        """
        match h:
            case "R":
                return 1/(p1.rank + self.caps[p2] * p2.rank)
            case "C":
                return Utils.distance(self.square[p1], self.square[p2]) + Utils.distance(self.square[p1], self.center)

    def __repr__(self) -> str:
        """The representation of an object of class State
        
        Implements a readable and informative string to represent a State object.

        Returns:
            A string representation
        """
        repr = ""
        for p in self.ps:
            repr += f"{p}-{self.square[p]}-{self.caps[p]}\n"
        return repr
    
    def __hash__(self) -> int:
        return hash(self.__repr__())