from panda3d.core import Shader, TransparencyAttrib, Vec3

from lib.app.context import AppContext
from lib.app.state import AppState
from lib.map.constants import EARTH_RADIUS
from lib.model.data_type import DataType
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
        self.triggerMany(
            [state.showSurfaceLayer, state.view3D],
            self.updateVisibility,
            triggerImmediately=True,
        )
        self.bind(
            state.surfaceOpacity,
            lambda opacity: self.surface.setShaderInput("opacity", opacity),
        )
        self.triggerMany(
            [state.velThreshold, state.refThreshold, state.dataType],
            self.updateThreshold,
            triggerImmediately=True,
        )
        self.triggerMany(
            [state.velComposite, state.refComposite, state.dataType],
            self.updateComposite,
            triggerImmediately=True,
        )
        self.surface.setShaderInput("earth_center", Vec3(0, 0, -EARTH_RADIUS))

    def updateVisibility(self) -> None:
        visible = (
            self.state.showSurfaceLayer.getValue() or not self.state.view3D.getValue()
        )

        if visible:
            self.surface.show()
        else:
            self.surface.hide()

    def updateThreshold(self) -> None:
        threshold = (
            self.state.refThreshold.getValue()
            if self.state.dataType.getValue() == DataType.REFLECTIVITY
            else self.state.velThreshold.getValue()
        )

        self.surface.setShaderInput("threshold", threshold)

    def updateComposite(self) -> None:
        composite = (
            self.state.refComposite.getValue()
            if self.state.dataType.getValue() == DataType.REFLECTIVITY
            else self.state.velComposite.getValue()
        )

        self.surface.setShaderInput("max_el_index", 100 if composite else 1)

    def updateShader(self, smooth: bool) -> None:
        self.surface.setShader(self.smoothShader if smooth else self.sharpShader)

    def destroy(self) -> None:
        super().destroy()

        self.surface.removeNode()
