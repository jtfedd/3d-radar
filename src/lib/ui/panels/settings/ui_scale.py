from __future__ import annotations

from panda3d.core import NodePath, PandaNode

from lib.ui.core.alignment import HAlign, VAlign
from lib.ui.core.components.text import Text
from lib.ui.core.components.text_input import TextInput
from lib.ui.core.constants import UIConstants
from lib.ui.core.context import UIContext
from lib.ui.panels.core.panel_component import PanelComponent
from lib.util.events.event_dispatcher import EventDispatcher


class UIScaleInput(PanelComponent):
    MIN_SCALE = 25
    MAX_SCALE = 300

    def __init__(self, root: NodePath[PandaNode], ctx: UIContext, label: str):
        super().__init__(root)

        self.ctx = ctx

        self.label = Text(
            root=self.root,
            font=ctx.fonts.bold,
            text=label,
            x=UIConstants.panelPadding,
            y=-UIConstants.panelInputHeight / 2,
            hAlign=HAlign.LEFT,
            vAlign=VAlign.CENTER,
        )

        self.input = TextInput(
            ctx=ctx,
            root=self.root,
            font=ctx.fonts.regular,
            x=UIConstants.panelContentWidth + UIConstants.panelPadding - 0.04,
            y=-UIConstants.panelInputHeight / 2,
            hAlign=HAlign.RIGHT,
            vAlign=VAlign.CENTER,
            width=UIConstants.panelContentWidth / 4,
            size=UIConstants.fontSizeRegular,
            initialText=self.scaleStr(),
        )

        self.percent = Text(
            root=self.root,
            font=ctx.fonts.regular,
            text="%",
            x=UIConstants.panelContentWidth + UIConstants.panelPadding,
            y=-UIConstants.panelInputHeight / 2,
            hAlign=HAlign.RIGHT,
            vAlign=VAlign.CENTER,
        )

        self.inputChangeSub = self.input.onChange.listen(self.handleScaleChange)
        self.onScaleChange = EventDispatcher[float]()

    def scaleStr(self) -> str:
        return str(int(self.ctx.anchors.scale * 100))

    def resetValue(self) -> None:
        self.input.setText(self.scaleStr())

    def handleScaleChange(self, value: str) -> None:
        try:
            newScale = int(value)
        except ValueError:
            self.resetValue()
            return

        if newScale < self.MIN_SCALE or newScale > self.MAX_SCALE:
            newScale = min(self.MAX_SCALE, max(self.MIN_SCALE, newScale))
            self.input.setText(str(newScale))

        self.onScaleChange.send(newScale / 100.0)

    def getHeight(self) -> float:
        return UIConstants.panelInputHeight

    def destroy(self) -> None:
        super().destroy()

        self.inputChangeSub.cancel()
        self.onScaleChange.close()

        self.label.destroy()
        self.input.destroy()
        self.percent.destroy()
