class BlockingInfoDS:
    def __init__(self):
        self.hor = Node()
        self.vert = Node()
        self.dig1 = Node()
        self.dig2 = Node()
        self.possible_knight_attacks = 0

    def remove(self):
        # Remove square from all its linked lists structures
        # Happens when the square becomes unoccupied after a move
        for node in [self.hor, self.vert, self.dig1, self.dig2]:
            if node.prev is not None:
                node.prev.next = node.next
            if node.next is not None:
                node.next.prev = node.prev

    def add_back(self):
        # Add square back to its linked list structures
        # Happens when a move is made undone, after a backtrack
        for node in [self.hor, self.vert, self.dig1, self.dig2]:
            if node.prev is not None:
                node.prev.next = node
            if node.next is not None:
                node.next.prev = node

    def empty(self):
        # Check whether square is completely secluded, by checking if there are other squares in its linked list structures
        empty = True
        for node in [self.hor, self.vert, self.dig1, self.dig2]:
            if node.prev is not None:
                empty = False
            if node.next is not None:
                empty = False
        return empty


class Node:
    def __init__(self):
        self.next = None
        self.prev = None
