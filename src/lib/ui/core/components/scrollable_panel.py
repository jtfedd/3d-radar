from __future__ import annotations

import direct.gui.DirectGuiGlobals as DGG
from direct.gui.DirectScrolledFrame import DirectScrolledFrame
from direct.task.Task import Task
from panda3d.core import NodePath, PandaNode, TransparencyAttrib

from lib.app.context import AppContext
from lib.app.events import AppEvents
from lib.ui.core.alignment import HAlign, VAlign
from lib.ui.core.colors import UIColors
from lib.ui.core.constants import UIConstants
from lib.ui.core.layers import UILayer
from lib.util.errors import InvalidArgumentException


class ScrollablePanel:
    SCROLLBAR_FADE_IN = 0.1
    SCROLLBAR_FADE_OUT = 0.4

    def __init__(
        self,
        root: NodePath[PandaNode],
        ctx: AppContext,
        events: AppEvents,
        x: float = 0,
        y: float = 0,
        width: float = 1,
        height: float = 1,
        canvasHeight: float = 1,
        hAlign: HAlign = HAlign.CENTER,
        vAlign: VAlign = VAlign.CENTER,
        layer: UILayer = UILayer.CONTENT_INTERACTION,
        scrollbarPadding: float = 0,
    ) -> None:
        self.ctx = ctx
        self.events = events

        self.width = width
        self.scrollbarPadding = scrollbarPadding

        xPos = self.correctXForAlignment(x, width, hAlign)
        yPos = self.correctYForAlignment(y, height, vAlign)

        self.frame = DirectScrolledFrame(
            parent=root,
            pos=(xPos, 0, yPos),
            manageScrollBars=False,
            autoHideScrollBars=False,
            frameColor=UIColors.TRANSPARENT,
            scrollBarWidth=UIConstants.scrollbarWidth,
            verticalScroll_borderWidth=(0, 0),
            verticalScroll_frameColor=UIColors.INSET,
            verticalScroll_thumb_frameColor=UIColors.CONTENT,
        )

        self.frame.setBin("fixed", layer.value)

        self.frame.horizontalScroll.hide()
        self.frame.verticalScroll.incButton.hide()
        self.frame.verticalScroll.decButton.hide()
        self.frame.verticalScroll.setTransparency(TransparencyAttrib.MAlpha)

        self.scrollbarAlpha = 0.0
        self.lastScrollbarUpdate = 0.0
        self.updateTask = self.ctx.base.addTask(self.updateScrollbar)

        self.updateFrame(height, canvasHeight)

        self.inBounds = False
        self.frame["state"] = DGG.NORMAL
        self.frame.bind(DGG.WITHIN, lambda w, _: self.updateInBounds(w), [True])
        self.frame.bind(DGG.WITHOUT, lambda w, _: self.updateInBounds(w), [False])

        self.scrollSub = self.events.input.scroll.listen(self.handleScroll)

    def correctXForAlignment(self, x: float, width: float, align: HAlign) -> float:
        if align == HAlign.LEFT:
            return x

        if align == HAlign.CENTER:
            return x - (width / 2)

        if align == HAlign.RIGHT:
            return x - width

        raise InvalidArgumentException("align has invalid value " + align.value)

    def correctYForAlignment(self, y: float, height: float, align: VAlign) -> float:
        if align == VAlign.TOP:
            return y

        if align == VAlign.CENTER:
            return y + (height / 2)

        if align in (VAlign.BOTTOM, VAlign.BASELINE):
            return y + height

        raise InvalidArgumentException("align has invalid value " + align.value)

    def hide(self) -> None:
        self.frame.hide()

    def show(self) -> None:
        self.frame.show()

    def updateInBounds(self, inBounds: bool) -> None:
        self.inBounds = inBounds

    def updateScrollbar(self, task: Task) -> int:
        dt = task.time - self.lastScrollbarUpdate
        self.lastScrollbarUpdate = task.time

        if self.inBounds:
            self.scrollbarAlpha += dt / self.SCROLLBAR_FADE_IN
            self.scrollbarAlpha = min(1.0, self.scrollbarAlpha)
        else:
            self.scrollbarAlpha -= dt / self.SCROLLBAR_FADE_OUT
            self.scrollbarAlpha = max(0.0, self.scrollbarAlpha)

        self.frame.verticalScroll.setAlphaScale(self.scrollbarAlpha)

        return task.cont

    def handleScroll(self, direction: int) -> None:
        if not self.inBounds or self.frame.verticalScroll.isHidden():
            return

        self.frame.verticalScroll.scrollStep(direction)

    def updateFrame(self, frameHeight: float, canvasHeight: float) -> None:
        canvasHeight = max(canvasHeight, frameHeight)

        self.frame["frameSize"] = (0, self.width, -frameHeight, 0)
        self.frame["canvasSize"] = (0, self.width, -canvasHeight, 0)
        self.frame.verticalScroll["range"] = (0, 1)
        self.frame.verticalScroll["pageSize"] = frameHeight / canvasHeight

        if canvasHeight <= frameHeight:
            self.frame.verticalScroll.hide()
            return

        self.frame.verticalScroll.show()
        self.frame.verticalScroll.setPos(
            self.width - self.scrollbarPadding, 0, -frameHeight / 2
        )
        self.frame.verticalScroll.setScale(
            1, 1, (frameHeight / 2) - self.scrollbarPadding
        )

        scrollSteps = (canvasHeight - frameHeight) * UIConstants.scrollSensitivity
        scrollSize = 1 / scrollSteps
        self.frame.verticalScroll["scrollSize"] = scrollSize

    def getCanvas(self) -> NodePath[PandaNode]:
        return self.frame.getCanvas()

    def destroy(self) -> None:
        self.updateTask.cancel()
        self.scrollSub.cancel()

        self.frame.destroy()
