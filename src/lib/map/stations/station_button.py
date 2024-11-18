from __future__ import annotations

from direct.task.Task import Task
from panda3d.core import NodePath, PandaNode

from lib.app.context import AppContext
from lib.app.state import AppState
from lib.model.radar_station import RadarStation
from lib.ui.core.components.button import Button
from lib.ui.core.constants import UIConstants
from lib.ui.core.layers import UILayer
from lib.util.events.listener import Listener

from ..util import toGlobe, toScreen


class StationButton(Listener):
    def __init__(
        self,
        ctx: AppContext,
        state: AppState,
        root: NodePath[PandaNode],
        station: RadarStation,
    ):
        super().__init__()

        self.ctx = ctx
        self.state = state

        self.station = station

        self.visible = False

        self.posRoot = root.attachNewNode(station.stationID + "-pos-root")
        self.posRoot.setPos(toGlobe(station.geoPoint))

        self.root = ctx.base.aspect2dp.attachNewNode(station.stationID + "-icon-root")

        self.button = Button(
            self.root,
            ctx=ctx,
            width=UIConstants.stationMapButtonWidth,
            height=UIConstants.stationMapButtonHeight,
            bgLayer=UILayer.STATIONS_BUTTON_BACKGROUND,
            contentLayer=UILayer.STATIONS_BUTTON_CONTENT,
            interactionLayer=UILayer.STATIONS_BUTTON_INTERACTION,
            text=station.stationID,
        )

        self.bind(state.uiScale, self.root.setScale)
        self.updateTask = ctx.base.taskMgr.add(
            self.update, station.stationID + "-update"
        )

    def updateVisiblity(self, visible: bool) -> None:
        self.visible = visible

    def update(self, task: Task) -> int:
        if not self.visible:
            self.root.hide()
            return task.cont

        onscreenPos = toScreen(self.ctx, self.posRoot.getPos(self.ctx.base.render))
        if onscreenPos is None:
            self.root.hide()
        else:
            self.root.show()
            self.root.setPos(onscreenPos)

        return task.cont

    def destroy(self) -> None:
        super().destroy()

        self.updateTask.cancel()

        self.button.destroy()
        self.root.removeNode()
