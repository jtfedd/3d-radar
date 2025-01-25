from panda3d.core import Shader, Vec3

from lib.app.context import AppContext
from lib.app.state import AppState
from lib.map.constants import EARTH_RADIUS
from lib.util.events.listener import Listener
from lib.util.optional import unwrap


class SurfaceRenderer(Listener):
    def __init__(self, ctx: AppContext, state: AppState) -> None:
        super().__init__()

        self.ctx = ctx
        self.state = state

        self.smoothShader = Shader.load(
            Shader.SL_GLSL,
            vertex="shaders/gen/surface_vertex.glsl",
            fragment="shaders/gen/surface_smooth_fragment.glsl",
        )

        self.sharpShader = Shader.load(
            Shader.SL_GLSL,
            vertex="shaders/gen/surface_vertex.glsl",
            fragment="shaders/gen/surface_sharp_fragment.glsl",
        )

        self.surface = unwrap(
            ctx.base.loader.loadModel("assets/models/earth_surface.glb")
        )
        self.surface.reparentTo(ctx.base.render)
        self.surface.setZ(-EARTH_RADIUS)
        self.surface.setScale(EARTH_RADIUS)

        self.bind(state.smooth, self.updateShader)
        self.surface.setShaderInput("earth_center", Vec3(0, 0, -EARTH_RADIUS))

    def updateShader(self, smooth: bool) -> None:
        self.surface.setShader(self.smoothShader if smooth else self.sharpShader)

    def destroy(self) -> None:
        super().destroy()

        self.surface.removeNode()
