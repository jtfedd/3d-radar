from abc import ABC, abstractmethod

from lib.app.focus.manager import FocusManager
from lib.app.input.events import InputEvents
from lib.util.events.event_subscription import EventSubscription
from lib.util.uuid import uuid


class Focusable(ABC):
    def __init__(self, focusManager: FocusManager, events: InputEvents):
        self.focusManager = focusManager
        self.events = events
        self.focusID = uuid()

        self.nextFocusable: Focusable | None = None
        self.prevFocusable: Focusable | None = None
        self.tabForwardSub: EventSubscription[bool] | None = None
        self.tabBackwardSub: EventSubscription[bool] | None = None

    @abstractmethod
    def focus(self) -> None:
        pass

    @abstractmethod
    def blur(self) -> None:
        pass

    def tabForward(self) -> None:
        if not self.focused():
            return

        if self.nextFocusable:
            self.nextFocusable.focus()

    def tabBackward(self) -> None:
        if not self.focused():
            return

        if self.prevFocusable:
            self.prevFocusable.focus()

    def focused(self) -> bool:
        return self.focusID in self.focusManager.focusedItems

    def onFocus(self, focused: bool) -> None:
        if self.tabForwardSub:
            self.tabForwardSub.cancel()
            self.tabForwardSub = None

        if self.tabBackwardSub:
            self.tabBackwardSub.cancel()
            self.tabBackwardSub = None

        if focused:
            self.tabForwardSub = self.events.tab.listen(lambda _: self.tabForward())
            self.tabBackwardSub = self.events.shiftTab.listen(
                lambda _: self.tabBackward()
            )

        self.focusManager.focus(self.focusID, focused)

    def destroy(self) -> None:
        self.onFocus(False)
