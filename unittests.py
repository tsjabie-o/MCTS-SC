import unittest
from pieces import Piece
from state import State
from utils import Square
from mcts import MCTS, Node

class TestState(unittest.TestCase):
    def alignSetUp(self):
        self.p1 = Piece("P")
        self.p2 = Piece("P")
        self.p3 = Piece("P")
        ps = {self.p1, self.p2, self.p3}
        square = dict()
        self.s = State(ps, square)
    
    def test_alignVer(self):
        self.alignSetUp()

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

        # cleanup
        self.s.square.clear()


    def test_alignHor(self):
        self.alignSetUp()

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

        # cleanup
        self.s.square.clear()

    def test_alignDia(self):
        self.alignSetUp()

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

        # clean up
        self.s.square.clear()

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
            p1: Square(3, 4),
            p2: Square(4, 5)
        }
        s = State({k, p1, p2}, square)

        self.assertTrue(s.valCap(k, p1))
        self.assertFalse(s.valCap(k, p2))

    def test_nextState(self):
        p1 = Piece("P")
        p2 = Piece("P")

        square = {
            p1: Square(3,3),
            p2: Square(4, 4)
        }

        s0 = State({p1, p2}, square)
        s2 = s0.nextState(p1, p2)

        self.assertNotIn(p2, s2.ps)
        self.assertNotIn(p2, s2.square)
        self.assertNotIn(p2, s2.caps)
        self.assertEqual((s2.square[p1].x, s2.square[p1].y), (4,4))
        self.assertEqual(s2.caps[p1], 1)

class TestNode(unittest.TestCase):
    def test_getNexts(self):
        k = Piece("K")
        p = Piece("P")

        square = {
            k: Square(3, 3),
            p: Square(3, 4)
        }

        s0 = State({k, p}, square)

        n = Node(s0, None, None)
        n.getNexts()
        self.assertTrue(len(n.nexts) == 1)
        self.assertTrue(n.nexts[0].parent == n)

        k = Piece("K")

        square = {
            k: Square(3, 3)
        }

        s0 = State({k}, square)

        n = Node(s0, None)
        n.getNexts()
        self.assertTrue(len(n.nexts) == 0)

    def test_getValue(self):
        k = Piece("K")
        square = {k: Square(3,3)}
        s = State({k}, square)

        n = Node(s, None)
        self.assertEqual(n.getValue(), 1)

        p = Piece("P")
        square = {p: Square(3,3)}
        s = State({p}, square)

        n = Node(s, None)
        self.assertEqual(n.getValue(), 0)

    def test_clearNexts(self):
        k = Piece("K")
        p = Piece("P")

        square = {
            k: Square(3, 3),
            p: Square(3, 4)
        }

        s0 = State({k, p}, square)

        n = Node(s0, None)
        n.getNexts()
        n2 = n.nexts[0]
        n.clearNexts()
        self.assertEqual(len(n.nexts), 0)
        self.assertIsNotNone(n2)

class TestPuzzles(unittest.TestCase):
    def setUp(self):
        self.mcts = MCTS()

    def test_WrongMovePoss(self):
        k = Piece("K")
        n1 = Piece("N")
        n2 = Piece("N")

        square = {
            k: Square(3, 1),
            n1: Square(3, 2),
            n2: Square(2, 4)
        }

        s0 = State({k, n1, n2}, square)
        self.mcts.setup(s0)
        res = self.mcts.run()

        self.assertTrue(len(res) == 3)
        self.assertTrue(res[2].isGoal())

    def test_oneStepWin(self):
        k = Piece("K")
        p = Piece("P")

        square = {
            k: Square(3, 3),
            p: Square(3, 4)
        }

        s0 = State({k, p}, square)

        self.mcts.setup(s0)
        res = self.mcts.run()
        self.assertEqual(len(res), 2)
    
    def test_instantWin(self):
        k = Piece("K")

        square = {
            k: Square(3, 3)
        }

        s0 = State({k}, square)

        self.mcts.setup(s0)
        res = self.mcts.run()
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0], s0)

    def test_hardLvl5(self):
        k = Piece("K")
        n1 = Piece("N")
        n2 = Piece("N")
        r1 = Piece("R")
        r2 = Piece("R")
        p = Piece("P")

        square = {
            k: Square(7, 3),
            n1: Square(8, 3),
            n2: Square(6, 1),
            r1: Square(8, 2),
            r2: Square(2, 1),
            p: Square(2, 2)
        }

        s0 = State({k, n1, n2, r1, r2, p}, square)

        self.mcts.setup(s0)
        res = self.mcts.run()

    def test_lvl10(self):
        k = Piece("K")
        r1 = Piece("R")
        r2 = Piece("R")
        r3 = Piece("R")
        r4 = Piece("R")
        r5 = Piece("R")
        r6 = Piece("R")
        r7 = Piece("R")
        b1 = Piece("B")
        q1 = Piece("Q")
        n1 = Piece("N")

        square = {
            k: Square(1,6),
            r1: Square(1,7),
            r2: Square(2,7),
            r3: Square(2,5),
            r4: Square(2,2),
            r5: Square(4,6),
            r6: Square(7,7),
            r7: Square(8,7),
            b1: Square(5,4),
            q1: Square(7,2),
            n1: Square(6,5)
        }

        s0 = State({k, r1, r2, r3, r4, r5, r6, r7, b1, q1, n1}, square)

        self.mcts.setup(s0)
        res = self.mcts.run()


if __name__ == "__main__":
    unittest.main()