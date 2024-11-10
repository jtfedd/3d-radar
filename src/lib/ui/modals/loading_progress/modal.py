from lib.app.events import AppEvents
from lib.model.loading_progress_payload import LoadingProgressPayload
from lib.ui.context import UIContext
from lib.ui.core.alignment import HAlign
from lib.ui.core.components.progress_bar import ProgressBar
from lib.ui.core.constants import UIConstants
from lib.ui.core.layers import UILayer
from lib.util.events.listener import Listener

from ..core.footer_button import FooterButton
from ..core.modal import Modal
from ..core.title import ModalTitle


class LoadingProgressModal(Modal):
    def __init__(
        self,
        ctx: UIContext,
        events: AppEvents,
        payload: LoadingProgressPayload,
    ):
        super().__init__(
            ctx,
            events,
            UIConstants.loadingProgressModalWidth,
            UIConstants.loadingProgressModalHeight,
        )

        self.listener = Listener()

        self.title = ModalTitle(
            ctx,
            self.topLeft,
            "Loading Data...",
            UIConstants.loadingProgressModalWidth,
        )

        self.progressBar = ProgressBar(
            self.topLeft,
            x=UIConstants.modalPadding,
            y=-(self.title.height() + UIConstants.modalPadding),
            width=UIConstants.loadingProgressModalWidth
            - (2 * UIConstants.modalPadding),
            hAlign=HAlign.LEFT,
            progress=0,
            layer=UILayer.MODAL_CONTENT_INTERACTION,
            bgLayer=UILayer.MODAL_CONTENT,
        )

        self.cancelButton = FooterButton(
            ctx,
            self.bottomLeft,
            UIConstants.loadingProgressModalWidth,
            "Cancel",
        )

        self.listener.listen(
            self.cancelButton.button.onClick, lambda _: payload.cancel()
        )
        self.listener.bind(payload.progress, self.progressBar.setProgress)
        self.listener.listen(payload.onComplete, lambda _: self.destroy())

    def destroy(self) -> None:
        super().destroy()
        self.listener.destroy()

        self.title.destroy()
        self.progressBar.destroy()
        self.cancelButton.destroy()
