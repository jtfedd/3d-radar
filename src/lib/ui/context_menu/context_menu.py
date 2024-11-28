from typing import List

from panda3d.core import Point2

from lib.app.context import AppContext
from lib.ui.context_menu.components.context_menu_component import ContextMenuComponent
from lib.ui.context_menu.context_menu_group import ContextMenuGroup
from lib.ui.core.alignment import HAlign, VAlign
from lib.ui.core.colors import UIColors
from lib.ui.core.components.background_card import BackgroundCard
from lib.ui.core.constants import UIConstants
from lib.ui.core.layers import UILayer


class ContextMenu:
    def __init__(
        self, ctx: AppContext, screenPoint: Point2, groups: List[ContextMenuGroup]
    ) -> None:
        self.root = ctx.base.aspect2dp.attachNewNode("context-menu")
        self.root.setX(screenPoint.x)
        self.root.setZ(screenPoint.y)

        self.components: List[ContextMenuComponent] = []
        height = UIConstants.contextMenuPadding

        for group in groups:
            groupComponents = group.render(ctx, self.root, height)
            for component in groupComponents:
                self.components.append(component)
                height += component.height()
            # TODO render divider between groups

        height += UIConstants.contextMenuPadding

        self.bg = BackgroundCard(
            root=self.root,
            width=UIConstants.contextMenuWidth,
            height=height,
            hAlign=HAlign.LEFT,
            vAlign=VAlign.TOP,
            layer=UILayer.CONTEXT_MENU_BACKGROUND,
            color=UIColors.BACKGROUND,
        )

    def destroy(self) -> None:
        self.root.removeNode()

        for component in self.components:
            component.destroy()
