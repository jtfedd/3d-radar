from __future__ import annotations

from typing import List

from panda3d.core import NodePath, PandaNode

from lib.app.context import AppContext
from lib.app.events import AppEvents
from lib.app.state import AppState
from lib.model.geo_point import GeoPoint
from lib.model.radar_station import RadarStation
from lib.ui.context_menu.context_menu_item import ContextMenuItem
from lib.ui.core.alignment import HAlign, VAlign
from lib.ui.core.components.text import Text
from lib.ui.core.constants import UIConstants
from lib.ui.core.layers import UILayer
from lib.util.state import dataQueryFromState


class StationItem(ContextMenuItem):
    def __init__(
        self,
        events: AppEvents,
        state: AppState,
        station: RadarStation,
        selectionPoint: GeoPoint,
    ):
        self.state = state
        self.events = events
        self.station = station
        self.selectionPoint = selectionPoint

    def renderText(
        self,
        ctx: AppContext,
        leftRoot: NodePath[PandaNode],
        rightRoot: NodePath[PandaNode],
    ) -> List[Text]:
        stationId = Text(
            root=leftRoot,
            font=ctx.fonts.mono,
            text=self.station.stationID,
            y=-UIConstants.contextMenuItemHeight / 2,
            hAlign=HAlign.LEFT,
            vAlign=VAlign.CENTER,
            layer=UILayer.CONTEXT_MENU_CONTENT,
        )

        stationName = Text(
            root=leftRoot,
            font=ctx.fonts.regular,
            text=self.station.name,
            y=-UIConstants.contextMenuItemHeight / 2,
            x=stationId.getWidth() + UIConstants.contextMenuPadding,
            hAlign=HAlign.LEFT,
            vAlign=VAlign.CENTER,
            layer=UILayer.CONTEXT_MENU_CONTENT,
        )

        dist = self.selectionPoint.dist(self.station.geoPoint)

        distText = Text(
            root=rightRoot,
            font=ctx.fonts.light,
            text=f"{dist:.1f} km",
            y=-UIConstants.contextMenuItemHeight / 2,
            hAlign=HAlign.RIGHT,
            vAlign=VAlign.CENTER,
            layer=UILayer.CONTEXT_MENU_CONTENT,
        )

        return [stationId, stationName, distText]

    def onClick(self) -> None:
        query = dataQueryFromState(self.state)
        query.radar = self.station.stationID
        self.events.requestData.send(query)
