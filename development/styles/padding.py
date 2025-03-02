class Padding:
    def __init__(self, all=None, top=None, right=None, bottom=None, left=None):
        if all is not None:
            self.top = self.right = self.bottom = self.left = all
        else:
            self.top = top or 0
            self.right = right or 0
            self.bottom = bottom or 0
            self.left = left or 0

    def __str__(self):
        return f"{self.top}px {self.right}px {self.bottom}px {self.left}px"
