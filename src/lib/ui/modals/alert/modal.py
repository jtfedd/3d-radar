from lib.app.events import AppEvents
from lib.model.alert import Alert
from lib.ui.context import UIContext
from lib.ui.core.alignment import HAlign, VAlign
from lib.ui.core.components.scrollable_panel import ScrollablePanel
from lib.ui.core.components.text import Text
from lib.ui.core.constants import UIConstants
from lib.ui.core.layers import UILayer

from ..core.footer_button import FooterButton
from ..core.modal import Modal
from ..core.title import ModalTitle


class AlertModal(Modal):
    def __init__(self, ctx: UIContext, events: AppEvents, alert: Alert):
        super().__init__(
            ctx,
            events,
            UIConstants.alertModalWidth,
            UIConstants.alertModalMaxHeight,
            closeButton=True,
        )

        self.title = ModalTitle(
            ctx,
            self.topLeft,
            alert.event,
            UIConstants.alertModalWidth,
        )

        self.scroll = ScrollablePanel(
            root=self.topLeft,
            ctx=ctx,
            events=events,
            y=-(self.title.height()),
            width=UIConstants.alertModalWidth + UIConstants.modalPadding,
            hAlign=HAlign.LEFT,
            vAlign=VAlign.TOP,
            layer=UILayer.MODAL_CONTENT_INTERACTION,
            scrollbarPadding=UIConstants.modalScrollbarPadding,
        )

        self.headline = Text(
            root=self.scroll.getCanvas(),
            font=ctx.fonts.mono,
            text=alert.headline,
            vAlign=VAlign.TOP,
            size=UIConstants.fontSizeDetail,
            layer=UILayer.MODAL_CONTENT,
            hAlign=HAlign.LEFT,
            maxWidth=UIConstants.alertModalWidth,
        )

        self.description = Text(
            root=self.scroll.getCanvas(),
            font=ctx.fonts.mono,
            text=alert.description,
            vAlign=VAlign.TOP,
            y=-(self.headline.getHeight() + UIConstants.modalPadding),
            size=UIConstants.fontSizeDetail,
            layer=UILayer.MODAL_CONTENT,
            hAlign=HAlign.LEFT,
            maxWidth=UIConstants.alertModalWidth,
        )

        self.backButton = FooterButton(
            ctx,
            self.bottomLeft,
            UIConstants.alertModalWidth,
            "Back",
        )

        self.backSub = self.backButton.button.onClick.listen(
            events.ui.modals.alerts.send
        )

        contentHeight = (
            self.headline.getHeight()
            + self.description.getHeight()
            + UIConstants.modalPadding
        )

        frameHeight = min(
            contentHeight,
            UIConstants.alertModalMaxHeight
            - self.title.height()
            - UIConstants.modalFooterButtonHeight
            - UIConstants.modalPadding,
        )

        self.scroll.updateFrame(frameHeight, contentHeight)
        self.updateSize(
            UIConstants.alertModalWidth,
            frameHeight
            + self.title.height()
            + UIConstants.modalFooterButtonHeight
            + UIConstants.modalPadding,
        )

    def destroy(self) -> None:
        super().destroy()
        self.backSub.cancel()

        self.title.destroy()
        self.headline.destroy()
        self.description.destroy()
        self.scroll.destroy()
        self.backButton.destroy()
