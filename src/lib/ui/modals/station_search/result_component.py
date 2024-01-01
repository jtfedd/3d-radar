from __future__ import annotations

from typing import Dict, List

from panda3d.core import NodePath, PandaNode

from lib.app.events import AppEvents
from lib.model.radar_station import RadarStation
from lib.ui.context import UIContext
from lib.ui.core.alignment import HAlign, VAlign
from lib.ui.core.components.scrollable_panel import ScrollablePanel
from lib.ui.core.constants import UIConstants
from lib.ui.core.layers import UILayer

from ..address_search.results_component import AddressResultsComponent
from .radar_button import RadarButton


class RadarStationsResult(AddressResultsComponent):
    def __init__(
        self,
        ctx: UIContext,
        root: NodePath[PandaNode],
        events: AppEvents,
        top: float,
        radarStations: List[RadarStation],
        distances: Dict[str, float],
    ):
        self.scroll = ScrollablePanel(
            root=root,
            ctx=ctx,
            events=events,
            y=-(top + UIConstants.modalPadding),
            width=UIConstants.addressModalWidth + UIConstants.modalPadding,
            height=0.2,
            canvasHeight=(0.05 * len(radarStations)),
            hAlign=HAlign.LEFT,
            vAlign=VAlign.TOP,
            layer=UILayer.MODAL_CONTENT_INTERACTION,
            scrollbarPadding=UIConstants.modalScrollbarPadding,
        )

        self.buttons: List[RadarButton] = []

        for i, radarStation in enumerate(radarStations):
            self.buttons.append(
                RadarButton(
                    ctx,
                    self.scroll.getCanvas(),
                    0.05 * i,
                    UIConstants.addressModalWidth,
                    radarStation,
                    distances[radarStation.stationID],
                )
            )

    def height(self) -> float:
        return 0.2 + UIConstants.modalPadding

    def destroy(self) -> None:
        for button in self.buttons:
            button.destroy()

        self.scroll.destroy()
