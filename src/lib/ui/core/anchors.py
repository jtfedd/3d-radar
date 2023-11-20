from __future__ import annotations

from direct.showbase.DirectObject import DirectObject
from direct.showbase.ShowBase import ShowBase
from direct.task.Task import Task

from lib.ui.core.constants import UIConstants
from lib.ui.core.keybindings.keybinding_manager import KeybindingManager
from lib.util.events.event_dispatcher import EventDispatcher


class UIAnchors(DirectObject):
    ANIMATION_TIME = 0.1

    def __init__(self, base: ShowBase, keybindings: KeybindingManager, scale: float):
        self.base = base
        self.keybindings = keybindings
        self.scale = scale

        self.animating = False
        self.hidden = False
        self.hideFactor = 0.0

        self.width = 1.0
        self.height = 1.0

        root = base.aspect2dp

        self.center = root.attachNewNode("center")

        self.top = root.attachNewNode("top")
        self.bottom = root.attachNewNode("bottom")
        self.left = root.attachNewNode("left")
        self.right = root.attachNewNode("right")

        self.topLeft = root.attachNewNode("top-left")
        self.topRight = root.attachNewNode("top-right")
        self.bottomLeft = root.attachNewNode("bottom-left")
        self.bottomRight = root.attachNewNode("bottom-right")

        self.onUpdate = EventDispatcher[None]()

        self.update()
        self.accept("window-event", lambda _: self.update())
        self.hideSub = self.keybindings.hideEvent.listen(lambda _: self.toggleHide())

    def toggleHide(self) -> None:
        if self.animating:
            return

        self.animating = True

        if self.hidden:
            self.addTask(self.show, "show-anchors")
        else:
            self.addTask(self.hide, "hide-anchors")

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
        aspectRatio = self.base.getAspectRatio()

        width = aspectRatio
        height = 1.0

        if aspectRatio < 1.0:
            width = 1.0
            height = 1 / aspectRatio

        top = height + (self.hideFactor * UIConstants.headerFooterHeight)
        bottom = -height - (self.hideFactor * UIConstants.headerFooterHeight)
        right = width
        left = -width - (self.hideFactor * UIConstants.panelWidth)

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
        self.center.setScale(self.scale)

        self.top.setScale(self.scale)
        self.bottom.setScale(self.scale)
        self.left.setScale(self.scale)
        self.right.setScale(self.scale)

        self.topLeft.setScale(self.scale)
        self.topRight.setScale(self.scale)
        self.bottomLeft.setScale(self.scale)
        self.bottomRight.setScale(self.scale)

        self.onUpdate.send(None)

    def updateScale(self, newScale: float) -> None:
        self.scale = newScale
        self.update()

    def destroy(self) -> None:
        self.onUpdate.close()

        self.removeAllTasks()

        self.center.removeNode()

        self.top.removeNode()
        self.bottom.removeNode()
        self.left.removeNode()
        self.right.removeNode()

        self.topLeft.removeNode()
        self.topRight.removeNode()

        self.bottomLeft.removeNode()
        self.bottomRight.removeNode()

        self.ignoreAll()
        self.hideSub.cancel()
