from typing import Any, Callable, List, TypeVar

from .event_dispatcher import EventDispatcher
from .event_subscription import EventSubscription

T = TypeVar("T")


class Listener:
    def __init__(self) -> None:
        self.subscriptions: List[EventSubscription[Any]] = []  # type: ignore

    def listen(
        self,
        dispatcher: EventDispatcher[T],
        callback: Callable[[T], None],
    ) -> None:
        self.subscriptions.append(dispatcher.listen(callback))

    def destroy(self) -> None:
        for sub in self.subscriptions:
            sub.cancel()
