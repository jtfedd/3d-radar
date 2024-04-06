from lib.app.events import AppEvents
from lib.app.state import AppState
from lib.ui.context import UIContext
from lib.ui.core.alignment import HAlign, VAlign
from lib.ui.core.components.button import Button
from lib.ui.core.constants import UIConstants
from lib.ui.core.icons import Icons


class AlertsButton:
    def __init__(self, ctx: UIContext, state: AppState, events: AppEvents) -> None:
        self.ctx = ctx
        self.state = state
        self.events = events

        self.button = Button(
            root=ctx.anchors.topRight,
            ctx=ctx,
            width=UIConstants.headerButtonWidth,
            height=UIConstants.headerFooterHeight,
            x=-UIConstants.clockWidth,
            hAlign=HAlign.RIGHT,
            vAlign=VAlign.TOP,
            icon=Icons.WARNING,
            iconWidth=UIConstants.headerFooterHeight,
            iconHeight=UIConstants.headerFooterHeight,
        )

    def destroy(self) -> None:
        self.button.destroy()
