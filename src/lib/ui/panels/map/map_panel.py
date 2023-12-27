from lib.app.events import AppEvents
from lib.app.state import AppState
from lib.ui.context import UIContext
from lib.ui.core.constants import UIConstants
from lib.ui.panels.components.spacer import SpacerComponent
from lib.ui.panels.components.text_input import PanelTextInput
from lib.ui.panels.components.title import TitleComponent
from lib.ui.panels.core.panel_content import PanelContent
from lib.util.events.listener import Listener
from lib.util.events.observable import Observable


class MapPanel(PanelContent):
    def __init__(self, ctx: UIContext, state: AppState, events: AppEvents) -> None:
        super().__init__(ctx, state, events)

        self.listener = Listener()

        self.addComponent(TitleComponent(self.root, ctx, "Layers"))

    def headerText(self) -> str:
        return "Map"

    def destroy(self) -> None:
        super().destroy()

        self.listener.destroy()
