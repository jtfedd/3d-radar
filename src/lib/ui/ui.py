from lib.app.context import AppContext
from lib.app.events import AppEvents
from lib.app.state import AppState
from lib.ui.context_menu.manager import ContextMenuManager
from lib.ui.footer.footer import Footer
from lib.ui.header.header import Header
from lib.ui.legend.label import Label
from lib.ui.legend.scale import Scale
from lib.ui.modals.manager import ModalManager
from lib.ui.panels.panel_module import PanelModule


class UI:
    def __init__(self, ctx: AppContext, state: AppState, events: AppEvents) -> None:
        self.header = Header(ctx, state, events)
        self.footer = Footer(ctx, state, events)
        self.panels = PanelModule(ctx, state, events)
        self.modals = ModalManager(ctx, state, events)
        self.contextMenu = ContextMenuManager(ctx, state, events)

        self.label = Label(ctx, state, events)
        self.scale = Scale(ctx, state)

    def destroy(self) -> None:
        self.modals.destroy()
        self.contextMenu.destroy()
        self.header.destroy()
        self.footer.destroy()
        self.panels.destroy()
        self.label.destroy()
