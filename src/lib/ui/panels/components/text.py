from __future__ import annotations

from panda3d.core import NodePath, PandaNode

from lib.ui.context import UIContext
from lib.ui.core.alignment import HAlign, VAlign
from lib.ui.core.components.text import Text
from lib.ui.core.constants import UIConstants
from lib.ui.panels.core.panel_component import PanelComponent


class PanelText(PanelComponent):
    def __init__(
        self,
        root: NodePath[PandaNode],
        ctx: UIContext,
        text: str,
    ):
        super().__init__(root)

        self.text = Text(
            root=self.root,
            font=ctx.fonts.regular,
            text=text,
            x=UIConstants.panelPadding,
            y=-UIConstants.panelTextHeight / 2,
            hAlign=HAlign.LEFT,
            vAlign=VAlign.CENTER,
        )

    def getHeight(self) -> float:
        return UIConstants.panelTextHeight

    def destroy(self) -> None:
        self.text.destroy()
