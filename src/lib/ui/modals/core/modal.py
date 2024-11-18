from lib.app.context import AppContext
from lib.app.events import AppEvents
from lib.app.focus.focusable import Focusable
from lib.ui.core.alignment import HAlign, VAlign
from lib.ui.core.colors import UIColors
from lib.ui.core.components.background_card import BackgroundCard
from lib.ui.core.components.button import Button
from lib.ui.core.constants import UIConstants
from lib.ui.core.icons import Icons
from lib.ui.core.layers import UILayer


class Modal(Focusable):
    def __init__(
        self,
        ctx: AppContext,
        events: AppEvents,
        contentWidth: float,
        contentHeight: float,
        closeButton: bool = False,
    ):
        super().__init__(ctx.focusManager, events.input)
        self.onFocus(True)
        self.closed = False

        self.shadow = BackgroundCard(
            ctx.anchors.center,
            width=UIConstants.infinity,
            height=UIConstants.infinity,
            color=UIColors.MODAL_SHADOW,
            layer=UILayer.MODAL_SHADOW,
        )

        self.background = BackgroundCard(
            ctx.anchors.center,
            width=contentWidth + 2 * UIConstants.modalPadding,
            height=contentHeight + 2 * UIConstants.modalPadding,
            color=UIColors.BACKGROUND,
            layer=UILayer.MODAL_BACKGROUND,
        )

        self.topLeft = ctx.anchors.center.attachNewNode("modal-top-left")
        self.topLeft.setX(-contentWidth / 2)
        self.topLeft.setZ(contentHeight / 2)

        self.bottomLeft = ctx.anchors.center.attachNewNode("modal-bottom-left")
        self.bottomLeft.setX(-contentWidth / 2)
        self.bottomLeft.setZ(-contentHeight / 2)

        self.closeButton: None | Button = None
        if closeButton:
            self.closeButton = Button(
                self.topLeft,
                ctx=ctx,
                width=UIConstants.modalTitleHeight,
                height=UIConstants.modalTitleHeight,
                x=contentWidth,
                y=0,
                hAlign=HAlign.RIGHT,
                vAlign=VAlign.TOP,
                bgLayer=UILayer.MODAL_CONTENT_BACKGROUND,
                contentLayer=UILayer.MODAL_CONTENT,
                interactionLayer=UILayer.MODAL_CONTENT_INTERACTION,
                icon=Icons.CLOSE,
                iconWidth=UIConstants.modalTitleHeight,
                iconHeight=UIConstants.modalTitleHeight,
            )
            self.closeButtonSub = self.closeButton.onClick.listen(
                lambda _: self.destroy()
            )

    def updateSize(self, contentWidth: float, contentHeight: float) -> None:
        self.topLeft.setX(-contentWidth / 2)
        self.topLeft.setZ(contentHeight / 2)

        self.bottomLeft.setX(-contentWidth / 2)
        self.bottomLeft.setZ(-contentHeight / 2)

        self.background.updateSize(
            width=contentWidth + 2 * UIConstants.modalPadding,
            height=contentHeight + 2 * UIConstants.modalPadding,
        )

    def focus(self) -> None:
        pass

    def blur(self) -> None:
        pass

    def destroy(self) -> None:
        self.closed = True

        super().destroy()

        self.shadow.destroy()
        self.background.destroy()
        self.topLeft.removeNode()
        self.bottomLeft.removeNode()

        if self.closeButton:
            self.closeButton.destroy()
            self.closeButtonSub.cancel()
