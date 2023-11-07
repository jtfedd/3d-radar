from lib.ui.core.alignment import HAlign, VAlign
from lib.ui.core.colors import UIColors
from lib.ui.core.components.background_card import BackgroundCard
from lib.ui.core.config import UIConfig
from lib.ui.core.constants import UIConstants


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

    def destroy(self) -> None:
        self.background.destroy()
