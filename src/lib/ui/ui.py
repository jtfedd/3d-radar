from direct.showbase.ShowBase import ShowBase

from lib.app.app_config import AppConfig
from lib.ui.core.config import UIConfig
from lib.ui.footer.footer import Footer
from lib.ui.header.header import Header
from lib.ui.panels.panel_module import PanelModule


class UI:
    def __init__(self, base: ShowBase, config: AppConfig) -> None:
        self.config = UIConfig(base, scale=config.uiScale)

        self.header = Header(self.config)
        self.footer = Footer(self.config)
        self.panels = PanelModule(self.config)

        self.scaleSub = self.panels.events.scaleChanged.listen(self.config.setScale)

    def destroy(self) -> None:
        self.header.destroy()
        self.footer.destroy()
        self.panels.destroy()

        self.scaleSub.cancel()
