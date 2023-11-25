from lib.app.events import AppEvents
from lib.app.state import AppState
from lib.ui.context import UIContext
from lib.ui.panels.core.panel_buttons import PanelButtons
from lib.ui.panels.core.panel_content import PanelContent
from lib.ui.panels.panel_type import PanelType
from lib.ui.panels.radar_visualization.radar_visualization_panel import (
    RadarVisualizationPanel,
)
from lib.ui.panels.settings.settings_panel import SettingsPanel
from lib.util.errors import InvalidArgumentException


class PanelModule:
    def __init__(self, ctx: UIContext, state: AppState, events: AppEvents) -> None:
        self.events = events
        self.state = state

        self.panelType = PanelType.NONE

        self.settingsPanel = SettingsPanel(ctx, state, events.ui)
        self.radarVizPanel = RadarVisualizationPanel(ctx, state, events.ui)

        self.currentPanel: PanelContent = self.settingsPanel

        self.buttons = PanelButtons(ctx, self.events.ui.panels)
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

        self.events.ui.panels.panelChanged.send(self.panelType)

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
        self.events.ui.panels.panelChanged.send(self.panelType)

    def destroy(self) -> None:
        self.events.destroy()
        self.buttons.destroy()
        self.buttonsSub.cancel()

        self.settingsPanel.destroy()
