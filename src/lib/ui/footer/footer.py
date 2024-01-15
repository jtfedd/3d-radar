from lib.app.events import AppEvents
from lib.app.state import AppState
from lib.ui.context import UIContext
from lib.ui.core.alignment import VAlign
from lib.ui.core.colors import UIColors
from lib.ui.core.components.background_card import BackgroundCard
from lib.ui.core.constants import UIConstants
from lib.ui.core.layers import UILayer
from lib.util.events.listener import Listener

from .animation_controls.animation_controls import AnimationControls


class Footer(Listener):
    def __init__(self, ctx: UIContext, state: AppState, events: AppEvents):
        super().__init__()

        self.background = BackgroundCard(
            ctx.anchors.bottom,
            width=UIConstants.infinity,
            height=UIConstants.headerFooterHeight,
            color=UIColors.BACKGROUND,
            vAlign=VAlign.BOTTOM,
            layer=UILayer.BACKGROUND,
        )

        self.animationControls = AnimationControls(ctx, state, events)

    def destroy(self) -> None:
        super().destroy()

        self.background.destroy()
        self.animationControls.destroy()
