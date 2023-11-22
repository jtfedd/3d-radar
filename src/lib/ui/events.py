from lib.util.events.event_dispatcher import EventDispatcher

from .panels.panel_events import PanelEvents


class UIEvents:
    def __init__(self) -> None:
        self.panels = PanelEvents()

        self.onAnchorUpdate = EventDispatcher[None]()

    def destroy(self) -> None:
        self.panels.destroy()

        self.onAnchorUpdate.close()
