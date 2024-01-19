from __future__ import annotations

from typing import List

from panda3d.core import NodePath, PandaNode

from lib.app.events import AppEvents
from lib.model.location import Location
from lib.ui.context import UIContext
from lib.ui.core.alignment import HAlign, VAlign
from lib.ui.core.components.scrollable_panel import ScrollablePanel
from lib.ui.core.constants import UIConstants
from lib.ui.core.layers import UILayer
from lib.util.events.listener import Listener

from ..address_search.results_component import AddressResultsComponent


class MarkerResult(AddressResultsComponent, Listener):
    def __init__(
        self,
        ctx: UIContext,
        root: NodePath[PandaNode],
        events: AppEvents,
        top: float,
        locations: List[Location],
    ):
        super().__init__()

        self.contentHeight = 0.0

        buttonListHeight = (
            len(radarStations) * UIConstants.stationModalResultButtonHeight
            + (len(radarStations) - 1) * UIConstants.stationModalResultButtonPadding
        )

        self.scroll: ScrollablePanel | None = None
        buttonTopOffset = top + self.contentHeight
        buttonRoot: NodePath[PandaNode]

        if buttonListHeight > UIConstants.stationModalResultButtonsMaxHeight:
            self.scroll = ScrollablePanel(
                root=root,
                ctx=ctx,
                events=events,
                y=-(top + self.contentHeight),
                width=UIConstants.addressModalWidth + UIConstants.modalPadding,
                height=UIConstants.stationModalResultButtonsMaxHeight,
                canvasHeight=buttonListHeight,
                hAlign=HAlign.LEFT,
                vAlign=VAlign.TOP,
                layer=UILayer.MODAL_CONTENT_INTERACTION,
                scrollbarPadding=UIConstants.modalScrollbarPadding,
            )
            self.contentHeight += UIConstants.stationModalResultButtonsMaxHeight
            buttonTopOffset = 0
            buttonRoot = self.scroll.getCanvas()
        else:
            self.contentHeight += buttonListHeight
            buttonRoot = root

        self.buttons: List[RadarButton] = []

        for i, radarStation in enumerate(radarStations):
            buttonTop = buttonTopOffset + i * (
                UIConstants.stationModalResultButtonHeight
                + UIConstants.stationModalResultButtonPadding
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
