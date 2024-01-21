from __future__ import annotations

from panda3d.core import NodePath, PandaNode

from lib.app.events import AppEvents
from lib.app.state import AppState
from lib.ui.context import UIContext
from lib.ui.panels.core.panel_component import PanelComponent


class MarkersComponent(PanelComponent):
    def __init__(
        self,
        root: NodePath[PandaNode],
        ctx: UIContext,
        state: AppState,
        events: AppEvents,
    ):
        super().__init__(root)

    def getHeight(self) -> float:
        return 5

    def destroy(self) -> None:
        super().destroy()
