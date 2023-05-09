from panda3d.core import Vec4


class Gradient:
    def __init__(self, min, max):
        self.min = min
        self.max = max

    def value(self, value):
        mid = (self.min + self.max) / 2
        if value < mid:
            return Vec4((value - self.min) / (mid - self.min), 1, 0, 1)
        return Vec4(1, 1 - ((value - mid) / (self.max - mid)), 0, 1)
