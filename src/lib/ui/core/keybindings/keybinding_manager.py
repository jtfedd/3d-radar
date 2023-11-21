from direct.showbase.DirectObject import DirectObject

from lib.ui.core.focus.focus_manager import FocusManager
from lib.util.events.event_dispatcher import EventDispatcher


class KeybindingManager(DirectObject):
    def __init__(self, focusManager: FocusManager):
        self.focusManager = focusManager

        self.hideEvent = EventDispatcher[None]()

        self.createBindings()

    def createBindings(self) -> None:
        self.accept("h", lambda: self.send(self.hideEvent))

    def send(self, event: EventDispatcher[None]) -> None:
        if self.focusManager.focused():
            return

        event.send(None)

    def destroy(self) -> None:
        self.ignoreAll()
        self.hideEvent.close()
