from math import sqrt, log
from state import State
import random as rd
import math

class Node():
    def __init__(self, s: State, parent = None, prevAction = None):
        self.s = s
        self.nexts = []
        self.parent = parent
        self.prevAction = prevAction

    def getNexts(self):
        new_states = self.s.transition()
        for a in new_states:
            new_node = Node(new_states[a], self, a)
            self.nexts.append(new_node)

    def clearNexts(self):
        # clear the nexts list, in case of simulation
        self.nexts.clear()

    def getValue(self):
        return 1 if self.s.isGoal() else 0

class MCTS():
    def __init__(self, c = 2):
        self.c = c
        self.vals = dict()
        self.ns = dict()

    def setup(self, s0):
        self.root = Node(s0, None, None)
        self.ns[self.root] = 0
        self.vals[self.root] = 0


    def run(self):
        while True:
            print("STARTING EXPLORATION\n\n")
            cur = self.root
            print(f"Root state: \n{cur.s}\n")
            while len(cur.nexts) != 0:
                # select child with highest uct metric
                ucts = {node: self.uct(node) for node in cur.nexts}
                child = max(ucts, key=ucts.get)
                cur = child
                print(f"Taking action {cur.prevAction} into state: \n{cur.s}\n")


            # at a leaf node
            if self.ns[cur] == 0:
                # no sims yet, do sim
                (v, end) = self.simulate(cur)
                if v == 1:
                    print(f"state was solution!\n")
                    return self.getroute(end)
                else:
                    print("state was not a solution\n")
                    self.backprop(cur, v)
            else:
                # has been simulated, expand node
                print("expanding this node\n")
                self.expand(cur)
                
                if len(cur.nexts) != 0:
                    # not a losing state
                    # select child with highest uct metric
                    ucts = {node: self.uct(node) for node in cur.nexts}
                    child = max(ucts, key=ucts.get)
                    cur = child
                
                # simulate that child
                (v, end) = self.simulate(cur)
                if v == 1:

                    print(f"state was solution!\n")
                    return self.getroute(end)
                else:
                    print("state was not a solution\n")
                    self.backprop(cur, v)

    def getroute(self, node: Node):
        cur = node
        route = [cur.s]
        while cur.parent is not None:
            cur = cur.parent
            route.append(cur.s)
        route.reverse()
        return route

    def simulate(self, node: Node):
        print(f"SIMULATION\n starting from state[\n{node.s}\n]")
        node.getNexts()
        cur = node
        while(len(cur.nexts) != 0):
            # select best node from nexts based on heuristics
            temp = rd.choice(cur.nexts) # for now, random choice of action
            cur.clearNexts() # keep mem usage low
            cur = temp
            cur.getNexts()
            print(f"Taking action {cur.prevAction} into state: \n{cur.s}\n")

        
        # leaf node, get value win or loss
        v = cur.getValue()
        
        # prune simulated tree
        node.clearNexts()
        return (v, cur)

    def backprop(self, node: Node, v):
        cur = node
        self.vals[cur] += v
        self.ns[cur] += 1
        while cur.parent is not None:
            cur = cur.parent
            self.vals[cur] += v
            self.ns[cur] += 1

    def expand(self, node: Node):
        node.getNexts()

        for n in node.nexts:
            self.vals[n] = 0
            self.ns[n] = 0

    def uct(self, node):
        if self.ns[node] == 0:
            return math.inf
        else:
            exploitation = self.vals[node] / self.ns[node]
            exploration = sqrt(log(self.ns[node.parent])/self.ns[node])
            return exploitation + self.c * exploration
    
