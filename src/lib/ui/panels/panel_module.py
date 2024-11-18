from lib.app.context import AppContext
from lib.app.events import AppEvents
from lib.app.state import AppState
from lib.ui.panels.core.panel_buttons import PanelButtons
from lib.ui.panels.core.panel_content import PanelContent
from lib.ui.panels.info.info_panel import InfoPanel
from lib.ui.panels.map.map_panel import MapPanel
from lib.ui.panels.panel_type import PanelType
from lib.ui.panels.radar_data.radar_data_panel import RadarDataPanel
from lib.ui.panels.radar_viewer.radar_viewer_panel import RadarViewerPanel
from lib.ui.panels.settings.settings_panel import SettingsPanel
from lib.util.errors import InvalidArgumentException


class PanelModule:
    def __init__(self, ctx: AppContext, state: AppState, events: AppEvents) -> None:
        self.events = events
        self.state = state

        self.panelType = PanelType.NONE

        self.settingsPanel = SettingsPanel(ctx, state, events)
        self.radarDataPanel = RadarDataPanel(ctx, state, events)
        self.radarVizPanel = RadarViewerPanel(ctx, state, events)
        self.mapPanel = MapPanel(ctx, state, events)
        self.infoPanel = InfoPanel(ctx, state, events)

        self.currentPanel: PanelContent = self.settingsPanel

        self.buttons = PanelButtons(ctx, self.events.ui.panels)
        self.buttonsSub = events.ui.panels.panelChanged.listen(self.panelTypeChanged)

    def panelTypeChanged(self, newPanelType: PanelType) -> None:
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
        elif panel is PanelType.RADAR_DATA:
            self.currentPanel = self.radarDataPanel
        elif panel is PanelType.RADAR_VIEWER:
            self.currentPanel = self.radarVizPanel
        elif panel is PanelType.MAP:
            self.currentPanel = self.mapPanel
        elif panel is PanelType.ABOUT:
            self.currentPanel = self.infoPanel
        else:
            raise InvalidArgumentException("Unsupported panel type: " + str(panel))

        self.currentPanel.show()

        self.panelType = panel

    def destroy(self) -> None:
        self.buttons.destroy()
        self.buttonsSub.cancel()

        self.settingsPanel.destroy()
