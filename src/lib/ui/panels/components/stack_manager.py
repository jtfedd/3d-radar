from typing import List

from lib.ui.panels.components.stackable_component import StackableComponent
from lib.util.events.event_subscription import EventSubscription


class StackManager:
    def __init__(self) -> None:
        self.components: List[StackableComponent] = []
        self.subscriptions: List[EventSubscription[None]] = []

    def add(self, component: StackableComponent) -> None:
        self.subscriptions.append(component.onChange.listen(lambda _: self.update()))

    def update(self) -> None:
        offset = 0.0

        for component in self.components:
            component.setOffset(offset)
            offset += component.getHeight()

    def destroy(self) -> None:
        self.components.clear()
        for sub in self.subscriptions:
            sub.cancel()
