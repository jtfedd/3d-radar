from lib.app.input.events import InputEvents
from lib.app.window.events import WindowEvents
from lib.ui.events import UIEvents
from lib.util.events.event_dispatcher import EventDispatcher


class AppEvents:
    def __init__(self) -> None:
        self.ui = UIEvents()
        self.input = InputEvents()
        self.window = WindowEvents()

        self.requestData = EventDispatcher[None]()

    def destroy(self) -> None:
        self.ui.destroy()
        self.input.destroy()
        self.window.destroy()

        self.requestData.close()
