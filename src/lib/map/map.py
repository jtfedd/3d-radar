from __future__ import annotations

import math

from panda3d.core import (
    GeomNode,
    NodePath,
    PandaNode,
    Shader,
    TransparencyAttrib,
    Vec3,
    Vec4,
)

from lib.app.context import AppContext
from lib.app.events import AppEvents
from lib.app.state import AppState
from lib.geometry.segments import Segments
from lib.model.alert_type import AlertType
from lib.ui.core.colors import UIColors
from lib.ui.core.layers import UILayer
from lib.util.events.listener import Listener
from lib.util.optional import unwrap

from .alert_renderer import AlertRenderer
from .constants import EARTH_RADIUS, RADAR_RANGE
from .lighting import LightingManager
from .markers.markers_manager import MarkersManager
from .markers.markers_renderer import MarkersRenderer


class Map(Listener):
    def __init__(self, ctx: AppContext, state: AppState, events: AppEvents):
        super().__init__()

        self.ctx = ctx
        self.state = state

        self.lightingManager = LightingManager(ctx, state)

        self.markersManager = MarkersManager(ctx, state, events)

        self.root = ctx.base.render.attachNewNode("map-root")
        self.root.setZ(-EARTH_RADIUS)
        self.root.setScale(EARTH_RADIUS)
        self.root.setH(180)
        self.root.setP(90)

        self.latRoot = self.root.attachNewNode("map-lat")
        self.longRoot = self.latRoot.attachNewNode("map-long")

        self.mapRoot = self.longRoot.attachNewNode("map-layers")
        self.mapRoot.setH(90)

        mapShader = Shader.load(
            Shader.SL_GLSL,
            vertex="shaders/gen/map_vertex.glsl",
            geometry="shaders/gen/map_geometry.glsl",
            fragment="shaders/gen/map_fragment.glsl",
        )

        self.mapRoot.setShader(mapShader)
        self.mapRoot.setShaderInput("thickness", 1.0)

        self.ctx.windowManager.resolutionProvider.addNode(self.mapRoot)

        clipPlaneOffset = -(EARTH_RADIUS * (1 - math.cos(RADAR_RANGE / EARTH_RADIUS)))
        self.mapRoot.setShaderInput("clip_z", clipPlaneOffset)

        self.boundary = ctx.base.render.attachNewNode(self.drawCircle())
        self.boundary.setZ(clipPlaneOffset)
        self.boundary.setScale(EARTH_RADIUS * math.sin(RADAR_RANGE / EARTH_RADIUS))
        self.boundary.setShader(mapShader)
        self.boundary.setShaderInput("thickness", 1.0)
        self.boundary.setShaderInput("clip_z", 2 * clipPlaneOffset)
        self.boundary.setColorScale(UIColors.MAP_BOUNDARIES)
        self.ctx.windowManager.resolutionProvider.addNode(self.boundary)

        self.states = self.loadMapLayer(
            "states", UILayer.MAP_STATES, UIColors.MAP_BOUNDARIES
        )
        self.counties = self.loadMapLayer(
            "counties", UILayer.MAP_COUNTIES, UIColors.MAP_BOUNDARIES
        )
        self.roads = self.loadMapLayer("roads", UILayer.MAP_ROADS, UIColors.MAP_DETAILS)

        self.states.setShaderInput("thickness", 2.0)

        self.warningsRoot = self.mapRoot.attachNewNode("warningsRoot")
        self.warningsRoot.setLightOff()
        self.warningsRoot.setAlphaScale(state.warningsOpacity.value)
        self.warningsRoot.setTransparency(TransparencyAttrib.MAlpha)

        self.towRoot = self.warningsRoot.attachNewNode("towRoot")
        self.towRoot.setBin("background", UILayer.MAP_TOW.value)
        self.towRoot.setDepthTest(False)

        self.svwRoot = self.warningsRoot.attachNewNode("svwRoot")
        self.svwRoot.setBin("background", UILayer.MAP_SVW.value)
        self.svwRoot.setDepthTest(False)

        self.towRenderer = AlertRenderer(self.towRoot, state, AlertType.TORNADO_WARNING)
        self.svwRenderer = AlertRenderer(
            self.svwRoot, state, AlertType.SEVERE_THUNDERSTORM_WARNING
        )

        self.markersRoot = self.mapRoot.attachNewNode("map-markers")
        self.markersRenderer = MarkersRenderer(ctx, state, self.markersRoot)

        self.updatePosition(state.station.value)
        self.listen(state.station, self.updatePosition)

        self.updateLayers()
        self.listen(state.mapStates, lambda _: self.updateLayers())
        self.listen(state.mapCounties, lambda _: self.updateLayers())
        self.listen(state.mapRoads, lambda _: self.updateLayers())
        self.listen(state.showTornadoWarnings, lambda _: self.updateLayers())
        self.listen(state.showSevereThunderstormWarnings, lambda _: self.updateLayers())

        self.listen(state.warningsOpacity, self.warningsRoot.setAlphaScale)

    def updateLayers(self) -> None:
        self.states.hide()
        self.counties.hide()
        self.roads.hide()
        self.towRoot.hide()
        self.svwRoot.hide()

        if self.state.mapStates.value:
            self.states.show()
        if self.state.mapCounties.value:
            self.counties.show()
        if self.state.mapRoads.value:
            self.roads.show()
        if self.state.showTornadoWarnings.value:
            self.towRoot.show()
        if self.state.showSevereThunderstormWarnings.value:
            self.svwRoot.show()

    def loadMapLayer(
        self, name: str, layer: UILayer, color: Vec4
    ) -> NodePath[PandaNode]:
        node = unwrap(self.ctx.base.loader.loadModel("assets/maps/" + name + ".bam"))
        node.reparentTo(self.mapRoot)
        node.setColorScale(color)
        node.setLightOff()
        node.setBin("background", layer.value)
        node.setDepthTest(False)
        return node

    def updatePosition(self, stationID: str) -> None:
        radarStation = self.ctx.services.nws.getStation(stationID)
        if not radarStation:
            return

        self.latRoot.setP(-radarStation.geoPoint.lat)
        self.longRoot.setH(-radarStation.geoPoint.lon)

    def drawCircle(self) -> GeomNode:
        steps = 720
        stepSize = (math.pi * 2) / steps

        segments = Segments(steps)
        segments.addLoop(
            [
                Vec3(
                    math.cos(i * stepSize),
                    math.sin(i * stepSize),
                    0,
                )
                for i in range(steps)
            ]
        )
        return segments.create()

    def destroy(self) -> None:
        super().destroy()

        self.ctx.windowManager.resolutionProvider.removeNode(self.mapRoot)

        self.lightingManager.destroy()
        self.markersManager.destroy()
        self.markersRenderer.destroy()
        self.towRenderer.destroy()
        self.svwRenderer.destroy()

        self.root.removeNode()
