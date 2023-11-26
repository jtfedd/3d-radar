from lib.app.events import AppEvents
from lib.app.state import AppState
from lib.ui.context import UIContext
from lib.ui.panels.components.spacer import SpacerComponent
from lib.ui.panels.core.panel_content import PanelContent


class RadarDataPanel(PanelContent):
    def __init__(self, ctx: UIContext, state: AppState, events: AppEvents) -> None:
        super().__init__(ctx, state, events)

        self.addComponent(SpacerComponent(self.root))

    def headerText(self) -> str:
        return "Radar Data"
