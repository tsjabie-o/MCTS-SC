from mcts import MCTS
from generator import Generator
from utils import Utils, Square
from pieces import Piece
from state import State
import time

if __name__ == "__main__":
    mcts = MCTS()
    gen = Generator()

    # times = []

    # s0 = gen.getPuzzle(5)

    # s0 = State({
    #     Piece("K"): Square(4, 7),
    #     Piece("Q"): Square(5,7),
    #     Piece("Q"): Square(5, 6),
    #     Piece("N"): Square(6,6),
    #     Piece("P"): Square(7, 5)
    # })

    # Utils.visualizeState(s0)


    # mcts.setup(s0)
    # mcts.run()

    # print("solved")

    for i in range(1000):
        s0 = gen.getPuzzle(10)
        mcts.setup(s0)
        
        # start = time.time()
        mcts.run()
        # stopped = time.time()
        
        # times.append(stopped - start)
        print(f"solved {i}")

    # print(f"avg time to solve {sum(times)/len(times)} seconds")
