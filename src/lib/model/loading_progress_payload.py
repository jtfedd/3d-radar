from typing import Callable

from lib.util.events.event_dispatcher import EventDispatcher
from lib.util.events.observable import Observable


class LoadingProgressPayload:
    def __init__(
        self,
        progress: Observable[float],
        onComplete: EventDispatcher[None],
        cancel: Callable[[], None],
    ) -> None:
        self.progress = progress
        self.onComplete = onComplete
        self.cancel = cancel
