from __future__ import annotations

from panda3d.core import NodePath, PandaNode

from lib.ui.context_menu.components.context_menu_component import ContextMenuComponent
from lib.ui.core.constants import UIConstants


class ContextMenuDividerComponent(ContextMenuComponent):
    def __init__(
        self,
        root: NodePath[PandaNode],
        offset: float,
    ) -> None:
        ContextMenuComponent.__init__(self, root, offset)

    def height(self) -> float:
        return UIConstants.contextMenuItemPadding
