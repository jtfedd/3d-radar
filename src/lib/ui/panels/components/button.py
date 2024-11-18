from __future__ import annotations

from panda3d.core import NodePath, PandaNode

from lib.app.context import AppContext
from lib.ui.core.alignment import HAlign, VAlign
from lib.ui.core.components.button import Button, ButtonSkin
from lib.ui.core.constants import UIConstants
from lib.ui.panels.core.panel_component import PanelComponent


class PanelButton(PanelComponent):
    def __init__(
        self,
        root: NodePath[PandaNode],
        ctx: AppContext,
        text: str,
    ):
        super().__init__(root)

        self.button = Button(
            root=self.root,
            ctx=ctx,
            x=UIConstants.panelPadding,
            width=UIConstants.panelContentWidth,
            height=UIConstants.panelInputHeight,
            hAlign=HAlign.LEFT,
            vAlign=VAlign.TOP,
            text=text,
            skin=ButtonSkin.ACCENT,
        )

    def getHeight(self) -> float:
        return UIConstants.panelInputHeight

    def destroy(self) -> None:
        super().destroy()

        self.button.destroy()
