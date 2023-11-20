from typing import Callable, List, Tuple

from lib.ui.core.alignment import HAlign, VAlign
from lib.ui.core.components.icon_toggle_button import IconToggleButton
from lib.ui.core.config import UIConfig
from lib.ui.core.constants import UIConstants
from lib.ui.core.icons import Icons
from lib.ui.panels.panel_events import PanelEvents
from lib.ui.panels.panel_type import PanelType
from lib.util.events.event_dispatcher import EventDispatcher
from lib.util.events.event_subscription import EventSubscription


class PanelButtons:
    buttonConfig: List[Tuple[PanelType, str]] = [
        (PanelType.SETTINGS, Icons.GEAR),
        (PanelType.DATA, Icons.RADAR),
    ]

    def __init__(self, config: UIConfig, panelEvents: PanelEvents) -> None:
        self.config = config

        self.onClick = EventDispatcher[PanelType]()

        self.buttons: List[IconToggleButton] = []
        self.subs: List[EventSubscription[None]] = []

        for i, settings in enumerate(self.buttonConfig):
            panelType = settings[0]
            icon = settings[1]

            button = IconToggleButton(
                config.anchors.bottomLeft,
                icon,
                x=i * (UIConstants.panelWidth / len(self.buttonConfig)),
                width=UIConstants.panelWidth / len(self.buttonConfig),
                height=UIConstants.headerFooterHeight,
                iconWidth=UIConstants.headerFooterHeight,
                iconHeight=UIConstants.headerFooterHeight,
                hAlign=HAlign.LEFT,
                vAlign=VAlign.BOTTOM,
            )

            sub = button.onClick.listen(self.handleClick(panelType))

            self.buttons.append(button)
            self.subs.append(sub)

        self.panelTypeSub = panelEvents.panelChanged.listen(self.updateToggleButtons)

    def handleClick(self, panelType: PanelType) -> Callable[[None], None]:
        return lambda _: self.onClick.send(panelType)

    def updateToggleButtons(self, panelType: PanelType) -> None:
        for i, button in enumerate(self.buttons):
            button.setToggleState(panelType == self.buttonConfig[i][0])

    def destroy(self) -> None:
        self.onClick.close()
        self.panelTypeSub.cancel()

        for button in self.buttons:
            button.destroy()

        for sub in self.subs:
            sub.cancel()