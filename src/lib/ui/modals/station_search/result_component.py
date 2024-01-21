from __future__ import annotations

from typing import Dict, List

from panda3d.core import NodePath, PandaNode

from lib.app.events import AppEvents
from lib.model.location import Location
from lib.model.radar_station import RadarStation
from lib.ui.context import UIContext
from lib.ui.core.constants import UIConstants
from lib.util.events.listener import Listener

from ..address_search.results_component import AddressResultsComponent
from ..core.text import ModalText
from .radar_button import RadarButton


class RadarStationsResult(AddressResultsComponent, Listener):
    def __init__(
        self,
        ctx: UIContext,
        root: NodePath[PandaNode],
        events: AppEvents,
        top: float,
        location: Location,
        radarStations: List[RadarStation],
        distances: Dict[str, float],
    ):
        super().__init__()

        self.contentHeight = 0.0
        self.locationText = ModalText(ctx, root, top, location.getLabel())
        self.contentHeight = self.locationText.height() + UIConstants.modalPadding

        buttonListHeight = (
            len(radarStations) * UIConstants.addressModalResultButtonHeight
            + (len(radarStations) - 1) * UIConstants.addressModalResultButtonPadding
        )

        (self.scroll, buttonRoot, self.contentHeight, buttonTop) = self.setupButtonRoot(
            ctx, events, top, self.contentHeight, buttonListHeight, root
        )

        self.buttons: List[RadarButton] = []

        for i, radarStation in enumerate(radarStations):
            buttonTop = buttonTop + i * (
                UIConstants.addressModalResultButtonHeight
                + UIConstants.addressModalResultButtonPadding
            )

            self.buttons.append(
                RadarButton(
                    ctx,
                    buttonRoot,
                    buttonTop,
                    UIConstants.addressModalWidth,
                    radarStation,
                    distances[radarStation.stationID],
                )
            )

        for button in self.buttons:
            self.listen(button.onClick, events.ui.modals.stationSelected.send)

    def height(self) -> float:
        return self.contentHeight

    def destroy(self) -> None:
        super().destroy()

        self.locationText.destroy()

        for button in self.buttons:
            button.destroy()

        if self.scroll:
            self.scroll.destroy()
