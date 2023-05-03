from direct.showbase.ShowBase import ShowBase
from direct.showbase.DirectObject import DirectObject


class CameraControl(DirectObject):
    def __init__(self, base: ShowBase):
        self.base = base

        # Disable the built-in mouse camera control
        self.base.disableMouse()

        # Consts
        self.movementFactor = 50
        self.rotateFactor = 80
        self.zoomFactor = 1.2

        # Set up state
        self.x = 0
        self.y = 0
        self.lastX = 0
        self.lastY = 0

        self.pitch = 0
        self.heading = 0
        self.zoom = 100

        # Set up nodes
        self.slider = base.render.attachNewNode("camera-slider")
        self.pivot = base.render.attachNewNode("camera-pivot")
        self.mount = base.render.attachNewNode("camera-mount")

        self.pivot.reparentTo(self.slider)
        self.mount.reparentTo(self.pivot)
        base.camera.reparentTo(self.mount)

        self.updatePositions()

        # Set up events
        self.lastMouseX = 0
        self.lastMouseY = 0

        self.dragging = False
        self.accept("mouse1", self.handleDragStart)
        self.accept("mouse1-up", self.handleDragStop)

        self.rotating = False
        self.accept("mouse3", self.handleRotateStart)
        self.accept("mouse3-up", self.handleRotateStop)

        self.accept("wheel_up", self.handleZoomIn)
        self.accept("wheel_down", self.handleZoomOut)

        base.task_mgr.add(self.update, "camera-update")

    def update(self, task):
        self.handleMouseUpdate()
        self.updatePositions()

        return task.cont

    def updatePositions(self):
        # Apply x and y as relative properties
        self.slider.setX(self.slider, self.x - self.lastX)
        self.slider.setY(self.slider, self.y - self.lastY)
        self.lastX = self.x
        self.lastY = self.y

        # Apply heading, pitch, and zoom as absolute properties
        self.slider.setH(self.heading)
        self.pivot.setP(-self.pitch)
        self.mount.setY(-self.zoom)

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

    def handleMouseUpdate(self):
        mouseX = self.lastMouseX
        mouseY = self.lastMouseY

        if self.base.mouseWatcherNode.hasMouse():
            mouseX = self.base.mouseWatcherNode.getMouseX()
            mouseY = self.base.mouseWatcherNode.getMouseY()

        dX = mouseX - self.lastMouseX
        dY = mouseY - self.lastMouseY

        if self.dragging:
            self.x += -dX * self.movementFactor
            self.y += -dY * self.movementFactor
        elif self.rotating:
            self.pitch += -dY * self.rotateFactor
            self.heading += -dX * self.rotateFactor

        self.lastMouseX = mouseX
        self.lastMouseY = mouseY
