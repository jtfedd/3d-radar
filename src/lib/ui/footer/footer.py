from direct.showbase.DirectObject import DirectObject

from lib.ui.core.alignment import VAlign
from lib.ui.core.colors import UIColors
from lib.ui.core.components.background_card import BackgroundCard
from lib.ui.core.config import UIConfig
from lib.ui.core.constants import UIConstants


class Footer(DirectObject):
    def __init__(self, config: UIConfig):
        self.config = config

        self.background = BackgroundCard(
            config.anchors.bottom,
            width=UIConstants.infinity,
            height=UIConstants.headerFooterHeight,
            color=UIColors.GRAY,
            vAlign=VAlign.BOTTOM,
        )

    def destroy(self) -> None:
        self.background.destroy()
