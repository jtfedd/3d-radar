from lib.ui.core.alignment import HAlign, VAlign
from lib.ui.core.colors import UIColors
from lib.ui.core.components.background_card import BackgroundCard
from lib.ui.core.config import UIConfig
from lib.ui.core.constants import UIConstants
from lib.ui.core.layers import UILayer
from lib.ui.panels.components.panel_header import PanelHeader
from lib.ui.panels.components.scrollable_panel import ScrollablePanel


class PanelBackground:
    def __init__(self, config: UIConfig) -> None:
        self.config = config

        self.background = BackgroundCard(
            config.anchors.left,
            width=UIConstants.panelWidth,
            height=UIConstants.infinite,
            color=UIColors.GRAY,
            vAlign=VAlign.CENTER,
            hAlign=HAlign.LEFT,
        )

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

        self.header = PanelHeader(config, "Hello, World")

        self.scroller = ScrollablePanel(config)

    def destroy(self) -> None:
        self.scroller.destroy()
        self.background.destroy()
        self.footer.destroy()
