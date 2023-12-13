import math
from typing import Dict

import numpy as np
from direct.filter.FilterManager import FilterManager
from direct.task import Task
from panda3d.core import GeomEnums, GraphicsWindow, PTA_float, Shader, Texture

from lib.app.context import AppContext
from lib.app.events import AppEvents
from lib.app.state import AppState
from lib.model.scan import Scan
from lib.util.events.listener import Listener
from lib.util.optional import unwrap


class VolumeRenderer(Listener):
    def __init__(self, ctx: AppContext, state: AppState, events: AppEvents) -> None:
        super().__init__()

        self.ctx = ctx
        self.state = state

        self.data: Dict[str, Scan] = {}

        shader = Shader.load(
            Shader.SL_GLSL,
            vertex="shader/vertex.glsl",
            fragment="shader/fragment.glsl",
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
        self.plane.setShaderInput("time_ms", 0)

        self.plane.setShaderInput(
            "projection_matrix_inverse",
            self.ctx.base.cam.node().getLens().getProjectionMatInv(),
        )

        self.setDensityParams()
        self.listen(self.state.volumeMin, lambda _: self.setDensityParams())
        self.listen(self.state.volumeMax, lambda _: self.setDensityParams())
        self.listen(self.state.volumeFalloff, lambda _: self.setDensityParams())

        # For some reason this seems to be typed incorrectly; override the type
        window: GraphicsWindow = self.ctx.base.win  # type: ignore
        self.windowSize = (window.getXSize(), window.getYSize())
        self.plane.setShaderInput("resolution", self.windowSize)
        self.listen(events.window.onWindowUpdate, self.handleWindowEvent)

        self.ctx.base.taskMgr.add(self.updateCameraParams, "update-camera-params")
        self.ctx.base.taskMgr.add(self.updateTime, "update-time")

        self.listen(state.animationFrame, lambda _: self.updateFrame())
        self.listen(state.dataType, lambda _: self.updateFrame())

    def setData(self, data: Dict[str, Scan]) -> None:
        self.data = data
        self.updateFrame()

    def updateFrame(self) -> None:
        if not self.state.animationFrame:
            return

        if self.state.animationFrame.value not in self.data:
            return

        self.updateVolumeData(self.data[self.state.animationFrame.value])

    def updateVolumeData(self, scan: Scan) -> None:
        # velocity scale: -100 to 100
        # reflectivity scale: -20 to 80
        scaleMin = -20
        scaleMax = 80

        # Scale the data to 0..1, based on the scale range, and clip any outliers
        data = scan.reflectivity
        data = data - scaleMin
        data = data / (scaleMax - scaleMin)
        data = np.clip(data, 0, 1)

        # Turn any nan into -1
        data = np.nan_to_num(data, nan=-1)

        # Get the bytes
        dataBytes = data.flatten().tobytes()

        # Params to change to get velocity to be both negative and positive
        # reflectivity = 0, 1
        # velocity = -0.5, 2
        self.plane.setShaderInput("d_offset", 0)
        self.plane.setShaderInput("d_factor", 1)

        # Load the color scale image and send it to the shader
        colorScale = self.ctx.base.loader.loadTexture("assets/reflectivity_scale.png")
        self.plane.setShaderInput("color_scale", colorScale)

        buffer = Texture("volume_data")
        buffer.setup_buffer_texture(
            len(dataBytes), Texture.T_float, Texture.F_r32, GeomEnums.UH_dynamic
        )
        self.plane.setShaderInput("volume_data", buffer)

        dataView = memoryview(buffer.modifyRamImage())  # type: ignore
        dataView[0 : len(dataBytes)] = dataBytes

        self.plane.setShaderInput("el_min", float(scan.elevations[0]))
        self.plane.setShaderInput("el_max", float(scan.elevations[-1]))

        self.plane.setShaderInput("el_length", len(scan.elevations))

        elevations = PTA_float.emptyArray(20)
        for i, elevation in enumerate(scan.elevations):
            elevations.setElement(i, math.radians(elevation))
        self.plane.setShaderInput("el_values", elevations)

        self.plane.setShaderInput("az_length", 720)
        self.plane.setShaderInput("az_step", math.pi / 360)

        self.plane.setShaderInput("r_length", scan.reflectivity.shape[2])
        self.plane.setShaderInput("r_min", float(scan.ranges[0]))
        self.plane.setShaderInput("r_step", 0.25)

    def setDensityParams(self) -> None:
        # Params for rendering the volume
        densityMin = self.state.volumeMin.value
        densityMax = self.state.volumeMax.value
        densityScale = densityMax - densityMin
        densityExp = math.pow(10, self.state.volumeFalloff.value)

        self.plane.setShaderInput("d_min", densityMin)
        self.plane.setShaderInput("d_scale", densityScale)
        self.plane.setShaderInput("d_exp", densityExp)

    def handleWindowEvent(self, win: GraphicsWindow) -> None:
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
