from __future__ import annotations

from typing import Dict

from panda3d.core import NodePath, PandaNode

from lib.app.events import AppEvents
from lib.app.state import AppState
from lib.ui.context import UIContext
from lib.ui.core.constants import UIConstants
from lib.ui.panels.core.panel_component import PanelComponent

from .marker_item import MarkerItem


class MarkersComponent(PanelComponent):
    def __init__(
        self,
        root: NodePath[PandaNode],
        ctx: UIContext,
        state: AppState,
        events: AppEvents,
    ):
        super().__init__(root)
        self.ctx = ctx
        self.state = state
        self.events = events

        self.contentHeight = 0.0
        self.markerItems: Dict[str, MarkerItem] = {}

        self.generateMarkers()
        self.markerSub = state.mapMarkers.listen(lambda _: self.generateMarkers())

    def clearMarkers(self) -> None:
        for item in self.markerItems.values():
            item.destroy()
        self.markerItems.clear()

    def generateMarkers(self) -> None:
        newMarkerItems: Dict[str, MarkerItem] = {}

        top = 0.0
        for marker in self.state.mapMarkers.value:
            if marker.id in self.markerItems:
                item = self.markerItems[marker.id]
                del self.markerItems[marker.id]

                item.update(top, marker.visible)
            else:
                item = MarkerItem(self.root, self.ctx, self.events, marker, top)

            newMarkerItems[marker.id] = item

            top += item.height()
            top += UIConstants.markerItemPadding

        self.clearMarkers()
        self.markerItems = newMarkerItems

        self.contentHeight = top - UIConstants.markerItemPadding
        self.onHeightChange.send(None)

    def getHeight(self) -> float:
        return self.contentHeight

    def destroy(self) -> None:
        super().destroy()

        self.clearMarkers()
        self.markerSub.cancel()
