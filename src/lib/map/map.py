from __future__ import annotations

import math
from typing import Callable

from direct.task.Task import Task
from panda3d.core import NodePath, PandaNode, Shader, TransparencyAttrib, Vec4

from lib.app.context import AppContext
from lib.app.events import AppEvents
from lib.app.state import AppState
from lib.map.radar_boundary import RadarBoundary
from lib.model.alert_type import AlertType
from lib.ui.core.colors import UIColors
from lib.ui.core.layers import UILayer
from lib.util.events.listener import Listener
from lib.util.optional import unwrap

from .alert_renderer import AlertRenderer
from .camera import CameraControl
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
        self.root.setH(180)
        self.root.setP(90)

        self.latRoot = self.root.attachNewNode("map-lat")
        self.longRoot = self.latRoot.attachNewNode("map-long")
        self.globeRoot = self.longRoot.attachNewNode("globe-root")
        self.globeRoot.setH(90)

        self.mapRoot = self.globeRoot.attachNewNode("map-layers")
        self.mapRoot.setScale(EARTH_RADIUS)
        self.mapRoot.setLightOff()

        self.cameraControl = CameraControl(ctx, state, events, self.globeRoot)

        clipPlaneOffset = -(EARTH_RADIUS * (1 - math.cos(RADAR_RANGE / EARTH_RADIUS)))

        mapShader = Shader.load(
            Shader.SL_GLSL,
            vertex="shaders/gen/map_vertex.glsl",
            geometry="shaders/gen/map_geometry.glsl",
            fragment="shaders/gen/map_fragment.glsl",
        )

        self.mapRoot.setShader(mapShader)
        self.mapRoot.setShaderInput("thickness", 1.0)
        self.mapRoot.setShaderInput("clip_z", clipPlaneOffset)
        self.mapRoot.setShaderInput("world_pos", self.root.getPos())
        self.mapRoot.setShaderInput(
            "camera_pos", ctx.base.camera.getPos(ctx.base.render)
        )
        self.ctx.windowManager.resolutionProvider.addNode(self.mapRoot)

        self.boundary = RadarBoundary(ctx, state, self.mapRoot)

        self.states = self.loadMapLayer(
            "states", UILayer.MAP_STATES, UIColors.MAP_BOUNDARIES
        )
        self.counties = self.loadMapLayer(
            "counties", UILayer.MAP_COUNTIES, UIColors.MAP_BOUNDARIES
        )
        self.roads = self.loadMapLayer("roads", UILayer.MAP_ROADS, UIColors.MAP_DETAILS)

        self.states.setShaderInput("thickness", 2.0)

        self.warningsRoot = self.mapRoot.attachNewNode("warningsRoot")
        self.warningsRoot.setAlphaScale(state.warningsOpacity.value)
        self.warningsRoot.setTransparency(TransparencyAttrib.MAlpha)
        self.warningsRoot.setDepthTest(False)

        self.towRoot = self.warningsRoot.attachNewNode("towRoot")
        self.towRoot.setBin("background", UILayer.MAP_TOW.value)

        self.svwRoot = self.warningsRoot.attachNewNode("svwRoot")
        self.svwRoot.setBin("background", UILayer.MAP_SVW.value)

        self.towRenderer = AlertRenderer(self.towRoot, state, AlertType.TORNADO_WARNING)
        self.svwRenderer = AlertRenderer(
            self.svwRoot, state, AlertType.SEVERE_THUNDERSTORM_WARNING
        )

        self.markersRoot = self.mapRoot.attachNewNode("map-markers")
        self.markersRenderer = MarkersRenderer(ctx, state, self.markersRoot)

        self.updatePosition(state.station.value)
        self.listen(state.station, self.updatePosition)

        self.bind(state.mapStates, self.updateLayer(self.states))
        self.bind(state.mapCounties, self.updateLayer(self.counties))
        self.bind(state.mapRoads, self.updateLayer(self.roads))
        self.bind(state.showTornadoWarnings, self.updateLayer(self.towRoot))
        self.bind(state.showSevereThunderstormWarnings, self.updateLayer(self.svwRoot))

        self.listen(state.warningsOpacity, self.warningsRoot.setAlphaScale)

        self.updateTask = ctx.base.taskMgr.add(self.update, "map-update")

    def update(self, task: Task) -> int:
        cameraPos = self.ctx.base.camera.getPos(self.ctx.base.render)
        self.mapRoot.setShaderInput("camera_pos", cameraPos)
        return task.cont

    def updateLayer(self, node: NodePath[PandaNode]) -> Callable[[bool], None]:
        return lambda visible: node.show() if visible else node.hide()

    def loadMapLayer(
        self, name: str, layer: UILayer, color: Vec4
    ) -> NodePath[PandaNode]:
        node = unwrap(self.ctx.base.loader.loadModel("assets/maps/" + name + ".bam"))
        node.reparentTo(self.mapRoot)
        node.setColorScale(color)
        node.setBin("background", layer.value)
        node.setDepthTest(False)
        return node

    def updatePosition(self, stationID: str) -> None:
        radarStation = self.ctx.services.nws.getStation(stationID)
        if not radarStation:
            return

        self.latRoot.setP(-radarStation.geoPoint.lat)
        self.longRoot.setH(-radarStation.geoPoint.lon)

    def destroy(self) -> None:
        super().destroy()

        self.updateTask.cancel()

        self.cameraControl.destroy()
        self.ctx.windowManager.resolutionProvider.removeNode(self.mapRoot)

        self.boundary.destroy()

        self.lightingManager.destroy()
        self.markersManager.destroy()
        self.markersRenderer.destroy()
        self.towRenderer.destroy()
        self.svwRenderer.destroy()

        self.root.removeNode()
