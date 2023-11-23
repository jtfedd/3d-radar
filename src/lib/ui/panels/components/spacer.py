from __future__ import annotations

from panda3d.core import NodePath, PandaNode

from lib.ui.core.constants import UIConstants
from lib.ui.panels.core.panel_component import PanelComponent


class SpacerComponent(PanelComponent):
    def __init__(
        self,
        root: NodePath[PandaNode],
        space: float = UIConstants.panelPadding,
    ):
        super().__init__(root)

        self.space = space

    def getHeight(self) -> float:
        return self.space
