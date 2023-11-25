from lib.util.events.event_dispatcher import EventDispatcher


class InputEvents:
    def __init__(self) -> None:
        self.onHide = EventDispatcher[None]()

    def destroy(self) -> None:
        self.onHide.close()
