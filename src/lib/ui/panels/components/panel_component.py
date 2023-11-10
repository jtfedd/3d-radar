from abc import ABC, abstractmethod

from lib.util.events.event_dispatcher import EventDispatcher


class PanelComponent(ABC):
    def __init__(self) -> None:
        self.onChange = EventDispatcher[None]()

    @abstractmethod
    def getHeight(self) -> float:
        pass

    @abstractmethod
    def setOffset(self, offset: float) -> float:
        pass

    def destroy(self) -> None:
        self.onChange.close()
