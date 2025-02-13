from lib.util.events.event_dispatcher import EventDispatcher


class AnimationEvents:
    def __init__(self) -> None:
        self.play = EventDispatcher[None]()
        self.next = EventDispatcher[None]()
        self.previous = EventDispatcher[None]()

    def destroy(self) -> None:
        self.play.close()
        self.next.close()
        self.previous.close()
