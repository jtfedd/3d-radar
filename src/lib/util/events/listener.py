from typing import Any, Callable, List, TypeVar

from .event_dispatcher import EventDispatcher
from .event_subscription import EventSubscription
from .observable import Observable

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

    def bind(
        self,
        observable: Observable[T],
        callback: Callable[[T], None],
    ) -> None:
        callback(observable.getValue())
        self.listen(observable, callback)

    def trigger(
        self,
        dispatcher: EventDispatcher[T],
        callback: Callable[[], None],
        triggerImmediately: bool = False,
    ) -> None:
        if triggerImmediately:
            callback()
        self.subscriptions.append(dispatcher.listen(lambda _: callback()))

    def triggerMany(  # type: ignore
        self,
        dispatchers: List[EventDispatcher[Any]],
        callback: Callable[[], None],
        triggerImmediately: bool = False,
    ) -> None:
        for dispatcher in dispatchers:
            self.trigger(dispatcher, callback, triggerImmediately=triggerImmediately)

    def destroy(self) -> None:
        for sub in self.subscriptions:
            sub.cancel()
