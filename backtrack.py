from mcts import Node

class Backtrack():
    """A basic implementation of Backtracking
    
    This should be roughly the same implementation as that of Verlaan
    """
    def __init__(self, s0, h=None):
        self.s0 = s0
        self.h = h
        self.root = Node(self.s0, None, None)
        self.seen = set()
    
    def run(self):
        self.seen.add(self.root.s)
        if not self.run_rec(self.root):
            print("no solution found")
            return None
        return

    def run_rec(self, node: Node):
        # Base case: If the current node is the goal, return True
        if node.getValue() == 1:
            return True
        
        node.getNexts()
        
        # manage already seen states
        node.nexts = [n for n in node.nexts if n.s not in self.seen]
        for n in node.nexts:
            self.seen.add(n.s)
        
        
        if self.h is not None:
            # order the .nexts list by heuristic value
            node.nexts = {next: node.s.heuristic(self.h, next.prevAction[0], next.prevAction[1]) for next in node.nexts}
            node.nexts = [node[0] for node in sorted(node.nexts.items(), key=lambda x:x[1])]

    
        # Iterate over the children nodes
        for child in node.nexts:
            # Recursive call to explore the child node
            found_solution = self.run_rec(child)
            if found_solution:
                return True

        return False