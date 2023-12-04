from typing import List

from lib.ui.panels.core.panel_component import PanelComponent
from lib.util.events.event_dispatcher import EventDispatcher
from lib.util.events.event_subscription import EventSubscription


class PanelComponentManager:
    def __init__(self) -> None:
        self.components: List[PanelComponent] = []
        self.subscriptions: List[EventSubscription[None]] = []

        self.onUpdate = EventDispatcher[float]()

    def add(self, component: PanelComponent) -> None:
        component.setOffset(self.getHeight())
        self.components.append(component)
        self.subscriptions.append(
            component.onHeightChange.listen(lambda _: self.update())
        )

    def update(self) -> None:
        height = 0.0

        for component in self.components:
            component.setOffset(height)
            height += component.height()

        self.onUpdate.send(height)

    def getHeight(self) -> float:
        return sum(c.height() for c in self.components)

    def destroy(self) -> None:
        self.components.clear()
        for sub in self.subscriptions:
            sub.cancel()

        self.onUpdate.close()
