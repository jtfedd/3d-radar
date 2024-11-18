from typing import List

from lib.app.context import AppContext
from lib.app.events import AppEvents
from lib.model.location import Location

from ..address_search.modal import AddressSearchModal
from ..address_search.results_component import AddressResultsComponent
from .result_component import MarkerResult


class MarkerSearchModal(AddressSearchModal):
    def __init__(self, ctx: AppContext, events: AppEvents):
        super().__init__(
            ctx,
            events,
            title="Add Marker",
            description="Search for an address to add a marker to the map.",
        )

        self.appEvents = events

        self.listener.listen(events.ui.modals.markerSelected, lambda _: self.destroy())

    def resultsLimit(self) -> int:
        return 10

    def handleSearchResult(self, results: List[Location]) -> AddressResultsComponent:
        return MarkerResult(
            self.ctx,
            self.topLeft,
            self.appEvents,
            self.headerHeight,
            results,
        )
