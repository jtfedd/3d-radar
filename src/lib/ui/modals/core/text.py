from __future__ import annotations

from panda3d.core import NodePath, PandaNode

from lib.ui.context import UIContext
from lib.ui.core.alignment import HAlign, VAlign
from lib.ui.core.components.text import Text
from lib.ui.core.constants import UIConstants
from lib.ui.core.layers import UILayer


class ModalText:
    def __init__(
        self,
        ctx: UIContext,
        root: NodePath[PandaNode],
        top: float,
        text: str,
    ):
        self.ctx = ctx
        self.numLines = len(text.split("\n"))

        self.text = Text(
            root=root,
            font=ctx.fonts.regular,
            text=text,
            vAlign=VAlign.TOP,
            y=-top,
            size=UIConstants.fontSizeRegular,
            layer=UILayer.MODAL_CONTENT,
            hAlign=HAlign.LEFT,
        )

    def height(self) -> float:
        return (
            self.ctx.fonts.regular.getLineHeight()
            * UIConstants.fontSizeRegular
            * self.numLines
        )

    def destroy(self) -> None:
        self.text.destroy()