from direct.showbase.DirectObject import DirectObject

from lib.ui.core.colors import UIColors
from lib.ui.core.components.background_card import BackgroundCard
from lib.ui.core.config import UIConfig


class Footer(DirectObject):
    def __init__(self, config: UIConfig):
        self.config = config

        self.background = BackgroundCard(
            config.anchors.bottomLeft,
            0,
            config.footerHeight.value,
            config.footerWidth.value,
            config.footerHeight.value,
            UIColors.BLACK,
        )

    def destroy(self) -> None:
        self.background.destroy()
