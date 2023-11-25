from __future__ import annotations

from direct.task.Task import Task
from panda3d.core import PythonTask

from lib.app.context import AppContext
from lib.app.events import AppEvents
from lib.app.state import AppState
from lib.ui.core.constants import UIConstants
from lib.util.events.listener import Listener


class UIAnchors(Listener):
    ANIMATION_TIME = 0.1

    def __init__(
        self,
        ctx: AppContext,
        state: AppState,
        events: AppEvents,
    ):
        super().__init__()

        self.ctx = ctx
        self.state = state
        self.events = events

        self.animating = False
        self.hidden = False
        self.hideFactor = 0.0

        self.width = 1.0
        self.height = 1.0

        root = self.ctx.base.aspect2dp

        self.center = root.attachNewNode("center")

        self.top = root.attachNewNode("top")
        self.bottom = root.attachNewNode("bottom")
        self.left = root.attachNewNode("left")
        self.right = root.attachNewNode("right")

        self.topLeft = root.attachNewNode("top-left")
        self.topRight = root.attachNewNode("top-right")
        self.bottomLeft = root.attachNewNode("bottom-left")
        self.bottomRight = root.attachNewNode("bottom-right")

        self.update()
        self.listen(self.events.window.onWindowUpdate, lambda _: self.update())
        self.listen(self.events.input.onHide, lambda _: self.toggleHide())
        self.listen(self.state.uiScale, lambda _: self.update())

        self.hideTask: PythonTask | None = None

    def toggleHide(self) -> None:
        if self.animating:
            return

        self.animating = True

        if self.hidden:
            self.hideTask = self.ctx.base.addTask(self.show, "show-anchors")
        else:
            self.hideTask = self.ctx.base.addTask(self.hide, "hide-anchors")

    def hide(self, task: Task) -> int:
        progress = task.time / self.ANIMATION_TIME

        if progress >= 1.0:
            self.hideFactor = 1.0
            self.animating = False
            self.hidden = True
            self.update()
            return task.exit

        self.hideFactor = progress
        self.update()

        return task.cont

    def show(self, task: Task) -> int:
        progress = task.time / self.ANIMATION_TIME

        if progress >= 1.0:
            self.hideFactor = 0.0
            self.animating = False
            self.hidden = False
            self.update()
            return task.exit

        self.hideFactor = 1 - progress
        self.update()

        return task.cont

    def update(self) -> None:
        aspectRatio = self.ctx.base.getAspectRatio()

        width = aspectRatio
        height = 1.0

        if aspectRatio < 1.0:
            width = 1.0
            height = 1 / aspectRatio

        scale = self.state.uiScale.value

        top = height + (self.hideFactor * UIConstants.headerFooterHeight * scale)
        bottom = -height - (self.hideFactor * UIConstants.headerFooterHeight * scale)
        right = width
        left = -width - (self.hideFactor * UIConstants.panelWidth * scale)

        self.height = top - bottom
        self.width = right - left

        # Update positions
        self.center.setPos(0, 0, 0)

        self.top.setPos(0, 0, top)
        self.bottom.setPos(0, 0, bottom)
        self.left.setPos(left, 0, 0)
        self.right.setPos(0, 0, right)

        self.topLeft.setPos(left, 0, top)
        self.topRight.setPos(right, 0, top)
        self.bottomLeft.setPos(left, 0, bottom)
        self.bottomRight.setPos(right, 0, bottom)

        # Update scale
        self.center.setScale(scale)

        self.top.setScale(scale)
        self.bottom.setScale(scale)
        self.left.setScale(scale)
        self.right.setScale(scale)

        self.topLeft.setScale(scale)
        self.topRight.setScale(scale)
        self.bottomLeft.setScale(scale)
        self.bottomRight.setScale(scale)

        self.events.ui.onAnchorUpdate.send(None)

    def destroy(self) -> None:
        super().destroy()

        if self.hideTask:
            self.hideTask.cancel()

        self.center.removeNode()

        self.top.removeNode()
        self.bottom.removeNode()
        self.left.removeNode()
        self.right.removeNode()

        self.topLeft.removeNode()
        self.topRight.removeNode()

        self.bottomLeft.removeNode()
        self.bottomRight.removeNode()
