from direct.showbase.DirectObject import DirectObject

from lib.ui.core.colors import UIColors
from lib.ui.core.components.background_card import BackgroundCard
from lib.ui.core.config import UIConfig
from lib.util.events.event_collection import EventCollection


class Footer(DirectObject):
    def __init__(self, config: UIConfig):
        self.events = EventCollection()

        self.config = config

        self.background = BackgroundCard(
            config.anchors.bottomLeft,
            0,
            config.footerHeight.value,
            config.footerWidth.value,
            config.footerHeight.value,
            UIColors.BLACK,
        )

        self.events.add(self.config.footerWidth, self.update)
        self.events.add(self.config.footerHeight, self.update)

    def update(self) -> None:
        self.background.update(
            0,
            self.config.footerHeight.value,
            self.config.footerWidth.value,
            self.config.footerHeight.value,
        )

    def destroy(self) -> None:
        self.events.destroy()

        self.background.destroy()
