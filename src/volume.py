from direct.showbase.DirectObject import DirectObject
from direct.showbase.ShowBase import ShowBase
from panda3d.core import GraphicsWindow, Shader


class App(DirectObject):
    def __init__(self, showbase: ShowBase) -> None:
        self.base = showbase

        self.base.setBackgroundColor(0, 0, 0, 1)
        # self.wireframe On()
        self.base.cam.setPos(0, -40, 0)

        shader = Shader.load(
            Shader.SL_GLSL,
            vertex="shaders/volume-vert.glsl",
            fragment="shaders/volume-frag.glsl",
        )

        plane = self.base.loader.loadModel("../assets/plane.glb")
        if plane:
            self.plane = plane

        self.plane.reparentTo(self.base.render)
        self.plane.setP(90)
        self.plane.setScale(100)
        self.plane.setShader(shader)

        # For some reason this seems to be typed incorrectly; override the type
        window: GraphicsWindow = self.base.win  # type: ignore
        self.windowSize = (window.getXSize(), window.getYSize())

        self.plane.setShaderInput("resolution", self.windowSize)

        self.accept("window-event", self.handleWindowEvent)

    def handleWindowEvent(self, win: GraphicsWindow) -> None:
        newSize = (win.getXSize(), win.getYSize())
        if newSize[0] == self.windowSize[0] and newSize[1] == self.windowSize[1]:
            return

        self.windowSize = newSize
        self.plane.setShaderInput("resolution", self.windowSize)


base = ShowBase()
app = App(base)
base.run()
