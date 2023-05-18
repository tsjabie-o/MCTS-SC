import unittest
from pieces import Piece
from state import State
from utils import Square

class TestAlignment(unittest.TestCase):
    def setUp(self):
        self.p1 = Piece("P")
        self.p2 = Piece("P")
        self.p3 = Piece("P")
        ps = {self.p1, self.p2, self.p3}
        square = dict()
        self.s = State(ps, square)

    def tearDown(self):
        self.s.square.clear()
    
    def test_alignVer(self):
        # normal alignment
        self.s.square = {
            self.p1: Square(1,1),
            self.p2: Square(1,2),
            self.p3: Square(1,3)
        }
        self.assertTrue(self.s.alignVer(self.p1, self.p2))
        self.assertTrue(self.s.alignVer(self.p2, self.p1))

        # piece in between
        self.assertFalse(self.s.alignVer(self.p1, self.p3))

    def test_alignHor(self):
        # normal alignment
        self.s.square = {
            self.p1: Square(1, 1),
            self.p2: Square(2, 1),
            self.p3: Square(3, 1)
        }
        self.assertTrue(self.s.alignHor(self.p1, self.p2))
        self.assertTrue(self.s.alignHor(self.p2, self.p1))

        # piece in between
        self.assertFalse(self.s.alignHor(self.p1, self.p3))

    def test_alignDia(self):
        # left-up to right-down
        # aligned
        self.s.square = {
            self.p1: Square(1,3),
            self.p2: Square(2,2),
            self.p3: Square(3,1)
        }
        self.assertTrue(self.s.alignDia(self.p1, self.p2))
        self.assertTrue(self.s.alignDia(self.p2, self.p1))
        # piece in between
        self.assertFalse(self.s.alignDia(self.p1, self.p3))

        # left-down to right-up
        self.s.square = {
            self.p1: Square(1,1),
            self.p2: Square(2,2),
            self.p3: Square(3,3)
        }
        self.assertTrue(self.s.alignDia(self.p1, self.p2))
        self.assertTrue(self.s.alignDia(self.p2, self.p1))
        # piece in between
        self.assertFalse(self.s.alignDia(self.p1, self.p3))

        # one in dia-1, one in dia-2
        self.s.square = {
            self.p1: Square(1,3),
            self.p2: Square(2,2),
            self.p3: Square(3,3)
        }
        self.assertTrue(self.s.alignDia(self.p1, self.p2))
        self.assertTrue(self.s.alignDia(self.p2, self.p1))
        self.assertTrue(self.s.alignDia(self.p3, self.p2))
        self.assertTrue(self.s.alignDia(self.p2, self.p3))
        self.assertFalse(self.s.alignDia(self.p1, self.p3))

class TestCaptures(unittest.TestCase):
    def test_side(self):
        q = Piece("Q")
        k = Piece("K")

        square = {
            q: Square(3,3),
            k: Square(4, 3)
        }

        caps = {
            q: 2,
            k: 0
        }

        s = State({q, k}, square, caps=caps)

        self.assertFalse(s.valCap(q, q))
        self.assertFalse(s.valCap(q, k))
        self.assertFalse(s.valCap(k, q))

    def test_sliding(self):
        q = Piece("Q")
        p1 = Piece("P")
        p2 = Piece("P")
        p3 = Piece("P")
        p4 = Piece("P")
        p5 = Piece("P")
        square = {
            q: Square(3,3),
            p1: Square(5,3),
            p2: Square(3, 5),
            p3: Square(1, 5),
            p4: Square(2, 1),
            p5: Square(4, 3)
        }
        s = State({q, p1, p2, p3, p4, p5}, square)

        # regular capture
        self.assertTrue(s.valCap(q, p5))
        self.assertTrue(s.valCap(q, p2))
        self.assertTrue(s.valCap(q, p3))

        # piece in between
        self.assertFalse(s.valCap(q, p1))

        # not in line
        self.assertFalse(s.valCap(q, p4))

    def test_knight(self):
        n = Piece("N")
        p1 = Piece("P")
        p2 = Piece("P")
        p3 = Piece("P")
        p4 = Piece("P")
        p5 = Piece("P")
        p6 = Piece("P")
        p7 = Piece("P")
        p8 = Piece("P")
        p9 = Piece("P")
        p10 = Piece("P")
        square = {
            n: Square(3,3),
            p1: Square(1, 4),
            p2: Square(2, 5),
            p3: Square(4, 5),
            p4: Square(5, 4),
            p5: Square(5, 2),
            p6: Square(4, 1),
            p7: Square(2, 1),
            p8: Square(1, 2),
            p9: Square(2, 3),
            p10: Square(5, 5)
        }
        s = State({n, p1, p2, p3, p4, p5, p6, p7, p8, p9, p10}, square)

        self.assertTrue(s.valCap(n, p1))
        self.assertTrue(s.valCap(n, p2))
        self.assertTrue(s.valCap(n, p3))
        self.assertTrue(s.valCap(n, p4))
        self.assertTrue(s.valCap(n, p5))
        self.assertTrue(s.valCap(n, p6))
        self.assertTrue(s.valCap(n, p7))
        self.assertTrue(s.valCap(n, p8))
        self.assertFalse(s.valCap(n, p9))
        self.assertFalse(s.valCap(n, p10))

    def test_pawn(self):
        p = Piece("P")
        p1 = Piece("P")
        p2 = Piece("P")
        p3 = Piece("P")
        p4 = Piece("P")

        square = {
            p: Square(3, 3),
            p1: Square(2, 4),
            p2: Square(4, 4),
            p3: Square(3, 4),
            p4: Square(2, 2)
        }

        s = State({p, p1, p2, p3, p4}, square)

        self.assertTrue(s.valCap(p, p1))
        self.assertTrue(s.valCap(p, p2))
        self.assertFalse(s.valCap(p, p3))
        self.assertFalse(s.valCap(p, p4))

    def test_king(self):
        k = Piece("K")
        p1 = Piece("P")
        p2 = Piece("P")
        square = {
            k: Square(3,3),
            p1: Square(4, 3),
            p2: Square(4, 5)
        }
        s = State({k, p1, p2}, square)

        self.assertTrue(s.valCap(k, p1))
        self.assertFalse(s.valCap(k, p2))


if __name__ == "__main__":
    unittest.main()