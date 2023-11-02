from __future__ import annotations

from direct.showbase.DirectObject import DirectObject
from direct.showbase.ShowBase import ShowBase


class UIAnchors(DirectObject):
    def __init__(self, base: ShowBase, scale: float):
        self.base = base
        self.scale = scale

        root = base.aspect2dp

        self.center = root.attachNewNode("center")

        self.top = root.attachNewNode("top")
        self.bottom = root.attachNewNode("bottom")
        self.left = root.attachNewNode("left")
        self.right = root.attachNewNode("right")

        self.topLeft = self.top.attachNewNode("top-left")
        self.topCenter = self.top.attachNewNode("top-center")
        self.topRight = self.top.attachNewNode("top-right")

        self.bottomLeft = self.bottom.attachNewNode("bottom-left")
        self.bottomCenter = self.bottom.attachNewNode("bottom-center")
        self.bottomRight = self.bottom.attachNewNode("bottom-right")

        self.leftTop = self.left.attachNewNode("left-top")
        self.leftCenter = self.left.attachNewNode("left-center")
        self.leftBottom = self.left.attachNewNode("left-bottom")

        self.rightTop = self.right.attachNewNode("right-top")
        self.rightCenter = self.right.attachNewNode("right-center")
        self.rightBottom = self.right.attachNewNode("right-bottom")

        self.update()
        self.accept("window-event", lambda _: self.update())

    def update(self) -> None:
        aspectRatio = self.base.getAspectRatio()

        self.center.setPos(0, 0, 0)

        self.top.setPos(0, 0, 1)
        self.bottom.setPos(0, 0, -1)
        self.left.setPos(-aspectRatio, 0, 0)
        self.right.setPos(0, 0, aspectRatio)

        self.topLeft.setPos(-aspectRatio, 0, 0)
        self.topCenter.setPos(0, 0, 0)
        self.topRight.setPos(aspectRatio, 0, 0)

        self.bottomLeft.setPos(-aspectRatio, 0, 0)
        self.bottomCenter.setPos(0, 0, 0)
        self.bottomRight.setPos(aspectRatio, 0, 0)

        self.leftTop.setPos(0, 0, 1)
        self.leftCenter.setPos(0, 0, 0)
        self.leftBottom.setPos(0, 0, -1)

        self.rightTop.setPos(0, 0, 1)
        self.rightCenter.setPos(0, 0, 0)
        self.rightBottom.setPos(0, 0, -1)

        self.updateScale(self.scale)

    def updateScale(self, newScale: float) -> None:
        self.scale = newScale

        self.center.setScale(self.scale)

        self.topLeft.setScale(self.scale)
        self.topCenter.setScale(self.scale)
        self.topRight.setScale(self.scale)

        self.bottomLeft.setScale(self.scale)
        self.bottomCenter.setScale(self.scale)
        self.bottomRight.setScale(self.scale)

        self.leftTop.setScale(self.scale)
        self.leftCenter.setScale(self.scale)
        self.leftBottom.setScale(self.scale)

        self.rightTop.setScale(self.scale)
        self.rightCenter.setScale(self.scale)
        self.rightBottom.setScale(self.scale)

    def destroy(self) -> None:
        self.center.removeNode()

        self.top.removeNode()
        self.bottom.removeNode()
        self.left.removeNode()
        self.right.removeNode()

        self.topLeft.removeNode()
        self.topCenter.removeNode()
        self.topRight.removeNode()

        self.bottomLeft.removeNode()
        self.bottomCenter.removeNode()
        self.bottomRight.removeNode()

        self.leftTop.removeNode()
        self.leftCenter.removeNode()
        self.leftBottom.removeNode()

        self.rightTop.removeNode()
        self.rightCenter.removeNode()
        self.rightBottom.removeNode()

        self.ignoreAll()
