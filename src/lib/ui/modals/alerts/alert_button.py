from __future__ import annotations

from panda3d.core import NodePath, PandaNode

from lib.model.alert import Alert
from lib.model.alert_type import AlertType
from lib.ui.context import UIContext
from lib.ui.core.alignment import HAlign, VAlign
from lib.ui.core.colors import UIColors
from lib.ui.core.components.background_card import BackgroundCard
from lib.ui.core.components.button import Button, ButtonSkin
from lib.ui.core.components.text import Text
from lib.ui.core.constants import UIConstants
from lib.ui.core.layers import UILayer
from lib.util.events.event_dispatcher import EventDispatcher
from lib.util.events.listener import Listener


class AlertButton(Listener):
    def __init__(
        self,
        ctx: UIContext,
        root: NodePath[PandaNode],
        alert: Alert,
        top: float,
        contentWidth: float,
    ) -> None:
        super().__init__()

        self.button = Button(
            root=root,
            ctx=ctx,
            width=contentWidth,
            height=UIConstants.alertsButtonHeight,
            y=-top,
            hAlign=HAlign.LEFT,
            vAlign=VAlign.TOP,
            bgLayer=UILayer.MODAL_CONTENT_BACKGROUND,
            contentLayer=UILayer.MODAL_CONTENT,
            interactionLayer=UILayer.MODAL_CONTENT_INTERACTION,
            textSize=UIConstants.fontSizeRegular,
            skin=ButtonSkin.ACCENT,
        )

        borderColor = UIColors.WHITE
        if alert.alertType == AlertType.TORNADO_WARNING:
            borderColor = UIColors.RED
        elif alert.alertType == AlertType.SEVERE_THUNDERSTORM_WARNING:
            borderColor = UIColors.ORANGE

        self.leftBorder = BackgroundCard(
            root=root,
            width=UIConstants.alertsButtonBorderWidth,
            height=UIConstants.alertsButtonHeight,
            x=0,
            y=-top,
            color=borderColor,
            hAlign=HAlign.LEFT,
            vAlign=VAlign.TOP,
            layer=UILayer.MODAL_CONTENT,
        )

        self.nameText = Text(
            root=root,
            font=ctx.fonts.bold,
            text=alert.name,
            x=UIConstants.alertsButtonTextLeftPadding,
            y=-(top + UIConstants.alertsButtonTextVerticalPadding),
            size=UIConstants.fontSizeRegular,
            vAlign=VAlign.TOP,
            layer=UILayer.MODAL_CONTENT,
        )

        self.countiesText = Text(
            root=root,
            font=ctx.fonts.regular,
            text="nothing here yet",
            x=UIConstants.alertsButtonTextLeftPadding,
            y=-(
                top
                + (
                    UIConstants.alertsButtonHeight
                    - UIConstants.alertsButtonTextVerticalPadding
                )
            ),
            size=UIConstants.fontSizeRegular,
            vAlign=VAlign.BOTTOM,
            hAlign=HAlign.LEFT,
            layer=UILayer.MODAL_CONTENT,
        )

        self.onClick = EventDispatcher[str]()
        self.listen(self.button.onClick, lambda _: self.onClick.send(""))

    def destroy(self) -> None:
        super().destroy()

        self.button.destroy()
        self.leftBorder.destroy()
        self.nameText.destroy()
        self.countiesText.destroy()

        self.onClick.close()
