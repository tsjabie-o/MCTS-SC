class Square():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f"{self.x}, {self.y}"
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    def __hash__(self) -> int:
        # prime factorisation so unique
        return hash(2**(self.x) * 3**(self.y))