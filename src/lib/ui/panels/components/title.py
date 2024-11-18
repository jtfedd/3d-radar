from __future__ import annotations

from panda3d.core import NodePath, PandaNode

from lib.app.context import AppContext
from lib.ui.core.alignment import HAlign, VAlign
from lib.ui.core.components.text import Text
from lib.ui.core.constants import UIConstants
from lib.ui.panels.core.panel_component import PanelComponent


class TitleComponent(PanelComponent):
    def __init__(
        self,
        root: NodePath[PandaNode],
        ctx: AppContext,
        text: str,
    ):
        super().__init__(root)

        self.text = Text(
            root=self.root,
            font=ctx.fonts.bold,
            text=text,
            size=UIConstants.fontSizeTitle,
            x=UIConstants.panelPadding + UIConstants.panelContentWidth / 2,
            y=-UIConstants.panelTitleHeight / 2,
            hAlign=HAlign.CENTER,
            vAlign=VAlign.CENTER,
        )

    def getHeight(self) -> float:
        return UIConstants.panelTitleHeight

    def destroy(self) -> None:
        super().destroy()

        self.text.destroy()
