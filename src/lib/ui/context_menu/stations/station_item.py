from __future__ import annotations

from typing import List

from panda3d.core import NodePath, PandaNode

from lib.app.context import AppContext
from lib.app.events import AppEvents
from lib.app.state import AppState
from lib.model.radar_station import RadarStation
from lib.ui.context_menu.context_menu_item import ContextMenuItem
from lib.ui.core.alignment import HAlign, VAlign
from lib.ui.core.components.text import Text
from lib.ui.core.constants import UIConstants
from lib.ui.core.layers import UILayer
from lib.util.state import dataQueryFromState


class StationItem(ContextMenuItem):
    def __init__(self, events: AppEvents, state: AppState, station: RadarStation):
        self.state = state
        self.events = events
        self.station = station

    def renderText(self, ctx: AppContext, root: NodePath[PandaNode]) -> List[Text]:
        text = Text(
            root=root,
            font=ctx.fonts.regular,
            text=self.station.stationID,
            y=-UIConstants.contextMenuItemHeight / 2,
            hAlign=HAlign.LEFT,
            vAlign=VAlign.CENTER,
            layer=UILayer.CONTEXT_MENU_CONTENT,
        )

        return [text]

    def onClick(self) -> None:
        query = dataQueryFromState(self.state)
        query.radar = self.station.stationID
        self.events.requestData.send(query)
