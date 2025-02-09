from __future__ import annotations

from typing import List

from panda3d.core import NodePath, PandaNode

from lib.app.context import AppContext
from lib.app.events import AppEvents
from lib.app.state import AppState
from lib.map.stations.station_button import StationButton
from lib.util.events.listener import Listener


class StationsRenderer(Listener):
    def __init__(
        self,
        ctx: AppContext,
        state: AppState,
        events: AppEvents,
        root: NodePath[PandaNode],
    ):
        super().__init__()

        self.buttons: List[StationButton] = []

        for station in ctx.services.nws.radarStations.values():
            self.buttons.append(StationButton(ctx, state, events, root, station))

        self.bind(state.showStations, self.showStationButtons)

    def showStationButtons(self, visible: bool) -> None:
        for button in self.buttons:
            button.updateVisiblity(visible)

    def destroy(self) -> None:
        super().destroy()

        for button in self.buttons:
            button.destroy()
