from typing import Tuple

from direct.showbase.ShowBase import ShowBase


class UIAnchors:
    def __init__(
        self,
        base: ShowBase,
        windowSize: Tuple[int, int],
    ):
        self.topLeft = base.pixel2d.attachNewNode("top-left")
        self.topCenter = base.pixel2d.attachNewNode("top-center")
        self.topRight = base.pixel2d.attachNewNode("top-right")
        self.centerLeft = base.pixel2d.attachNewNode("center-left")
        self.center = base.pixel2d.attachNewNode("center")
        self.centerRight = base.pixel2d.attachNewNode("center-right")
        self.bottomLeft = base.pixel2d.attachNewNode("bottom-left")
        self.bottomCenter = base.pixel2d.attachNewNode("bottom-center")
        self.bottomRight = base.pixel2d.attachNewNode("bottom-right")

        self.update(windowSize)

    def update(self, windowSize: Tuple[int, int]) -> None:
        width = windowSize[0]
        height = windowSize[1]

        self.topLeft.setPos(0, 0, 0)
        self.topCenter.setPos(width / 2, 0, 0)
        self.topRight.setPos(width, 0, 0)
        self.centerLeft.setPos(0, 0, -height / 2)
        self.center.setPos(width / 2, 0, -height / 2)
        self.centerRight.setPos(width, 0, -height / 2)
        self.bottomLeft.setPos(0, 0, -height)
        self.bottomCenter.setPos(width / 2, 0, -height)
        self.bottomRight.setPos(width, 0, -height)

    def destroy(self) -> None:
        self.topLeft.removeNode()
        self.topCenter.removeNode()
        self.topRight.removeNode()
        self.centerLeft.removeNode()
        self.center.removeNode()
        self.centerRight.removeNode()
        self.bottomLeft.removeNode()
        self.bottomCenter.removeNode()
        self.bottomRight.removeNode()
