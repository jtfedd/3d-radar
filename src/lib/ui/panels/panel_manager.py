from lib.ui.core.config import UIConfig
from lib.ui.panels.components.panel_background import PanelBackground
from lib.ui.panels.components.panel_buttons import PanelButtons
from lib.ui.panels.panel_events import PanelEvents
from lib.ui.panels.panel_type import PanelType
from lib.util.optional import unwrap


class PanelManager:
    def __init__(self, config: UIConfig) -> None:
        self.config = config

        self.panelType = PanelType.NONE
        self.panelBackground: PanelBackground | None = None

        self.buttons = PanelButtons(config)
        self.buttonsSub = self.buttons.onClick.listen(self.panelTypeClicked)

        self.events = PanelEvents()

    def panelTypeClicked(self, newPanelType: PanelType) -> None:
        if self.panelType == PanelType.NONE and newPanelType == PanelType.NONE:
            return

        if newPanelType in (PanelType.NONE, self.panelType):
            self.closePanel()
        else:
            self.openPanel(newPanelType)

    def closePanel(self) -> None:
        self.panelType = PanelType.NONE
        self.events.panelChanged.send(self.panelType)

        if self.panelBackground is not None:
            unwrap(self.panelBackground).destroy()
            self.panelBackground = None

    def openPanel(self, panel: PanelType) -> None:
        self.panelType = panel
        self.events.panelChanged.send(self.panelType)

        if self.panelBackground is None:
            self.panelBackground = PanelBackground(self.config)

    def destroy(self) -> None:
        self.events.destroy()
        self.buttons.destroy()
        self.buttonsSub.cancel()

        if self.panelBackground is not None:
            unwrap(self.panelBackground).destroy()
            self.panelBackground = None
