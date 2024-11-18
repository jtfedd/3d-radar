from __future__ import annotations

from panda3d.core import NodePath, PandaNode

from lib.app.context import AppContext
from lib.model.alert import Alert
from lib.model.alert_type import AlertType
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
        ctx: AppContext,
        root: NodePath[PandaNode],
        alert: Alert,
        top: float,
        contentWidth: float,
    ) -> None:
        super().__init__()

        self.ctx = ctx

        self.nameText = Text(
            root=root,
            font=ctx.fonts.bold,
            text=alert.event,
            x=UIConstants.alertsButtonTextLeftPadding,
            y=-(top + UIConstants.alertsButtonTextVerticalPadding),
            size=UIConstants.fontSizeRegular,
            vAlign=VAlign.TOP,
            layer=UILayer.MODAL_CONTENT,
        )

        self.countiesText = Text(
            root=root,
            font=ctx.fonts.regular,
            text=alert.area,
            x=UIConstants.alertsButtonTextLeftPadding,
            y=-(
                top
                + (UIConstants.alertsButtonHeight / 2)
                + UIConstants.alertsButtonTextVerticalPadding
            ),
            size=UIConstants.fontSizeRegular,
            vAlign=VAlign.TOP,
            layer=UILayer.MODAL_CONTENT,
            maxWidth=UIConstants.alertsModalWidth
            - UIConstants.alertsButtonTextLeftPadding
            - UIConstants.alertsButtonTextRightPadding,
        )

        lineHeight = (
            self.ctx.fonts.regular.getLineHeight() * UIConstants.fontSizeRegular
        )
        excessHeight = self.countiesText.getHeight() - lineHeight
        self.buttonHeight = UIConstants.alertsButtonHeight + excessHeight

        self.button = Button(
            root=root,
            ctx=ctx,
            width=contentWidth,
            height=self.buttonHeight,
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
            height=self.buttonHeight,
            x=0,
            y=-top,
            color=borderColor,
            hAlign=HAlign.LEFT,
            vAlign=VAlign.TOP,
            layer=UILayer.MODAL_CONTENT,
        )

        self.onClick = EventDispatcher[None]()
        self.listen(self.button.onClick, lambda _: self.onClick.send(None))

    def getHeight(self) -> float:
        return self.buttonHeight

    def destroy(self) -> None:
        super().destroy()

        self.button.destroy()
        self.leftBorder.destroy()
        self.nameText.destroy()
        self.countiesText.destroy()

        self.onClick.close()
