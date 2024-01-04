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

        self.font = ctx.fonts.regular
        self.text = text

        self.component = Text(
            root=self.root,
            font=ctx.fonts.regular,
            text=text,
            x=UIConstants.panelPadding,
            hAlign=HAlign.LEFT,
            vAlign=VAlign.TOP,
        )

    def updateText(self, text: str) -> None:
        self.text = text
        self.component.updateText(text)
        self.onHeightChange.send(None)

    def getHeight(self) -> float:
        return (
            len(self.text.split("\n"))
            * self.font.getLineHeight()
            * UIConstants.fontSizeRegular
        )

    def destroy(self) -> None:
        self.component.destroy()
