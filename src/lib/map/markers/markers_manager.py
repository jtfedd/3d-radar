from typing import List

from lib.app.context import AppContext
from lib.app.events import AppEvents
from lib.app.state import AppState
from lib.model.location import Location
from lib.model.location_marker import LocationMarker
from lib.util.events.listener import Listener
from lib.util.optional import unwrap


class MarkersManager(Listener):
    def __init__(self, ctx: AppContext, state: AppState, events: AppEvents):
        super().__init__()
        self.state = state
        self.ctx = ctx

        self.reorderMarkers()

        self.listen(state.station, lambda _: self.reorderMarkers())
        self.listen(events.ui.modals.markerSelected, self.addMarker)
        self.listen(events.ui.panels.removeMarker, self.removeMarker)
        self.listen(events.ui.panels.toggleMarker, self.toggleMarker)

    def addMarker(self, location: Location) -> None:
        newMarkers = self.state.mapMarkers.value.copy()
        newMarkers.append(LocationMarker(location, True))

        self.sortMarkers(newMarkers)

        self.state.mapMarkers.setValue(newMarkers, forceSend=True)

    def removeMarker(self, toRemove: str) -> None:
        self.state.mapMarkers.setValue(
            list(
                filter(
                    lambda marker: marker.id != toRemove, self.state.mapMarkers.value
                )
            ),
            forceSend=True,
        )

    def toggleMarker(self, toToggle: str) -> None:
        newMarkers = []

        for marker in self.state.mapMarkers.value:
            if marker.id == toToggle:
                marker.visible = not marker.visible
            newMarkers.append(marker)

        self.state.mapMarkers.setValue(newMarkers, forceSend=True)

    def reorderMarkers(self) -> None:
        sortedMarkers = self.state.mapMarkers.value.copy()
        self.sortMarkers(sortedMarkers)
        self.state.mapMarkers.setValue(sortedMarkers, forceSend=True)

    def sortMarkers(self, markers: List[LocationMarker]) -> None:
        station = self.ctx.services.nws.getStation(self.state.station.value)
        if not station:
            return

        s = unwrap(station)
        markers.sort(key=lambda m: m.location.geoPoint.dist(s.geoPoint))
