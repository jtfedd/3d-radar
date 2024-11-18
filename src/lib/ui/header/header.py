from lib.app.context import AppContext
from lib.app.events import AppEvents
from lib.app.state import AppState
from lib.ui.core.alignment import VAlign
from lib.ui.core.colors import UIColors
from lib.ui.core.components.background_card import BackgroundCard
from lib.ui.core.constants import UIConstants

from .alerts_button import AlertsButton
from .clock import Clock
from .refresh_button import RefreshButton


class Header:
    def __init__(self, ctx: AppContext, state: AppState, events: AppEvents):
        self.background = BackgroundCard(
            ctx.anchors.top,
            width=UIConstants.infinity,
            height=UIConstants.headerFooterHeight,
            color=UIColors.BACKGROUND,
            vAlign=VAlign.TOP,
        )

        self.clock = Clock(ctx, events)
        self.alerts = AlertsButton(ctx, state, events)
        self.refresh = RefreshButton(ctx, state, events)

    def destroy(self) -> None:
        self.background.destroy()
        self.clock.destroy()
        self.alerts.destroy()
        self.refresh.destroy()
