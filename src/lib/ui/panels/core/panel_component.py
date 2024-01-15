from __future__ import annotations

from abc import ABC, abstractmethod

from panda3d.core import NodePath, PandaNode

from lib.util.events.event_dispatcher import EventDispatcher


class PanelComponent(ABC):
    def __init__(self, root: NodePath[PandaNode]) -> None:
        self.onHeightChange = EventDispatcher[None]()
        self.root = root.attachNewNode("component-root")
        self.hidden = False

    def setHidden(self, hidden: bool) -> None:
        if hidden == self.hidden:
            return

        self.hidden = hidden

        if hidden:
            self.root.hide()
        else:
            self.root.show()

        self.onHeightChange.send(None)

    def height(self) -> float:
        if self.hidden:
            return 0

        return self.getHeight()

    @abstractmethod
    def getHeight(self) -> float:
        pass

    def setOffset(self, offset: float) -> None:
        self.root.setZ(-offset)

    def destroy(self) -> None:
        self.onHeightChange.close()
        self.root.removeNode()
