from lib.app.events import AppEvents
from lib.app.state import AppState
from lib.ui.context import UIContext
from lib.ui.core.alignment import VAlign
from lib.ui.core.colors import UIColors
from lib.ui.core.components.background_card import BackgroundCard
from lib.ui.core.constants import UIConstants

from .alerts import Alerts
from .clock import Clock


class Header:
    def __init__(self, ctx: UIContext, state: AppState, events: AppEvents):
        self.background = BackgroundCard(
            ctx.anchors.top,
            width=UIConstants.infinity,
            height=UIConstants.headerFooterHeight,
            color=UIColors.BACKGROUND,
            vAlign=VAlign.TOP,
        )

        self.clock = Clock(ctx, events)
        self.alerts = Alerts(ctx, state, events)

    def destroy(self) -> None:
        self.background.destroy()
        self.clock.destroy()
        self.alerts.destroy()
