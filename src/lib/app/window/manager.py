from direct.showbase.DirectObject import DirectObject
from direct.showbase.ShowBase import ShowBase

from .events import WindowEvents
from .resolution_provider import ResolutionProvider


class WindowManager(DirectObject):
    def __init__(self, base: ShowBase, events: WindowEvents):
        self.accept("window-event", events.onWindowUpdate.send)

        self.resolutionProvider = ResolutionProvider(base, events)

    def destroy(self) -> None:
        self.ignoreAll()
