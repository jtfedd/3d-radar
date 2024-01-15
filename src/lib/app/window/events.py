from panda3d.core import GraphicsWindow

from lib.util.events.event_dispatcher import EventDispatcher


class WindowEvents:
    def __init__(self) -> None:
        self.onWindowUpdate = EventDispatcher[GraphicsWindow]()

    def destroy(self) -> None:
        self.onWindowUpdate.close()
