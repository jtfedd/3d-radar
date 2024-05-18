from __future__ import annotations

from typing import List

from direct.showbase.ShowBase import ShowBase
from panda3d.core import GraphicsWindow, NodePath, PandaNode

from lib.app.window.events import WindowEvents
from lib.util.events.listener import Listener


class ResolutionProvider(Listener):
    def __init__(self, base: ShowBase, events: WindowEvents):
        super().__init__()

        self.base = base

        self.nodes: List[NodePath[PandaNode]] = []

        # For some reason this seems to be typed incorrectly; override the type
        window: GraphicsWindow = base.win  # type: ignore
        self.windowSize = (0, 0)
        self.updateScreenResolution(window)
        self.listen(events.onWindowUpdate, self.updateScreenResolution)

    def addNode(self, node: NodePath[PandaNode]) -> None:
        self.update(node)
        self.nodes.append(node)

    def removeNode(self, node: NodePath[PandaNode]) -> None:
        self.nodes.remove(node)

    def updateScreenResolution(self, win: GraphicsWindow) -> None:
        newSize = (win.getXSize(), win.getYSize())
        if newSize[0] == self.windowSize[0] and newSize[1] == self.windowSize[1]:
            return

        self.windowSize = newSize

        for node in self.nodes:
            self.update(node)

    def update(self, node: NodePath[PandaNode]) -> None:
        node.setShaderInput("window_size", self.windowSize)
