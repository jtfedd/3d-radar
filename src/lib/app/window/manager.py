from direct.showbase.DirectObject import DirectObject

from .events import WindowEvents


class WindowManager(DirectObject):
    def __init__(self, events: WindowEvents):
        self.accept("window-event", events.onWindowUpdate.send)

    def destroy(self) -> None:
        self.ignoreAll()
