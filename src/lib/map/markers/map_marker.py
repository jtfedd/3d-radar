from __future__ import annotations

import math

from direct.task.Task import Task
from panda3d.core import NodePath, PandaNode

from lib.app.context import AppContext
from lib.app.state import AppState
from lib.model.location_marker import LocationMarker
from lib.ui.core.alignment import HAlign, VAlign
from lib.ui.core.colors import UIColors
from lib.ui.core.components.image import Image
from lib.ui.core.constants import UIConstants
from lib.ui.core.icons import Icons
from lib.ui.core.layers import UILayer
from lib.util.events.listener import Listener
from lib.util.map_3d_to_2d import map3dToAspect2d
from lib.util.optional import unwrap

from ..constants import RADAR_RANGE
from ..util import toGlobe


class MapMarker(Listener):
    def __init__(
        self,
        ctx: AppContext,
        state: AppState,
        root: NodePath[PandaNode],
        marker: LocationMarker,
    ):
        super().__init__()

        self.ctx = ctx
        self.state = state

        self.marker = marker

        self.inRadarRange = False
        self.visible = marker.visible

        self.posRoot = root.attachNewNode(marker.id + "-pos-root")
        self.posRoot.setPos(toGlobe(marker.location.geoPoint))

        self.iconRoot = ctx.base.aspect2dp.attachNewNode(marker.id + "-icon-root")
        self.iconRoot.setScale(state.uiScale.value)
        self.icon = Image(
            self.iconRoot,
            Icons.LOCATION,
            width=UIConstants.mapMarkerSize,
            height=UIConstants.mapMarkerSize,
            hAlign=HAlign.CENTER,
            vAlign=VAlign.BOTTOM,
            layer=UILayer.MARKER,
            color=UIColors.ORANGE,
        )

        self.model = unwrap(
            ctx.base.loader.loadModel("assets/models/marker.glb", noCache=True)
        )
        self.model.reparentTo(ctx.base.render)
        self.model.hide()
        self.model.setColorScale(UIColors.ORANGE)
        self.model.setScale(10)

        self.updateInRadarRange()
        self.listen(state.station, lambda _: self.updateInRadarRange())
        self.listen(state.uiScale, self.iconRoot.setScale)
        self.updateTask = ctx.base.taskMgr.add(self.update, marker.id + "-update")

    def updateInRadarRange(self) -> None:
        station = self.ctx.services.nws.getStation(self.state.station.value)
        if not station:
            return

        self.inRadarRange = (
            station.geoPoint.dist(self.marker.location.geoPoint) < RADAR_RANGE
        )

    def updateVisiblity(self, visible: bool) -> None:
        self.visible = visible

    def update(self, task: Task) -> int:
        markerOnscreenPos = map3dToAspect2d(
            self.ctx, self.ctx.base.render, self.posRoot.getPos(self.ctx.base.render)
        )

        show2dMarker = (
            self.visible and self.inRadarRange and not self.state.show3dMarkers.value
        )
        show3dMarker = (
            self.visible and self.inRadarRange and self.state.show3dMarkers.value
        )

        if markerOnscreenPos is None or not show2dMarker:
            self.iconRoot.hide()
        else:
            self.iconRoot.show()
            self.iconRoot.setPos(markerOnscreenPos)

        if not show3dMarker:
            self.model.hide()
        else:
            self.model.show()
            self.model.setPos(self.posRoot.getPos(self.ctx.base.render))

            pointX = self.model.getX(self.ctx.base.render)
            pointY = self.model.getY(self.ctx.base.render)

            camX = self.ctx.base.camera.getX(self.ctx.base.render)
            camY = self.ctx.base.camera.getY(self.ctx.base.render)

            heading = math.degrees(math.atan2(camY - pointY, camX - pointX))
            self.model.setH(heading)

        return task.cont

    def destroy(self) -> None:
        super().destroy()

        self.updateTask.cancel()

        self.icon.destroy()
        self.iconRoot.removeNode()

        self.iconRoot.removeNode()
