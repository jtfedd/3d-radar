from panda3d.core import Vec4


class Gradient:
    def __init__(self, gradientMin: float, gradientMax: float) -> None:
        self.gradientMin = gradientMin
        self.gradientMax = gradientMax

    def value(self, value: float) -> Vec4:
        mid = (self.gradientMin + self.gradientMax) / 2
        if value < mid:
            return Vec4((value - self.gradientMin) / (mid - self.gradientMax), 1, 0, 1)
        return Vec4(1, 1 - ((value - mid) / (self.gradientMax - mid)), 0, 1)
