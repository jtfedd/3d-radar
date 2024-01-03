from typing import List

from lib.app.events import AppEvents
from lib.model.location import Location
from lib.ui.context import UIContext

from ..address_search.modal import AddressSearchModal
from ..address_search.results_component import AddressResultsComponent
from .result_component import TimezoneResult


class TimezoneSearchModal(AddressSearchModal):
    TITLE = "Timezone Lookup"
    DESC = "Search for an address or location to\ndetermine its timezone."

    def __init__(self, ctx: UIContext, events: AppEvents):
        super().__init__(
            ctx,
            events,
            title=self.TITLE,
            description=self.DESC,
        )

        self.appEvents = events

        self.listener.listen(
            events.ui.modals.timeZoneSelected, lambda _: self.destroy()
        )

    def resultsLimit(self) -> int:
        return 1

    def handleSearchResult(self, results: List[Location]) -> AddressResultsComponent:
        location = results[0]

        tz = self.ctx.appContext.timeUtil.findTimezone(location.geoPoint)

        return TimezoneResult(
            self.ctx,
            self.topLeft,
            self.appEvents,
            self.headerHeight,
            location,
            tz,
        )
