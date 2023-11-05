from lib.ui.core.alignment import HAlign, VAlign
from lib.ui.core.components.icon_toggle_button import IconToggleButton
from lib.ui.core.config import UIConfig
from lib.ui.core.constants import UIConstants
from lib.ui.panels.panel_type import PanelType
from lib.util.events.event_dispatcher import EventDispatcher


class PanelButtons:
    def __init__(self, config: UIConfig) -> None:
        self.config = config

        self.onClick = EventDispatcher[PanelType]()

        self.settingsButton = IconToggleButton(
            config.anchors.bottomLeft,
            "assets/gear.png",
            width=UIConstants.headerFooterHeight,
            height=UIConstants.headerFooterHeight,
            hAlign=HAlign.LEFT,
            vAlign=VAlign.BOTTOM,
        )

    def destroy(self) -> None:
        self.onClick.close()

        self.settingsButton.destroy()