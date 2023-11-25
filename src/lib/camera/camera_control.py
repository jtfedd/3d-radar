from direct.showbase.DirectObject import DirectObject
from direct.task import Task
from panda3d.core import Vec3

from lib.app.context import AppContext


class CameraControl(DirectObject):
    DEFAULT_X = 0
    DEFAULT_Y = 0

    DEFAULT_PITCH = 30
    DEFAULT_HEADING = 0
    DEFAULT_ZOOM = 300

    def __init__(self, ctx: AppContext, enable: bool = True):
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

        if enable:
            self.enable()

        base.task_mgr.add(self.update, "camera-update")

    def enable(self) -> None:
        self.accept("mouse1", self.handleDragStart)
        self.accept("mouse1-up", self.handleDragStop)

        self.accept("mouse3", self.handleRotateStart)
        self.accept("mouse3-up", self.handleRotateStop)

        self.accept("wheel_up", self.handleZoomIn)
        self.accept("wheel_down", self.handleZoomOut)

    def disable(self) -> None:
        self.dragging = False
        self.rotating = False
        self.ignoreAll()

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
            self.x = newPos.x
            self.y = newPos.y

        if self.rotating:
            self.heading += -deltaX * self.rotateFactor
            self.pitch += -deltaY * self.rotateFactor

        self.lastMouseX = mouseX
        self.lastMouseY = mouseY

    def handleDragStart(self) -> None:
        self.dragging = True

    def handleDragStop(self) -> None:
        self.dragging = False

    def handleRotateStart(self) -> None:
        self.rotating = True

    def handleRotateStop(self) -> None:
        self.rotating = False

    def handleZoomIn(self) -> None:
        self.zoom = self.zoom / self.zoomFactor

    def handleZoomOut(self) -> None:
        self.zoom = self.zoom * self.zoomFactor
