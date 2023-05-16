class Utils():
    @classmethod
    def alignVer(cls, s1, s2, ps, square):

        # check if same x coordinate
        if s1.x != s2.x:
            return False

        # check if any piece in between
        y_low = min(s1.y, s2.y)
        y_high = max(s1.y, s2.y)
        for p in self.ps:
            if self.square[p].x == s1.x:
                if y_low < self.square[p].y < y_high:
                    return False
        return True

    def alignHor(self, p1, p2):
        s1 = self.square[p1]
        s2 = self.square[p2]
        
        # check if same y coordinate
        if s1.y != s2.y:
            return False

        # check if any piece in between
        x_low = min(s1.x, s2.x)
        x_high = max(s1.x, s2.x)
        for p in self.ps:
            if self.square[p].y == s1.y:
                if x_low < self.square[p].x < x_high:
                    return False
        return True

    def alignDia(self, p1, p2):
        s1 = self.square[p1]
        s2 = self.square[p2]
        x_low = min(s1.x, s2.x)
        x_high = max(s1.x, s2.x)

        # check alignment 1 (left-up to right-down)
        align1 = s1.x + s1.y == s2.x + s2.y

        # check alignment 2 (left-down to right-up)
        align2 = s1.x - s1.y == s2.x - s2.y

        # check if any piece in between p1 and p2 on the diagonal
        if align1 or align2:
            for p in self.ps:
                s = self.square[p]
                if (align1 and s.x + s.y == s2.x + s2.y) or (align2 and s.x - s.y == s2.x - s2.y):
                    if x_low < s.x < x_high:
                        # piece in between
                        return False
            return True

        # they are not on the same diagonal
        return False