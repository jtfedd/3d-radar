from direct.showbase.DirectObject import DirectObject

from lib.ui.core.colors import UIColors
from lib.ui.core.components.text import Text
from lib.ui.core.config import UIConfig
from lib.ui.core.constants import UIConstants


class Clock(DirectObject):
    def __init__(self, config: UIConfig):
        self.config = config

        self.text = Text(
            config.anchors.topCenter,
            "The quick brown fox jumps over the lazy dog",
            0,
            -UIConstants.headerFooterHeight,
            UIConstants.fontSizeRegular,
            UIColors.BLACK,
            config.font,
        )

    def destroy(self) -> None:
        self.text.destroy()
