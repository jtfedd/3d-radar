from __future__ import annotations

from panda3d.core import NodePath, PandaNode

from lib.app.context import AppContext
from lib.ui.context_menu.components.context_menu_component import ContextMenuComponent
from lib.ui.core.alignment import HAlign, VAlign
from lib.ui.core.components.text import Text
from lib.ui.core.constants import UIConstants
from lib.ui.core.layers import UILayer


class ContextMenuHeaderComponent(ContextMenuComponent):
    def __init__(
        self,
        ctx: AppContext,
        root: NodePath[PandaNode],
        offset: float,
        text: str,
    ) -> None:
        ContextMenuComponent.__init__(self, root, offset)

        self.header = Text(
            root=self.root,
            font=ctx.fonts.regular,
            text=text,
            y=-UIConstants.contextMenuItemHeight / 2,
            hAlign=HAlign.LEFT,
            vAlign=VAlign.CENTER,
            layer=UILayer.CONTEXT_MENU_CONTENT,
        )

    def destroy(self) -> None:
        ContextMenuComponent.destroy(self)

        self.header.destroy()
