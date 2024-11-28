from lib.model.context_menu_payload import ContextMenuPayload
from lib.util.events.event_dispatcher import EventDispatcher

from .modals.events import ModalEvents
from .panels.events import PanelEvents


class UIEvents:
    def __init__(self) -> None:
        self.panels = PanelEvents()
        self.modals = ModalEvents()

        self.onAnchorUpdate = EventDispatcher[None]()
        self.requestContextMenu = EventDispatcher[ContextMenuPayload]()
        self.closeContextMenu = EventDispatcher[None]()

    def destroy(self) -> None:
        self.panels.destroy()
        self.modals.destroy()

        self.onAnchorUpdate.close()
        self.requestContextMenu.close()
        self.closeContextMenu.close()
