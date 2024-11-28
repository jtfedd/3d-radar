from __future__ import annotations

from abc import ABC

from panda3d.core import NodePath, PandaNode

from lib.ui.core.constants import UIConstants


class ContextMenuComponent(ABC):
    def __init__(self, root: NodePath[PandaNode], offset: float):
        self.root = root.attachNewNode("context-menu-componnet")
        self.root.setX(UIConstants.contextMenuPadding)
        self.root.setZ(-offset)

    def height(self) -> float:
        return UIConstants.contextMenuItemHeight

    def destroy(self) -> None:
        self.root.removeNode()
