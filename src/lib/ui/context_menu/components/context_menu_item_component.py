from __future__ import annotations

from panda3d.core import NodePath, PandaNode

from lib.app.context import AppContext
from lib.app.events import AppEvents
from lib.ui.context_menu.components.context_menu_component import ContextMenuComponent
from lib.ui.context_menu.context_menu_item import ContextMenuItem
from lib.ui.core.alignment import HAlign, VAlign
from lib.ui.core.components.button import Button, ButtonSkin
from lib.ui.core.constants import UIConstants
from lib.ui.core.layers import UILayer
from lib.util.events.listener import Listener


class ContextMenuItemComponent(ContextMenuComponent, Listener):
    def __init__(
        self,
        ctx: AppContext,
        events: AppEvents,
        root: NodePath[PandaNode],
        offset: float,
        item: ContextMenuItem,
    ) -> None:
        Listener.__init__(self)
        ContextMenuComponent.__init__(self, root, offset)

        self.ctx = ctx

        self.button = self.buildButton(UIConstants.contextMenuItemWidth)
        self.texts = item.renderText(ctx, self.root)
        self.leftCap = item.renderLeftCap(self.root)

        self.listen(self.button.onClick, lambda _: item.onClick())
        self.listen(self.button.onClick, events.ui.closeContextMenu.send)

    def setContextMenuWidth(self, width: float) -> None:
        self.button.destroy()
        self.button = self.buildButton(width)

    def buildButton(self, width: float) -> Button:
        return Button(
            root=self.root,
            ctx=self.ctx,
            width=width,
            height=UIConstants.contextMenuItemHeight,
            hAlign=HAlign.LEFT,
            vAlign=VAlign.TOP,
            bgLayer=UILayer.CONTEXT_MENU_CONTENT_BACKGROUND,
            contentLayer=UILayer.CONTEXT_MENU_CONTENT,
            interactionLayer=UILayer.CONTEXT_MENU_CONTENT_INTERACTION,
            skin=ButtonSkin.ACCENT,
        )

    def destroy(self) -> None:
        Listener.destroy(self)
        ContextMenuComponent.destroy(self)

        for text in self.texts:
            text.destroy()

        if self.leftCap is not None:
            self.leftCap.destroy()

        self.button.destroy()
