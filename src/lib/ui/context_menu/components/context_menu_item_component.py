from __future__ import annotations

from panda3d.core import NodePath, PandaNode

from lib.app.context import AppContext
from lib.ui.context_menu.components.context_menu_component import ContextMenuComponent
from lib.ui.context_menu.context_menu_item import ContextMenuItem
from lib.ui.core.alignment import HAlign, VAlign
from lib.ui.core.components.button import Button
from lib.ui.core.constants import UIConstants
from lib.ui.core.layers import UILayer
from lib.util.events.listener import Listener


class ContextMenuItemComponent(ContextMenuComponent, Listener):
    def __init__(
        self,
        ctx: AppContext,
        root: NodePath[PandaNode],
        offset: float,
        item: ContextMenuItem,
    ) -> None:
        Listener.__init__(self)
        ContextMenuComponent.__init__(self, root, offset)

        self.button = Button(
            root=self.root,
            ctx=ctx,
            width=UIConstants.contextMenuItemWidth,
            height=UIConstants.contextMenuItemHeight,
            hAlign=HAlign.LEFT,
            vAlign=VAlign.TOP,
            bgLayer=UILayer.CONTEXT_MENU_CONTENT_BACKGROUND,
            contentLayer=UILayer.CONTEXT_MENU_CONTENT,
            interactionLayer=UILayer.CONTEXT_MENU_CONTENT_INTERACTION,
        )

        self.texts = item.renderText(ctx, self.root)

        self.leftCap = item.renderLeftCap(self.root)

        self.listen(self.button.onClick, lambda _: item.onClick())

    def destroy(self) -> None:
        Listener.destroy(self)
        ContextMenuComponent.destroy(self)

        for text in self.texts:
            text.destroy()

        if self.leftCap is not None:
            self.leftCap.destroy()

        self.button.destroy()
