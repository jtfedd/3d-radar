from __future__ import annotations

import math

from panda3d.core import NodePath, PandaNode

from lib.app.context import AppContext
from lib.app.state import AppState
from lib.geometry.circle import drawCircle
from lib.map.util import toGlobe
from lib.ui.core.colors import UIColors
from lib.util.events.listener import Listener

from .constants import EARTH_RADIUS, RADAR_RANGE


class RadarBoundary(Listener):
    def __init__(
        self,
        ctx: AppContext,
        state: AppState,
        mapRoot: NodePath[PandaNode],
    ) -> None:
        super().__init__()

        self.ctx = ctx
        self.mapRoot = mapRoot

        self.root = mapRoot.attachNewNode("radar-boundary")
        self.boundary = self.root.attachNewNode(drawCircle())
        self.boundary.setP(90)
        self.boundary.setY(1 - math.cos(RADAR_RANGE / EARTH_RADIUS))
        self.boundary.setScale(math.sin(RADAR_RANGE / EARTH_RADIUS))
        self.boundary.setColorScale(UIColors.MAP_BOUNDARIES)

        # Should not clip, set the clip plane to something lower than this will ever be
        self.boundary.setShaderInput("clip_z", -EARTH_RADIUS)

        self.bind(state.station, self.updatePosition)

    def updatePosition(self, radar: str) -> None:
        radarStation = self.ctx.services.nws.getStation(radar)
        if not radarStation:
            return

        pos = toGlobe(radarStation.geoPoint)
        self.root.setPos(pos)
        self.root.lookAt(self.mapRoot)
