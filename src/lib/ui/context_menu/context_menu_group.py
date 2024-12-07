from __future__ import annotations

from typing import List

from panda3d.core import NodePath, PandaNode

from lib.app.context import AppContext
from lib.app.events import AppEvents
from lib.ui.context_menu.components.context_menu_component import ContextMenuComponent
from lib.ui.context_menu.components.context_menu_header_component import (
    ContextMenuHeaderComponent,
)

from .components.context_menu_item_component import ContextMenuItemComponent
from .context_menu_item import ContextMenuItem


class ContextMenuGroup:
    def __init__(
        self,
        header: str | None,
        items: List[ContextMenuItem],
    ) -> None:
        self.header = header
        self.items = items

    def render(
        self,
        ctx: AppContext,
        events: AppEvents,
        root: NodePath[PandaNode],
        offset: float,
    ) -> List[ContextMenuComponent]:
        components: List[ContextMenuComponent] = []

        if self.header is not None:
            header = ContextMenuHeaderComponent(ctx, root, offset, self.header)
            offset += header.height()
            components.append(header)

        for item in self.items:
            itemComponent = ContextMenuItemComponent(ctx, events, root, offset, item)
            offset += itemComponent.height()
            components.append(itemComponent)

        return components
