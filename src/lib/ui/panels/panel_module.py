from lib.app.state import AppState
from lib.ui.core.context import UIContext
from lib.ui.events import UIEvents
from lib.ui.panels.core.panel_buttons import PanelButtons
from lib.ui.panels.core.panel_content import PanelContent
from lib.ui.panels.panel_type import PanelType
from lib.ui.panels.radar_visualization.radar_visualization_panel import (
    RadarVisualizationPanel,
)
from lib.ui.panels.settings.settings_panel import SettingsPanel
from lib.util.errors import InvalidArgumentException


class PanelModule:
    def __init__(self, ctx: UIContext, state: AppState, events: UIEvents) -> None:
        self.events = events
        self.state = state

        self.panelType = PanelType.NONE

        self.settingsPanel = SettingsPanel(ctx, state, events)
        self.radarVizPanel = RadarVisualizationPanel(ctx, state, events)

        self.currentPanel: PanelContent = self.settingsPanel

        self.buttons = PanelButtons(ctx, self.events.panels)
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

        self.events.panels.panelChanged.send(self.panelType)

    def openPanel(self, panel: PanelType) -> None:
        self.currentPanel.hide()

        if panel is PanelType.SETTINGS:
            self.currentPanel = self.settingsPanel
        elif panel is PanelType.RADAR_VISUALIZATION:
            self.currentPanel = self.radarVizPanel
        else:
            raise InvalidArgumentException("Unsupported panel type: " + str(panel))

        self.currentPanel.show()

        self.panelType = panel
        self.events.panels.panelChanged.send(self.panelType)

    def destroy(self) -> None:
        self.events.destroy()
        self.buttons.destroy()
        self.buttonsSub.cancel()

        self.settingsPanel.destroy()
