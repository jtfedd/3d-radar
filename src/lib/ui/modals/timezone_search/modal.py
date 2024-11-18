from typing import List

from lib.app.context import AppContext
from lib.app.events import AppEvents
from lib.model.location import Location

from ..address_search.modal import AddressSearchModal
from ..address_search.results_component import AddressResultsComponent
from .result_component import TimezoneResult


class TimezoneSearchModal(AddressSearchModal):
    def __init__(self, ctx: AppContext, events: AppEvents):
        super().__init__(
            ctx,
            events,
            title="Timezone Lookup",
            description="Search for an address or location to\ndetermine its timezone.",
        )

        self.appEvents = events

        self.listener.listen(
            events.ui.modals.timeZoneSelected, lambda _: self.destroy()
        )

    def resultsLimit(self) -> int:
        return 1

    def handleSearchResult(self, results: List[Location]) -> AddressResultsComponent:
        location = results[0]

        tz = self.ctx.timeUtil.findTimezone(location.geoPoint)

        return TimezoneResult(
            self.ctx, self.topLeft, self.appEvents, self.headerHeight, location, tz
        )
