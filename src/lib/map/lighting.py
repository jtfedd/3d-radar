from panda3d.core import AmbientLight, DirectionalLight

from lib.app.context import AppContext
from lib.app.state import AppState
from lib.util.events.listener import Listener


class LightingManager(Listener):
    def __init__(self, ctx: AppContext, state: AppState):
        super().__init__()

        dlight = DirectionalLight("dlight")
        dlight.setColor((1, 1, 1, 1))
        dlnp = ctx.base.render.attachNewNode(dlight)
        dlnp.setHpr(0, -60, 0)
        ctx.base.render.setLight(dlnp)

        alight = AmbientLight("alight")
        alight.setColor((0.2, 0.2, 0.2, 1))
        alnp = ctx.base.render.attachNewNode(alight)
        ctx.base.render.setLight(alnp)
