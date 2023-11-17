from lib.ui.core.config import UIConfig
from lib.ui.panels.core.panel_buttons import PanelButtons
from lib.ui.panels.panel_events import PanelEvents
from lib.ui.panels.panel_type import PanelType
from lib.ui.panels.settings.settings_panel import SettingsPanel
from lib.util.errors import InvalidArgumentException


class PanelModule:
    def __init__(self, config: UIConfig) -> None:
        self.config = config
        self.events = PanelEvents()

        self.panelType = PanelType.NONE

        self.settingsPanel = SettingsPanel(self.config)

        self.currentPanel = self.settingsPanel

        self.buttons = PanelButtons(config, self.events)
        self.buttonsSub = self.buttons.onClick.listen(self.panelTypeClicked)

    def panelTypeClicked(self, newPanelType: PanelType) -> None:
        if self.panelType == PanelType.NONE and newPanelType == PanelType.NONE:
            return

        if newPanelType in (PanelType.NONE, self.panelType):
            self.closePanel()
        else:
            self.openPanel(newPanelType)

    def closePanel(self) -> None:
        self.panelType = PanelType.NONE
        self.currentPanel.hide()

        self.events.panelChanged.send(self.panelType)

    def openPanel(self, panel: PanelType) -> None:
        self.currentPanel.hide()

        if panel is PanelType.SETTINGS:
            self.currentPanel = self.settingsPanel
        else:
            raise InvalidArgumentException("Unsupported panel type: " + str(panel))

        self.currentPanel.show()

        self.panelType = panel
        self.events.panelChanged.send(self.panelType)

    def destroy(self) -> None:
        self.events.destroy()
        self.buttons.destroy()
        self.buttonsSub.cancel()

        self.settingsPanel.destroy()
