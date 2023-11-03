from direct.showbase.DirectObject import DirectObject

from lib.ui.core.alignment import HAlign, VAlign
from lib.ui.core.components.text import Text
from lib.ui.core.config import UIConfig
from lib.ui.core.constants import UIConstants


class Clock(DirectObject):
    def __init__(self, config: UIConfig):
        self.config = config

        self.text = Text(
            config.anchors.topCenter,
            config.fonts.bold,
            "The quick brown fox jumps over the lazy dog",
            y=-UIConstants.headerFooterHeight / 2,
            hAlign=HAlign.CENTER,
            vAlign=VAlign.CENTER,
        )

    def destroy(self) -> None:
        self.text.destroy()
