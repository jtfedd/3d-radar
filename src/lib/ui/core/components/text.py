from __future__ import annotations

from direct.gui.OnscreenText import OnscreenText
from panda3d.core import DynamicTextFont, NodePath, PandaNode, TextNode, Vec4

from lib.ui.core.alignment import HAlign, VAlign
from lib.ui.core.colors import UIColors
from lib.ui.core.constants import UIConstants
from lib.ui.core.layers import UILayer


class Text:
    def __init__(
        self,
        root: NodePath[PandaNode],
        font: DynamicTextFont,
        text: str,
        x: float = 0,
        y: float = 0,
        size: float = UIConstants.fontSizeRegular,
        color: Vec4 = UIColors.WHITE,
        hAlign: HAlign = HAlign.LEFT,
        vAlign: VAlign = VAlign.BASELINE,
        layer: UILayer = UILayer.CONTENT,
    ):
        self.root = root

        align = TextNode.ALeft
        if hAlign == HAlign.CENTER:
            align = TextNode.ACenter
        elif hAlign == HAlign.RIGHT:
            align = TextNode.ARight

        yPos = y
        if vAlign == VAlign.TOP:
            yPos -= size
        elif vAlign == VAlign.CENTER:
            yPos -= size / 3.5
        elif vAlign == VAlign.BOTTOM:
            yPos += size * (font.line_height - 1)

        self.text = OnscreenText(
            parent=root,
            text=text,
            pos=(x, yPos),
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
