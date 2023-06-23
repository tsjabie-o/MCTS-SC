from mcts import Node

class Backtrack():
    """A basic implementation of Backtracking
    
    This should be roughly the same implementation as that of Verlaan
    """
    def __init__(self, s0, h=None):
        self.s0 = s0
        self.h = h
        self.root = Node(self.s0, None, None)
        self.visited = 0
        self.tree = {self.root.s}
    
    def run(self):
        if not self.run_rec(self.root):
            print("no solution found")
            return None
        return

    def run_rec(self, node: Node):
        self.visited += 1
        # Base case: If the current node is the goal, return True
        if node.getValue() == 1:
            return True
        
        if node.isTerminal():
            return False
        
        node.getNexts()
        node.nexts = [n for n in node.nexts if n.s not in self.tree]
        
        for n in node.nexts:
            self.tree.add(n.s)
        
        if self.h is not None:
            # order the .nexts list by heuristic value
            node.nexts = {next: node.s.heuristic(self.h, next.prevAction[0], next.prevAction[1]) for next in node.nexts}
            node.nexts = [node[0] for node in sorted(node.nexts.items(), key=lambda x:x[1], reverse=True)]

        # print(f"children of {node}: {node.nexts}")
    
        # Iterate over the children nodes
        for child in node.nexts:
            # Recursive call to explore the child node
            found_solution = self.run_rec(child)
            if found_solution:
                return True
        
        # print(f"no solution found in {node}")
        node.clearNexts()

        return False