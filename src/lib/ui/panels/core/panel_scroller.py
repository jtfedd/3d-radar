from __future__ import annotations

import direct.gui.DirectGuiGlobals as DGG
from direct.gui.DirectScrolledFrame import DirectScrolledFrame
from direct.showbase.DirectObject import DirectObject
from direct.task.Task import Task
from panda3d.core import NodePath, PandaNode, TransparencyAttrib

from lib.ui.core.colors import UIColors
from lib.ui.core.config import UIConfig
from lib.ui.core.constants import UIConstants
from lib.ui.panels.core.panel_component_manager import PanelComponentManager


class PanelScroller(DirectObject):
    SCROLLBAR_FADE_IN = 0.1
    SCROLLBAR_FADE_OUT = 0.4

    def __init__(self, config: UIConfig, components: PanelComponentManager) -> None:
        self.config = config
        self.components = components

        self.frame = DirectScrolledFrame(
            parent=config.anchors.topLeft,
            pos=(0, 0, -UIConstants.headerFooterHeight - UIConstants.panelHeaderHeight),
            manageScrollBars=False,
            autoHideScrollBars=False,
            frameColor=UIColors.TRANSPARENT,
            scrollBarWidth=UIConstants.scrollbarWidth,
            verticalScroll_borderWidth=(0, 0),
            verticalScroll_frameColor=UIColors.BLACK,
            verticalScroll_thumb_frameColor=UIColors.WHITE,
        )

        self.frame.horizontalScroll.hide()
        self.frame.verticalScroll.incButton.hide()
        self.frame.verticalScroll.decButton.hide()
        self.frame.verticalScroll.setTransparency(TransparencyAttrib.MAlpha)

        self.scrollbarAlpha = 0.0
        self.lastScrollbarUpdate = 0.0
        self.addTask(self.updateScrollbar)

        self.updateFrame()

        self.windowSub = self.config.anchors.onUpdate.listen(
            lambda _: self.updateFrame()
        )

        self.contentSub = self.components.onUpdate.listen(self.updateFrameForCanvasSize)

        self.inBounds = False
        self.frame["state"] = DGG.NORMAL
        self.frame.bind(DGG.WITHIN, lambda w, _: self.updateInBounds(w), [True])
        self.frame.bind(DGG.WITHOUT, lambda w, _: self.updateInBounds(w), [False])

        self.accept("wheel_up-up", self.handleScroll, [-1])
        self.accept("wheel_down-up", self.handleScroll, [1])

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
        windowHeight = self.config.anchors.height
        headerFooterHeight = UIConstants.headerFooterHeight * self.config.anchors.scale
        panelHeaderHeight = UIConstants.panelHeaderHeight * self.config.anchors.scale
        panelFooterHeight = UIConstants.panelBorderWidth * self.config.anchors.scale

        absolutePanelHeight = (
            windowHeight
            - (headerFooterHeight * 2)
            - panelHeaderHeight
            - panelFooterHeight
        )

        return absolutePanelHeight / self.config.anchors.scale

    def getContentHeight(self) -> float:
        return self.components.getHeight()

    def getCanvas(self) -> NodePath[PandaNode]:
        return self.frame.getCanvas()

    def destroy(self) -> None:
        self.ignoreAll()
        self.removeAllTasks()
        self.windowSub.cancel()
        self.contentSub.cancel()
        self.frame.destroy()
