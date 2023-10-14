import math

import numpy as np
from direct.filter.FilterManager import FilterManager
from direct.showbase.DirectObject import DirectObject
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from panda3d.core import GeomEnums, GraphicsWindow, PTA_float, Shader, Texture

from lib.model.scan import Scan
from lib.util.optional import unwrap


class VolumeRenderer(DirectObject):
    def __init__(self, showbase: ShowBase) -> None:
        self.base = showbase

        shader = Shader.load(
            Shader.SL_GLSL,
            vertex="shader/vertex.glsl",
            fragment="shader/fragment.glsl",
        )

        self.densityMin = 0.0
        self.densityMax = 1.0

        manager = FilterManager(self.base.win, self.base.cam)  # type: ignore
        scene = Texture()
        depth = Texture()
        self.plane = unwrap(manager.renderSceneInto(colortex=scene, depthtex=depth))

        self.plane.setShader(shader)
        self.plane.setShaderInput("scene", scene)
        self.plane.setShaderInput("depth", depth)
        self.plane.setShaderInput("bounds_start", (-1000, -1000, 0))
        self.plane.setShaderInput("bounds_end", (1000, 1000, 20))
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
        self.base.taskMgr.add(self.updateCameraParams, "update-camera-params")
        self.base.taskMgr.add(self.updateTime, "update-time")

    def updateVolumeData(self, scan: Scan) -> None:
        # velocity scale: -100 to 100
        # reflectivity scale: -35 to 80

        # density curve
        # k -0.5..1
        # density = abs(d)^(10^k)
        k = 0.5

        scaleMin = -35
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

        # Params for rendering the volume
        densityMin = 0
        densityMax = 1
        densityScale = densityMax - densityMin
        densityExp = math.pow(10, k)

        self.plane.setShaderInput("d_min", densityMin)
        self.plane.setShaderInput("d_scale", densityScale)
        self.plane.setShaderInput("d_exp", densityExp)

        # Params to change to get velocity to be both negative and positive
        # reflectivity = 0, 1
        # velocity = -0.5, 2
        self.plane.setShaderInput("d_offset", 0)
        self.plane.setShaderInput("d_factor", 1)

        # Load the color scale image and send it to the shader
        colorScale = self.base.loader.loadTexture("assets/reflectivity_scale.png")
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

        self.plane.setShaderInput("r_length", 2001)
        self.plane.setShaderInput("r_min", float(scan.ranges[0]))
        self.plane.setShaderInput("r_step", 0.25)

    def updateDensityExponent(self, k: float) -> None:
        densityExp = math.pow(10, k)
        self.plane.setShaderInput("d_exp", densityExp)

    def updateMin(self, value: float) -> None:
        self.densityMin = value
        self.plane.setShaderInput("d_min", self.densityMin)
        self.plane.setShaderInput("d_scale", self.densityMax - self.densityMin)

    def updateMax(self, value: float) -> None:
        self.densityMax = value
        self.plane.setShaderInput("d_scale", self.densityMax - self.densityMin)

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

    def updateTime(self, task: Task.Task) -> int:
        self.plane.setShaderInput("time", task.time)

        return task.cont
