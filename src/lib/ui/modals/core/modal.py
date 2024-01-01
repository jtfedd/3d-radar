from lib.app.events import AppEvents
from lib.app.focus.focusable import Focusable
from lib.ui.context import UIContext
from lib.ui.core.colors import UIColors
from lib.ui.core.components.background_card import BackgroundCard
from lib.ui.core.constants import UIConstants
from lib.ui.core.layers import UILayer


class Modal(Focusable):
    def __init__(
        self,
        ctx: UIContext,
        events: AppEvents,
        contentWidth: float,
        contentHeight: float,
    ):
        super().__init__(ctx.appContext.focusManager, events.input)
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
