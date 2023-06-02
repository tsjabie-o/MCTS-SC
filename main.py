from mcts import MCTS
from generator import Generator
from utils import Utils
from backtrack import Backtrack
import time
import random

if __name__ == "__main__":
    gen = Generator()
    ps = [gen.getPuzzle(13) for i in range(15)]
    times = []

    for i, p in enumerate(ps):
        print(i)

        mcts = MCTS()
        

        mcts.setup(p)
        # s = time.time()
        mcts.run()
        # st = time.time()
        # e1 = st - s

        # bt = Backtrack()
        # bt.setup(p)
        # s = time.time()
        # bt.run()
        # st = time.time()
        # e2 = st - s

    
    # print(sum(times)/len(times))




        