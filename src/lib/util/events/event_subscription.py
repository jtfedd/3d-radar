from typing import Callable, Generic, TypeVar

from lib.util.errors import StateError

T = TypeVar("T")


class EventSubscription(Generic[T]):
    def __init__(
        self,
        callback: Callable[[T], None],
        cancelCallback: Callable[[], None],
    ) -> None:
        self.callback = callback
        self.cancelCallback = cancelCallback
        self.cancelled = False

    def cancel(self) -> None:
        if self.cancelled:
            raise StateError("EventSubscription is already cancelled")

        self.cancelled = True
        self.cancelCallback()

    def send(self, payload: T) -> None:
        if self.cancelled:
            raise StateError("EventSubscription cannot send events when cancelled")

        self.callback(payload)
