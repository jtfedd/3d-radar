from __future__ import annotations

from abc import ABC, abstractmethod

from panda3d.core import NodePath, PandaNode

from lib.util.events.event_dispatcher import EventDispatcher


class PanelComponent(ABC):
    def __init__(self, root: NodePath[PandaNode]) -> None:
        self.onChange = EventDispatcher[None]()
        self.root = root.attachNewNode("component-root")

    @abstractmethod
    def getHeight(self) -> float:
        pass

    def setOffset(self, offset: float) -> None:
        self.root.setY(-offset)

    def destroy(self) -> None:
        self.onChange.close()
        self.root.removeNode()
