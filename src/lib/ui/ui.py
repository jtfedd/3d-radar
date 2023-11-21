from direct.showbase.ShowBase import ShowBase

from lib.app.app_config import AppConfig
from lib.ui.core.context import UIContext
from lib.ui.footer.footer import Footer
from lib.ui.header.header import Header
from lib.ui.panels.panel_module import PanelModule


class UI:
    def __init__(self, base: ShowBase, config: AppConfig) -> None:
        self.ctx = UIContext(base, scale=config.uiScale)

        self.header = Header(self.ctx)
        self.footer = Footer(self.ctx)
        self.panels = PanelModule(self.ctx)

        self.scaleSub = self.panels.events.scaleChanged.listen(self.ctx.setScale)

    def destroy(self) -> None:
        self.header.destroy()
        self.footer.destroy()
        self.panels.destroy()

        self.scaleSub.cancel()
