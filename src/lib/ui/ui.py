from lib.ui.core.config import UIConfig
from lib.ui.footer.footer import Footer
from lib.ui.header.header import Header
from lib.ui.panels.panel_module import PanelModule


class UI:
    def __init__(self, config: UIConfig) -> None:
        self.config = config

        self.header = Header(self.config)
        self.footer = Footer(self.config)
        self.panels = PanelModule(self.config)

    def destroy(self) -> None:
        self.header.destroy()
        self.footer.destroy()
        self.panels.destroy()
