from __future__ import annotations

from typing import List

from panda3d.core import NodePath, PandaNode

from lib.app.context import AppContext
from lib.model.alert import Alert
from lib.model.alert_type import AlertType
from lib.ui.context_menu.context_menu_item import ContextMenuItem
from lib.ui.core.alignment import HAlign, VAlign
from lib.ui.core.colors import UIColors
from lib.ui.core.components.background_card import BackgroundCard
from lib.ui.core.components.text import Text
from lib.ui.core.constants import UIConstants
from lib.ui.core.layers import UILayer


class WarningItem(ContextMenuItem):
    def __init__(self, alert: Alert):
        self.alert = alert

    def renderText(
        self,
        ctx: AppContext,
        leftRoot: NodePath[PandaNode],
        rightRoot: NodePath[PandaNode],
    ) -> List[Text]:
        return [
            Text(
                root=leftRoot,
                font=ctx.fonts.regular,
                text=self.alert.event,
                y=-UIConstants.contextMenuItemHeight / 2,
                hAlign=HAlign.LEFT,
                vAlign=VAlign.CENTER,
                layer=UILayer.CONTEXT_MENU_CONTENT,
            )
        ]

    def renderLeftCap(self, root: NodePath[PandaNode]) -> BackgroundCard | None:
        borderColor = UIColors.WHITE
        if self.alert.alertType == AlertType.TORNADO_WARNING:
            borderColor = UIColors.RED
        elif self.alert.alertType == AlertType.SEVERE_THUNDERSTORM_WARNING:
            borderColor = UIColors.ORANGE

        return BackgroundCard(
            root=root,
            y=-UIConstants.contextMenuItemHeight / 2,
            height=UIConstants.contextMenuItemLeftCapHeight,
            width=UIConstants.contextMenuItemLeftCapWidth,
            color=borderColor,
            hAlign=HAlign.LEFT,
            vAlign=VAlign.CENTER,
            layer=UILayer.CONTEXT_MENU_CONTENT,
        )

    def onClick(self) -> None:
        pass
