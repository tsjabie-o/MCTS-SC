import state, pieces

class Instance():
    k, l: int # board size
    d: int # nr of captures
    s0: state.State # the initial state
    P: list[pieces.Piece] # list of the pieces