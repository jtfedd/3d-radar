from lib.app.context import AppContext
from lib.app.events import AppEvents
from lib.app.state import AppState
from lib.ui.core.anchors import UIAnchors
from lib.ui.core.font import UIFonts


class UIContext:
    def __init__(self, ctx: AppContext, state: AppState, events: AppEvents) -> None:
        self.appContext = ctx
        self.fonts = UIFonts()
        self.anchors = UIAnchors(ctx, state, events)

    def destroy(self) -> None:
        self.anchors.destroy()
