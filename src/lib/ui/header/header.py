from lib.app.events import AppEvents
from lib.ui.context import UIContext
from lib.ui.core.alignment import VAlign
from lib.ui.core.colors import UIColors
from lib.ui.core.components.background_card import BackgroundCard
from lib.ui.core.constants import UIConstants
from lib.ui.header.clock import Clock


class Header:
    def __init__(self, ctx: UIContext, events: AppEvents):
        self.background = BackgroundCard(
            ctx.anchors.top,
            width=UIConstants.infinity,
            height=UIConstants.headerFooterHeight,
            color=UIColors.BACKGROUND,
            vAlign=VAlign.TOP,
        )

        self.clock = Clock(ctx, events)

    def destroy(self) -> None:
        self.background.destroy()
        self.clock.destroy()
