from __future__ import annotations

from direct.gui.OnscreenText import OnscreenText
from panda3d.core import DynamicTextFont, NodePath, PandaNode, TextNode, Vec4

from lib.ui.core.alignment import HAlign, VAlign
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
        font: DynamicTextFont,
        hAlign: HAlign = HAlign.LEFT,
        layer: UILayer = UILayer.CONTENT,
    ):
        self.root = root

        align = TextNode.ALeft
        if hAlign == HAlign.CENTER:
            align = TextNode.ACenter
        elif hAlign == HAlign.RIGHT:
            align = TextNode.ARight

        self.text = OnscreenText(
            parent=root,
            text=text,
            pos=(x, y),
            scale=size,
            fg=color,
            font=font,
            sort=layer.value,
            align=align,  # type:ignore
        )

    def updateText(self, text: str) -> None:
        self.text.setText(text)

    def destroy(self) -> None:
        self.text.destroy()
