from __future__ import annotations

from direct.gui.OnscreenText import OnscreenText
from panda3d.core import NodePath, PandaNode, TextNode, Vec4

from lib.ui.core.layers import UILayer


class Text:
    def __init__(
        self,
        root: NodePath[PandaNode],
        text: str,
        x: float,
        y: float,
        size: float,
        color: Vec4,
        layer: UILayer = UILayer.CONTENT,
    ):
        self.text = OnscreenText(
            text=text,
            pos=(x, y),
            scale=size,
            fg=color,
            sort=layer.value,
            parent=root,
            align=TextNode.ACenter,
        )

    def update(self, x: float, y: float, size: float) -> None:
        self.text.setPos(x, y)
        self.text.setScale(size)

    def updateText(self, text: str) -> None:
        self.text.setText(text)

    def destroy(self) -> None:
        self.text.destroy()
