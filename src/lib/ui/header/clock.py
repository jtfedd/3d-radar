from direct.showbase.DirectObject import DirectObject

from lib.ui.core.colors import UIColors
from lib.ui.core.components.text import Text
from lib.ui.core.config import UIConfig


class Clock(DirectObject):
    def __init__(self, config: UIConfig):
        self.config = config

        self.text = Text(
            config.anchors.topCenter,
            "The quick brown fox jumps\nover the lazy dog",
            0,
            -config.headerHeight.value,
            UIColors.BLACK,
            font=config.font,
        )

    def destroy(self) -> None:
        self.text.destroy()
