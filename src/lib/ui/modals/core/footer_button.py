from __future__ import annotations

from panda3d.core import NodePath, PandaNode

from lib.app.context import AppContext
from lib.ui.core.alignment import HAlign, VAlign
from lib.ui.core.components.button import Button, ButtonSkin
from lib.ui.core.constants import UIConstants
from lib.ui.core.layers import UILayer


class FooterButton:
    def __init__(
        self,
        ctx: AppContext,
        root: NodePath[PandaNode],
        modalWidth: float,
        text: str,
    ) -> None:
        self.button = Button(
            root=root,
            ctx=ctx,
            width=UIConstants.modalFooterButtonWidth,
            height=UIConstants.modalFooterButtonHeight,
            x=modalWidth / 2,
            hAlign=HAlign.CENTER,
            vAlign=VAlign.BOTTOM,
            bgLayer=UILayer.MODAL_CONTENT_BACKGROUND,
            contentLayer=UILayer.MODAL_CONTENT,
            interactionLayer=UILayer.MODAL_CONTENT_INTERACTION,
            textSize=UIConstants.fontSizeRegular,
            skin=ButtonSkin.ACCENT,
            text=text,
        )

    def destroy(self) -> None:
        self.button.destroy()
