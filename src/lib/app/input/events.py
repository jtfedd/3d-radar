from lib.util.events.event_dispatcher import EventDispatcher


class InputEvents:
    def __init__(self) -> None:
        self.onHide = EventDispatcher[None]()
        self.onPlay = EventDispatcher[None]()
        self.nextFrame = EventDispatcher[None]()
        self.prevFrame = EventDispatcher[None]()
        self.scroll = EventDispatcher[int]()
        self.zoom = EventDispatcher[int]()
        self.leftMouse = EventDispatcher[bool]()
        self.rightMouse = EventDispatcher[bool]()
        self.tab = EventDispatcher[bool]()
        self.shiftTab = EventDispatcher[bool]()

    def destroy(self) -> None:
        self.onHide.close()
        self.onPlay.close()
        self.scroll.close()
        self.zoom.close()
        self.leftMouse.close()
        self.rightMouse.close()
        self.tab.close()
        self.shiftTab.close()
