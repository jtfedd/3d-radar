from typing import Tuple

from panda3d.core import NodePath, PandaNode


class UIAnchors:
    def __init__(self, root: NodePath[PandaNode], windowSize: Tuple[int, int]):
        self.topLeft = root.attachNewNode("top-left")
        self.topCenter = root.attachNewNode("top-center")
        self.topRight = root.attachNewNode("top-right")
        self.centerLeft = root.attachNewNode("center-left")
        self.center = root.attachNewNode("center")
        self.centerRight = root.attachNewNode("center-right")
        self.bottomLeft = root.attachNewNode("bottom-left")
        self.bottomCenter = root.attachNewNode("bottom-center")
        self.bottomRight = root.attachNewNode("bottom-right")

        self.update(windowSize)

    def update(self, windowSize: Tuple[int, int]) -> None:
        width = windowSize[0]
        height = windowSize[1]

        self.topLeft.setPos(0, 0, 0)
        self.topCenter.setPos(width / 2, 0, 0)
        self.topRight.setPos(width, 0, 0)
        self.centerLeft.setPos(0, 0, height / 2)
        self.center.setPos(width / 2, 0, height / 2)
        self.centerRight.setPos(width, 0, height / 2)
        self.bottomLeft.setPos(0, 0, height)
        self.bottomCenter.setPos(width / 2, 0, height)
        self.bottomRight.setPos(width, 0, height)

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
