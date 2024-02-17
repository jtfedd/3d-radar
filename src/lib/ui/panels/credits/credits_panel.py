from lib.app.events import AppEvents
from lib.app.state import AppState
from lib.ui.context import UIContext
from lib.ui.panels.components.title import TitleComponent
from lib.ui.panels.core.panel_content import PanelContent


class CreditsPanel(PanelContent):
    def __init__(self, ctx: UIContext, state: AppState, events: AppEvents) -> None:
        super().__init__(ctx, state, events)

        self.addComponent(TitleComponent(self.root, ctx, "Weather Data"))
        self.addComponent(TitleComponent(self.root, ctx, "Map Data"))
        self.addComponent(TitleComponent(self.root, ctx, "UI Resources"))

    def headerText(self) -> str:
        return "Credits"
