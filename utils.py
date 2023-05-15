from bids import BlockingInfoDS

class Square():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.bids = BlockingInfoDS()

    def alignHor(self, s):
        # Check whether two squares align horizontally on the board
        return self.y == s.y and (self.bids.hor.next == s.bids.hor or self.bids.hor.prev == s.bids.hor)
        
    def alignVer(self, s):
        # Check whether two squares align vertically on the board
        return self.x == s.x and (self.bids.vert.next == s.bids.vert or self.bids.vert.prev == s.bids.vert)

    def alignDia1(self, s):
        # Check whether two squares align diagonally on the board
        return self.x + self.y == s.x + s.y and (self.bids.dig1.next == s.bids.dig1 or self.bids.dig1.prev == s.bids.dig1)

    def alignDia2(self, s):
        # Check whether two squares align diagonally on the board
        return self.x - self.y == s.x - s.y and (self.bids.dig2.next == s.bids.dig2 or self.bids.dig2.prev == s.bids.dig2)