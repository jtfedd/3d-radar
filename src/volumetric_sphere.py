import math

from direct.filter.FilterManager import FilterManager
from direct.showbase.DirectObject import DirectObject
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from panda3d.core import GraphicsWindow, Shader, Texture

from lib.camera.camera_control import CameraControl
from lib.util.optional import unwrap
from lib.util.util import defaultLight


class App(DirectObject):
    def __init__(self, showbase: ShowBase) -> None:
        self.base = showbase

        self.base.setBackgroundColor(0, 0, 0, 1)
        defaultLight(self.base)

        self.cameraControl = CameraControl(self.base)
        self.cameraControl.zoom = 15

        self.cube = unwrap(self.base.loader.loadModel("../assets/cube.glb"))
        self.cube.reparentTo(self.base.render)

        shader = Shader.load(
            Shader.SL_GLSL,
            vertex="shaders/vertex_passthrough.glsl",
            fragment="shaders/fragment_volumetric_sphere.glsl",
        )

        manager = FilterManager(self.base.win, self.base.cam)  # type: ignore
        scene = Texture()
        depth = Texture()
        self.plane = unwrap(manager.renderSceneInto(colortex=scene, depthtex=depth))

        self.plane.setShader(shader)
        self.plane.setShaderInput("scene", scene)
        self.plane.setShaderInput("depth", depth)
        self.plane.setShaderInput("bounds_start", (0, -2, -2))
        self.plane.setShaderInput("bounds_end", (2, 2, 2))
        self.plane.setShaderInput("camera", self.base.camera)
        self.plane.setShaderInput("time_ms", 0)

        self.plane.setShaderInput(
            "projection_matrix_inverse",
            self.base.cam.node().getLens().getProjectionMatInv(),
        )

        # For some reason this seems to be typed incorrectly; override the type
        window: GraphicsWindow = self.base.win  # type: ignore
        self.windowSize = (window.getXSize(), window.getYSize())
        self.plane.setShaderInput("resolution", self.windowSize)

        self.accept("window-event", self.handleWindowEvent)
        base.taskMgr.add(self.updateCameraParams, "update-camera-params")
        base.taskMgr.add(self.updateCubePos, "update-cube-pos")
        base.taskMgr.add(self.updateTime, "update-time")

    def handleWindowEvent(self, win: GraphicsWindow) -> None:
        newSize = (win.getXSize(), win.getYSize())
        if newSize[0] == self.windowSize[0] and newSize[1] == self.windowSize[1]:
            return

        self.windowSize = newSize
        self.plane.setShaderInput("resolution", self.windowSize)

    def updateCameraParams(self, task: Task.Task) -> int:
        self.plane.setShaderInput(
            "camera_position",
            self.base.camera.getPos(self.base.render),
        )

        self.plane.setShaderInput(
            "projection_matrix_inverse",
            self.base.cam.node().getLens().getProjectionMatInv(),
        )

        return task.cont

    def updateCubePos(self, task: Task.Task) -> int:
        self.cube.setX(math.sin(task.time) * 3)

        return task.cont

    def updateTime(self, task: Task.Task) -> int:
        self.plane.setShaderInput("time", task.time)

        return task.cont


base = ShowBase()
app = App(base)
base.run()
