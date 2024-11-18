from __future__ import annotations

from panda3d.core import NodePath, PandaNode

from lib.app.context import AppContext
from lib.app.events import AppEvents
from lib.app.state import AppState
from lib.ui.core.alignment import HAlign, VAlign
from lib.ui.core.components.text import Text
from lib.ui.core.constants import UIConstants
from lib.ui.panels.components.text_input import PanelTextInput
from lib.ui.panels.core.panel_component import PanelComponent


class UIScaleInput(PanelComponent):
    MIN_SCALE = 50
    MAX_SCALE = 150

    def __init__(
        self,
        root: NodePath[PandaNode],
        ctx: AppContext,
        state: AppState,
        events: AppEvents,
    ):
        super().__init__(root)

        self.ctx = ctx
        self.state = state

        self.input = PanelTextInput(
            root=self.root,
            ctx=ctx,
            events=events,
            label="UI Scale:",
            initialValue=self.scaleStr(),
            inputWidth=UIConstants.panelContentWidth / 4,
            rightMargin=0.04,
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

        self.inputChangeSub = self.input.input.onCommit.listen(self.handleScaleChange)
        self.scaleChangeSub = self.state.uiScale.listen(lambda _: self.resetValue())

    def scaleStr(self) -> str:
        return str(int(self.state.uiScale.value * 100))

    def resetValue(self) -> None:
        self.input.input.setText(self.scaleStr())

    def handleScaleChange(self, value: str) -> None:
        try:
            newScale = int(value)
        except ValueError:
            self.resetValue()
            return

        if newScale < self.MIN_SCALE or newScale > self.MAX_SCALE:
            newScale = min(self.MAX_SCALE, max(self.MIN_SCALE, newScale))

        self.state.uiScale.setValue(newScale / 100.0)

    def getHeight(self) -> float:
        return UIConstants.panelInputHeight

    def destroy(self) -> None:
        super().destroy()

        self.inputChangeSub.cancel()

        self.input.destroy()
        self.percent.destroy()
