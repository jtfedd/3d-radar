from __future__ import annotations

import math

from panda3d.core import NodePath, PandaNode, Plane, PlaneNode, Vec4

from lib.app.context import AppContext
from lib.app.state import AppState
from lib.ui.core.colors import UIColors
from lib.util.events.listener import Listener
from lib.util.optional import unwrap

EARTH_RADIUS = 6378.1
RADAR_RANGE = 400


class Map(Listener):
    def __init__(self, ctx: AppContext, state: AppState):
        super().__init__()

        self.ctx = ctx

        self.root = ctx.base.render.attachNewNode("map-root")
        self.root.setZ(-EARTH_RADIUS)
        self.root.setH(180)
        self.root.setP(90)

        self.latRoot = self.root.attachNewNode("map-lat")
        self.longRoot = self.latRoot.attachNewNode("map-long")
        self.mapRoot = self.longRoot.attachNewNode("map-layers")

        clipPlaneOffset = -(EARTH_RADIUS * (1 - math.cos(RADAR_RANGE / EARTH_RADIUS)))

        clipPlane = Plane((0, 0, 0), (1, 0, 0), (0, 1, 0))
        clipPlaneNode = PlaneNode("clip-plane", clipPlane)
        clipPlaneNP = ctx.base.render.attachNewNode(clipPlaneNode)
        clipPlaneNP.setZ(clipPlaneOffset)
        self.mapRoot.setClipPlane(clipPlaneNP)

        self.states = self.loadMapLayer("states", UIColors.MAP_BOUNDARIES)
        self.counties = self.loadMapLayer("counties", UIColors.MAP_BOUNDARIES)
        self.roads = self.loadMapLayer("roads", UIColors.MAP_DETAILS)

        self.updatePosition(state.station.value)
        self.listen(state.station, self.updatePosition)

    def loadMapLayer(self, name: str, color: Vec4) -> NodePath[PandaNode]:
        node = unwrap(self.ctx.base.loader.loadModel("assets/maps/" + name + ".bam"))
        node.reparentTo(self.mapRoot)
        node.setScale(EARTH_RADIUS)
        node.setColorScale(color)
        node.setLightOff()
        node.setH(90)
        return node

    def updatePosition(self, stationID: str) -> None:
        radarStation = self.ctx.services.nws.getStation(stationID)
        if not radarStation:
            return

        self.latRoot.setP(-radarStation.lat)
        self.longRoot.setH(-radarStation.long)
