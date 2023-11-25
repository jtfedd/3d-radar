from direct.showbase.DirectObject import DirectObject

from lib.app.focus.manager import FocusManager
from lib.app.state import AppState
from lib.util.events.event_dispatcher import EventDispatcher

from .events import InputEvents


class InputManager(DirectObject):
    def __init__(
        self,
        focusManager: FocusManager,
        state: AppState,
        events: InputEvents,
    ):
        self.focusManager = focusManager
        self.events = events

        self.createBindings()

    def createBindings(self) -> None:
        self.ignoreAll()
        self.accept("h", lambda: self.send(self.events.onHide))

    def send(self, event: EventDispatcher[None]) -> None:
        if self.focusManager.focused():
            return

        event.send(None)

    def destroy(self) -> None:
        self.ignoreAll()
