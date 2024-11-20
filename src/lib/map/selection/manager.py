import copy

from panda3d.core import (
    CollisionHandlerQueue,
    CollisionNode,
    CollisionRay,
    CollisionSphere,
    CollisionTraverser,
    LPoint2,
)

from lib.app.context import AppContext
from lib.app.events import AppEvents
from lib.map.constants import EARTH_RADIUS
from lib.util.events.listener import Listener


class SelectionManager(Listener):
    def __init__(self, ctx: AppContext, events: AppEvents) -> None:
        super().__init__()

        self.ctx = ctx

        self.savedMousePos: LPoint2 | None = None

        self.cs = CollisionSphere(0, 0, 0, EARTH_RADIUS)
        self.cnodePath = ctx.base.render.attachNewNode(CollisionNode("cnode"))
        self.cnodePath.setZ(-EARTH_RADIUS)
        self.cnodePath.node().addSolid(self.cs)

        self.cr = CollisionRay()
        self.rnodePath = ctx.base.camera.attachNewNode(CollisionNode("rnode"))
        self.rnodePath.node().addSolid(self.cr)

        self.handler = CollisionHandlerQueue()

        self.traverser = CollisionTraverser("mouse picker")
        self.traverser.addCollider(self.rnodePath, self.handler)

        # Debug
        self.cnodePath.show()
        self.traverser.showCollisions(ctx.base.render)

        self.listen(events.input.rightMouse, self.onSelect)

    def onSelect(self, isDown: bool) -> None:
        if not self.ctx.base.mouseWatcherNode.hasMouse():
            self.savedMousePos = None
            return

        mpos = self.ctx.base.mouseWatcherNode.getMouse()

        if isDown:
            self.savedMousePos = copy.copy(mpos)
            return

        if self.savedMousePos is None or mpos != self.savedMousePos:
            self.savedMousePos = None
            return

        self.savedMousePos = None

        self.cr.setFromLens(self.ctx.base.camNode, mpos.x, mpos.y)
        self.traverser.traverse(self.cnodePath)
        if self.handler.getNumEntries() > 0:
            self.handler.sortEntries()
            # TODO calculate geopoint
