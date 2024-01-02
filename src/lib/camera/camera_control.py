from direct.task import Task
from panda3d.core import Vec3

from lib.app.context import AppContext
from lib.app.events import AppEvents
from lib.map.constants import RADAR_RANGE
from lib.util.events.listener import Listener


class CameraControl(Listener):
    DEFAULT_X = 0
    DEFAULT_Y = 0

    DEFAULT_PITCH = 30
    DEFAULT_HEADING = 0
    DEFAULT_ZOOM = 300

    MIN_ZOOM = 10
    MAX_ZOOM = 2250

    def __init__(self, ctx: AppContext, events: AppEvents):
        super().__init__()

        self.base = ctx.base

        # Disable the built-in mouse camera control
        self.base.disableMouse()

        # Consts
        self.movementFactor = 0.0015
        self.rotateFactor = 0.3
        self.zoomFactor = 1.2

        # Set up state
        self.x: float = self.DEFAULT_X
        self.y: float = self.DEFAULT_Y

        self.pitch: float = self.DEFAULT_PITCH
        self.heading: float = self.DEFAULT_HEADING
        self.zoom: float = self.DEFAULT_ZOOM

        self.lastMouseX: float = 0
        self.lastMouseY: float = 0

        # Set up nodes
        self.slider = self.base.render.attachNewNode("camera-slider")
        self.pivot = self.base.render.attachNewNode("camera-pivot")
        self.mount = self.base.render.attachNewNode("camera-mount")

        self.pivot.reparentTo(self.slider)
        self.mount.reparentTo(self.pivot)
        self.base.camera.reparentTo(self.mount)

        self.updatePositions()

        # Set up events
        self.dragging = False
        self.rotating = False

        self.listen(events.input.leftMouse, self.handleDrag)
        self.listen(events.input.rightMouse, self.handleRotate)
        self.listen(events.input.zoom, self.handleZoom)

        self.updateTask = ctx.base.taskMgr.add(self.update, "camera-update")

    def resetPosition(
        self,
        x: float = 0,
        y: float = 0,
    ) -> None:
        if x is not None:
            self.x = x
        if y is not None:
            self.y = y

    def resetOrientation(
        self,
        pitch: float = 30,
        heading: float = 0,
        zoom: float = 300,
    ) -> None:
        if pitch is not None:
            self.pitch = pitch
        if heading is not None:
            self.heading = heading
        if zoom is not None:
            self.zoom = zoom

    def update(self, task: Task.Task) -> int:
        self.handleMouseUpdate()
        self.updatePositions()
        self.updateNearFar()

        return task.cont

    def updatePositions(self) -> None:
        self.pitch = min(self.pitch, 90)
        self.pitch = max(self.pitch, -90)

        self.slider.setX(self.x)
        self.slider.setY(self.y)

        self.slider.setH(self.heading)
        self.pivot.setP(-self.pitch)
        self.mount.setY(-self.zoom)

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
            moveDX = -deltaX * self.movementFactor * self.zoom
            moveDY = -deltaY * self.movementFactor * self.zoom
            newPos = self.base.render.getRelativePoint(
                self.slider, Vec3(moveDX, moveDY, 0)
            )

            if newPos.length() > RADAR_RANGE:
                newPos = newPos.normalized() * RADAR_RANGE

            self.x = newPos.x
            self.y = newPos.y

        if self.rotating:
            self.heading += -deltaX * self.rotateFactor
            self.pitch += -deltaY * self.rotateFactor

        self.lastMouseX = mouseX
        self.lastMouseY = mouseY

    def handleDrag(self, value: bool) -> None:
        self.dragging = value

    def handleRotate(self, value: bool) -> None:
        self.rotating = value

    def handleZoom(self, direction: int) -> None:
        self.zoom = self.zoom * pow(self.zoomFactor, direction)
        self.zoom = min(self.MAX_ZOOM, max(self.MIN_ZOOM, self.zoom))

    def updateNearFar(self) -> None:
        # Clips the near and far planes of the camera to reduce z-fighting between
        # the map and the volume

        # Get a unit vector in the direction the camera is pointing
        cameraForward = self.base.render.getRelativeVector(
            self.base.camera, Vec3(0, 1, 0)
        )

        # Get the near and far points of the scene along the vector the camera is facing
        # Transform back to be relative to the camera
        sceneNear = self.base.camera.getRelativePoint(
            self.base.render, -cameraForward * RADAR_RANGE
        )
        sceneFar = self.base.camera.getRelativePoint(
            self.base.render, cameraForward * RADAR_RANGE
        )

        # To set the near and far plane to the correct distance we just need to extract
        # the y-coordinate from the camera-relative points
        near = sceneNear.y
        far = sceneFar.y

        # Ensure we don't end up with invalid values
        near = max(1, near)
        far = max(far, near + 1)

        # Apply the values to the lens
        self.base.cam.node().getLens().setNearFar(near, far)
