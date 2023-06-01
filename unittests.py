import unittest
from pieces import Piece
from state import State
from utils import Square, Utils
from mcts import MCTS, Node
from generator import Generator

class TestState(unittest.TestCase):
    def test_alignVer(self):
        p1 = Piece("P")
        p2 = Piece("P")
        p3 = Piece("P")

        # normal alignment
        square = {
            p1: Square(1,1),
            p2: Square(1,2),
            p3: Square(1,3)
        }
        s = State(square)

        self.assertTrue(Utils.alignVer(s.square[p1], s.square[p2], s.qs))
        self.assertTrue(Utils.alignVer(s.square[p2], s.square[p1], s.qs))

        # piece in between
        self.assertFalse(Utils.alignVer(s.square[p1], s.square[p3], s.qs))

        # cleanup
        s.square.clear()

    def test_alignHor(self):
        p1 = Piece("P")
        p2 = Piece("P")
        p3 = Piece("P")

        # normal alignment
        square = {
            p1: Square(1, 1),
            p2: Square(2, 1),
            p3: Square(3, 1)
        }
        s = State(square)

        self.assertTrue(Utils.alignHor(s.square[p1], s.square[p2], s.qs))
        self.assertTrue(Utils.alignHor(s.square[p2], s.square[p1], s.qs))

        # piece in between
        self.assertFalse(Utils.alignHor(s.square[p1], s.square[p3], s.qs))

        # cleanup
        s.square.clear()

    def test_alignDia(self):
        p1 = Piece("P")
        p2 = Piece("P")
        p3 = Piece("P")

        # left-up to right-down
        # aligned
        square = {
            p1: Square(1,3),
            p2: Square(2,2),
            p3: Square(3,1)
        }
        s = State(square)

        self.assertTrue(Utils.alignDia(s.square[p1], s.square[p2], s.qs))
        self.assertTrue(Utils.alignDia(s.square[p2], s.square[p1], s.qs))
        # piece in between
        self.assertFalse(Utils.alignDia(s.square[p1], s.square[p3], s.qs))

        # left-down to right-up
        s.set_square({
            p1: Square(1,1),
            p2: Square(2,2),
            p3: Square(3,3)
        })
        self.assertTrue(Utils.alignDia(s.square[p1], s.square[p2], s.qs))
        self.assertTrue(Utils.alignDia(s.square[p2], s.square[p1], s.qs))
        # piece in between
        self.assertFalse(Utils.alignDia(s.square[p1], s.square[p3], s.qs))

        # one in dia-1, one in dia-2
        s.set_square({
            p1: Square(1,3),
            p2: Square(2,2),
            p3: Square(3,3)
        })
        self.assertTrue(Utils.alignDia(s.square[p1], s.square[p2], s.qs))
        self.assertTrue(Utils.alignDia(s.square[p2], s.square[p1], s.qs)) 
        self.assertTrue(Utils.alignDia(s.square[p3], s.square[p2], s.qs))
        self.assertTrue(Utils.alignDia(s.square[p2], s.square[p3], s.qs))
        self.assertFalse(Utils.alignDia(s.square[p1], s.square[p3], s.qs))

        # clean up
        s.square.clear()

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

        s = State(square, caps=caps)

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
        s = State(square)

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
        s = State(square)

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

        s = State(square)

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
        s = State(square)

        self.assertTrue(s.valCap(k, p1))
        self.assertFalse(s.valCap(k, p2))

    def test_nextState(self):
        p1 = Piece("P")
        p2 = Piece("P")

        square = {
            p1: Square(3,3),
            p2: Square(4, 4)
        }

        s0 = State(square)
        s2 = s0.nextState(p1, p2)

        self.assertNotIn(p2, s2.ps)
        self.assertNotIn(p2, s2.square)
        self.assertNotIn(p2, s2.caps)
        self.assertEqual((s2.square[p1].x, s2.square[p1].y), (4,4))
        self.assertEqual(s2.caps[p1], 1)

    def test_heuristic(self):
        # Rank heuristic

        # low captured over high captured
        # p1 takes p2 should have higher value than not p1 takes n
        p1 = Piece("P")
        p2 = Piece("P")
        n = Piece("N")
    
        square = {
            p1: Square(1, 0),
            p2: Square(2, 1),
            n: Square(0, 1)
        }
        s = State(square)

        self.assertTrue(s.heuristic("R", p1, p2) > s.heuristic("R", p1, n))

        # low capturer over high capturer
        # p1 takes p2 should have higher value than b takes p1
        p1 = Piece("P")
        p2 = Piece("P")
        b = Piece("B")

        square = {
            p1: Square(1, 0),
            p2: Square(2, 1),
            b: Square(0, 1)
        }

        s = State(square)

        self.assertTrue(s.heuristic("R", p1, p2) > s.heuristic("R", b, p1))

        # Center heuristic

        # moves over longer distance preferred
        # b takes p1 should have higher value than b takes p2
        p1 = Piece("P")
        p2 = Piece("P")
        b = Piece("B")

        square = {
            b: Square(3,3),
            p1: Square(0,0),
            p2: Square(4,4)
        }

        s = State(square, center = Square(3,3))

        self.assertTrue(s.heuristic("C", b, p1) > s.heuristic("C", b, p2))

        # moves further from the center preferred
        # b2 takes b1 should have higher value than b1 takes b2
        b1 = Piece("B")
        b2 = Piece("B")

        square = {
            b1: Square(3,3),
            b2: Square(6,6)
        }

        s = State(square, center = Square(3, 3))

        self.assertTrue(s.heuristic("C", b2, b1) > s.heuristic("C", b1, b2))

class TestNode(unittest.TestCase):
    def test_getNexts(self):
        k = Piece("K")
        p = Piece("P")

        square = {
            k: Square(3, 3),
            p: Square(3, 4)
        }

        s0 = State(square)

        n = Node(s0, None, None)
        n.getNexts()
        self.assertTrue(len(n.nexts) == 1)
        self.assertTrue(n.nexts[0].parent == n)

        k = Piece("K")

        square = {
            k: Square(3, 3)
        }

        s0 = State(square)

        n = Node(s0, None)
        n.getNexts()
        self.assertTrue(len(n.nexts) == 0)

    def test_getValue(self):
        k = Piece("K")
        square = {k: Square(3,3)}
        s = State(square)

        n = Node(s, None)
        self.assertEqual(n.getValue(), 1)

        p = Piece("P")
        square = {p: Square(3,3)}
        s = State(square)

        n = Node(s, None)
        self.assertEqual(n.getValue(), 0)

    def test_clearNexts(self):
        k = Piece("K")
        p = Piece("P")

        square = {
            k: Square(3, 3),
            p: Square(3, 4)
        }

        s0 = State(square)

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

        s0 = State(square)
        self.mcts.setup(s0)
        res = self.mcts.run()

        self.assertTrue(len(res) == 3)
        self.assertTrue(res[2].s.isGoal())

    def test_oneStepWin(self):
        k = Piece("K")
        p = Piece("P")

        square = {
            k: Square(3, 3),
            p: Square(3, 4)
        }

        s0 = State(square)

        self.mcts.setup(s0)
        res = self.mcts.run()
        self.assertEqual(len(res), 2)
    
    def test_instantWin(self):
        k = Piece("K")

        square = {
            k: Square(3, 3)
        }

        s0 = State(square)

        self.mcts.setup(s0)
        res = self.mcts.run()
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0].s, s0)

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

        s0 = State(square)

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

        s0 = State(square)

        self.mcts.setup(s0)
        res = self.mcts.run()

class TestGenerator(unittest.TestCase):
    def test_expand(self):
        g = Generator()
        p = Piece("Q")
        s = Square(1,1)
        ps = {p}
        qs = {Square(2,2)}
        caps = {p: 2}
        square = {p: Square(2,2)}
        
        g.expand(p, s, ps, qs, caps, square)
        
        # test new square is correct
        self.assertTrue(square[p] == s)

        # test caps is 1 less
        self.assertTrue(caps[p] == 1)

        # test entries for new piece
        self.assertTrue(len(square) == 2)
        self.assertTrue(len(caps) == 2)
        self.assertTrue(len(ps) == 2)
        self.assertTrue(len(qs) == 2)
    
    def test_getExpansions(self):
        g = Generator()
        
        # check inside board bounds
        q = Piece("Q")
        p = Piece("P")
        square = {q: Square(1,1), p: Square(2,2)}
        qs = {Square(1,1), Square(2,2)}

        sqrs = g.getExpansions(q, square, qs)

        self.assertTrue(Square(0, 1) in sqrs)
        self.assertTrue(Square(-1, 1) not in sqrs)
        self.assertTrue(Square(0, 2) in sqrs)
        self.assertTrue(Square(-1, 3) not in sqrs)

        # check not occupied or obstructed
        self.assertTrue(Square(2, 2) not in sqrs)
        self.assertTrue(Square(3, 3) not in sqrs)

        # soft check for complex pieces
        # Knight
        n = Piece("N")
        square = {n: Square(4,4)}
        qs = {Square(4,4)}

        sqrs = g.getExpansions(n, square, qs)

        self.assertTrue(len(sqrs) == 8)

        # King
        k = Piece("K")
        square = {k: Square(4,4)}

        sqrs = g.getExpansions(k, square, qs)

        self.assertTrue(len(sqrs) == 8)
    
    def test_fullGeneration(self):
        g = Generator()
        s0 = g.getPuzzle(4)
        
        self.assertTrue(len(s0.ps) == 4)



if __name__ == "__main__":
    unittest.main()