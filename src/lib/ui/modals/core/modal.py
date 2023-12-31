from lib.app.events import AppEvents
from lib.app.focus.focusable import Focusable
from lib.ui.context import UIContext
from lib.ui.core.colors import UIColors
from lib.ui.core.components.background_card import BackgroundCard
from lib.ui.core.constants import UIConstants
from lib.ui.core.layers import UILayer


class Modal(Focusable):
    def __init__(self, ctx: UIContext, events: AppEvents, width: float, height: float):
        super().__init__(ctx.appContext.focusManager, events.input)
        self.onFocus(True)

        self.contentWidth = width - UIConstants.modalPadding * 2

        self.shadow = BackgroundCard(
            ctx.anchors.center,
            width=UIConstants.infinity,
            height=UIConstants.infinity,
            color=UIColors.MODAL_SHADOW,
            layer=UILayer.MODAL_SHADOW,
        )

        self.background = BackgroundCard(
            ctx.anchors.center,
            width=width,
            height=height,
            color=UIColors.BACKGROUND,
            layer=UILayer.MODAL_BACKGROUND,
        )

        self.root = ctx.anchors.center.attachNewNode("modal-root")
        self.root.setX(-width / 2 + UIConstants.modalPadding)
        self.root.setZ(height / 2 - UIConstants.modalPadding)

    def focus(self) -> None:
        pass

    def blur(self) -> None:
        pass

    def destroy(self) -> None:
        super().destroy()

        self.shadow.destroy()
        self.background.destroy()
        self.root.removeNode()
