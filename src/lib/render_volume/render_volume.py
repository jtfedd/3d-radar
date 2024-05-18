from direct.filter.FilterManager import FilterManager
from direct.task import Task
from panda3d.core import Shader, Texture

from lib.app.context import AppContext
from lib.app.state import AppState
from lib.map.constants import RADAR_RANGE
from lib.util.events.listener import Listener
from lib.util.optional import unwrap

from .lighting_data_provider import LightingDataProvider
from .volume_data_provider import VolumeDataProvider


class VolumeRenderer(Listener):
    def __init__(self, ctx: AppContext, state: AppState) -> None:
        super().__init__()

        self.ctx = ctx
        self.state = state

        self.smoothShader = Shader.load(
            Shader.SL_GLSL,
            vertex="shaders/gen/vertex.glsl",
            fragment="shaders/gen/fragment_smooth.glsl",
        )

        self.sharpShader = Shader.load(
            Shader.SL_GLSL,
            vertex="shaders/gen/vertex.glsl",
            fragment="shaders/gen/fragment_sharp.glsl",
        )

        manager = FilterManager(self.ctx.base.win, self.ctx.base.cam)
        scene = Texture()
        depth = Texture()
        self.plane = unwrap(manager.renderSceneInto(colortex=scene, depthtex=depth))

        self.updateShader(state.smooth.value)
        self.listen(state.smooth, self.updateShader)

        self.plane.setShaderInput("scene", scene)
        self.plane.setShaderInput("depth", depth)
        self.plane.setShaderInput("bounds_start", (-RADAR_RANGE, -RADAR_RANGE, 0))
        self.plane.setShaderInput("bounds_end", (RADAR_RANGE, RADAR_RANGE, 15))
        self.plane.setShaderInput("camera", self.ctx.base.camera)
        self.plane.setShaderInput("time", 0)

        self.plane.setShaderInput(
            "projection_matrix_inverse",
            self.ctx.base.cam.node().getLens().getProjectionMatInv(),
        )

        self.cameraTask = self.ctx.base.taskMgr.add(
            self.updateCameraParams, "update-camera-params"
        )
        self.timeTask = self.ctx.base.taskMgr.add(self.updateTime, "update-time")

        self.volumeDataProvider = VolumeDataProvider(ctx, state)
        self.lightingDataProvider = LightingDataProvider(ctx, state)
        self.volumeDataProvider.addNode(self.plane)
        self.lightingDataProvider.addNode(self.plane)

    def updateShader(self, smooth: bool) -> None:
        if smooth:
            self.plane.setShader(self.smoothShader)
        else:
            self.plane.setShader(self.sharpShader)

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

    def destroy(self) -> None:
        super().destroy()

        self.lightingDataProvider.destroy()
        self.volumeDataProvider.destroy()

        self.cameraTask.cancel()
        self.timeTask.cancel()
