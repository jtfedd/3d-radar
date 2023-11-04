from lib.ui.core.config import UIConfig
from lib.ui.footer.footer import Footer
from lib.ui.header.header import Header


class UI:
    def __init__(self, config: UIConfig) -> None:
        self.config = config

        self.header = Header(self.config)
        self.footer = Footer(self.config)

    def destroy(self) -> None:
        self.header.destroy()
        self.footer.destroy()
