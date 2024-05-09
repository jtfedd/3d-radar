from panda3d.core import AmbientLight, DirectionalLight

from lib.app.context import AppContext
from lib.app.state import AppState
from lib.util.events.listener import Listener


class LightingManager(Listener):
    def __init__(self, ctx: AppContext, state: AppState):
        super().__init__()

        self.ctx = ctx

        self.headingRoot = ctx.base.render.attachNewNode("light-heading-root")
        self.pitchRoot = self.headingRoot.attachNewNode("light-pitch-root")

        self.alight = AmbientLight("alight")
        self.alnp = ctx.base.render.attachNewNode(self.alight)
        ctx.base.render.setLight(self.alnp)

        self.dlight = DirectionalLight("dlight")
        self.dlnp = self.pitchRoot.attachNewNode(self.dlight)
        ctx.base.render.setLight(self.dlnp)

        self.bind(state.ambientLightIntensity, self.updateAmbientIntensity)
        self.bind(state.directionalLightIntensity, self.updateDirectionalIntensity)
        self.bind(state.directionalLightHeading, self.updateDirectionalHeading)
        self.bind(state.directionalLightPitch, self.updateDirectionalPitch)

    def updateAmbientIntensity(self, ali: float) -> None:
        self.alight.setColor((ali, ali, ali, 1))

    def updateDirectionalIntensity(self, dli: float) -> None:
        self.dlight.setColor((dli, dli, dli, 1))

    def updateDirectionalHeading(self, dlh: float) -> None:
        self.headingRoot.setH(dlh * -360)

    def updateDirectionalPitch(self, dlp: float) -> None:
        self.pitchRoot.setP(dlp * -90)

    def destroy(self) -> None:
        super().destroy()

        self.ctx.base.render.clearLight(self.alnp)
        self.ctx.base.render.clearLight(self.dlnp)

        self.alnp.removeNode()
        self.dlnp.removeNode()

        self.pitchRoot.removeNode()
        self.headingRoot.removeNode()
