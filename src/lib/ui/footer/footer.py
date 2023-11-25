from lib.ui.context import UIContext
from lib.ui.core.alignment import VAlign
from lib.ui.core.colors import UIColors
from lib.ui.core.components.background_card import BackgroundCard
from lib.ui.core.constants import UIConstants


class Footer:
    def __init__(self, ctx: UIContext):
        self.background = BackgroundCard(
            ctx.anchors.bottom,
            width=UIConstants.infinity,
            height=UIConstants.headerFooterHeight,
            color=UIColors.GRAY,
            vAlign=VAlign.BOTTOM,
        )

    def destroy(self) -> None:
        self.background.destroy()
