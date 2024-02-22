from typing import Callable, List, Tuple

from lib.ui.context import UIContext
from lib.ui.core.alignment import HAlign, VAlign
from lib.ui.core.components.button import Button
from lib.ui.core.constants import UIConstants
from lib.ui.core.icons import Icons
from lib.ui.panels.events import PanelEvents
from lib.ui.panels.panel_type import PanelType
from lib.util.events.listener import Listener


class PanelButtons(Listener):
    buttonConfig: List[Tuple[PanelType, str]] = [
        (PanelType.SETTINGS, Icons.GEAR),
        (PanelType.RADAR_DATA, Icons.RADAR),
        (PanelType.RADAR_VIEWER, Icons.RADAR_DISPLAY),
        (PanelType.MAP, Icons.MAP),
        (PanelType.ABOUT, Icons.INFO),
    ]

    def __init__(self, ctx: UIContext, events: PanelEvents) -> None:
        super().__init__()
        self.events = events

        self.buttons: List[Button] = []

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

            self.buttons.append(button)
            self.listen(button.onClick, self.handleClick(panelType))

        self.listen(events.panelChanged, self.updateToggleButtons)

    def handleClick(self, panelType: PanelType) -> Callable[[None], None]:
        return lambda _: self.events.panelChanged.send(panelType)

    def updateToggleButtons(self, panelType: PanelType) -> None:
        for i, button in enumerate(self.buttons):
            button.setToggleState(panelType == self.buttonConfig[i][0])

    def destroy(self) -> None:
        super().destroy()

        for button in self.buttons:
            button.destroy()
