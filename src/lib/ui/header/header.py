from direct.showbase.DirectObject import DirectObject

from lib.ui.core.colors import UIColors
from lib.ui.core.components.background_card import BackgroundCard
from lib.ui.core.config import UIConfig


class Header(DirectObject):
    def __init__(self, config: UIConfig):
        self.config = config

        self.background = BackgroundCard(
            config.anchors.topLeft,
            0,
            0,
            config.headerWidth.value,
            config.headerHeight.value,
            UIColors.BLACK,
        )

    def destroy(self) -> None:
        self.background.destroy()
