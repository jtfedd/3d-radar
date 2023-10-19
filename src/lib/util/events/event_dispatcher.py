from typing import Callable, Generic, List, TypeVar

from lib.util.errors import StateError
from lib.util.events.event_subscription import EventSubscription

T = TypeVar("T")


class EventDispatcher(Generic[T]):
    def __init__(self) -> None:
        self.closed = False
        self.subscriptions: List[EventSubscription[T]] = []

    def remove(self, subscription: EventSubscription[T]) -> None:
        self.subscriptions.remove(subscription)

    def close(self) -> None:
        if self.closed:
            raise StateError("EventDispatcher is already closed")

        self.closed = True

        while len(self.subscriptions) > 0:
            self.subscriptions[0].cancel()

    def listen(self, callback: Callable[[T], None]) -> EventSubscription[T]:
        if self.closed:
            raise StateError("EventDispatcher cannot accept listeners when closed")

        subscription = EventSubscription(self, callback)
        self.subscriptions.append(subscription)
        return subscription

    def send(self, payload: T) -> None:
        if self.closed:
            raise StateError("EventDispatcher cannot send events when closed")

        for subscription in self.subscriptions:
            subscription.send(payload)
