from __future__ import annotations

from panda3d.core import NodePath, PandaNode, Vec4

from lib.ui.context import UIContext
from lib.ui.core.alignment import HAlign, VAlign
from lib.ui.core.colors import UIColors
from lib.ui.core.constants import UIConstants
from lib.ui.core.layers import UILayer

from .component import Component
from .image import Image
from .text import Text


class Badge(Component):
    def __init__(
        self,
        root: NodePath[PandaNode],
        ctx: UIContext,
        x: float,
        y: float,
        color: Vec4,
        text: str,
    ):
        self.bg = Image(
            root=root,
            image="assets/circle.png",
            width=UIConstants.badgeSize,
            height=UIConstants.badgeSize,
            x=x,
            y=y,
            color=color,
            layer=UILayer.CONTENT_BADGE_BACKGROUND,
        )

        self.text = Text(
            root=root,
            font=ctx.fonts.regular,
            text=text,
            x=x,
            y=y,
            size=UIConstants.fontSizeDetail,
            color=UIColors.CONTENT,
            hAlign=HAlign.CENTER,
            vAlign=VAlign.CENTER,
            layer=UILayer.CONTENT_BADGE_FOREGROUND,
        )

    def hide(self) -> None:
        self.bg.hide()
        self.text.hide()

    def show(self) -> None:
        self.bg.show()
        self.text.show()

    def setColor(self, color: Vec4) -> None:
        self.bg.updateColor(color)

    def setText(self, text: str) -> None:
        self.text.updateText(text)

    def destroy(self) -> None:
        self.bg.destroy()
        self.text.destroy()
