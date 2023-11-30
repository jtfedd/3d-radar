from typing import Callable, List, Tuple

from lib.ui.context import UIContext
from lib.ui.core.alignment import HAlign, VAlign
from lib.ui.core.components.button import Button
from lib.ui.core.constants import UIConstants
from lib.ui.core.icons import Icons
from lib.ui.panels.panel_events import PanelEvents
from lib.ui.panels.panel_type import PanelType
from lib.util.events.event_dispatcher import EventDispatcher
from lib.util.events.event_subscription import EventSubscription


class PanelButtons:
    buttonConfig: List[Tuple[PanelType, str]] = [
        (PanelType.SETTINGS, Icons.GEAR),
        (PanelType.RADAR_DATA, Icons.RADAR),
        (PanelType.RADAR_VISUALIZATION, Icons.RADAR_DISPLAY),
    ]

    def __init__(self, ctx: UIContext, panelEvents: PanelEvents) -> None:
        self.onClick = EventDispatcher[PanelType]()

        self.buttons: List[Button] = []
        self.subs: List[EventSubscription[None]] = []

        for i, settings in enumerate(self.buttonConfig):
            panelType = settings[0]
            icon = settings[1]

            button = Button(
                ctx.anchors.topLeft,
                ctx,
                x=i * (UIConstants.panelWidth / len(self.buttonConfig)),
                width=UIConstants.panelWidth / len(self.buttonConfig),
                height=UIConstants.headerFooterHeight,
                iconWidth=UIConstants.headerFooterHeight,
                iconHeight=UIConstants.headerFooterHeight,
                hAlign=HAlign.LEFT,
                vAlign=VAlign.TOP,
                icon=icon,
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
