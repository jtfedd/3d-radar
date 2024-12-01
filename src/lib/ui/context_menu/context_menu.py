from typing import List

from panda3d.core import Point2

from lib.app.context import AppContext
from lib.app.events import AppEvents
from lib.app.state import AppState
from lib.ui.context_menu.components.context_menu_component import ContextMenuComponent
from lib.ui.context_menu.context_menu_group import ContextMenuGroup
from lib.ui.core.alignment import HAlign, VAlign
from lib.ui.core.colors import UIColors
from lib.ui.core.components.background_card import BackgroundCard
from lib.ui.core.constants import UIConstants
from lib.ui.core.layers import UILayer
from lib.util.events.listener import Listener


class ContextMenu(Listener):
    def __init__(
        self,
        ctx: AppContext,
        state: AppState,
        events: AppEvents,
        screenPoint: Point2,
        groups: List[ContextMenuGroup],
    ) -> None:
        super().__init__()
        self.ctx = ctx

        self.root = ctx.base.aspect2dp.attachNewNode("context-menu-root")
        self.root.setX(screenPoint.x)
        self.root.setZ(screenPoint.y)
        self.bind(state.uiScale, self.root.setScale)

        self.contentRoot = self.root.attachNewNode("context-menu")

        self.components: List[ContextMenuComponent] = []
        height = UIConstants.contextMenuPadding

        for group in groups:
            groupComponents = group.render(ctx, events, self.contentRoot, height)
            for component in groupComponents:
                self.components.append(component)
                height += component.height()
            # TODO render divider between groups

        height += UIConstants.contextMenuPadding

        self.bg = BackgroundCard(
            root=self.contentRoot,
            width=UIConstants.contextMenuWidth,
            height=height,
            hAlign=HAlign.LEFT,
            vAlign=VAlign.TOP,
            layer=UILayer.CONTEXT_MENU_BACKGROUND,
            color=UIColors.ACCENT,
        )

        # TODO adjust content root position to keep on screen

    def destroy(self) -> None:
        super().destroy()

        self.root.removeNode()
        self.contentRoot.removeNode()

        for component in self.components:
            component.destroy()
