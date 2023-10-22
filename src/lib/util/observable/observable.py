from typing import TypeVar

from lib.util.errors import StateError
from lib.util.events.event_dispatcher import EventDispatcher

T = TypeVar("T")


class Observable(EventDispatcher[T]):
    def __init__(self, value: T) -> None:
        super().__init__()

        self.value = value

    def setValue(self, newValue: T) -> None:
        if self.closed:
            raise StateError("Observable is closed")

        if newValue == self.value:
            return

        self.value = newValue
        self.send(newValue)

    def getValue(self) -> T:
        return self.value
