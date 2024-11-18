from __future__ import annotations

import math

import direct.gui.DirectGuiGlobals as DGG
from direct.task.Task import Task
from panda3d.core import NodePath, PandaNode

from lib.app.context import AppContext
from lib.ui.core.alignment import VAlign
from lib.ui.core.colors import UIColors
from lib.ui.core.components.button import Button, ButtonSkin
from lib.ui.core.components.image import Image
from lib.ui.core.constants import UIConstants
from lib.ui.core.icons import Icons
from lib.ui.core.layers import UILayer
from lib.util.events.listener import Listener
from lib.util.events.observable import Observable


class AnglePicker(Listener):
    def __init__(
        self,
        root: NodePath[PandaNode],
        ctx: AppContext,
        observable: Observable[float],
        scale: float,
        offset: float,
        centerOffset: float = 0,
        showLimits: bool = False,
    ):
        super().__init__()

        self.ctx = ctx

        self.scale = scale
        self.offset = offset
        self.showLimits = showLimits

        self.observable = observable

        self.button = Button(
            root,
            ctx,
            width=UIConstants.lightingParametersSize,
            height=UIConstants.lightingParametersSize,
            skin=ButtonSkin.ACCENT,
            bgLayer=UILayer.BACKGROUND_DECORATION,
        )

        self.sun = Image(
            root,
            image=Icons.SUN,
            x=centerOffset,
            y=centerOffset,
            width=UIConstants.lightingParametersIconSize,
            height=UIConstants.lightingParametersIconSize,
            color=UIColors.CONTENT,
            layer=UILayer.CONTENT,
        )

        self.arrowRoot = root.attachNewNode("arrow-root")
        self.arrowRoot.setX(centerOffset)
        self.arrowRoot.setZ(centerOffset)

        self.arrow = Image(
            self.arrowRoot,
            image=Icons.ARROW,
            width=UIConstants.lightingParametersIconSize,
            height=UIConstants.lightingParametersIconSize,
            x=0,
            y=UIConstants.lightingParametersIconSize / 2,
            vAlign=VAlign.BOTTOM,
            color=UIColors.CONTENT,
            layer=UILayer.CONTENT,
        )

        if showLimits:
            self.zeroLimit = root.attachNewNode("zero-limit")
            self.zeroLimit.setX(centerOffset)
            self.zeroLimit.setZ(centerOffset)

            self.zeroLimit.setR(self.offset)

            self.zeroLimitIcon = Image(
                self.zeroLimit,
                image=Icons.DASHED_LINE,
                width=UIConstants.lightingParametersIconSize,
                height=UIConstants.lightingParametersIconSize,
                x=0,
                y=UIConstants.lightingParametersIconSize / 2,
                vAlign=VAlign.BOTTOM,
                color=UIColors.CONTENT,
                layer=UILayer.CONTENT_BACKGROUND,
            )

            self.oneLimit = root.attachNewNode("one-limit")
            self.oneLimit.setX(centerOffset)
            self.oneLimit.setZ(centerOffset)

            self.oneLimit.setR(self.offset + self.scale)

            self.oneLimitIcon = Image(
                self.oneLimit,
                image=Icons.DASHED_LINE,
                width=UIConstants.lightingParametersIconSize,
                height=UIConstants.lightingParametersIconSize,
                x=0,
                y=UIConstants.lightingParametersIconSize / 2,
                vAlign=VAlign.BOTTOM,
                color=UIColors.CONTENT,
                layer=UILayer.CONTENT_BACKGROUND,
            )

        self.bind(
            observable,
            lambda value: self.arrowRoot.setR((self.scale * value) + self.offset),
        )

        self.updateTask = ctx.base.taskMgr.add(self.update, "angle-update")

    def update(self, task: Task) -> int:
        buttonState = self.button.button.guiItem.getState()  # type:ignore
        if buttonState != DGG.BUTTON_DEPRESSED_STATE:
            return task.cont

        mouseWatcher = self.ctx.base.mouseWatcherNode
        if not mouseWatcher.hasMouse():
            return task.cont

        mouseX = mouseWatcher.getMouseX()
        mouseY = mouseWatcher.getMouseY()

        aspectRatio = self.ctx.base.getAspectRatio()
        if aspectRatio >= 1:
            mouseX *= aspectRatio
        else:
            mouseY /= aspectRatio

        pivot = self.arrowRoot.getPos(self.ctx.base.aspect2dp)
        dx = mouseX - pivot.getX()
        dy = mouseY - pivot.getZ()

        angle = math.degrees(math.atan2(dy, dx))
        angle = (90 - angle) % 360

        value = (angle - self.offset) / self.scale
        value = min(1, max(value, 0))

        self.observable.setValue(value)

        return task.cont

    def destroy(self) -> None:
        super().destroy()
        self.updateTask.cancel()

        self.button.destroy()
        self.sun.destroy()
        self.arrow.destroy()

        self.arrowRoot.removeNode()

        if self.showLimits:
            self.zeroLimitIcon.destroy()
            self.zeroLimit.removeNode()

            self.oneLimitIcon.destroy()
            self.oneLimit.removeNode()
