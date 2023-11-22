from direct.showbase.ShowBase import ShowBase

from lib.app.state import AppState
from lib.ui.core.context import UIContext
from lib.ui.footer.footer import Footer
from lib.ui.header.header import Header
from lib.ui.panels.panel_module import PanelModule

from .events import UIEvents


class UI:
    def __init__(self, base: ShowBase, state: AppState) -> None:
        self.events = UIEvents()
        self.ctx = UIContext(base, state, self.events)

        self.header = Header(self.ctx)
        self.footer = Footer(self.ctx)
        self.panels = PanelModule(self.ctx, state, self.events)

    def destroy(self) -> None:
        self.header.destroy()
        self.footer.destroy()
        self.panels.destroy()
