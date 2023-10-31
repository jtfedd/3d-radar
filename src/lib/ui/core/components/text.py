from __future__ import annotations

from panda3d.core import DynamicTextFont, NodePath, PandaNode, TextNode, Vec4

from lib.ui.core.layers import UILayer


class Text:
    def __init__(
        self,
        root: NodePath[PandaNode],
        text: str,
        x: float,
        y: float,
        color: Vec4,
        font: DynamicTextFont,
        layer: UILayer = UILayer.CONTENT,
    ):
        self.root = root

        self.text = TextNode("text")
        self.text.setText(text)
        self.text.setTextColor(color)
        self.text.setFont(font)

        print("width", self.text.getWidth())
        print("height", self.text.getHeight())

        node = self.text.generate()
        self.nodePath = root.attachNewNode(node, sort=layer.value)

        xPos = int(x - (self.text.getWidth() / 2))
        yPos = int(y - 18)

        self.nodePath.setPos(xPos + 0.5, 0, yPos + 0.5)

    def update(self, x: float, y: float, size: float) -> None:
        self.nodePath.setPos(x, 0, y)
        self.nodePath.setScale(size)

    def updateText(self, text: str) -> None:
        self.text.setText(text)

    def destroy(self) -> None:
        self.nodePath.removeNode()
