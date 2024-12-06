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
        self.events = events
        self.item = item

        self.leftRoot = self.root.attachNewNode("left-text")
        self.rightRoot = self.root.attachNewNode("right-text")

        self.button = self.buildButton(UIConstants.contextMenuItemWidth)
        self.texts = item.renderText(ctx, self.leftRoot, self.rightRoot)
        self.leftCap = item.renderLeftCap(self.root)
        if self.leftCap is not None:
            self.leftRoot.setX(UIConstants.contextMenuPadding)

    def setContextMenuWidth(self, width: float) -> None:
        self.button.destroy()
        self.button = self.buildButton(width)
        self.rightRoot.setX(width)

    def buildButton(self, width: float) -> Button:
        btn = Button(
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

        self.listen(btn.onClick, lambda _: self.item.onClick())
        self.listen(btn.onClick, self.events.ui.closeContextMenu.send)

        return btn

    def width(self) -> float:
        width = 0.0
        if self.leftCap is not None:
            width += UIConstants.contextMenuPadding
        for text in self.texts:
            width += text.getWidth()

        if len(self.texts) > 1:
            width += UIConstants.contextMenuPadding * (len(self.texts) - 1)

        return width

    def destroy(self) -> None:
        Listener.destroy(self)
        ContextMenuComponent.destroy(self)

        for text in self.texts:
            text.destroy()

        if self.leftCap is not None:
            self.leftCap.destroy()

        self.button.destroy()
