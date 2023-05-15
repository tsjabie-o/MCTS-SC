import state, solochess

class Instance():
    k, l: int # board size
    d: int # nr of captures
    s0: state.State # the initial state
    P: list[solochess.Piece] # list of the pieces