from lib.app.events import AppEvents
from lib.ui.context import UIContext
from lib.ui.core.alignment import HAlign, VAlign
from lib.ui.core.components.button import Button, ButtonSkin
from lib.ui.core.constants import UIConstants
from lib.ui.core.layers import UILayer

from ..core.modal import Modal
from ..core.text import ModalText
from .license import LICENSE_TEXT


class LicenseModal(Modal):
    def __init__(self, ctx: UIContext, events: AppEvents):
        super().__init__(
            ctx,
            events,
            UIConstants.licenseModalWidth,
            UIConstants.licenseModalHeight,
        )

        self.text = ModalText(
            ctx,
            self.topLeft,
            0,
            LICENSE_TEXT,
            fontSize=UIConstants.fontSizeDetail,
        )

        self.button = Button(
            root=self.bottomLeft,
            ctx=ctx,
            width=UIConstants.modalFooterButtonWidth,
            height=UIConstants.modalFooterButtonHeight,
            x=UIConstants.licenseModalWidth / 2,
            hAlign=HAlign.CENTER,
            vAlign=VAlign.BOTTOM,
            layer=UILayer.MODAL_CONTENT_INTERACTION,
            textSize=UIConstants.fontSizeRegular,
            skin=ButtonSkin.ACCENT,
            text="OK",
        )

        self.closeSub = self.button.onClick.listen(lambda _: self.destroy())

    def destroy(self) -> None:
        super().destroy()
        self.closeSub.cancel()

        self.text.destroy()
        self.button.destroy()
