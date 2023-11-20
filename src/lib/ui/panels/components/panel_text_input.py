from __future__ import annotations

from panda3d.core import NodePath, PandaNode

from lib.ui.core.alignment import HAlign, VAlign
from lib.ui.core.components.text import Text
from lib.ui.core.components.text_input import TextInput
from lib.ui.core.config import UIConfig
from lib.ui.core.constants import UIConstants
from lib.ui.panels.core.panel_component import PanelComponent


class PanelTextInput(PanelComponent):
    def __init__(self, root: NodePath[PandaNode], config: UIConfig, label: str):
        super().__init__(root)

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
            x=UIConstants.panelContentWidth + UIConstants.panelPadding,
            y=-UIConstants.panelInputHeight / 2,
            hAlign=HAlign.RIGHT,
            vAlign=VAlign.CENTER,
            width=UIConstants.panelContentWidth / 2,
            size=UIConstants.fontSizeRegular,
        )

    def getHeight(self) -> float:
        return UIConstants.panelInputHeight

    def destroy(self) -> None:
        super().destroy()

        self.label.destroy()
        self.input.destroy()
