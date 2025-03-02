class BorderRadius:
    def __init__(self, all=None, top_left=None, top_right=None, bottom_right=None, bottom_left=None):
        if all is not None:
            self.top_left = self.top_right = self.bottom_right = self.bottom_left = all
        else:
            self.top_left = top_left or 0
            self.top_right = top_right or 0
            self.bottom_right = bottom_right or 0
            self.bottom_left = bottom_left or 0

    def __str__(self):
        return f"{self.top_left}px {self.top_right}px {self.bottom_right}px {self.bottom_left}px"
