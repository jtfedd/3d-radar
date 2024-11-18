from __future__ import annotations

from panda3d.core import NodePath, PandaNode

from lib.app.context import AppContext
from lib.ui.core.alignment import HAlign, VAlign
from lib.ui.core.components.text import Text
from lib.ui.core.constants import UIConstants
from lib.ui.core.layers import UILayer


class ModalTitle:
    def __init__(
        self,
        ctx: AppContext,
        root: NodePath[PandaNode],
        text: str,
        modalContentWidth: float = 0,
    ):
        self.text = Text(
            root=root,
            font=ctx.fonts.bold,
            text=text,
            vAlign=VAlign.TOP,
            size=UIConstants.fontSizeHeader,
            layer=UILayer.MODAL_CONTENT,
            x=modalContentWidth / 2,
            hAlign=HAlign.CENTER,
        )

    def height(self) -> float:
        return UIConstants.modalTitleHeight

    def destroy(self) -> None:
        self.text.destroy()
