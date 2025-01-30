from panda3d.core import Shader, TransparencyAttrib, Vec3

from lib.app.context import AppContext
from lib.app.state import AppState
from lib.map.constants import EARTH_RADIUS
from lib.ui.core.layers import UILayer
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
        self.surface.setBin("background", UILayer.RADAR_SURFACE.value)
        self.surface.setTransparency(TransparencyAttrib.MAlpha)

        self.bind(state.smooth, self.updateShader)
        self.bind(state.showSurfaceLayer, lambda _: self.updateVisibility())
        self.bind(
            state.surfaceOpacity,
            lambda opacity: self.surface.setShaderInput("opacity", opacity),
        )
        self.bind(
            state.surfaceThreshold,
            lambda threshold: self.surface.setShaderInput("threshold", threshold),
        )
        self.bind(
            state.surfaceComposite,
            lambda composite: self.surface.setShaderInput(
                "max_el_index", 100 if composite else 1
            ),
        )
        self.surface.setShaderInput("earth_center", Vec3(0, 0, -EARTH_RADIUS))

    def updateVisibility(self) -> None:
        visible = self.state.showSurfaceLayer.getValue()

        if visible:
            self.surface.show()
        else:
            self.surface.hide()

    def updateShader(self, smooth: bool) -> None:
        self.surface.setShader(self.smoothShader if smooth else self.sharpShader)

    def destroy(self) -> None:
        super().destroy()

        self.surface.removeNode()
