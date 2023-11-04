from direct.showbase.DirectObject import DirectObject

from lib.ui.core.alignment import VAlign
from lib.ui.core.colors import UIColors
from lib.ui.core.components.background_card import BackgroundCard
from lib.ui.core.config import UIConfig
from lib.ui.core.constants import UIConstants
from lib.ui.header.clock import Clock


class Header(DirectObject):
    def __init__(self, config: UIConfig):
        self.config = config

        self.background = BackgroundCard(
            config.anchors.topCenter,
            width=UIConstants.infinite,
            height=UIConstants.headerFooterHeight,
            color=UIColors.GRAY,
            vAlign=VAlign.TOP,
        )

        self.clock = Clock(config)

    def destroy(self) -> None:
        self.background.destroy()
        self.clock.destroy()
