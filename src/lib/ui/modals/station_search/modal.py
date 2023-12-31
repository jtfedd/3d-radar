from lib.app.events import AppEvents
from lib.map.constants import RADAR_RANGE
from lib.ui.context import UIContext
from lib.ui.core.alignment import HAlign, VAlign
from lib.ui.core.components.text_input import TextInput
from lib.ui.core.constants import UIConstants
from lib.ui.core.layers import UILayer
from lib.util.events.listener import Listener

from ..core.modal import Modal
from ..core.text import ModalText
from ..core.title import ModalTitle
from .radar_button import RadarButton


class StationSearchModal(Modal):
    def __init__(self, ctx: UIContext, events: AppEvents):
        super().__init__(ctx, events, 0.8, 0.5)

        self.listener = Listener()

        self.ctx = ctx

        self.title = ModalTitle(
            ctx,
            self.root,
            "Find Radar Station",
            modalContentWidth=self.contentWidth,
        )

        self.detailText = ModalText(
            ctx,
            self.root,
            self.title.height(),
            "Search for an address or location to locate\nnearby radar stations.",
        )

        self.searchbar = TextInput(
            ctx,
            events,
            self.root,
            font=ctx.fonts.regular,
            size=UIConstants.fontSizeRegular,
            width=self.contentWidth,
            y=-(
                self.title.height()
                + self.detailText.height()
                + UIConstants.modalPadding
            ),
            hAlign=HAlign.LEFT,
            vAlign=VAlign.TOP,
            layer=UILayer.MODAL_CONTENT_INTERACTION,
        )

        self.searchbar.onCommit.listen(self.search)

    def search(self, address: str) -> None:
        print("Searching", address)

        results = self.ctx.appContext.services.locations.search(address)
        if not results or len(results) < 1:
            return

        location = results[0]
        distances = {}
        stationsInRange = []

        for radarStation in self.ctx.appContext.services.nws.radarStations.values():
            dist = location.geoPoint.dist(radarStation.geoPoint)
            if dist < RADAR_RANGE:
                distances[radarStation.stationID] = dist
                stationsInRange.append(radarStation)

        stationsInRange.sort(key=lambda s: distances[s.stationID])

        for i, radarStation in enumerate(stationsInRange):
            RadarButton(
                self.ctx,
                self.root,
                0.2 + 0.05 * i,
                self.contentWidth,
                radarStation,
                distances[radarStation.stationID],
            )

    def destroy(self) -> None:
        super().destroy()
        self.listener.destroy()

        self.title.destroy()
        self.searchbar.destroy()
