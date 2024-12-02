from __future__ import annotations

from panda3d.core import DynamicTextFont, NodePath, PandaNode, TextNode, Vec4

from lib.ui.core.alignment import HAlign, VAlign
from lib.ui.core.colors import UIColors
from lib.ui.core.constants import UIConstants
from lib.ui.core.layers import UILayer
from lib.ui.core.util import correctYForTextAlignment, horizontalAlignToTextNodeAlign

from .component import Component


class Text(Component):
    def __init__(
        self,
        root: NodePath[PandaNode],
        font: DynamicTextFont,
        text: str,
        x: float = 0,
        y: float = 0,
        size: float = UIConstants.fontSizeRegular,
        color: Vec4 = UIColors.CONTENT,
        hAlign: HAlign = HAlign.LEFT,
        vAlign: VAlign = VAlign.BASELINE,
        layer: UILayer = UILayer.CONTENT,
        maxWidth: float = -1,
        italic: bool = False,
    ):
        self.root = root
        self.size = size

        yPos = correctYForTextAlignment(y, font, size, vAlign)

        slant = 0.0
        if italic:
            slant = 0.25

        self.text = TextNode("text")
        self.text.setFont(font)
        self.text.setText(text)
        self.text.setTextColor(color)
        if maxWidth > 0:
            self.text.setWordwrap(maxWidth / size)
        self.text.setAlign(horizontalAlignToTextNodeAlign(hAlign))  # type:ignore
        self.text.setSlant(slant)

        self.textNP = self.root.attachNewNode(self.text)
        self.textNP.setPos(x, 0, yPos)
        self.textNP.setScale(size)

        self.textNP.setBin("fixed", layer.value)

    def hide(self) -> None:
        self.textNP.hide()

    def show(self) -> None:
        self.textNP.show()

    def updateText(self, text: str) -> None:
        self.text.setText(text)

    def updateColor(self, color: Vec4) -> None:
        self.text.setTextColor(color)

    def getHeight(self) -> float:
        return self.text.getHeight() * self.size

    def getWidth(self) -> float:
        return self.text.getWidth() * self.size

    def destroy(self) -> None:
        self.textNP.removeNode()
