from math import sqrt, log
from state import State
import random as rd
import math

class Node():
    """A class which represents a node in a game tree
    
    Specifically made for representing a state in the game of Solo Chess.

    Attributes:
        s: the corresponding state of a solo chess game
        nexts: a list of nodes representing states that can be reached from this node's state by taking an action (capture). In other words: children of this node
        parent: the parent node of this node
        prevAction: the action taken from the parent node to arrive at this child node
    """
    def __init__(self, s: State, parent = None, prevAction = None):
        """Initialises an instance of Node
        
        Args:
            s: the corresponding state of a solo chess game
            nexts: a list of nodes representing states that can be reached from this node's state by taking an action (capture). In other words: children of this node
            parent = None: the parent node of this node
            prevAction = None: the action taken from the parent node to arrive at this child node
        """
        self.s = s
        self.nexts = []
        self.parent = parent
        self.prevAction = prevAction
        self.wins = 0
        self.visits = 0
        self.leaf = True

    def getNexts(self):
        """Method to fill the self.nexts list
        
        Uses methods of the self.s state object to retreive all next possible states.
        Then nodes are created corresponding to those states, complete with information about parent and action taken.
        These nodes are added to the self.nexts list
        """
        if len(self.nexts) > 0:
            return
        new_states = self.s.transition()
        for a in new_states:
            new_node = Node(new_states[a], self, a)
            self.nexts.append(new_node)

    def clearNexts(self):
        """Clears the self.nexts list
        
        In case of a simulation phase, the explored children should be removed from memory.
        """
        self.nexts.clear()

    def getValue(self):
        """Retrieves the value of the corresponding state
        """
        return 1 if self.s.isGoal() else 0
    
    def isTerminal(self):
        return self.s.isTerminal()

class MCTS():
    """A class which represents a MCTS algorithm
    
    The class contains the logic for traversing the tree and simulating rollouts. The tree structure is
    implicitly embedded in the Node objects
    """
    def __init__(self, s0, h = None, c = 2):
        """Initialises an instance of MCTS
        
        Args:
            c: the exploration coefficient
            vals: a dictionary keeping track of values of nodes/states
            ns: a dictionary keeping track of the number of times a node has been visited
            h: whether to implement heuristics
        """
        self.c = c
        self.root = Node(s0, None, None)
        self.h = h

        self.tree = {self.root.s}        
        self.visited = 0

    def run(self):
        """Starts the mcts algorithm on the initial state
        
        This is the main loop of the mcts algorithm. The selection phase is fully contained here.
        When a leaf node is found, this method calls a function to expand and simulate a node.
        After that, it calls a method for performing backpropogation.
        If a solution is found, this method calls a method to retrieve the route (sequence of actions) from the tree and returns, stopping the loop
        """
        while True:
            self.visited += 1
            cur = self.root
            while len(cur.nexts) > 0:
                if rd.randint(0,100) <= 5:
                    # select random child
                    child = rd.choice(cur.nexts)
                else:
                    # select child with highest uct metric
                    ucts = {node: self.uct(node) for node in cur.nexts}
                    child = max(ucts, key=ucts.get)

                cur = child
                self.visited += 1

            if cur.visits > 0:
                # has been simulated, expand node
                self.expand(cur)
                if len(cur.nexts) > 0:
                    cur.leaf = False
                    
                    # not a losing/terminal state

                    if rd.randint(0,100) <= 10:
                        # select random child
                        child = rd.choice(cur.nexts)
                    else:
                        # select child with highest uct metric
                        ucts = {node: self.uct(node) for node in cur.nexts}
                        child = max(ucts, key=ucts.get)
                    cur = child
                    self.visited += 1
                
            # simulate that child
            v = self.simulate(cur)
            if v == 1:
                return
            else:
                self.backprop(cur, v)

    def getroute(self, node: Node):
        """Retrieves the route from the root to a node
        
        Assuming the node is a goal state (which this method does not check), this route contains the sequence of actions which solve the puzzle
        The method uses the parent attribute of the Node class to determine the route.

        Args:
            node: the node from which to find the route to the root node
            
        Returns:
            A list containing the nodes on route from the root to the supplied node
        """
        route = [node]
        while node.parent is not None:
            node = node.parent
            route.append(node)
        
        route.reverse()
        return route

    def simulate(self, node: Node):
        """Performs the simulation phase of the mcts algorithm
        
        This method performs the simulation phase starting from the supplied node. It uses the heuristics by Verlaan to determine which actions to take.
        When a terminal state is found, the value is retrieved and is returned.

        Args:
            node: the node from which to perform simulation.
        Returns:
            the value of the terminal state.
        """
        node.getNexts()
        cur = node

        # Keep choosing a new action as long as current state is not terminal
        while(len(cur.nexts)!=0):
            self.visited += 1

            if self.h is not None:
                # use heuristics
                hvals = {next: cur.s.heuristic(self.h, next.prevAction[0], next.prevAction[1]) for next in cur.nexts}
                next = max(hvals, key=hvals.get)
            else:
                # uniform random
                next = rd.choice(cur.nexts)
            
            # self.prune(cur)
            # cur = next
            # self.expand(cur)

            cur.clearNexts()
            cur = next
            cur.getNexts()
        
        # terminal node, get value win ratio or just 1
        v = (len(self.root.s.ps) - len(cur.s.ps))/len(self.root.s.ps) if not cur.s.isGoal() else 1
        # self.prune(cur)
        cur.clearNexts()
        return v

    def backprop(self, node: Node, v):
        """Performs the backpropagation phase of mcts
        
        Moves up through the tree from the supplied node to the root, updating the wins and visits stats.
        
        Args:
            node: the node from which to start backpropagating
            v: the value of node
        """
        cur = node
        cur.wins += v
        cur.visits += 1
        self.visited += 1
        while cur.parent is not None:
            cur = cur.parent
            cur.wins += v
            cur.visits += 1
            self.visited += 1

    def expand(self, node: Node):
        """Performs the expansion phase of mcts
        
        Expands a node by calling the getNexts() method of the Node object.
        
        Args:
            node: the node to expand
            """
        node.getNexts()
        node.nexts = [n for n in node.nexts if n.s not in self.tree]
        
        for n in node.nexts:
            self.tree.add(n.s)

    def prune(self, node: Node):
        for n in node.nexts:
            self.tree.remove(n.s)
        node.clearNexts()

    def uct(self, node):
        """Performs the UCT calculation
        
        Args:
            node: the node for which to calculate the UCT value
            
        Returns:
            The UCT value of node, according to the original UCT formula as designed by Kocsis et al
            """
        if node.visits == 0:
            return math.inf
        else:
            exploitation = node.wins / node.visits
            exploration = sqrt(log(node.parent.visits)/node.visits)
            return exploitation + self.c * exploration
    
