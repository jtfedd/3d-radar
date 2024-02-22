from lib.app.events import AppEvents
from lib.ui.context import UIContext
from lib.ui.core.constants import UIConstants

from ..core.footer_button import FooterButton
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

        self.button = FooterButton(
            ctx,
            self.bottomLeft,
            UIConstants.licenseModalWidth,
            "OK",
        )

        self.closeSub = self.button.button.onClick.listen(lambda _: self.destroy())

    def destroy(self) -> None:
        super().destroy()
        self.closeSub.cancel()

        self.text.destroy()
        self.button.destroy()
