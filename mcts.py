from math import sqrt, log
from state import State
import random as rd

class Node():
    def __init__(self, s: State, parent):
        self.s = s
        self.nexts = []
        self.parent = parent

    def getNexts(self):
        new_states = self.s.transition()
        for s in new_states:
            new_node = Node(s, self)
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
        self.root = Node(s0, None)
        self.ns[self.root] = 0
        self.vals[self.root] = 0


    def run(self):
        while True:
            cur = self.root
            while len(cur.nexts) != 0:
                # select child with highest uct metric
                ucts = {node: self.uct(node) for node in cur.nexts}
                child = max(ucts, key=ucts.get)
                cur = child

            # at a leaf node
            if self.ns[cur] == 0:
                # no sims yet, do sim
                (v, end) = self.simulate(cur)
                if v == 1:
                    return self.getroute(end)
                else:
                    self.backprop(cur, v)
            else:
                # has been simulated, expand node
                self.expand(cur)
                
                # select child with highest uct metric
                ucts = {node: self.uct(node) for node in cur.nexts}
                child = max(ucts, key=ucts.get)
                cur = child
                
                # simulate that child
                (v, end) = self.simulate(cur)
                if v == 1:
                    return self.getroute(end)
                else:
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
        node.getNexts()
        cur = node
        while(len(cur.nexts) != 0):
            # select best node from nexts based on heuristics
            temp = rd.choice(cur.nexts) # for now, random choice of action
            cur.clearNexts() # keep mem usage low
            cur = temp
            cur.getNexts()
        
        # leaf node, get value win or loss
        v = cur.getValue()
        
        # prune simulated tree
        node.clearNexts()
        return (v, cur)

    def backprop(self, node: Node, v):
        cur = node
        while cur.parent is not None:
            self.vals[cur] += v
            self.ns[cur] += 1
            cur = cur.parent

    def expand(self, node: Node):
        node.getNexts()
        for n in node.nexts:
            self.vals[n] = 0
            self.ns[n] = 0

    def uct(self, node):
        return self.vals[node] + self.c * sqrt(log(self.ns[node.parent])/self.ns[node])
    
