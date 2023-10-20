from typing import Callable, Dict, Generic, TypeVar

from lib.util.errors import StateError
from lib.util.events.event_subscription import EventSubscription
from lib.util.uuid import uuid

T = TypeVar("T")


class EventDispatcher(Generic[T]):
    def __init__(self) -> None:
        self.closed = False
        self.subscriptions: Dict[str, EventSubscription[T]] = {}

    def remove(self, subscriptionID: str) -> None:
        if subscriptionID in self.subscriptions:
            del self.subscriptions[subscriptionID]

    def close(self) -> None:
        if self.closed:
            raise StateError("EventDispatcher is already closed")

        self.closed = True

        for key in list(self.subscriptions.keys()):
            self.remove(key)

    def listen(self, callback: Callable[[T], None]) -> EventSubscription[T]:
        if self.closed:
            raise StateError("EventDispatcher cannot accept listeners when closed")

        subscriptionID = uuid()
        subscription = EventSubscription(callback, lambda: self.remove(subscriptionID))
        self.subscriptions[subscriptionID] = subscription

        return subscription

    def send(self, payload: T) -> None:
        if self.closed:
            raise StateError("EventDispatcher cannot send events when closed")

        for subscription in self.subscriptions.values():
            subscription.send(payload)
