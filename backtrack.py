from mcts import Node

class Backtrack():
    """A basic implementation of Backtracking
    
    This should be roughly the same implementation as that of Verlaan
    """
    def setup(self, s0, h=None):
        self.s0 = s0
        self.h = h
        self.root = Node(self.s0, None, None)
    
    def run(self):
        sol = []
        if not self.run_rec(self.root, sol):
            print("no solution found")
            return None
        return sol

    def run_rec(self, node: Node, solution):
        # Add the current node to the solution
        solution.append(node)

        # Base case: If the current node is the goal, return True
        if node.getValue() == 1:
            return True
        
        node.getNexts()
        if self.h is not None:
            # order the .nexts list by heuristic value
            node.nexts = {next: node.s.heuristic(self.h, next.prevAction[0], next.prevAction[1]) for next in node.nexts}
            node.nexts = [node[0] for node in sorted(node.nexts.items(), key=lambda x:x[1])]


        # Iterate over the children nodes
        for child in node.nexts:
            # Recursive call to explore the child node
            found_solution = self.run_rec(child, solution)
            if found_solution:
                return True

        # If no child node leads to a solution, backtrack by removing the current node from the solution
        solution.remove(node)
        return False