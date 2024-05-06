from __future__ import annotations

from typing import Dict

from panda3d.core import NodePath, PandaNode

from lib.app.context import AppContext
from lib.app.state import AppState
from lib.util.events.listener import Listener

from .map_marker import MapMarker


class MarkersRenderer(Listener):
    def __init__(
        self,
        ctx: AppContext,
        state: AppState,
        root: NodePath[PandaNode],
    ) -> None:
        super().__init__()

        self.ctx = ctx
        self.state = state
        self.root = root

        self.markers: Dict[str, MapMarker] = {}

        self.generateMarkers()
        self.listen(state.mapMarkers, lambda _: self.generateMarkers())

    def clearMarkers(self) -> None:
        for item in self.markers.values():
            item.destroy()
        self.markers.clear()

    def generateMarkers(self) -> None:
        newMarkers: Dict[str, MapMarker] = {}

        for marker in self.state.mapMarkers.value:
            if marker.id in self.markers:
                item = self.markers[marker.id]
                del self.markers[marker.id]

                item.updateVisiblity(marker.visible)
            else:
                item = MapMarker(self.ctx, self.state, self.root, marker)

            newMarkers[marker.id] = item

        self.clearMarkers()
        self.markers = newMarkers

    def destroy(self) -> None:
        super().destroy()

        self.clearMarkers()
