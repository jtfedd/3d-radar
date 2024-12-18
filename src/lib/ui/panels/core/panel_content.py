from abc import ABC, abstractmethod
from typing import List, TypeVar

from lib.app.context import AppContext
from lib.app.events import AppEvents
from lib.app.focus.focusable import Focusable
from lib.app.state import AppState
from lib.ui.core.alignment import HAlign, VAlign
from lib.ui.core.colors import UIColors
from lib.ui.core.components.background_card import BackgroundCard
from lib.ui.core.constants import UIConstants
from lib.ui.core.layers import UILayer
from lib.ui.panels.core.panel_component import PanelComponent
from lib.ui.panels.core.panel_component_manager import PanelComponentManager
from lib.ui.panels.core.panel_header import PanelHeader
from lib.ui.panels.core.panel_scroller import PanelScroller

T = TypeVar("T", bound=PanelComponent)


class PanelContent(ABC):
    def __init__(
        self,
        ctx: AppContext,
        state: AppState,
        events: AppEvents,
    ) -> None:
        self.components: List[PanelComponent] = []

        self.background = BackgroundCard(
            ctx.anchors.left,
            width=UIConstants.panelWidth,
            height=UIConstants.infinity,
            color=UIColors.BACKGROUND,
            vAlign=VAlign.CENTER,
            hAlign=HAlign.LEFT,
        )

        self.header = PanelHeader(ctx, events.ui.panels, self.headerText())

        self.footer = BackgroundCard(
            ctx.anchors.bottomLeft,
            y=UIConstants.headerFooterHeight,
            width=UIConstants.panelWidth,
            height=UIConstants.panelBorderWidth,
            color=UIColors.BACKGROUND_LIGHT,
            vAlign=VAlign.BOTTOM,
            hAlign=HAlign.LEFT,
            layer=UILayer.BACKGROUND_DECORATION,
        )

        self.componentManager = PanelComponentManager()
        self.scroller = PanelScroller(ctx, self.componentManager, state, events)
        self.root = self.scroller.getCanvas()

        self.hide()

    @abstractmethod
    def headerText(self) -> str:
        pass

    def hide(self) -> None:
        self.background.hide()
        self.header.hide()
        self.footer.hide()
        self.scroller.hide()

    def show(self) -> None:
        self.background.show()
        self.header.show()
        self.footer.show()
        self.scroller.show()

    def addComponent(self, component: T) -> T:
        self.componentManager.add(component)
        self.components.append(component)
        return component

    def setupFocusLoop(self, items: List[Focusable]) -> None:
        for i in range(0, len(items) - 1):
            items[i].nextFocusable = items[i + 1]
            items[i + 1].prevFocusable = items[i]

        items[len(items) - 1].nextFocusable = items[0]
        items[0].prevFocusable = items[len(items) - 1]

    def destroy(self) -> None:
        for component in self.components:
            component.destroy()

        self.background.destroy()
        self.header.destroy()
        self.footer.destroy()
        self.scroller.destroy()
