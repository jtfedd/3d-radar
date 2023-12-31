from lib.app.events import AppEvents
from lib.map.constants import RADAR_RANGE
from lib.ui.context import UIContext
from lib.ui.core.alignment import HAlign, VAlign
from lib.ui.core.components.button import Button, ButtonSkin
from lib.ui.core.components.scrollable_panel import ScrollablePanel
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
        super().__init__(ctx, events, 0.7, 0.4)

        self.listener = Listener()
        self.appEvents = events

        self.ctx = ctx

        self.title = ModalTitle(
            ctx,
            self.topLeft,
            "Find Radar Station",
            modalContentWidth=self.contentWidth,
        )

        self.detailText = ModalText(
            ctx,
            self.topLeft,
            self.title.height(),
            "Search for an address or location to locate\nnearby radar stations.",
        )

        self.searchbar = TextInput(
            ctx,
            events,
            self.topLeft,
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

        self.cancelButton = Button(
            root=self.bottomLeft,
            ctx=ctx,
            width=0.2,
            height=0.05,
            x=self.contentWidth / 2,
            hAlign=HAlign.CENTER,
            vAlign=VAlign.BOTTOM,
            layer=UILayer.MODAL_CONTENT_INTERACTION,
            textSize=UIConstants.fontSizeRegular,
            skin=ButtonSkin.ACCENT,
            text="Cancel",
        )

        self.listener.listen(self.cancelButton.onClick, lambda _: self.destroy())

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

        scroll = ScrollablePanel(
            root=self.topLeft,
            ctx=self.ctx,
            events=self.appEvents,
            y=-0.3,
            width=self.contentWidth + UIConstants.modalPadding,
            height=0.2,
            canvasHeight=(0.05 * len(stationsInRange)),
            hAlign=HAlign.LEFT,
            vAlign=VAlign.TOP,
            layer=UILayer.MODAL_CONTENT_INTERACTION,
            scrollbarPadding=UIConstants.modalScrollbarPadding,
        )

        for i, radarStation in enumerate(stationsInRange):
            RadarButton(
                self.ctx,
                scroll.getCanvas(),
                0.05 * i,
                self.contentWidth,
                radarStation,
                distances[radarStation.stationID],
            )

    def destroy(self) -> None:
        super().destroy()
        self.listener.destroy()

        self.title.destroy()
        self.searchbar.destroy()
        self.cancelButton.destroy()
