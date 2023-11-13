from __future__ import annotations

from panda3d.core import NodePath, PandaNode

from lib.ui.core.alignment import VAlign
from lib.ui.core.components.text import Text
from lib.ui.core.config import UIConfig
from lib.ui.core.constants import UIConstants
from lib.ui.panels.components.panel_component import PanelComponent


class TextComponent(PanelComponent):
    def __init__(self, root: NodePath[PandaNode], config: UIConfig):
        super().__init__(root)

        self.text = Text(
            root=self.root,
            font=config.fonts.medium,
            text="Hello, World",
            x=UIConstants.panelPadding,
            y=-0.05,
            vAlign=VAlign.CENTER,
        )

    def getHeight(self) -> float:
        return 0.1

    def destroy(self) -> None:
        self.text.destroy()

        super().destroy()
