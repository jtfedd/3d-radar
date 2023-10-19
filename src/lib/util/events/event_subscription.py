from typing import Callable, Generic, TypeVar

from lib.util.errors import StateError
from lib.util.events.event_dispatcher import EventDispatcher

T = TypeVar("T")


class EventSubscription(Generic[T]):
    def __init__(
        self, dispatcher: EventDispatcher, callback: Callable[[T], None]
    ) -> None:
        self.dispatcher = dispatcher
        self.callback = callback
        self.cancelled = False

    def cancel(self) -> None:
        if self.cancelled:
            raise StateError("EventSubscription is already cancelled")

        self.cancelled = True
        self.dispatcher.remove(self)

    def send(self, payload: T) -> None:
        if self.cancelled:
            raise StateError("EventSubscription cannot send events when cancelled")

        self.callback(payload)
