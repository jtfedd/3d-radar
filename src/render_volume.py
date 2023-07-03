import math

import numpy as np
from direct.filter.FilterManager import FilterManager
from direct.showbase.DirectObject import DirectObject
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from panda3d.core import GeomEnums, GraphicsWindow, PTA_float, Shader, Texture

from lib.camera.camera_control import CameraControl
from lib.util.optional import unwrap
from lib.util.util import defaultLight


class App(DirectObject):
    def __init__(self, showbase: ShowBase) -> None:
        self.base = showbase
        self.base.setFrameRateMeter(True)

        self.base.setBackgroundColor(0, 0, 0, 1)
        defaultLight(self.base)

        self.cameraControl = CameraControl(self.base)
        self.cameraControl.zoom = 15

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
        self.plane.setShaderInput("bounds_start", (-3, -3, 0))
        self.plane.setShaderInput("bounds_end", (3, 3, 2))
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

        volume_data = np.array(
            [
                0.1,
                0,
                0,
                0.2,
                0.3,
                0,
                0,
                0.4,
                0,
                0.5,
                0.6,
                0,
                0,
                0.7,
                0.8,
                0,
            ]
        ).astype(np.float32)

        buffer = Texture("volume_data")
        buffer.setup_buffer_texture(
            64, Texture.T_float, Texture.F_r32, GeomEnums.UH_dynamic
        )
        self.plane.setShaderInput("volume_data", buffer)

        dataView = memoryview(buffer.modifyRamImage())  # type: ignore
        dataView[0:64] = volume_data.tobytes()

        self.plane.setShaderInput("el_min", 0.0)
        self.plane.setShaderInput("el_max", math.pi / 4)

        self.plane.setShaderInput("el_length", 2)

        elevations = PTA_float([0, math.pi / 8])
        self.plane.setShaderInput("el_values", elevations)

        self.plane.setShaderInput("az_length", 4)
        self.plane.setShaderInput("az_step", math.pi / 2)

        self.plane.setShaderInput("r_length", 2)
        self.plane.setShaderInput("r_min", 2.5)
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
app = App(base)
base.run()
