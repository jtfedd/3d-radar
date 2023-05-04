from direct.showbase.ShowBase import ShowBase
from direct.showbase.DirectObject import DirectObject
from panda3d.core import Vec3


class CameraControl(DirectObject):
    def __init__(self, base: ShowBase, enable=True):
        self.base = base

        # Disable the built-in mouse camera control
        self.base.disableMouse()

        # Consts
        self.movementFactor = 0.15
        self.rotateFactor = 0.3
        self.zoomFactor = 1.2

        # Set up state
        self.x = 0
        self.y = 0

        self.pitch = 30
        self.heading = 0
        self.zoom = 300

        self.lastMouseX = 0
        self.lastMouseY = 0

        # Set up nodes
        self.slider = base.render.attachNewNode("camera-slider")
        self.pivot = base.render.attachNewNode("camera-pivot")
        self.mount = base.render.attachNewNode("camera-mount")

        self.pivot.reparentTo(self.slider)
        self.mount.reparentTo(self.pivot)
        base.camera.reparentTo(self.mount)

        self.updatePositions()

        # Set up events
        self.dragging = False
        self.rotating = False

        if enable:
            self.enable()

        base.task_mgr.add(self.update, "camera-update")

    def enable(self):
        self.accept("mouse1", self.handleDragStart)
        self.accept("mouse1-up", self.handleDragStop)

        self.accept("mouse3", self.handleRotateStart)
        self.accept("mouse3-up", self.handleRotateStop)

        self.accept("wheel_up", self.handleZoomIn)
        self.accept("wheel_down", self.handleZoomOut)

    def disable(self):
        self.dragging = False
        self.rotating = False
        self.ignoreAll()

    def overridePositions(self, x=None, y=None, pitch=None, heading=None, zoom=None):
        if x is not None:
            self.x = x
        if y is not None:
            self.y = y
        if pitch is not None:
            self.pitch = pitch
        if heading is not None:
            self.heading = heading
        if zoom is not None:
            self.zoom = zoom

    def update(self, task):
        self.handleMouseUpdate()
        self.updatePositions()

        return task.cont

    def updatePositions(self):
        if self.pitch > 90:
            self.pitch = 90
        if self.pitch < -90:
            self.pitch = -90

        self.slider.setX(self.x)
        self.slider.setY(self.y)

        self.slider.setH(self.heading)
        self.pivot.setP(-self.pitch)
        self.mount.setY(-self.zoom)

    def handleMouseUpdate(self):
        mouseX = self.lastMouseX
        mouseY = self.lastMouseY

        if self.base.mouseWatcherNode.hasMouse():
            mouseX = self.base.mouseWatcherNode.getMouseX()
            mouseY = self.base.mouseWatcherNode.getMouseY()

            winX, winY = self.base.getSize()
            mouseX *= winX / 2
            mouseY *= winY / 2

        dX = mouseX - self.lastMouseX
        dY = mouseY - self.lastMouseY

        if self.dragging:
            moveDX = -dX * self.movementFactor * self.zoomFactor
            moveDY = -dY * self.movementFactor * self.zoomFactor
            newPos = self.base.render.getRelativePoint(
                self.slider, Vec3(moveDX, moveDY, 0)
            )
            self.x = newPos.x
            self.y = newPos.y
        elif self.rotating:
            self.heading += -dX * self.rotateFactor
            self.pitch += -dY * self.rotateFactor

        self.lastMouseX = mouseX
        self.lastMouseY = mouseY

    def handleDragStart(self):
        self.dragging = True

    def handleDragStop(self):
        self.dragging = False

    def handleRotateStart(self):
        self.rotating = True

    def handleRotateStop(self):
        self.rotating = False

    def handleZoomIn(self):
        self.zoom = self.zoom / self.zoomFactor

    def handleZoomOut(self):
        self.zoom = self.zoom * self.zoomFactor
