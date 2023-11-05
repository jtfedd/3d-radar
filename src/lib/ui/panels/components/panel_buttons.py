from lib.ui.core.alignment import HAlign, VAlign
from lib.ui.core.components.icon_toggle_button import IconToggleButton
from lib.ui.core.config import UIConfig
from lib.ui.core.constants import UIConstants
from lib.ui.panels.panel_events import PanelEvents
from lib.ui.panels.panel_type import PanelType
from lib.util.events.event_dispatcher import EventDispatcher


class PanelButtons:
    def __init__(self, config: UIConfig, panelEvents: PanelEvents) -> None:
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

        self.radarButton = IconToggleButton(
            config.anchors.bottomLeft,
            "assets/radar.png",
            width=UIConstants.headerFooterHeight,
            height=UIConstants.headerFooterHeight,
            hAlign=HAlign.LEFT,
            vAlign=VAlign.BOTTOM,
            x=UIConstants.headerFooterHeight,
        )

        self.settingsSub = self.settingsButton.onClick.listen(
            lambda _: self.onClick.send(PanelType.SETTINGS)
        )

        self.radarSub = self.radarButton.onClick.listen(
            lambda _: self.onClick.send(PanelType.DATA)
        )

        self.panelTypeSub = panelEvents.panelChanged.listen(self.updateToggleButtons)

    def updateToggleButtons(self, panelType: PanelType) -> None:
        self.radarButton.setToggleState(panelType == PanelType.DATA)
        self.settingsButton.setToggleState(panelType == PanelType.SETTINGS)

    def destroy(self) -> None:
        self.onClick.close()
        self.panelTypeSub.cancel()

        self.settingsButton.destroy()
        self.radarButton.destroy()

        self.settingsSub.cancel()
        self.radarSub.cancel()
