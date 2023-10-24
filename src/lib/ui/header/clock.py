from direct.showbase.DirectObject import DirectObject

from lib.ui.core.colors import UIColors
from lib.ui.core.components.text import Text
from lib.ui.core.config import UIConfig


class Clock(DirectObject):
    def __init__(self, config: UIConfig):
        self.config = config

        self.text = Text(
            config.anchors.topCenter,
            "Hello, World!",
            0,
            -config.headerHeight.value / 2,
            config.fontSize.value,
            UIColors.WHTIE,
        )

    def destroy(self) -> None:
        self.text.destroy()
