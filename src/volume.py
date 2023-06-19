from direct.showbase.ShowBase import ShowBase
from panda3d.core import Shader, WindowProperties


class App(ShowBase):
    def __init__(self) -> None:
        ShowBase.__init__(self)
        self.setBackgroundColor(0, 0, 0, 1)
        # self.wireframe On()
        self.cam.setPos(0, -4, 0)

        self.accept("window-event", self.handleWindowEvent)

        shader = Shader.load(
            Shader.SL_GLSL,
            vertex="shaders/volume-vert.glsl",
            fragment="shaders/volume-frag.glsl",
        )

        plane = self.loader.loadModel("../assets/plane.glb")
        if plane:
            self.plane = plane

        self.plane.reparentTo(self.render)
        self.plane.setP(90)
        self.plane.setShader(shader)

        self.windowSize = self.getSize()
        self.plane.setShaderInput("resolution", self.windowSize)

    def handleWindowEvent(self, _: WindowProperties) -> None:
        newSize = self.getSize()
        if newSize[0] == self.windowSize[0] and newSize[1] == self.windowSize[1]:
            return

        self.windowSize = newSize
        self.plane.setShaderInput("resolution", self.windowSize)


app = App()

app.run()
