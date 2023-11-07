from __future__ import annotations

from direct.showbase.DirectObject import DirectObject
from direct.showbase.ShowBase import ShowBase


class UIAnchors(DirectObject):
    def __init__(self, base: ShowBase, scale: float):
        self.base = base
        self.scale = scale
        self.aspectRatio = -1.0

        root = base.aspect2dp

        self.center = root.attachNewNode("center")

        self.top = root.attachNewNode("top")
        self.bottom = root.attachNewNode("bottom")
        self.left = root.attachNewNode("left")
        self.right = root.attachNewNode("right")

        self.topLeft = root.attachNewNode("top-left")
        self.topRight = root.attachNewNode("top-right")
        self.bottomLeft = root.attachNewNode("bottom-left")
        self.bottomRight = root.attachNewNode("bottom-right")

        self.update()
        self.accept("window-event", lambda _: self.update())

    def update(self) -> None:
        aspectRatio = self.base.getAspectRatio()
        if aspectRatio == self.aspectRatio:
            return

        self.aspectRatio = aspectRatio

        width = aspectRatio
        height = 1.0

        if aspectRatio < 1.0:
            width = 1.0
            height = 1 / aspectRatio

        self.center.setPos(0, 0, 0)

        self.top.setPos(0, 0, height)
        self.bottom.setPos(0, 0, -height)
        self.left.setPos(-width, 0, 0)
        self.right.setPos(0, 0, width)

        self.topLeft.setPos(-width, 0, height)
        self.topRight.setPos(width, 0, height)
        self.bottomLeft.setPos(-width, 0, -height)
        self.bottomRight.setPos(width, 0, -height)

        self.updateScale(self.scale)

    def updateScale(self, newScale: float) -> None:
        self.scale = newScale

        self.center.setScale(self.scale)

        self.top.setScale(self.scale)
        self.bottom.setScale(self.scale)
        self.left.setScale(self.scale)
        self.right.setScale(self.scale)

        self.topLeft.setScale(self.scale)
        self.topRight.setScale(self.scale)
        self.bottomLeft.setScale(self.scale)
        self.bottomRight.setScale(self.scale)

    def destroy(self) -> None:
        self.center.removeNode()

        self.top.removeNode()
        self.bottom.removeNode()
        self.left.removeNode()
        self.right.removeNode()

        self.topLeft.removeNode()
        self.topRight.removeNode()

        self.bottomLeft.removeNode()
        self.bottomRight.removeNode()

        self.ignoreAll()
