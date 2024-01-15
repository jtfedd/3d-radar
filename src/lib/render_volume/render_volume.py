from direct.filter.FilterManager import FilterManager
from direct.task import Task
from panda3d.core import GraphicsWindow, Shader, Texture

from lib.app.context import AppContext
from lib.app.events import AppEvents
from lib.app.state import AppState
from lib.util.events.listener import Listener
from lib.util.optional import unwrap

from .volume_data_provider import VolumeDataProvider


class VolumeRenderer(Listener):
    def __init__(self, ctx: AppContext, state: AppState, events: AppEvents) -> None:
        super().__init__()

        self.ctx = ctx
        self.state = state

        shader = Shader.load(
            Shader.SL_GLSL,
            vertex="shader/vertex.glsl",
            fragment="shader/fragment.glsl",
        )

        self.reflectivityScale = self.ctx.base.loader.loadTexture(
            "assets/reflectivity_scale.png"
        )
        self.velocityScale = self.ctx.base.loader.loadTexture(
            "assets/velocity_scale.png"
        )

        manager = FilterManager(self.ctx.base.win, self.ctx.base.cam)  # type: ignore
        scene = Texture()
        depth = Texture()
        self.plane = unwrap(manager.renderSceneInto(colortex=scene, depthtex=depth))

        self.plane.setShader(shader)
        self.plane.setShaderInput("scene", scene)
        self.plane.setShaderInput("depth", depth)
        self.plane.setShaderInput("bounds_start", (-1000, -1000, 0))
        self.plane.setShaderInput("bounds_end", (1000, 1000, 20))
        self.plane.setShaderInput("camera", self.ctx.base.camera)
        self.plane.setShaderInput("time", 0)

        self.plane.setShaderInput(
            "projection_matrix_inverse",
            self.ctx.base.cam.node().getLens().getProjectionMatInv(),
        )

        # For some reason this seems to be typed incorrectly; override the type
        window: GraphicsWindow = self.ctx.base.win  # type: ignore
        self.windowSize = (0, 0)
        self.updateScreenResolution(window)
        self.listen(events.window.onWindowUpdate, self.updateScreenResolution)

        self.ctx.base.taskMgr.add(self.updateCameraParams, "update-camera-params")
        self.ctx.base.taskMgr.add(self.updateTime, "update-time")

        self.volumeDataProvider = VolumeDataProvider(ctx, state, events)
        self.volumeDataProvider.addNode(self.plane)

    def updateScreenResolution(self, win: GraphicsWindow) -> None:
        newSize = (win.getXSize(), win.getYSize())
        if newSize[0] == self.windowSize[0] and newSize[1] == self.windowSize[1]:
            return

        self.windowSize = newSize
        self.plane.setShaderInput("resolution", self.windowSize)

    def updateCameraParams(self, task: Task.Task) -> int:
        self.plane.setShaderInput(
            "camera_position",
            self.ctx.base.camera.getPos(self.ctx.base.render),
        )

        self.plane.setShaderInput(
            "projection_matrix_inverse",
            self.ctx.base.cam.node().getLens().getProjectionMatInv(),
        )

        return task.cont

    def updateTime(self, task: Task.Task) -> int:
        self.plane.setShaderInput("time", task.time)

        return task.cont
