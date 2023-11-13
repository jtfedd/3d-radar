from abc import ABC, abstractmethod

from lib.ui.core.alignment import HAlign, VAlign
from lib.ui.core.colors import UIColors
from lib.ui.core.components.background_card import BackgroundCard
from lib.ui.core.config import UIConfig
from lib.ui.core.constants import UIConstants
from lib.ui.core.layers import UILayer
from lib.ui.panels.components.panel_component_manager import PanelComponentManager
from lib.ui.panels.components.panel_header import PanelHeader
from lib.ui.panels.components.scrollable_panel import ScrollablePanel


class PanelContent(ABC):
    def __init__(self, config: UIConfig) -> None:
        self.background = BackgroundCard(
            config.anchors.left,
            width=UIConstants.panelWidth,
            height=UIConstants.infinite,
            color=UIColors.GRAY,
            vAlign=VAlign.CENTER,
            hAlign=HAlign.LEFT,
        )

        self.header = PanelHeader(config, self.headerText())

        self.footer = BackgroundCard(
            config.anchors.bottomLeft,
            y=UIConstants.headerFooterHeight,
            width=UIConstants.panelWidth,
            height=UIConstants.panelBorderWidth,
            color=UIColors.WHITE,
            vAlign=VAlign.BOTTOM,
            hAlign=HAlign.LEFT,
            layer=UILayer.BACKGROUND_DECORATION,
        )

        self.componentManager = PanelComponentManager()
        self.scroller = ScrollablePanel(config, self.componentManager)
        self.root = self.scroller.getCanvas()

    @abstractmethod
    def headerText(self) -> str:
        pass

    def destroy(self) -> None:
        self.background.destroy()
        self.header.destroy()
        self.footer.destroy()
        self.scroller.destroy()
