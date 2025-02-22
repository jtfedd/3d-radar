from __future__ import annotations

import math

from direct.task.Task import Task
from panda3d.core import NodePath, OrthographicLens, PandaNode

from lib.app.context import AppContext
from lib.app.events import AppEvents
from lib.app.state import AppState
from lib.map.constants import EARTH_RADIUS
from lib.util.events.listener import Listener


class CameraControl(Listener):
    DEFAULT_PITCH = 30
    DEFAULT_HEADING = 0
    DEFAULT_ZOOM = 500

    MIN_ZOOM = 10
    MAX_ZOOM = 8000

    def __init__(
        self,
        ctx: AppContext,
        state: AppState,
        events: AppEvents,
        root: NodePath[PandaNode],
    ):
        super().__init__()

        self.base = ctx.base
        self.state = state

        # Disable the built-in mouse camera control
        self.base.disableMouse()

        self.lens2D = OrthographicLens()
        self.lens2D.setFar(EARTH_RADIUS * 3)
        self.lens3D = ctx.base.cam.node().get_lens()

        # Consts
        self.movementFactor = 0.07
        self.rotateFactor = 0.3
        self.zoomFactor = 1.2

        # Set up state
        radarStation = ctx.services.nws.getStation(state.station.getValue())
        if not radarStation:
            return

        self.lat = radarStation.geoPoint.lat
        self.lon = radarStation.geoPoint.lon - 90

        self.pitch: float = self.DEFAULT_PITCH
        self.heading: float = self.DEFAULT_HEADING
        self.zoom: float = self.DEFAULT_ZOOM

        self.lastMouseX: float = 0
        self.lastMouseY: float = 0

        # Set up nodes
        self.root = root.attachNewNode("camera-root")
        self.cameraLon = self.root.attachNewNode("camera-lon")
        self.cameraLat = self.cameraLon.attachNewNode("camera-lat")
        self.cameraBase = self.cameraLat.attachNewNode("camera-position-base")
        self.cameraH = self.cameraBase.attachNewNode("camera-heading")
        self.cameraP = self.cameraH.attachNewNode("camera-pivot")
        self.cameraMount = self.cameraP.attachNewNode("camera-mount")

        self.cameraBase.setY(EARTH_RADIUS)
        self.cameraBase.setP(-90)
        self.cameraBase.setH(self.cameraBase, 180)

        self.camera2dMount = self.cameraBase.attachNewNode("camera-2d-mount")
        self.camera2dMount.setP(-90)
        self.camera2dMount.setY(self.camera2dMount, -EARTH_RADIUS * 2)

        self.updatePositions()

        # Set up events
        self.dragging = False
        self.rotating = False

        self.listen(events.input.leftMouse, self.handleDrag)
        self.listen(events.input.rightMouse, self.handleRotate)
        self.listen(events.input.zoom, self.handleZoom)
        self.bind(state.view3D, lambda _: self.updateLens())

        self.updateTask = ctx.base.taskMgr.add(self.update, "camera-update")

    def updateLens(self) -> None:
        self.resetOrientation()
        if self.state.view3D.getValue():
            self.base.cam.node().setLens(self.lens3D)
            self.base.camera.reparentTo(self.cameraMount)
        else:
            self.base.cam.node().setLens(self.lens2D)
            self.base.camera.reparentTo(self.camera2dMount)

    def update2dLens(self) -> None:
        aspectRatio = self.base.getAspectRatio()

        width = aspectRatio
        height = 1.0

        if aspectRatio < 1.0:
            width = 1.0
            height = 1 / aspectRatio

        self.lens2D.setFilmSize((self.zoom * width, self.zoom * height))

    def resetOrientation(self, resetZoom: bool = False) -> None:
        self.pitch = self.DEFAULT_PITCH
        self.heading = self.DEFAULT_HEADING
        if resetZoom:
            self.zoom = self.DEFAULT_ZOOM

    def update(self, task: Task) -> int:
        self.handleMouseUpdate()
        self.updatePositions()
        self.update2dLens()

        return task.cont

    def updatePositions(self) -> None:
        self.cameraLon.setH(self.lon)
        self.cameraLat.setP(self.lat)

        self.cameraH.setH(self.heading)
        self.cameraP.setP(-self.pitch)
        self.cameraMount.setY(-self.zoom)

    def handleMouseUpdate(self) -> None:
        mouseX = self.lastMouseX
        mouseY = self.lastMouseY

        if self.base.mouseWatcherNode.hasMouse():
            mouseX = self.base.mouseWatcherNode.getMouseX()
            mouseY = self.base.mouseWatcherNode.getMouseY()

            winX, winY = self.base.getSize()
            mouseX *= winX / 2
            mouseY *= winY / 2

        deltaX = mouseX - self.lastMouseX
        deltaY = mouseY - self.lastMouseY

        if self.dragging:
            moveDX = -deltaX * self.movementFactor * self.zoom / EARTH_RADIUS
            moveDY = -deltaY * self.movementFactor * self.zoom / EARTH_RADIUS

            headingRad = math.radians(self.heading)
            headingCos = math.cos(headingRad)
            headingSin = math.sin(headingRad)

            dLon = moveDX * headingCos - moveDY * headingSin
            dLat = moveDY * headingCos + moveDX * headingSin

            self.lat += dLat
            self.lon += dLon

            self.lat = min(self.lat, 90)
            self.lat = max(self.lat, -90)

        if self.rotating and self.state.view3D.getValue():
            self.heading += -deltaX * self.rotateFactor
            self.pitch += -deltaY * self.rotateFactor

            self.pitch = min(self.pitch, 90)
            self.pitch = max(self.pitch, 0)

        self.lastMouseX = mouseX
        self.lastMouseY = mouseY

    def handleDrag(self, value: bool) -> None:
        self.dragging = value

    def handleRotate(self, value: bool) -> None:
        self.rotating = value

    def handleZoom(self, direction: int) -> None:
        self.zoom = self.zoom * pow(self.zoomFactor, direction)
        self.zoom = min(self.MAX_ZOOM, max(self.MIN_ZOOM, self.zoom))
