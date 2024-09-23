from lib.ui.events import UIEvents
from lib.util.events.event_dispatcher import EventDispatcher

from .animation.events import AnimationEvents
from .input.events import InputEvents
from .window.events import WindowEvents


class AppEvents:
    def __init__(self) -> None:
        self.ui = UIEvents()
        self.input = InputEvents()
        self.window = WindowEvents()
        self.animation = AnimationEvents()

        self.requestData = EventDispatcher[None]()
        self.timeFormatChanged = EventDispatcher[None]()
        self.clearCache = EventDispatcher[None]()
        self.clearDataAndExit = EventDispatcher[None]()

    def destroy(self) -> None:
        self.ui.destroy()
        self.input.destroy()
        self.window.destroy()
        self.animation.destroy()

        self.requestData.close()
        self.timeFormatChanged.close()
        self.clearCache.close()
        self.clearDataAndExit.close()
