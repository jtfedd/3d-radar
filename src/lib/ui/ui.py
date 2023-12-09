from lib.app.context import AppContext
from lib.app.events import AppEvents
from lib.app.state import AppState
from lib.ui.context import UIContext
from lib.ui.footer.footer import Footer
from lib.ui.header.header import Header
from lib.ui.panels.panel_module import PanelModule


class UI:
    def __init__(self, ctx: AppContext, state: AppState, events: AppEvents) -> None:
        self.ctx = UIContext(ctx, state, events)

        self.header = Header(self.ctx)
        self.footer = Footer(self.ctx, state, events)
        self.panels = PanelModule(self.ctx, state, events)

    def destroy(self) -> None:
        self.header.destroy()
        self.footer.destroy()
        self.panels.destroy()

        self.ctx.destroy()
