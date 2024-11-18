from __future__ import annotations

from panda3d.core import NodePath, PandaNode

from lib.app.context import AppContext
from lib.ui.core.alignment import HAlign, VAlign
from lib.ui.core.components.text import Text
from lib.ui.core.constants import UIConstants
from lib.ui.core.layers import UILayer


class ModalText:
    def __init__(
        self,
        ctx: AppContext,
        root: NodePath[PandaNode],
        top: float,
        text: str,
        fontSize: float = UIConstants.fontSizeRegular,
    ):
        self.ctx = ctx
        self.numLines = len(text.split("\n"))

        self.fontSize = fontSize

        self.text = Text(
            root=root,
            font=ctx.fonts.regular,
            text=text,
            vAlign=VAlign.TOP,
            y=-top,
            size=fontSize,
            layer=UILayer.MODAL_CONTENT,
            hAlign=HAlign.LEFT,
        )

    def height(self) -> float:
        return self.ctx.fonts.regular.getLineHeight() * self.fontSize * self.numLines

    def destroy(self) -> None:
        self.text.destroy()
