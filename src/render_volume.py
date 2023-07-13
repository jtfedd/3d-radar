import math

import numpy as np
from direct.filter.FilterManager import FilterManager
from direct.showbase.DirectObject import DirectObject
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from panda3d.core import GeomEnums, GraphicsWindow, PTA_float, Shader, Texture

from lib.camera.camera_control import CameraControl
from lib.util.optional import unwrap
from lib.util.util import defaultLight, getData


class App(DirectObject):
    def __init__(self, showbase: ShowBase) -> None:
        self.base = showbase
        self.base.setFrameRateMeter(True)
        self.base.setBackgroundColor(0, 0, 0, 1)

        self.cameraControl = CameraControl(self.base)
        defaultLight(self.base)

        scan = getData()

        self.cube = unwrap(self.base.loader.loadModel("assets/cube.glb"))
        self.cube.reparentTo(self.base.render)
        self.cube.setScale(0)

        shader = Shader.load(
            Shader.SL_GLSL,
            vertex="shader/vertex.glsl",
            fragment="shader/fragment.glsl",
        )

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
        base.taskMgr.add(self.updateCameraParams, "update-camera-params")
        base.taskMgr.add(self.updateCubePos, "update-cube-pos")
        base.taskMgr.add(self.updateTime, "update-time")

        data = scan.reflectivity
        data = data - np.nanmin(data)
        data = data / np.nanmax(data)
        data = np.nan_to_num(data, nan=0)
        dataBytes = data.flatten().tobytes()

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
        for i, el in enumerate(scan.elevations):
            elevations.setElement(i, math.radians(el))
        self.plane.setShaderInput("el_values", elevations)

        self.plane.setShaderInput("az_length", 720)
        self.plane.setShaderInput("az_step", math.pi / 360)

        self.plane.setShaderInput("r_length", 2001)
        self.plane.setShaderInput("r_min", float(scan.ranges[0]))
        self.plane.setShaderInput("r_step", 0.25)

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
print("Max buffer size: %d" % (base.win.get_gsg().get_max_buffer_texture_size()))

app = App(base)
base.run()
