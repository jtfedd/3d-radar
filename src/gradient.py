from panda3d.core import Vec4

def gradient(min, max, val):
    mid = (min + max) / 2
    if (val < mid):
        return Vec4((val - min) / (mid - min), 1, 0, 1)
    return Vec4(1, 1 - ((val - mid) / (max - mid)), 0, 1)
