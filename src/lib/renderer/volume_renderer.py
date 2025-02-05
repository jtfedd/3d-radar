from direct.filter.FilterManager import FilterManager
from direct.task import Task
from panda3d.core import Shader, Texture, Vec3

from lib.app.context import AppContext
from lib.app.state import AppState
from lib.map.constants import EARTH_RADIUS, RADAR_RANGE
from lib.util.events.listener import Listener
from lib.util.optional import unwrap


class VolumeRenderer(Listener):
    def __init__(self, ctx: AppContext, state: AppState) -> None:
        super().__init__()

        self.ctx = ctx
        self.state = state

        self.smoothShader = Shader.load(
            Shader.SL_GLSL,
            vertex="shaders/gen/volume_vertex.glsl",
            fragment="shaders/gen/volume_smooth_fragment.glsl",
        )

        self.sharpShader = Shader.load(
            Shader.SL_GLSL,
            vertex="shaders/gen/volume_vertex.glsl",
            fragment="shaders/gen/volume_sharp_fragment.glsl",
        )

        manager = FilterManager(self.ctx.base.win, self.ctx.base.cam)
        scene = Texture()
        depth = Texture()
        self.plane = unwrap(manager.renderSceneInto(colortex=scene, depthtex=depth))

        self.bind(state.smooth, self.updateShader)

        ctx.windowManager.resolutionProvider.addNode(self.plane)

        self.plane.setShaderInput("scene", scene)
        self.plane.setShaderInput("depth", depth)
        self.plane.setShaderInput("earth_center", Vec3(0, 0, -EARTH_RADIUS))
        self.plane.setShaderInput("earth_radius", EARTH_RADIUS)
        self.plane.setShaderInput("camera", self.ctx.base.camera)
        self.plane.setShaderInput("time", 0)

        self.bind(state.view3D, lambda _: self.updateBounds())

        self.plane.setShaderInput(
            "projection_matrix_inverse",
            self.ctx.base.camLens.getProjectionMatInv(),
        )

        self.cameraTask = self.ctx.base.taskMgr.add(
            self.updateCameraParams, "update-camera-params"
        )
        self.timeTask = self.ctx.base.taskMgr.add(self.updateTime, "update-time")

    def updateBounds(self) -> None:
        if self.state.view3D.getValue():
            self.plane.setShaderInput("bounds_start", (-RADAR_RANGE, -RADAR_RANGE, 0))
            self.plane.setShaderInput("bounds_end", (RADAR_RANGE, RADAR_RANGE, 15))
        else:
            self.plane.setShaderInput("bounds_start", (0, 0, -1))
            self.plane.setShaderInput("bounds_end", (0, 0, -1))

    def updateShader(self, smooth: bool) -> None:
        self.plane.setShader(self.smoothShader if smooth else self.sharpShader)

    def updateCameraParams(self, task: Task.Task) -> int:
        self.plane.setShaderInput(
            "camera_position",
            self.ctx.base.camera.getPos(self.ctx.base.render),
        )

        self.plane.setShaderInput(
            "projection_matrix_inverse",
            self.ctx.base.camLens.getProjectionMatInv(),
        )

        return task.cont

    def updateTime(self, task: Task.Task) -> int:
        self.plane.setShaderInput("time", task.time)

        return task.cont

    def destroy(self) -> None:
        super().destroy()

        self.ctx.windowManager.resolutionProvider.removeNode(self.plane)

        self.cameraTask.cancel()
        self.timeTask.cancel()
