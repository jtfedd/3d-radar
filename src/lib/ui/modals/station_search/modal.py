from typing import List

from lib.app.events import AppEvents
from lib.map.constants import RADAR_RANGE
from lib.model.location import Location
from lib.ui.context import UIContext

from ..address_search.error_result_component import ErrorResultComponent
from ..address_search.modal import AddressSearchModal
from ..address_search.results_component import AddressResultsComponent
from .result_component import RadarStationsResult


class StationSearchModal(AddressSearchModal):
    TITLE = "Find Radar Station"
    DESC = "Search for an address or location to locate\nnearby radar stations."

    def __init__(self, ctx: UIContext, events: AppEvents):
        super().__init__(
            ctx,
            events,
            title=self.TITLE,
            description=self.DESC,
        )

        self.appEvents = events

    def resultsLimit(self) -> int:
        return 1

    def handleSearchResult(self, results: List[Location]) -> AddressResultsComponent:
        location = results[0]
        distances = {}
        stationsInRange = []

        for radarStation in self.ctx.appContext.services.nws.radarStations.values():
            dist = location.geoPoint.dist(radarStation.geoPoint)
            if dist < RADAR_RANGE:
                distances[radarStation.stationID] = dist
                stationsInRange.append(radarStation)

        if len(stationsInRange) == 0:
            return ErrorResultComponent(
                self.ctx,
                self.topLeft,
                self.headerHeight,
                "No nearby radar stations",
            )

        stationsInRange.sort(key=lambda s: distances[s.stationID])

        return RadarStationsResult(
            self.ctx,
            self.topLeft,
            self.appEvents,
            self.headerHeight,
            stationsInRange,
            distances,
        )
