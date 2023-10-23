from direct.showbase.DirectObject import DirectObject

from lib.ui.core.colors import UIColors
from lib.ui.core.components.background_card import BackgroundCard
from lib.ui.core.config import UIConfig
from lib.util.events.event_collection import EventCollection


class Header(DirectObject):
    def __init__(self, config: UIConfig):
        self.events = EventCollection()

        self.config = config

        self.background = BackgroundCard(
            config.anchors.topLeft,
            0,
            0,
            config.headerWidth.value,
            config.headerHeight.value,
            UIColors.BLACK,
        )

        self.events.add(self.config.headerWidth, self.update)
        self.events.add(self.config.headerHeight, self.update)

    def update(self) -> None:
        self.background.update(
            0,
            0,
            self.config.headerWidth.value,
            self.config.headerHeight.value,
        )

    def destroy(self) -> None:
        self.events.destroy()

        self.background.destroy()
