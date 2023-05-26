from mcts import MCTS
from generator import Generator
import time

if __name__ == "__main__":
    mcts = MCTS()
    gen = Generator()
    

    times = []

    for i in range(100):
        s0 = gen.getPuzzle(10)
        mcts.setup(s0)
        start = time.time()
        route = mcts.run()
        stopped = time.time()
        times.append(stopped - start)
        print(f"solved {i}")

    print(f"avg time to solve {sum(times)/len(times)} seconds")
