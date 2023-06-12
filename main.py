from mcts import MCTS
from generator import Generator
from utils import Utils
from backtrack import Backtrack

import time
import pandas as pd


if __name__ == "__main__":
    # Generating 100 puzzles of each size
    gen = Generator()
    ps = [gen.getPuzzle(i) for i in range(4, 10) for _ in range(10)]
    ps = {pid: p for pid, p in enumerate(ps)}

    print(f"{len(ps)} puzzles to solve")

    # to create the dataframe
    data = []

    for pid in ps:
        print(f"{int(pid/len(ps) * 100)}% done")

        # MCTS, random
        mcts = MCTS(ps[pid])

        start = time.process_time()
        mcts.run()
        stop = time.process_time()
        
        t = stop - start
        vn = mcts.visited
        
        data.append({
            "pid":pid,
            "n":len(ps[pid].ps),
            "method":"mcts",
            "heuristic":"random",
            "visited_nodes":vn,
            "time":t
        })

        # MCTS, Rank
        mcts = MCTS(ps[pid], h = "R")

        start = time.process_time()
        mcts.run()
        stop = time.process_time()
        
        t = stop - start
        vn = mcts.visited

        data.append({
            "pid":pid,
            "n":len(ps[pid].ps),
            "method":"mcts",
            "heuristic":"rank",
            "visited_nodes":vn,
            "time":t
        })

        # MCTS, Center

        mcts = MCTS(ps[pid], h = "C")

        start = time.process_time()
        mcts.run()
        stop = time.process_time()
        
        t = stop - start
        vn = mcts.visited

        data.append({
            "pid":pid,
            "n":len(ps[pid].ps),
            "method":"mcts",
            "heuristic":"center",
            "visited_nodes":vn,
            "time":t
        })

        # Backtrack, random
        bt = Backtrack(ps[pid])

        start = time.process_time()
        bt.run()
        stop = time.process_time()

        t = stop - start
        vn = bt.visited

        data.append({
            "pid":pid,
            "n":len(ps[pid].ps),
            "method":"bt",
            "heuristic":"random",
            "visited_nodes":vn,
            "time":t
        })

        # Backtrack, Rank
        bt = Backtrack(ps[pid], h = "R")

        start = time.process_time()
        bt.run()
        stop = time.process_time()

        t = stop - start
        vn = bt.visited

        data.append({
            "pid":pid,
            "n":len(ps[pid].ps),
            "method":"bt",
            "heuristic":"rank",
            "visited_nodes":vn,
            "time":t
        })

        # Backtrack, Center
        bt = Backtrack(ps[pid], h = "C")

        start = time.process_time()
        bt.run()
        stop = time.process_time()

        t = stop - start
        vn = bt.visited

        data.append({
            "pid":pid,
            "n":len(ps[pid].ps),
            "method":"bt",
            "heuristic":"center",
            "visited_nodes":vn,
            "time":t
        })

    df = pd.DataFrame(data)