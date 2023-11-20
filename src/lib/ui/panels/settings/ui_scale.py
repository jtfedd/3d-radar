from __future__ import annotations

from panda3d.core import NodePath, PandaNode

from lib.ui.core.alignment import HAlign, VAlign
from lib.ui.core.components.text import Text
from lib.ui.core.components.text_input import TextInput
from lib.ui.core.config import UIConfig
from lib.ui.core.constants import UIConstants
from lib.ui.panels.core.panel_component import PanelComponent


class UIScaleInput(PanelComponent):
    MIN_SCALE = 25
    MAX_SCALE = 300

    def __init__(self, root: NodePath[PandaNode], config: UIConfig, label: str):
        super().__init__(root)

        self.config = config

        self.label = Text(
            root=self.root,
            font=config.fonts.bold,
            text=label,
            x=UIConstants.panelPadding,
            y=-UIConstants.panelInputHeight / 2,
            hAlign=HAlign.LEFT,
            vAlign=VAlign.CENTER,
        )

        self.input = TextInput(
            config=config,
            root=self.root,
            font=config.fonts.regular,
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
            font=config.fonts.regular,
            text="%",
            x=UIConstants.panelContentWidth + UIConstants.panelPadding,
            y=-UIConstants.panelInputHeight / 2,
            hAlign=HAlign.RIGHT,
            vAlign=VAlign.CENTER,
        )

        self.inputChangeSub = self.input.onChange.listen(self.handleScaleChange)

    def scaleStr(self) -> str:
        return str(int(self.config.anchors.scale * 100))

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

        self.config.setScale(newScale / 100.0)

    def getHeight(self) -> float:
        return UIConstants.panelInputHeight

    def destroy(self) -> None:
        super().destroy()

        self.inputChangeSub.cancel()

        self.label.destroy()
        self.input.destroy()
        self.percent.destroy()
