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
        bold: bool = False,
        italic: bool = False,
        align: HAlign = HAlign.LEFT,
    ):
        super().__init__(root)

        self.font = ctx.fonts.regular
        if bold:
            self.font = ctx.fonts.bold
        self.text = text

        xPos = UIConstants.panelPadding
        if align == HAlign.CENTER:
            xPos += UIConstants.panelContentWidth / 2
        if align == HAlign.RIGHT:
            xPos = UIConstants.panelWidth - UIConstants.panelPadding

        self.component = Text(
            root=self.root,
            font=self.font,
            text=text,
            x=xPos,
            hAlign=align,
            vAlign=VAlign.TOP,
            italic=italic,
            maxWidth=UIConstants.panelContentWidth,
        )

    def updateText(self, text: str) -> None:
        self.text = text
        self.component.updateText(text)
        self.onHeightChange.send(None)

    def getHeight(self) -> float:
        return self.component.getHeight()

    def destroy(self) -> None:
        self.component.destroy()
