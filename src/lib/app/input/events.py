from lib.util.events.event_dispatcher import EventDispatcher


class InputEvents:
    def __init__(self) -> None:
        self.onHide = EventDispatcher[None]()
        self.scroll = EventDispatcher[int]()
        self.zoom = EventDispatcher[int]()
        self.leftMouse = EventDispatcher[bool]()
        self.rightMouse = EventDispatcher[bool]()

    def destroy(self) -> None:
        self.onHide.close()
        self.scroll.close()
        self.zoom.close()
        self.leftMouse.close()
        self.rightMouse.close()
