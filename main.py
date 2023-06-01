from mcts import MCTS
from generator import Generator
from utils import Utils
import time

if __name__ == "__main__":
    gen = Generator()
    puzzles = [gen.getPuzzle(10) for i in range(1000)]
    ts = []
    for i, p in enumerate(puzzles):
        print(f"puzzle {i}")
        tsh = []
        tsr = []
        mctsH = MCTS(h="R")
        mctsH.setup(p)
        mctsR = MCTS()
        mctsR.setup(p)

        for i in range(50):
            start = time.time()
            mctsH.run()
            stop = time.time()
            e = stop - start
            tsh.append(e)

            start = time.time()
            mctsR.run()
            stop = time.time()
            e = stop - start
            tsr.append(e)
        
        ts.append((sum(tsh)/len(tsh))/(sum(tsr)/len(tsr)))
    
    print(sum(ts)/len(ts))
    # about 0.12 on last run!


        