from __future__ import annotations

from panda3d.core import NodePath, PandaNode

from lib.app.events import AppEvents
from lib.app.state import AppState
from lib.ui.context import UIContext
from lib.ui.core.alignment import HAlign, VAlign
from lib.ui.core.components.scrollable_panel import ScrollablePanel
from lib.ui.core.constants import UIConstants
from lib.ui.panels.core.panel_component_manager import PanelComponentManager


class PanelScroller:
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

        self.frame = ScrollablePanel(
            root=ctx.anchors.topLeft,
            ctx=ctx,
            events=events,
            y=-UIConstants.headerFooterHeight - UIConstants.panelHeaderHeight,
            width=UIConstants.panelWidth,
            hAlign=HAlign.LEFT,
            vAlign=VAlign.TOP,
            scrollbarPadding=UIConstants.panelScrollbarPadding,
        )

        self.updateFrame()

        self.windowSub = events.ui.onAnchorUpdate.listen(lambda _: self.updateFrame())
        self.contentSub = self.components.onUpdate.listen(self.updateFrameForCanvasSize)

    def hide(self) -> None:
        self.frame.hide()

    def show(self) -> None:
        self.frame.show()

    def updateFrame(self) -> None:
        self.updateFrameForCanvasSize(self.getContentHeight())

    def updateFrameForCanvasSize(self, canvasHeight: float) -> None:
        frameHeight = self.getPanelHeight()
        self.frame.updateFrame(frameHeight, canvasHeight)

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
        self.windowSub.cancel()
        self.contentSub.cancel()

        self.frame.destroy()
