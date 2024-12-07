from typing import List

from panda3d.core import Point2, Point3

from lib.app.context import AppContext
from lib.app.events import AppEvents
from lib.app.state import AppState
from lib.ui.context_menu.components.context_menu_component import ContextMenuComponent
from lib.ui.context_menu.components.context_menu_divider_component import (
    ContextMenuDividerComponent,
)
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
        self.height = UIConstants.contextMenuPadding
        self.width = UIConstants.contextMenuWidth

        for i, group in enumerate(groups):
            if i > 0:
                self.addComponent(
                    ContextMenuDividerComponent(self.contentRoot, self.height)
                )

            groupComponents = group.render(ctx, events, self.contentRoot, self.height)
            for component in groupComponents:
                self.addComponent(component)

        for component in self.components:
            component.setContextMenuWidth(self.width)

        self.width += 2 * UIConstants.contextMenuPadding
        self.height += UIConstants.contextMenuPadding

        self.bg = BackgroundCard(
            root=self.contentRoot,
            width=self.width,
            height=self.height,
            hAlign=HAlign.LEFT,
            vAlign=VAlign.TOP,
            layer=UILayer.CONTEXT_MENU_BACKGROUND,
            color=UIColors.ACCENT,
        )

        bottomRight = self.ctx.base.render2d.getRelativePoint(
            self.contentRoot, Point3(self.width, 0, -self.height)
        )
        if bottomRight.getX() > 1:
            self.contentRoot.setX(-self.width)
        if bottomRight.getZ() < -1:
            self.contentRoot.setZ(self.height)

    def addComponent(self, component: ContextMenuComponent) -> None:
        self.components.append(component)
        self.height += component.height()
        self.width = max(self.width, component.width())

    def checkMouseInBounds(self) -> bool:
        if not self.ctx.base.mouseWatcherNode.hasMouse():
            return False

        mouse = self.ctx.base.mouseWatcherNode.getMouse()

        topLeft = self.ctx.base.render2d.getRelativePoint(
            self.contentRoot, Point3(0, 0, 0)
        )
        bottomRight = self.ctx.base.render2d.getRelativePoint(
            self.contentRoot, Point3(self.width, 0, -self.height)
        )

        return (
            topLeft.getX() <= mouse.getX()
            and mouse.getX() <= bottomRight.getX()
            and topLeft.getZ() >= mouse.getY()
            and mouse.getY() >= bottomRight.getZ()
        )

    def destroy(self) -> None:
        super().destroy()

        self.root.removeNode()
        self.contentRoot.removeNode()

        for component in self.components:
            component.destroy()
