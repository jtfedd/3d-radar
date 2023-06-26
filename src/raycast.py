from direct.filter.FilterManager import FilterManager
from direct.showbase.DirectObject import DirectObject
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from panda3d.core import GraphicsWindow, NodePath, Shader, Texture, TransparencyAttrib

from lib.camera.camera_control import CameraControl
from lib.util.optional import unwrap
from lib.util.util import defaultLight


class App(DirectObject):
    def setupShader(self, shader: Shader) -> NodePath:  # type:ignore
        # return self.setupShaderInCamera(shader)
        return self.setupShaderInFilter(shader)

    def __init__(self, showbase: ShowBase) -> None:
        self.base = showbase
        self.base.setBackgroundColor(0, 0, 0, 1)

        defaultLight(self.base)
        self.cameraControl = CameraControl(self.base)
        self.cameraControl.pitch = 0

        self.cube = unwrap(self.base.loader.loadModel("../assets/cube.glb"))
        self.cube.reparentTo(self.base.render)

        shader = Shader.load(
            Shader.SL_GLSL,
            vertex="shaders/vertex_passthrough.glsl",
            fragment="shaders/fragment_raycast.glsl",
        )

        self.plane = self.setupShader(shader)

        self.plane.setShaderInput("camera", self.base.camera)

        # For some reason this seems to be typed incorrectly; override the type
        window: GraphicsWindow = self.base.win  # type: ignore
        self.windowSize = (window.getXSize(), window.getYSize())
        self.plane.setShaderInput("resolution", self.windowSize)

        self.plane.setShaderInput(
            "projection_matrix_inverse",
            self.base.cam.node().getLens().getProjectionMatInv(),
        )

        self.accept("window-event", self.handleWindowEvent)
        base.taskMgr.add(self.updateCameraParams, "update-camera-params")

    def handleWindowEvent(self, win: GraphicsWindow) -> None:
        newSize = (win.getXSize(), win.getYSize())
        if newSize[0] == self.windowSize[0] and newSize[1] == self.windowSize[1]:
            return

        self.windowSize = newSize
        self.plane.setShaderInput("resolution", self.windowSize)

    def updateCameraParams(self, task: Task.Task) -> int:
        self.plane.setShaderInput(
            "projection_matrix_inverse",
            self.base.cam.node().getLens().getProjectionMatInv(),
        )

        return task.cont

    def setupShaderInCamera(self, shader: Shader) -> NodePath:  # type:ignore
        plane = unwrap(self.base.loader.loadModel("../assets/plane.glb"))

        plane.reparentTo(self.base.render)
        plane.setP(90)
        plane.setScale(100)
        plane.reparentTo(self.base.camera)
        plane.setY(10)
        plane.setShader(shader)
        plane.setTransparency(TransparencyAttrib.MAlpha)
        plane.setBin("fixed", 0)
        plane.setDepthTest(False)
        plane.setDepthWrite(False)

        return plane

    def setupShaderInFilter(self, shader: Shader) -> NodePath:  # type:ignore
        manager = FilterManager(self.base.win, self.base.cam)  # type: ignore
        scene = Texture()
        plane = unwrap(manager.renderSceneInto(colortex=scene))

        plane.setShader(shader)
        plane.setShaderInput("scene", scene)

        return plane


base = ShowBase()
app = App(base)
base.run()
