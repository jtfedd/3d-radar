from __future__ import annotations

import direct.gui.DirectGuiGlobals as DGG
from direct.gui.DirectScrolledFrame import DirectScrolledFrame
from direct.task.Task import Task
from panda3d.core import NodePath, PandaNode, TransparencyAttrib

from lib.app.events import AppEvents
from lib.app.state import AppState
from lib.ui.context import UIContext
from lib.ui.core.colors import UIColors
from lib.ui.core.constants import UIConstants
from lib.ui.core.layers import UILayer
from lib.ui.panels.core.panel_component_manager import PanelComponentManager


class PanelScroller:
    SCROLLBAR_FADE_IN = 0.1
    SCROLLBAR_FADE_OUT = 0.4

    def __init__(
        self,
        ctx: UIContext,
        components: PanelComponentManager,
        state: AppState,
        events: AppEvents,
    ) -> None:
        self.ctx = ctx
        self.components = components
        self.state = state
        self.events = events

        self.frame = DirectScrolledFrame(
            parent=ctx.anchors.topLeft,
            pos=(0, 0, -UIConstants.headerFooterHeight - UIConstants.panelHeaderHeight),
            manageScrollBars=False,
            autoHideScrollBars=False,
            frameColor=UIColors.TRANSPARENT,
            scrollBarWidth=UIConstants.scrollbarWidth,
            verticalScroll_borderWidth=(0, 0),
            verticalScroll_frameColor=UIColors.INSET,
            verticalScroll_thumb_frameColor=UIColors.CONTENT,
        )

        self.frame.setBin("fixed", UILayer.INTERACTION.value)

        self.frame.horizontalScroll.hide()
        self.frame.verticalScroll.incButton.hide()
        self.frame.verticalScroll.decButton.hide()
        self.frame.verticalScroll.setTransparency(TransparencyAttrib.MAlpha)

        self.scrollbarAlpha = 0.0
        self.lastScrollbarUpdate = 0.0
        self.updateTask = self.ctx.appContext.base.addTask(self.updateScrollbar)

        self.updateFrame()

        self.windowSub = self.events.ui.onAnchorUpdate.listen(
            lambda _: self.updateFrame()
        )
        self.contentSub = self.components.onUpdate.listen(self.updateFrameForCanvasSize)

        self.inBounds = False
        self.frame["state"] = DGG.NORMAL
        self.frame.bind(DGG.WITHIN, lambda w, _: self.updateInBounds(w), [True])
        self.frame.bind(DGG.WITHOUT, lambda w, _: self.updateInBounds(w), [False])

        self.scrollSub = self.events.input.scroll.listen(self.handleScroll)

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

    def updateFrame(self) -> None:
        self.updateFrameForCanvasSize(self.getContentHeight())

    def updateFrameForCanvasSize(self, canvasHeight: float) -> None:
        frameHeight = self.getPanelHeight()
        canvasHeight = max(canvasHeight, frameHeight)

        self.frame["frameSize"] = (0, UIConstants.panelWidth, -frameHeight, 0)
        self.frame["canvasSize"] = (0, UIConstants.panelWidth, -canvasHeight, 0)
        self.frame.verticalScroll["range"] = (0, 1)
        self.frame.verticalScroll["pageSize"] = frameHeight / canvasHeight

        if canvasHeight <= frameHeight:
            self.frame.verticalScroll.hide()
            return

        self.frame.verticalScroll.show()
        self.frame.verticalScroll.setPos(
            UIConstants.panelWidth - UIConstants.scrollbarPadding, 0, -frameHeight / 2
        )
        self.frame.verticalScroll.setScale(
            1, 1, (frameHeight / 2) - UIConstants.scrollbarPadding
        )

        scrollSteps = (canvasHeight - frameHeight) * UIConstants.scrollSensitivity
        scrollSize = 1 / scrollSteps
        self.frame.verticalScroll["scrollSize"] = scrollSize

    def getPanelHeight(self) -> float:
        windowHeight = self.ctx.anchors.height
        scale = self.state.uiScale.value
        headerFooterHeight = UIConstants.headerFooterHeight * scale
        panelHeaderHeight = UIConstants.panelHeaderHeight * scale
        panelFooterHeight = UIConstants.panelBorderWidth * scale

        absolutePanelHeight = (
            windowHeight
            - (headerFooterHeight * 2)
            - panelHeaderHeight
            - panelFooterHeight
        )

        return absolutePanelHeight / scale

    def getContentHeight(self) -> float:
        return self.components.getHeight()

    def getCanvas(self) -> NodePath[PandaNode]:
        return self.frame.getCanvas()

    def destroy(self) -> None:
        self.updateTask.cancel()
        self.scrollSub.cancel()
        self.windowSub.cancel()
        self.contentSub.cancel()
        self.frame.destroy()
