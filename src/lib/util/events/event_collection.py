from typing import Any, Callable, List

from lib.util.events.event_dispatcher import EventDispatcher
from lib.util.events.event_subscription import EventSubscription


class EventCollection:
    def __init__(self) -> None:
        self.subscriptions: List[EventSubscription[Any]] = []  # type:ignore

    def add(  # type:ignore
        self,
        event: EventDispatcher[Any],
        callback: Callable[[], None],
    ) -> None:
        self.subscriptions.append(event.listen(lambda _: callback()))

    def destroy(self) -> None:
        for subscription in self.subscriptions:
            subscription.cancel()
