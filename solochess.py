class Piece():
    type: str
    rank: int # used for one of the heuristics of Stan
    captures: int # nr captures left
    # something for the momevent pattern?

class Move():
    to: Piece
    frm: Piece

class Square():
    pass