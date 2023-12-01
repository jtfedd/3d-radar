from lib.ui.panels.panel_type import PanelType
from lib.util.events.event_dispatcher import EventDispatcher


class PanelEvents:
    def __init__(self) -> None:
        self.panelChanged = EventDispatcher[PanelType]()

    def destroy(self) -> None:
        self.panelChanged.close()
