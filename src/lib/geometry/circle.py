import math

from panda3d.core import GeomNode, Vec3

from .segments import Segments


def drawCircle(steps: int = 720) -> GeomNode:
    stepSize = (math.pi * 2) / steps

    segments = Segments(steps)
    segments.addLoop(
        [
            Vec3(
                math.cos(i * stepSize),
                math.sin(i * stepSize),
                0,
            )
            for i in range(steps)
        ]
    )
    return segments.create()
